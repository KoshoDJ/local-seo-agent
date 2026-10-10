"""Stage 1: deterministic DataForSEO contract tests without paid API calls."""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from dataforseo.client import DataForSEOClient, DataForSEOError
from dataforseo.config import DataForSEOConfig
from dataforseo.costs import BudgetExceeded
from dataforseo.keywords import extract_keyword_evidence
from dataforseo.paa import extract_paa


class Response:
    def __init__(self, data):
        self.data = json.dumps(data).encode()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.data


def envelope(task_status=20000, results=None):
    return {"status_code": 20000, "tasks": [
        {"status_code": task_status, "status_message": "fixture",
         "result": results if results is not None else [{"items": []}]}
    ]}


class DataForSEOContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.config = DataForSEOConfig("login", "password", 2840, None, "en",
                                      1, 2, Path(self.tmp.name))
        self.client = DataForSEOClient(self.config)

    def test_serp_endpoint_and_location(self):
        with patch("dataforseo.client.urllib.request.urlopen",
                   return_value=Response(envelope())) as request:
            self.client.serp("kids karate")
        sent = json.loads(request.call_args.args[0].data)
        self.assertEqual(sent[0]["location_code"], 2840)
        self.assertEqual(sent[0]["language_code"], "en")
        self.assertEqual(sent[0]["depth"], 10)
        self.assertIn("serp/google/organic/live/advanced", request.call_args.args[0].full_url)

    def test_cache_prevents_second_paid_call(self):
        with patch("dataforseo.client.urllib.request.urlopen",
                   return_value=Response(envelope())) as request:
            self.client.serp("kids karate")
            self.client.serp("kids karate")
        self.assertEqual(request.call_count, 1)

    def test_budget_blocks_second_distinct_serp(self):
        with patch("dataforseo.client.urllib.request.urlopen",
                   return_value=Response(envelope())) as request:
            self.client.serp("kids karate")
            with self.assertRaises(BudgetExceeded):
                self.client.serp("adult karate")
        self.assertEqual(request.call_count, 1)

    def test_task_failure_rejected_not_cached(self):
        with patch("dataforseo.client.urllib.request.urlopen",
                   return_value=Response(envelope(40501))):
            with self.assertRaises(DataForSEOError):
                self.client.serp("kids karate")
        self.assertEqual(len(list(Path(self.tmp.name).glob("*.json"))), 0)

    def test_missing_result_rejected(self):
        with patch("dataforseo.client.urllib.request.urlopen",
                   return_value=Response(envelope(results=[]))):
            with self.assertRaises(DataForSEOError):
                self.client.serp("kids karate")

    def test_timeout_rejected(self):
        with patch("dataforseo.client.urllib.request.urlopen",
                   side_effect=URLError("timeout")):
            with self.assertRaises(DataForSEOError):
                self.client.serp("kids karate")

    def test_direct_keyword_overview_shape(self):
        result = extract_keyword_evidence(envelope(results=[{
            "keyword": "kids karate el cajon",
            "keyword_info": {"search_volume": 120, "cpc": 2.1},
            "keyword_properties": {"keyword_difficulty": 19},
            "search_intent_info": {"main_intent": "commercial"}
        }]))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].search_volume, 120)
        self.assertEqual(result[0].keyword_difficulty, 19)

    def test_nested_keyword_shape(self):
        result = extract_keyword_evidence(envelope(results=[{
            "items": [{"keyword": "martial arts", "keyword_info": {"search_volume": 10}}]
        }]))
        self.assertEqual(result[0].keyword, "martial arts")

    def test_paa_fixture(self):
        response = envelope(results=[{"items": [
            {"type": "people_also_ask", "items": [
                {"title": "What age should children start karate?"}
            ]}
        ]}])
        self.assertEqual(extract_paa(response, "kids karate")[0].question,
                         "What age should children start karate?")


if __name__ == "__main__":
    unittest.main()
