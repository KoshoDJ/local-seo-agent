"""Provider-neutral DataForSEO evidence adapter."""

from .client import DataForSEOClient, DataForSEOError
from .confidence import ConfidenceGate, GateResult
from .content_match import ContentCandidate, ContentMatch, match_verified_content

__all__ = [
    "DataForSEOClient",
    "DataForSEOError",
    "ConfidenceGate",
    "GateResult",
    "ContentCandidate",
    "ContentMatch",
    "match_verified_content",
]
