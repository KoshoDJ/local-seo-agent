"""Organic SERP normalization and conservative clustering."""

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
    p = urlsplit(url)
    if p.scheme not in ("https", "http") or not p.netloc:
        return ""
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path.rstrip("/") or "/", "", ""))


def organic_urls(response: dict, limit: int = 10) -> tuple[str, ...]:
    urls = []
    for task in response.get("tasks") or []:
        if task.get("status_code") not in (None, 20000):
            continue
        for result in task.get("result") or []:
            for item in result.get("items") or []:
                if item.get("type") != "organic":
                    continue
                url = canonical_url(item.get("url", ""))
                if url and url not in urls:
                    urls.append(url)
                if len(urls) == limit:
                    return tuple(urls)
    return tuple(urls)


def compare_serps(a: dict, b: dict, threshold: int = 4) -> SerpOverlap:
    aa, bb = organic_urls(a), organic_urls(b)
    shared = len(set(aa) & set(bb))
    if len(aa) < 10 or len(bb) < 10:
        decision = "insufficient_evidence"
    elif shared >= threshold:
        decision = "same_page"
    elif shared <= 2:
        decision = "separate_pages"
    else:
        decision = "manual_review"
    return SerpOverlap(shared, threshold, decision, aa, bb)
