"""Normalize DataForSEO SERPs and compare result overlap."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlsplit, urlunsplit


@dataclass(frozen=True)
class SerpOverlap:
    shared_urls: int
    threshold: int
    decision: str
    urls_a: tuple[str, ...]
    urls_b: tuple[str, ...]


def canonical_url(url: str) -> str:
    parts = urlsplit(url)
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, "", ""))


def organic_urls(response: dict, limit: int = 10) -> tuple[str, ...]:
    urls: list[str] = []
    for task in response.get("tasks") or []:
        for result in task.get("result") or []:
            for item in result.get("items") or []:
                if item.get("type") != "organic" or not item.get("url"):
                    continue
                url = canonical_url(item["url"])
                if url not in urls:
                    urls.append(url)
                if len(urls) >= limit:
                    return tuple(urls)
    return tuple(urls)


def compare_serps(a: dict, b: dict, threshold: int = 4) -> SerpOverlap:
    urls_a, urls_b = organic_urls(a), organic_urls(b)
    shared = len(set(urls_a) & set(urls_b))
    # 4/10 is an internal convention. Exactly 3 is deliberately manual because
    # SERPs move and a one-URL change would flip the page decision.
    if shared >= threshold:
        decision = "same_page"
    elif shared <= 2:
        decision = "separate_pages"
    else:
        decision = "manual_review"
    return SerpOverlap(shared, threshold, decision, urls_a, urls_b)
