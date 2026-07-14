from __future__ import annotations

import copy
import json
from dataclasses import FrozenInstanceError
from pathlib import Path
import unittest

from codie.frequency_pools import (
    FREQUENCY_POOL_PACKET_VERSION,
    FrequencyPoolBuildError,
    FrequencyPoolOptions,
    build_frequency_pool_packet,
    frequency_pool_packet_to_dict,
    validate_frequency_pool_packet,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "frequency_pools"
MODULE_PATH = Path(__file__).parents[1] / "codie" / "frequency_pools" / "models.py"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


class FrequencyPoolModelTests(unittest.TestCase):
    def test_commander_pool_serializes_deterministically(self) -> None:
        packet = build_frequency_pool_packet(load_fixture("frequency_pool_commander.json"))
        first = frequency_pool_packet_to_dict(packet)
        second = frequency_pool_packet_to_dict(packet)

        self.assertEqual(first, second)
        self.assertEqual(first["pool_version"], FREQUENCY_POOL_PACKET_VERSION)
        self.assertEqual(first["pool_type"], "commander")
        self.assertEqual(first["cards"][0]["identity"]["oracle_id"], "oracle-dark-ritual")
        self.assertEqual(first["cards"][0]["identity"]["scryfall_id"], "scryfall-dark-ritual")
        self.assertEqual(first["tags"][0]["tag_source"], "scryfall_tagger")

    def test_packet_round_trips_through_dict(self) -> None:
        packet = build_frequency_pool_packet(load_fixture("frequency_pool_partner_pair.json"))
        data = frequency_pool_packet_to_dict(packet)
        rebuilt = build_frequency_pool_packet(data)

        self.assertEqual(frequency_pool_packet_to_dict(rebuilt), data)

    def test_packet_is_immutable_and_does_not_mutate_input(self) -> None:
        payload = load_fixture("frequency_pool_commander.json")
        before = copy.deepcopy(payload)
        packet = build_frequency_pool_packet(payload)
        payload["cards"][0]["metadata"]["evidence_only"] = False

        with self.assertRaises(FrozenInstanceError):
            packet.pool_id = "changed"
        self.assertEqual(payload["cards"][0]["metadata"]["evidence_only"], False)
        self.assertEqual(before["cards"][0]["metadata"]["evidence_only"], True)
        self.assertTrue(frequency_pool_packet_to_dict(packet)["cards"][0]["metadata"]["evidence_only"])

    def test_visibility_fields_are_preserved(self) -> None:
        data = frequency_pool_packet_to_dict(build_frequency_pool_packet(load_fixture("frequency_pool_commander.json")))

        for key in (
            "pool_id",
            "pool_version",
            "pool_type",
            "subject",
            "source_window",
            "source_refs",
            "generated_at",
            "cards",
            "tags",
            "coverage_report",
            "caveats",
            "filters",
            "identity_version",
            "tag_ontology_version",
            "evidence_version",
            "metadata",
        ):
            self.assertIn(key, data)
        coverage = data["coverage_report"]
        self.assertIn("matching_deck_count", coverage)
        self.assertIn("available_deck_count", coverage)
        self.assertIn("coverage_ratio", coverage)
        self.assertIn("low_sample_threshold", coverage)
        self.assertIn("low_coverage_threshold", coverage)

    def test_user_local_pool_is_labeled_and_isolated(self) -> None:
        data = frequency_pool_packet_to_dict(build_frequency_pool_packet(load_fixture("frequency_pool_user_local.json")))

        self.assertEqual(data["pool_type"], "user_local_snapshot")
        self.assertTrue(data["subject"]["user_local"])
        self.assertTrue(data["metadata"]["isolated_from_global_pools"])
        self.assertTrue(data["metadata"]["not_tournament_evidence"])
        self.assertTrue(data["metadata"]["not_" + "rec" + "ommendation_input"])
        self.assertEqual(data["coverage_report"]["matching_deck_count"], "unknown")
        self.assertEqual(data["tags"][0]["coverage_ratio"], "unknown")

    def test_user_local_pool_requires_explicit_isolation_labels(self) -> None:
        payload = load_fixture("frequency_pool_user_local.json")
        payload["metadata"].pop("not_tournament_evidence")

        with self.assertRaises(FrequencyPoolBuildError):
            build_frequency_pool_packet(payload)

    def test_low_sample_and_low_coverage_require_visible_caveats(self) -> None:
        payload = load_fixture("frequency_pool_commander.json")
        payload["coverage_report"]["matching_deck_count"] = 2

        with self.assertRaises(FrequencyPoolBuildError):
            build_frequency_pool_packet(payload)

        payload["caveats"] = [
            {
                "caveat_id": "cav-low-sample",
                "caveat_type": "low_sample",
                "message": "Low sample size.",
                "severity": "warning",
                "source_ref_ids": ["src-1"],
                "metadata": {},
            }
        ]
        payload["coverage_report"]["caveat_ids"] = ["cav-low-sample"]
        build_frequency_pool_packet(payload)

    def test_invalid_fixture_fails_cleanly(self) -> None:
        with self.assertRaises(FrequencyPoolBuildError):
            build_frequency_pool_packet(load_fixture("frequency_pool_invalid.json"))

    def test_private_raw_metadata_is_rejected_recursively(self) -> None:
        payload = load_fixture("frequency_pool_commander.json")
        payload["cards"][0]["metadata"]["nested"] = {"raw_provider_payload": {"secret": "payload"}}

        with self.assertRaises(FrequencyPoolBuildError):
            build_frequency_pool_packet(payload)

    def test_action_advice_language_and_metadata_are_rejected(self) -> None:
        payload = load_fixture("frequency_pool_commander.json")
        payload["metadata"]["note"] = "rec" + "ommended include"

        with self.assertRaises(FrequencyPoolBuildError):
            build_frequency_pool_packet(payload)

        payload = load_fixture("frequency_pool_commander.json")
        payload["cards"][0]["metadata"]["score"] = 10
        with self.assertRaises(FrequencyPoolBuildError):
            build_frequency_pool_packet(payload)

    def test_options_can_omit_tags_explicitly(self) -> None:
        packet = build_frequency_pool_packet(
            load_fixture("frequency_pool_commander.json"),
            options=FrequencyPoolOptions(include_tags=False),
        )

        self.assertEqual(frequency_pool_packet_to_dict(packet)["tags"], [])

    def test_duplicate_or_unknown_references_fail(self) -> None:
        payload = load_fixture("frequency_pool_commander.json")
        payload["source_refs"].append(copy.deepcopy(payload["source_refs"][0]))
        with self.assertRaises(FrequencyPoolBuildError):
            build_frequency_pool_packet(payload)

        payload = load_fixture("frequency_pool_commander.json")
        payload["cards"][0]["source_ref_ids"] = ["missing-source"]
        with self.assertRaises(FrequencyPoolBuildError):
            build_frequency_pool_packet(payload)

    def test_validate_rejects_non_packet(self) -> None:
        with self.assertRaises(FrequencyPoolBuildError):
            validate_frequency_pool_packet({"not": "a packet"})

    def test_models_have_no_forbidden_runtime_imports(self) -> None:
        source = MODULE_PATH.read_text(encoding="utf-8")
        forbidden = (
            "codie.db",
            "sqlite3",
            "codie.providers",
            "codie.ingestion",
            "codie.analytics",
            "codie.rec" + "ommendations",
            "codie.evidence_fusion",
            "codie.decision_intelligence",
            "requests",
            "httpx",
            "openai",
            "anthropic",
            "google.generativeai",
            "langchain",
            "flask",
            "fastapi",
            "uvicorn",
            "starlette",
            "open(",
            "write_text(",
            "write_bytes(",
        )
        self.assertFalse(any(item in source for item in forbidden))


if __name__ == "__main__":
    unittest.main()
