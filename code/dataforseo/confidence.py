"""Critical confidence gates for autonomous SEO/content actions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GateResult:
    eligible: bool
    action: str
    failed_gates: tuple[str, ...]


@dataclass(frozen=True)
class ConfidenceGate:
    autonomous_threshold: float = 0.95
    review_threshold: float = 0.80

    def evaluate(
        self,
        *,
        search_evidence: float,
        audience_fit: float,
        destination_match: float,
        content_quality: float,
        destination_verified: bool,
    ) -> GateResult:
        scores = {
            "search_evidence": search_evidence,
            "audience_fit": audience_fit,
            "destination_match": destination_match,
            "content_quality": content_quality,
        }
        if not destination_verified:
            return GateResult(False, "reject", ("destination_verified",))

        failed_auto = tuple(k for k, v in scores.items() if v < self.autonomous_threshold)
        if not failed_auto:
            return GateResult(True, "autonomous", ())

        if all(v >= self.review_threshold for v in scores.values()):
            return GateResult(False, "human_review", failed_auto)

        failed_review = tuple(k for k, v in scores.items() if v < self.review_threshold)
        return GateResult(False, "reject", failed_review)
