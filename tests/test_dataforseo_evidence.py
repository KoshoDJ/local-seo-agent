"""Unit tests for deterministic Milestone 1 safeguards."""

import unittest

from code.dataforseo.confidence import ConfidenceGate
from code.dataforseo.content_match import ContentCandidate, match_verified_content
from code.dataforseo.paa import extract_paa


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


if __name__ == "__main__":
    unittest.main()
