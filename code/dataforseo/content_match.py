"""Deterministic first-pass matching against a verified URL registry.

Semantic/LLM reasoning may propose candidates, but only verified registry URLs are eligible
and autonomous use requires the deterministic critical gates in confidence.py.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class ContentCandidate:
    url: str
    title: str
    page_type: str
    cluster: str
    keywords: tuple[str, ...] = ()
    verified: bool = True


@dataclass(frozen=True)
class ContentMatch:
    candidate: ContentCandidate | None
    score: float
    reasons: tuple[str, ...]


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def match_verified_content(
    query: str,
    candidates: list[ContentCandidate],
    required_cluster: str | None = None,
) -> ContentMatch:
    q = _tokens(query)
    best: ContentMatch = ContentMatch(None, 0.0, ("no verified candidate",))
    for candidate in candidates:
        if not candidate.verified:
            continue
        if urlparse(candidate.url).scheme not in {"http", "https"}:
            continue
        if required_cluster and candidate.cluster != required_cluster:
            continue

        target = _tokens(
            " ".join([candidate.title, candidate.page_type, candidate.cluster, *candidate.keywords])
        )
        if not q or not target:
            continue
        overlap = len(q & target) / len(q)
        specificity = 0.10 if candidate.page_type in {"supporting", "article", "service", "program"} else 0.0
        score = min(1.0, overlap + specificity)
        reasons = (
            f"token_overlap={overlap:.3f}",
            f"specificity_bonus={specificity:.2f}",
            "verified_url=true",
        )
        if score > best.score:
            best = ContentMatch(candidate, score, reasons)
    return best
