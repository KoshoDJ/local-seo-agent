"""Small JSON cache to control paid API usage and preserve evidence provenance."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


class JsonCache:
    def __init__(self, root: Path):
        self.root = root

    @staticmethod
    def _key(namespace: str, payload: dict) -> str:
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        return f"{namespace}-{hashlib.sha256(raw).hexdigest()}"

    def get(self, namespace: str, payload: dict, ttl_days: int) -> Any | None:
        path = self.root / f"{self._key(namespace, payload)}.json"
        if not path.exists():
            return None
        try:
            record = json.loads(path.read_text())
            fetched = datetime.fromisoformat(record["retrieved_at"])
            if datetime.now(timezone.utc) - fetched > timedelta(days=ttl_days):
                return None
            return record["data"]
        except (ValueError, KeyError, json.JSONDecodeError):
            return None

    def put(self, namespace: str, payload: dict, data: Any) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        path = self.root / f"{self._key(namespace, payload)}.json"
        path.write_text(json.dumps({
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "request": payload,
            "data": data,
        }, indent=2))
