"""Normalize keyword metrics returned by the SEO provider."""

from dataclasses import dataclass


@dataclass(frozen=True)
class KeywordEvidence:
    keyword: str
    search_volume: int | None
    keyword_difficulty: float | None
    cpc: float | None
    intent: str | None
    source: str = "DataForSEO"


def extract_keyword_evidence(response: dict) -> list[KeywordEvidence]:
    rows = []
    for task in response.get("tasks") or []:
        for result in task.get("result") or []:
            # Keyword Overview returns result rows directly; other Labs endpoints
            # may wrap keyword rows under result.items.
            items = result.get("items")
            if items is None:
                items = [result]
            for item in items:
                keyword = item.get("keyword")
                if not keyword:
                    continue
                info = item.get("keyword_info") or {}
                props = item.get("keyword_properties") or {}
                difficulty = props.get("keyword_difficulty")
                rows.append(KeywordEvidence(
                    keyword=keyword,
                    search_volume=info.get("search_volume"),
                    keyword_difficulty=float(difficulty) if difficulty is not None else None,
                    cpc=info.get("cpc"),
                    intent=(item.get("search_intent_info") or {}).get("main_intent"),
                ))
    return rows
