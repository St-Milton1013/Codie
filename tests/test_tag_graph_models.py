from __future__ import annotations

import copy
import json
from dataclasses import FrozenInstanceError
from pathlib import Path
import unittest

from codie.tag_graphs import (
    TAG_GRAPH_PACKET_VERSION,
    TagGraphBuildError,
    TagGraphOptions,
    build_tag_graph_packet,
    tag_graph_packet_to_dict,
    validate_tag_graph_packet,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "tag_graphs"
MODULE_PATH = Path(__file__).parents[1] / "codie" / "tag_graphs" / "models.py"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


class TagGraphModelTests(unittest.TestCase):
    def test_comparison_packet_serializes_deterministically(self) -> None:
        packet = build_tag_graph_packet(load_fixture("tag_graph_comparison.json"))
        first = tag_graph_packet_to_dict(packet)
        second = tag_graph_packet_to_dict(packet)

        self.assertEqual(first, second)
        self.assertEqual(first["graph_version"], TAG_GRAPH_PACKET_VERSION)
        self.assertEqual(first["graph_type"], "deck_vs_commander_average")
        self.assertEqual(first["selected_tags"][0]["tag_source"], "scryfall_tagger")
        self.assertEqual(first["metric_rows"][0]["source_packet_ids"], ["pool-user-local-bluefarm"])

    def test_packet_round_trips_through_dict(self) -> None:
        packet = build_tag_graph_packet(load_fixture("tag_graph_comparison.json"))
        data = tag_graph_packet_to_dict(packet)
        rebuilt = build_tag_graph_packet(data)

        self.assertEqual(tag_graph_packet_to_dict(rebuilt), data)

    def test_packet_is_immutable_and_does_not_mutate_input(self) -> None:
        payload = load_fixture("tag_graph_comparison.json")
        before = copy.deepcopy(payload)
        packet = build_tag_graph_packet(payload)
        payload["metadata"]["evidence_only"] = False

        with self.assertRaises(FrozenInstanceError):
            packet.graph_id = "changed"
        self.assertEqual(before["metadata"]["evidence_only"], True)
        self.assertTrue(tag_graph_packet_to_dict(packet)["metadata"]["evidence_only"])

    def test_required_visibility_fields_are_preserved(self) -> None:
        data = tag_graph_packet_to_dict(build_tag_graph_packet(load_fixture("tag_graph_comparison.json")))

        for key in (
            "graph_id",
            "graph_version",
            "graph_type",
            "subject",
            "selected_tags",
            "comparison_refs",
            "source_packet_ids",
            "metric_rows",
            "contributor_rows",
            "overlap_rows",
            "correlation_rows",
            "trend_rows",
            "numeric_tables",
            "card_lists",
            "caveats",
            "filters",
            "frequency_pool_packet_version",
            "tag_ontology_version",
            "evidence_version",
        ):
            self.assertIn(key, data)
        metric = data["metric_rows"][0]
        for key in (
            "raw_tag_count",
            "tag_density",
            "tag_inclusion_rate",
            "average_cards_per_deck_with_tag",
            "placement_weighted_tag_usage",
            "top_cut_tag_frequency",
            "winner_tag_frequency",
            "tag_trend_delta",
            "tag_confidence",
            "matching_deck_count",
            "available_deck_count",
            "coverage_ratio",
        ):
            self.assertIn(key, metric)

    def test_trend_packet_accepts_trend_rows_only(self) -> None:
        data = tag_graph_packet_to_dict(build_tag_graph_packet(load_fixture("tag_graph_trend.json")))

        self.assertEqual(data["graph_type"], "tag_trend_line")
        self.assertEqual(data["trend_rows"][0]["delta"], 0.06)
        self.assertEqual(data["metric_rows"], [])

    def test_selected_tags_must_be_one_to_six_and_unique(self) -> None:
        payload = load_fixture("tag_graph_comparison.json")
        payload["selected_tags"] = payload["selected_tags"] * 4
        with self.assertRaises(TagGraphBuildError):
            build_tag_graph_packet(payload)

        payload = load_fixture("tag_graph_comparison.json")
        payload["selected_tags"].append(copy.deepcopy(payload["selected_tags"][0]))
        with self.assertRaises(TagGraphBuildError):
            build_tag_graph_packet(payload)

    def test_invalid_fixture_fails_cleanly(self) -> None:
        with self.assertRaises(TagGraphBuildError):
            build_tag_graph_packet(load_fixture("tag_graph_invalid.json"))

    def test_private_raw_metadata_is_rejected_recursively(self) -> None:
        payload = load_fixture("tag_graph_comparison.json")
        payload["metric_rows"][0]["metadata"]["nested"] = {"raw_provider_payload": {"hidden": true_value()}}

        with self.assertRaises(TagGraphBuildError):
            build_tag_graph_packet(payload)

    def test_action_advice_language_and_metadata_are_rejected(self) -> None:
        payload = load_fixture("tag_graph_comparison.json")
        payload["metadata"]["note"] = "rec" + "ommended include"
        with self.assertRaises(TagGraphBuildError):
            build_tag_graph_packet(payload)

        payload = load_fixture("tag_graph_comparison.json")
        payload["metric_rows"][0]["metadata"]["score"] = 1
        with self.assertRaises(TagGraphBuildError):
            build_tag_graph_packet(payload)

    def test_unknown_source_or_caveat_references_fail(self) -> None:
        payload = load_fixture("tag_graph_comparison.json")
        payload["metric_rows"][0]["source_packet_ids"] = ["missing-packet"]
        with self.assertRaises(TagGraphBuildError):
            build_tag_graph_packet(payload)

        payload = load_fixture("tag_graph_comparison.json")
        payload["metric_rows"][0]["caveat_ids"] = ["missing-caveat"]
        with self.assertRaises(TagGraphBuildError):
            build_tag_graph_packet(payload)

    def test_options_can_omit_tables_and_card_lists(self) -> None:
        packet = build_tag_graph_packet(
            load_fixture("tag_graph_comparison.json"),
            options=TagGraphOptions(include_numeric_tables=False, include_card_lists=False),
        )
        data = tag_graph_packet_to_dict(packet)

        self.assertEqual(data["numeric_tables"], [])
        self.assertEqual(data["card_lists"], [])

    def test_validate_rejects_non_packet(self) -> None:
        with self.assertRaises(TagGraphBuildError):
            validate_tag_graph_packet({"not": "a packet"})

    def test_module_has_no_forbidden_runtime_imports(self) -> None:
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


def true_value() -> bool:
    return True


if __name__ == "__main__":
    unittest.main()
