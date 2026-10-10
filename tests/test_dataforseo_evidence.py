"""Unit tests for deterministic Milestone 1 safeguards."""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))

from dataforseo.confidence import ConfidenceGate
from dataforseo.content_match import ContentCandidate, match_verified_content
from dataforseo.paa import extract_paa
from dataforseo.opportunity import OpportunityInputs, score_opportunity
from dataforseo.serp import compare_serps


class EvidenceLayerTests(unittest.TestCase):
    def test_all_critical_gates_must_pass(self):
        result = ConfidenceGate().evaluate(
            search_evidence=.99,
            audience_fit=.99,
            destination_match=.94,
            content_quality=.99,
            destination_verified=True,
        )
        self.assertFalse(result.eligible)
        self.assertEqual(result.action, "human_review")
        self.assertIn("destination_match", result.failed_gates)

    def test_unverified_destination_is_rejected(self):
        result = ConfidenceGate().evaluate(
            search_evidence=1,
            audience_fit=1,
            destination_match=1,
            content_quality=1,
            destination_verified=False,
        )
        self.assertEqual(result.action, "reject")

    def test_match_excludes_unverified_and_wrong_cluster(self):
        candidates = [
            ContentCandidate("https://example.com/a", "Kids martial arts", "program", "karate", ("kids",), False),
            ContentCandidate("https://example.com/b", "Kids martial arts", "program", "karate", ("kids", "martial arts"), True),
            ContentCandidate("https://example.com/c", "Kids self defense", "program", "self-defense", ("kids",), True),
        ]
        result = match_verified_content("kids martial arts", candidates, required_cluster="karate")
        self.assertEqual(result.candidate.url, "https://example.com/b")

    def test_paa_deduplicates(self):
        response = {"tasks": [{"result": [{"items": [{
            "type": "people_also_ask",
            "items": [{"title": "Is karate good for kids?"}, {"title": "Is karate good for kids?"}],
        }]}]}]}
        questions = extract_paa(response, "kids karate")
        self.assertEqual(len(questions), 1)

    def test_serp_overlap_borderline_requires_review(self):
        def response(urls):
            return {"tasks": [{"result": [{"items": [
                {"type": "organic", "url": url} for url in urls
            ]}]}]}
        a = response(["https://a.com/1", "https://b.com/2", "https://c.com/3", "https://d.com/4"])
        b = response(["https://a.com/1", "https://b.com/2", "https://c.com/3", "https://x.com/9"])
        result = compare_serps(a, b)
        self.assertEqual(result.shared_urls, 3)
        self.assertEqual(result.decision, "insufficient_evidence")

    def test_opportunity_does_not_require_authority_score(self):
        result = score_opportunity(OpportunityInputs(
            intent_fit=1.0,
            serp_winnability=.8,
            topical_proximity=.9,
            business_value=1.0,
            demand_signal=.5,
            provider_difficulty=62,
        ))
        self.assertGreater(result.score, .8)
        self.assertEqual(result.components["provider_difficulty"], 62)
    def test_threshold_boundary(self):
        gate = ConfidenceGate()
        def evaluate(value):
            return gate.evaluate(search_evidence=value, audience_fit=1,
                                 destination_match=1, content_quality=1,
                                 destination_verified=True)
        self.assertEqual(evaluate(.96).action, "human_review")
        self.assertEqual(evaluate(.97).action, "autonomous")
        self.assertEqual(evaluate(.98).action, "autonomous")

    def test_invalid_confidence_is_rejected(self):
        self.assertEqual(ConfidenceGate().evaluate(
            search_evidence=float("nan"), audience_fit=1, destination_match=1,
            content_quality=1, destination_verified=True).action, "reject")

    def test_unverified_candidate_default(self):
        candidate = ContentCandidate("https://example.com", "Example", "article", "karate")
        self.assertFalse(candidate.verified)

    def test_lexical_match_never_certifies_destination(self):
        candidate = ContentCandidate("https://example.com/a", "kids karate", "article",
                                     "karate", ("kids", "karate"), True)
        result = match_verified_content("kids karate", [candidate])
        self.assertLess(result.score, .97)

    def test_complete_serp_borderline(self):
        def response(shared, prefix):
            urls = [f"https://shared.com/{i}" for i in range(shared)]
            urls += [f"https://{prefix}.com/{i}" for i in range(10 - shared)]
            return {"tasks": [{"result": [{"items": [
                {"type": "organic", "url": url} for url in urls
            ]}]}]}
        self.assertEqual(compare_serps(response(3, "one"), response(3, "two")).decision,
                         "manual_review")

if __name__ == "__main__":
    unittest.main()
