from __future__ import annotations

import ast
import json
import unittest
from pathlib import Path

from codie.probability_engine import (
    CardDefinitionManager,
    CardDefinitionStatus,
    SimulationDeck,
    SimulationDeckCard,
    SimulationTargetCondition,
    build_card_definition_load_result,
    classify_card_relevance,
    load_behavior_overlay_rows,
)


FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "probability_engine" / "card_definitions"


class ProbabilityEngineCardDefinitionManagerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.overlay_rows = json.loads((FIXTURE_ROOT / "simple_behavior_overlays.json").read_text(encoding="utf-8"))
        self.target = SimulationTargetCondition(
            target_card="Rhystic Study",
            target_card_id="rhystic_study",
            target_zone="stack",
            turn=2,
            condition_type="cast_or_access",
        )

    def test_load_behavior_overlay_rows_preserves_unknown_metadata(self) -> None:
        overlays = {card.card_id: card for card in load_behavior_overlay_rows(self.overlay_rows)}

        self.assertEqual(overlays["sol_ring"].board_abilities[0].produces[0].C, 2)
        self.assertTrue(overlays["mystery_card"].board_abilities[0].metadata["unmodeled_future_field"]["kept"])
        self.assertIn("behavior_version", overlays["sol_ring"].raw_reference_shape)

    def test_sol_ring_modeled_as_relevant_mana_source(self) -> None:
        result = classify_card_relevance(self._overlay("sol_ring"), self.target)

        self.assertEqual(result.classification, CardDefinitionStatus.MODELED_RELEVANT)
        self.assertIn("tap_for_mana", result.relevance_reasons)
        self.assertEqual(result.behavior_version, "sim-card-v1")

    def test_chrome_mox_reports_imprint_memory_requirement(self) -> None:
        result = classify_card_relevance(self._overlay("chrome_mox"), self.target)

        self.assertEqual(result.classification, CardDefinitionStatus.MODELED_RELEVANT)
        self.assertIn("requires_memory", result.pending_review_reasons)
        self.assertIn("store_memory_as", result.pending_review_reasons)

    def test_mox_diamond_reports_land_discard_requirement(self) -> None:
        result = classify_card_relevance(self._overlay("mox_diamond"), self.target)

        self.assertEqual(result.classification, CardDefinitionStatus.MODELED_RELEVANT)
        self.assertIn("require_type", self._overlay("mox_diamond").cast_actions[0].metadata)
        self.assertIn("store_memory_as", result.pending_review_reasons)

    def test_demonic_and_vampiric_tutors_are_relevant_for_target_search(self) -> None:
        demonic = classify_card_relevance(self._overlay("demonic_tutor"), self.target)
        vampiric = classify_card_relevance(self._overlay("vampiric_tutor"), self.target)

        self.assertIn("search_library", demonic.relevance_reasons)
        self.assertIn("search_library", vampiric.relevance_reasons)
        self.assertIn("search_targets", demonic.pending_review_reasons)
        self.assertIn("search_targets", vampiric.pending_review_reasons)

    def test_target_card_is_recognized(self) -> None:
        result = classify_card_relevance(self._overlay("rhystic_study"), self.target)

        self.assertEqual(result.classification, CardDefinitionStatus.TARGET_MODELED)
        self.assertIn("target_card", result.relevance_reasons)

    def test_unsupported_irrelevant_creature_is_inert_and_reported(self) -> None:
        deck = SimulationDeck(
            deck_hash="sha256:deck",
            cards=(
                SimulationDeckCard(quantity=1, name="Rhystic Study", model_id="rhystic_study"),
                SimulationDeckCard(quantity=1, name="Memnite", model_id="memnite"),
            ),
        )
        result = build_card_definition_load_result(deck, self.target, [self._overlay("rhystic_study")])

        self.assertEqual(result.confidence_level, "high")
        self.assertEqual(result.cards_unsupported_irrelevant, 1)
        self.assertEqual(result.unsupported_irrelevant_cards[0].card_name, "Memnite")
        self.assertEqual(result.unsupported_irrelevant_cards[0].relevance_classification, "unsupported_irrelevant")

    def test_unsupported_relevant_tutor_lowers_confidence(self) -> None:
        deck = SimulationDeck(
            deck_hash="sha256:deck",
            cards=(
                SimulationDeckCard(quantity=1, name="Rhystic Study", model_id="rhystic_study"),
                SimulationDeckCard(quantity=1, name="Demonic Tutor", model_id="demonic_tutor"),
            ),
        )
        result = build_card_definition_load_result(deck, self.target, [self._overlay("rhystic_study")])

        self.assertEqual(result.confidence_level, "low")
        self.assertEqual(result.cards_unsupported_relevant, 1)
        self.assertEqual(result.unsupported_relevant_cards[0].card_name, "Demonic Tutor")

    def test_unsupported_target_makes_result_invalid(self) -> None:
        deck = SimulationDeck(
            deck_hash="sha256:deck",
            cards=(SimulationDeckCard(quantity=1, name="Rhystic Study", model_id="rhystic_study"),),
        )
        result = build_card_definition_load_result(deck, self.target, [])

        self.assertEqual(result.confidence_level, "invalid")
        self.assertEqual(result.relevance_results[0].classification, CardDefinitionStatus.TARGET_MISSING_BEHAVIOR)

    def test_pending_review_and_versions_are_included_in_load_result(self) -> None:
        deck = SimulationDeck(
            deck_hash="sha256:deck",
            cards=(
                SimulationDeckCard(quantity=1, name="Rhystic Study", model_id="rhystic_study"),
                SimulationDeckCard(quantity=1, name="Chrome Mox", model_id="chrome_mox"),
                SimulationDeckCard(quantity=1, name="Mox Diamond", model_id="mox_diamond"),
            ),
        )
        manager = CardDefinitionManager.from_overlay_rows(self.overlay_rows)
        result = manager.build_load_result(deck, self.target, generated_at="2026-06-29T00:00:00Z")

        self.assertEqual(result.confidence_level, "medium")
        self.assertEqual(result.behavior_overlay_versions, ("sim-card-v1",))
        self.assertEqual({item.card_name for item in result.pending_review_cards}, {"Chrome Mox", "Mox Diamond"})
        self.assertEqual(result.to_dict()["generated_at"], "2026-06-29T00:00:00Z")

    def test_manager_has_no_forbidden_imports(self) -> None:
        root = Path(__file__).resolve().parents[1] / "codie" / "probability_engine"
        forbidden = (
            "codie.providers",
            "codie.db",
            "codie.analytics",
            "codie.recommendations",
            "codie.ingestion",
            "sqlite3",
            "requests",
            "httpx",
        )
        for path in (root / "card_definition_manager.py", root / "relevance.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            imports = [
                alias.name
                for node in ast.walk(tree)
                if isinstance(node, ast.Import)
                for alias in node.names
            ]
            imports.extend(
                node.module
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom) and node.module is not None
            )
            self.assertFalse(set(forbidden).intersection(imports), f"{path} has forbidden imports")

    def test_no_strategic_claim_language_in_manager_code(self) -> None:
        root = Path(__file__).resolve().parents[1] / "codie" / "probability_engine"
        forbidden = (
            "should " + "play",
            "must " + "include",
            "correct " + "card",
            "breaks " + "the format",
            "secretly " + "optimal",
            "cut " + "this",
            "you " + "should",
        )
        text = "\n".join(
            (root / name).read_text(encoding="utf-8")
            for name in ("card_definition_manager.py", "relevance.py")
        ).lower()
        self.assertFalse([phrase for phrase in forbidden if phrase in text])

    def _overlay(self, card_id: str):
        overlays = {card.card_id: card for card in load_behavior_overlay_rows(self.overlay_rows)}
        return overlays[card_id]


if __name__ == "__main__":
    unittest.main()
