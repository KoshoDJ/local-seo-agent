"""Provider-neutral DataForSEO evidence adapter."""

from .client import DataForSEOClient, DataForSEOError
from .confidence import ConfidenceGate, GateResult
from .content_match import ContentCandidate, ContentMatch, match_verified_content
from .opportunity import OpportunityInputs, OpportunityScore, score_opportunity
from .serp import SerpOverlap, compare_serps, organic_urls

__all__ = [
    "DataForSEOClient",
    "DataForSEOError",
    "ConfidenceGate",
    "GateResult",
    "ContentCandidate",
    "ContentMatch",
    "match_verified_content",
    "OpportunityInputs",
    "OpportunityScore",
    "score_opportunity",
    "SerpOverlap",
    "compare_serps",
    "organic_urls",
]
