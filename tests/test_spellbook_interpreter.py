from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from codie.combos.spellbook_interpreter import (
    SPELLBOOK_INTERPRETER_VERSION,
    SpellbookInterpreterError,
    SpellbookInterpreterOptions,
    build_spellbook_combo_interpretation,
    spellbook_combo_interpretation_to_dict,
    validate_spellbook_combo_interpretation,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "spellbook_interpreter"
MODULE_PATH = Path(__file__).parents[1] / "codie" / "combos" / "spellbook_interpreter.py"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


class SpellbookInterpreterTest(unittest.TestCase):
    def test_valid_combo_output_classification(self) -> None:
        interpretation = build_spellbook_combo_interpretation(
            load_fixture("spellbook_combo_outputs.json"),
            options=SpellbookInterpreterOptions(target_output_classes=("infinite_mana", "win_condition")),
            generated_at="2026-07-13T00:00:00Z",
        )
        data = spellbook_combo_interpretation_to_dict(interpretation)

        self.assertEqual(data["interpreter_version"], SPELLBOOK_INTERPRETER_VERSION)
        self.assertEqual(data["provider"], "commander_spellbook")
        self.assertEqual(data["provider_combo_id"], "spellbook-output-1")
        self.assertEqual(data["variant_ids"], ["variant-a", "variant-b"])
        self.assertEqual(
            [item["output_class"] for item in data["output_classes"]],
            ["infinite_mana", "infinite_draw"],
        )
        self.assertEqual(data["source_refs"][0]["raw_payload_hash"], "sha256:output-fixture")
        self.assertEqual(data["target_compatibility_items"][0]["compatibility"], "can_satisfy_target_output_class")

    def test_prerequisite_and_restriction_classification(self) -> None:
        data = spellbook_combo_interpretation_to_dict(
            build_spellbook_combo_interpretation(load_fixture("spellbook_combo_restrictions.json"))
        )

        self.assertIn(
            "requires_battlefield",
            {item["prerequisite_class"] for item in data["prerequisite_classes"]},
        )
        self.assertIn(
            "requires_tap",
            {item["prerequisite_class"] for item in data["prerequisite_classes"]},
        )
        self.assertIn(
            "summoning_sickness_sensitive",
            {item["restriction_class"] for item in data["restriction_classes"]},
        )
        self.assertIn(
            "once_per_turn_limit",
            {item["restriction_class"] for item in data["restriction_classes"]},
        )

    def test_unknowns_and_unsupported_items_remain_visible(self) -> None:
        data = spellbook_combo_interpretation_to_dict(
            build_spellbook_combo_interpretation(load_fixture("spellbook_combo_unknowns.json"))
        )

        self.assertEqual(data["output_classes"][0]["output_class"], "unknown")
        self.assertTrue(data["manual_review_items"])
        self.assertTrue(data["unsupported_items"])
        self.assertEqual(data["manual_review_items"][0]["item_type"], "missing_component_role")

    def test_options_can_hide_manual_review_and_unsupported_items_explicitly(self) -> None:
        data = spellbook_combo_interpretation_to_dict(
            build_spellbook_combo_interpretation(
                load_fixture("spellbook_combo_unknowns.json"),
                options=SpellbookInterpreterOptions(
                    include_manual_review_items=False,
                    include_unsupported_items=False,
                ),
            )
        )

        self.assertEqual(data["manual_review_items"], [])
        self.assertEqual(data["unsupported_items"], [])

    def test_deterministic_serialization_and_round_trip(self) -> None:
        interpretation = build_spellbook_combo_interpretation(
            load_fixture("spellbook_combo_outputs.json"),
            generated_at="2026-07-13T00:00:00Z",
        )
        first = spellbook_combo_interpretation_to_dict(interpretation)
        second = spellbook_combo_interpretation_to_dict(interpretation)

        self.assertEqual(first, second)
        rebuilt = build_spellbook_combo_interpretation(first)
        self.assertEqual(spellbook_combo_interpretation_to_dict(rebuilt), first)

    def test_input_payload_is_not_mutated(self) -> None:
        payload = load_fixture("spellbook_combo_outputs.json")
        before = copy.deepcopy(payload)

        build_spellbook_combo_interpretation(payload)

        self.assertEqual(payload, before)

    def test_malformed_payload_fails_cleanly(self) -> None:
        with self.assertRaises(SpellbookInterpreterError):
            build_spellbook_combo_interpretation({"provider_combo_id": "bad", "outputs": []})

    def test_no_combo_ranking_or_recommendation_language(self) -> None:
        data = spellbook_combo_interpretation_to_dict(
            build_spellbook_combo_interpretation(load_fixture("spellbook_combo_outputs.json"))
        )
        encoded = json.dumps(data, sort_keys=True).lower()

        forbidden = (
            "should include",
            "should cut",
            "must include",
            "must cut",
            "recommended include",
            "recommended cut",
            "strict upgrade",
            "score",
            "rank",
        )
        self.assertFalse(any(phrase in encoded for phrase in forbidden))

    def test_invalid_recommendation_language_is_rejected(self) -> None:
        interpretation = build_spellbook_combo_interpretation(load_fixture("spellbook_combo_outputs.json"))
        data = spellbook_combo_interpretation_to_dict(interpretation)
        data["warnings"] = [{"warning_type": "bad", "message": "recommended include"}]

        with self.assertRaises(SpellbookInterpreterError):
            validate_spellbook_combo_interpretation(build_spellbook_combo_interpretation(data))

    def test_interpreter_has_no_forbidden_runtime_imports(self) -> None:
        source = MODULE_PATH.read_text(encoding="utf-8")
        forbidden = (
            "codie.db",
            "sqlite3",
            "codie.providers",
            "codie.ingestion",
            "codie.analytics",
            "codie.recommendations",
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
        )
        self.assertFalse(any(item in source for item in forbidden))


if __name__ == "__main__":
    unittest.main()
