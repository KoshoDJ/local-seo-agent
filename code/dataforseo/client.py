"""Minimal DataForSEO REST client with cache and explicit call budgets."""

from __future__ import annotations

import base64
import json
import urllib.error
import urllib.request
from typing import Any

from .cache import JsonCache
from .config import DataForSEOConfig
from .costs import CallBudget


class DataForSEOError(RuntimeError):
    pass


class DataForSEOClient:
    BASE_URL = "https://api.dataforseo.com/v3"

    def __init__(self, config: DataForSEOConfig | None = None):
        self.config = config or DataForSEOConfig.from_env()
        self.cache = JsonCache(self.config.cache_dir)
        self.budget = CallBudget(
            max_serp=self.config.max_serp_calls,
            max_keyword=self.config.max_keyword_calls,
        )

    def _post(self, path: str, tasks: list[dict], kind: str, ttl_days: int) -> dict:
        cache_payload = {"path": path, "tasks": tasks}
        cached = self.cache.get(path.replace("/", "_"), cache_payload, ttl_days)
        if cached is not None:
            return cached

        self.budget.consume(kind)
        token = base64.b64encode(
            f"{self.config.login}:{self.config.password}".encode()
        ).decode()
        request = urllib.request.Request(
            f"{self.BASE_URL}/{path.lstrip('/')}",
            data=json.dumps(tasks).encode(),
            headers={
                "Authorization": f"Basic {token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                data = json.loads(response.read().decode())
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as exc:
            raise DataForSEOError(f"DataForSEO request failed: {exc}") from exc

        if int(data.get("status_code", 0)) != 20000:
            raise DataForSEOError(
                f"DataForSEO status {data.get('status_code')}: {data.get('status_message')}"
            )
        self.cache.put(path.replace("/", "_"), cache_payload, data)
        return data

    def _base_task(self, keyword: str) -> dict[str, Any]:
        return {
            "keyword": keyword,
            "language_code": self.config.language_code,
            **self.config.location_payload(),
        }

    def serp(self, keyword: str, depth: int = 10) -> dict:
        task = {**self._base_task(keyword), "depth": depth}
        return self._post("serp/google/organic/live/advanced", [task], "serp", 7)

    def keyword_overview(self, keywords: list[str]) -> dict:
        task = {
            "keywords": keywords,
            "language_code": self.config.language_code,
            **self.config.location_payload(),
        }
        return self._post(
            "dataforseo_labs/google/keyword_overview/live", [task], "keyword", 30
        )

    def search_intent(self, keywords: list[str]) -> dict:
        task = {
            "keywords": keywords,
            "language_code": self.config.language_code,
        }
        return self._post(
            "dataforseo_labs/google/search_intent/live", [task], "keyword", 30
        )
