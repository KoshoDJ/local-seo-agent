"""Provider-neutral opportunity scoring.

This score prioritizes work; it never authorizes a new URL or autonomous publish.
No Authority Score arithmetic is used.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OpportunityInputs:
    intent_fit: float
    serp_winnability: float
    topical_proximity: float
    business_value: float
    demand_signal: float
    provider_difficulty: float | None = None


@dataclass(frozen=True)
class OpportunityScore:
    score: float
    components: dict[str, float]


def score_opportunity(inputs: OpportunityInputs) -> OpportunityScore:
    values = {
        "intent_fit": inputs.intent_fit,
        "serp_winnability": inputs.serp_winnability,
        "topical_proximity": inputs.topical_proximity,
        "business_value": inputs.business_value,
        "demand_signal": inputs.demand_signal,
    }
    if any(v < 0 or v > 1 for v in values.values()):
        raise ValueError("Opportunity components must be normalized to 0..1")

    # Live evidence and business fit outweigh raw demand. Difficulty is retained
    # as evidence but is not subtracted from a domain-authority metric.
    weights = {
        "intent_fit": .25,
        "serp_winnability": .25,
        "topical_proximity": .20,
        "business_value": .20,
        "demand_signal": .10,
    }
    score = sum(values[k] * weights[k] for k in weights)
    components = dict(values)
    if inputs.provider_difficulty is not None:
        components["provider_difficulty"] = inputs.provider_difficulty
    return OpportunityScore(round(score, 4), components)
