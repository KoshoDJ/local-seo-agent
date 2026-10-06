# DataForSEO evidence layer

Milestone 1 keeps SEO evidence separate from orchestration and content generation.

## Rules

1. No numeric search-volume estimates. Missing provider data is N/A.
2. Location is explicit. The client will not silently default to a market.
3. Paid API calls are cached and subject to per-run hard budgets.
4. DataForSEO is evidence, not the decision maker.
5. PAA/intent/SERP evidence may propose content opportunities, but destination URLs must come from a verified registry.
6. Autonomous actions require every critical confidence gate to meet the threshold; weak scores cannot be averaged away.
7. n8n/Airtable/LLMs are downstream capabilities. They do not own these SEO rules.

Default freshness:
- SERP/PAA: 7 days
- keyword metrics/intent: 30 days

The first adapter intentionally uses Python standard library only so it does not introduce a dependency-management requirement into the existing repository.

## Phase 2 keyword research

`/keyword-research` now uses provider-neutral evidence rules:
- DataForSEO metrics are localized and never replaced with invented numeric estimates.
- Search intent labels are hints; live top-10 SERP composition is the final evidence.
- SERP clustering uses the repository convention: 4+ shared top-10 organic URLs = same-page candidate, 0-2 = separate-page candidate, exactly 3 = manual review.
- Opportunity scoring prioritizes intent fit, live-SERP winnability, topical proximity and business value over raw demand.
- DataForSEO keyword difficulty is retained as evidence but is never subtracted from a domain-authority metric.
- Money/service pages remain governed by what the business actually sells; opportunity scoring controls prioritization, not whether a legitimate service exists.
