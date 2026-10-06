"""People Also Ask extraction from DataForSEO advanced SERPs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class PAAQuestion:
    question: str
    source_keyword: str
    depth: int | None = None


def _walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def extract_paa(response: dict, source_keyword: str) -> list[PAAQuestion]:
    found: dict[str, PAAQuestion] = {}
    for node in _walk(response):
        node_type = str(node.get("type", "")).lower()
        if node_type not in {"people_also_ask", "people_also_ask_element"}:
            continue
        candidates: Iterable[dict] = node.get("items") or [node]
        for item in candidates:
            if not isinstance(item, dict):
                continue
            question = (item.get("title") or item.get("question") or "").strip()
            if not question:
                continue
            key = " ".join(question.lower().split())
            found.setdefault(
                key,
                PAAQuestion(
                    question=question,
                    source_keyword=source_keyword,
                    depth=item.get("depth"),
                ),
            )
    return list(found.values())
