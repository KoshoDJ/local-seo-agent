"""Fail-closed content decision gates. Scores are evidence assessments, not probabilities."""

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class GateResult:
    eligible: bool
    action: str
    failed_gates: tuple[str, ...]


@dataclass(frozen=True)
class ConfidenceGate:
    autonomous_threshold: float = 0.97
    review_threshold: float = 0.80

    def evaluate(self, *, search_evidence: float, audience_fit: float,
                 destination_match: float, content_quality: float,
                 destination_verified: bool) -> GateResult:
        scores = dict(search_evidence=search_evidence, audience_fit=audience_fit,
                      destination_match=destination_match, content_quality=content_quality)
        invalid = tuple(k for k, v in scores.items()
                        if isinstance(v, bool) or not isinstance(v, (int, float))
                        or not isfinite(v) or not 0 <= v <= 1)
        if invalid:
            return GateResult(False, "reject", invalid)
        if not destination_verified:
            return GateResult(False, "reject", ("destination_verified",))
        below_auto = tuple(k for k, v in scores.items() if v < self.autonomous_threshold)
        if not below_auto:
            return GateResult(True, "autonomous", ())
        below_review = tuple(k for k, v in scores.items() if v < self.review_threshold)
        if below_review:
            return GateResult(False, "reject", below_review)
        return GateResult(False, "human_review", below_auto)
