"""Candidate discovery only; lexical relevance never grants publishing confidence."""

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
    verified: bool = False


@dataclass(frozen=True)
class ContentMatch:
    candidate: ContentCandidate | None
    score: float
    reasons: tuple[str, ...]


_STOPWORDS = {"a", "an", "the", "is", "are", "for", "to", "of", "and", "in", "at", "on", "do", "does"}


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower())) - _STOPWORDS


def match_verified_content(query: str, candidates: list[ContentCandidate],
                           required_cluster: str | None = None) -> ContentMatch:
    q = _tokens(query)
    best = ContentMatch(None, 0.0, ("no verified candidate",))
    for candidate in candidates:
        parsed = urlparse(candidate.url)
        if not candidate.verified or parsed.scheme != "https" or not parsed.hostname:
            continue
        if required_cluster and candidate.cluster != required_cluster:
            continue
        target = _tokens(" ".join((candidate.title, candidate.cluster, *candidate.keywords)))
        if not q or not target:
            continue
        overlap = len(q & target) / len(q)
        # This is a retrieval ranking, NOT a calibrated relevance probability.
        score = min(overlap, 0.79)
        if score > best.score:
            best = ContentMatch(candidate, score,
                (f"lexical_retrieval={overlap:.3f}", "requires_semantic_and_factual_review"))
    return best
