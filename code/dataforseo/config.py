"""Configuration for DataForSEO and evidence-layer safeguards."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


class ConfigurationError(RuntimeError):
    pass


@dataclass(frozen=True)
class DataForSEOConfig:
    login: str
    password: str
    location_code: int | None
    location_name: str | None
    language_code: str
    max_serp_calls: int
    max_keyword_calls: int
    cache_dir: Path

    @classmethod
    def from_env(cls) -> "DataForSEOConfig":
        login = os.getenv("DATAFORSEO_LOGIN", "").strip()
        password = os.getenv("DATAFORSEO_PASSWORD", "").strip()
        if not login or not password:
            raise ConfigurationError(
                "DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD must be configured."
            )
        raw_location = os.getenv("DATAFORSEO_LOCATION_CODE", "").strip()
        return cls(
            login=login,
            password=password,
            location_code=int(raw_location) if raw_location else None,
            location_name=os.getenv("DATAFORSEO_LOCATION_NAME", "").strip() or None,
            language_code=os.getenv("DATAFORSEO_LANGUAGE_CODE", "en").strip() or "en",
            max_serp_calls=int(os.getenv("DATAFORSEO_MAX_SERP_CALLS_PER_RUN", "25")),
            max_keyword_calls=int(os.getenv("DATAFORSEO_MAX_KEYWORD_CALLS_PER_RUN", "50")),
            cache_dir=Path(os.getenv("DATAFORSEO_CACHE_DIR", "data/seo-cache")),
        )

    def location_payload(self) -> dict:
        if self.location_code is not None:
            return {"location_code": self.location_code}
        if self.location_name:
            return {"location_name": self.location_name}
        raise ConfigurationError(
            "Set DATAFORSEO_LOCATION_CODE or DATAFORSEO_LOCATION_NAME; "
            "SEO evidence must not silently default to the wrong market."
        )
