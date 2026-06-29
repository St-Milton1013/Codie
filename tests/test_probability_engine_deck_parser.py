from __future__ import annotations

import ast
import unittest
from pathlib import Path

from codie.probability_engine import (
    DeckParseIssue,
    SimulationDeckCard,
    parse_simulation_deck_rows,
    parse_simulation_deck_text,
    parse_target_condition,
    stable_deck_hash,
)


FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "probability_engine" / "deck_parser"


class ProbabilityEngineDeckParserTest(unittest.TestCase):
    def test_plain_text_deck_parses_into_simulation_deck(self) -> None:
        payload = (FIXTURE_ROOT / "plaintext_deck.txt").read_text(encoding="utf-8")

        parsed = parse_simulation_deck_text(payload, source_format="plain_text", source="fixture")

        self.assertIsNotNone(parsed.deck)
        assert parsed.deck is not None
        self.assertEqual(parsed.deck.source, "fixture")
        self.assertEqual([card.name for card in parsed.deck.commanders], ["Kraum, Ludevic's Opus", "Tymna the Weaver"])
        self.assertEqual(parsed.cards_total, 4)
        self.assertEqual(parsed.commanders_total, 2)
        self.assertEqual(parsed.deck.cards[2].name, "Sol Ring")
        self.assertEqual(parsed.deck.cards[2].quantity, 2)
        self.assertTrue(parsed.raw_input_hash.startswith("sha256:"))

    def test_moxfield_style_deck_parses_with_explicit_commanders(self) -> None:
        payload = (FIXTURE_ROOT / "moxfield_plaintext_deck.txt").read_text(encoding="utf-8")

        parsed = parse_simulation_deck_text(
            payload,
            source_format="moxfield_plaintext",
            commander_names=("Tymna the Weaver", "Kraum, Ludevic's Opus"),
        )

        self.assertIsNotNone(parsed.deck)
        assert parsed.deck is not None
        self.assertEqual(parsed.source_format, "moxfield_plaintext")
        self.assertEqual(parsed.commanders_total, 2)
        self.assertEqual(parsed.cards_total, 4)
        self.assertEqual({card.name for card in parsed.deck.commanders}, {"Tymna the Weaver", "Kraum, Ludevic's Opus"})

    def test_partner_pair_order_does_not_change_hash(self) -> None:
        first = (
            SimulationDeckCard(quantity=1, name="Tymna the Weaver", zone="command"),
            SimulationDeckCard(quantity=1, name="Kraum, Ludevic's Opus", zone="command"),
        )
        second = tuple(reversed(first))

        self.assertEqual(
            stable_deck_hash((SimulationDeckCard(quantity=1, name="Sol Ring"),), commanders=first),
            stable_deck_hash((SimulationDeckCard(quantity=1, name="sol   ring"),), commanders=second),
        )

    def test_comments_blank_lines_and_ignored_sections_are_reported(self) -> None:
        payload = (FIXTURE_ROOT / "plaintext_deck.txt").read_text(encoding="utf-8")

        parsed = parse_simulation_deck_text(payload)
        issue_types = [issue.issue_type for issue in parsed.issues]

        self.assertIn("ignored_comment", issue_types)
        self.assertIn("ignored_blank", issue_types)
        self.assertIn("ignored_section", issue_types)
        self.assertEqual({row["name"] for row in parsed.ignored_rows}, {"Ad Nauseam", "Mystic Remora"})

    def test_malformed_rows_and_invalid_quantities_produce_errors(self) -> None:
        payload = (FIXTURE_ROOT / "malformed_deck.txt").read_text(encoding="utf-8")

        parsed = parse_simulation_deck_text(payload)

        self.assertIsNone(parsed.deck)
        errors = [issue for issue in parsed.issues if issue.severity == "error"]
        self.assertGreaterEqual(len(errors), 4)
        self.assertIn("invalid_quantity", {issue.issue_type for issue in errors})
        self.assertIn("missing_card_name", {issue.issue_type for issue in errors})

    def test_unresolved_cards_are_preserved(self) -> None:
        parsed = parse_simulation_deck_rows(
            [
                {"quantity": 1, "name": "Rhystic Study", "zone": "main", "model_id": "rhystic_study"},
                {"quantity": 1, "name": "Sticker cards", "zone": "main", "model_id": None},
            ],
            require_model_ids=True,
            allow_partial=True,
        )

        self.assertIsNotNone(parsed.deck)
        assert parsed.deck is not None
        self.assertEqual(parsed.unresolved_cards, ("Sticker cards",))
        self.assertEqual(parsed.deck.unresolved_cards, ("Sticker cards",))
        self.assertIn("unresolved_card", {issue.issue_type for issue in parsed.issues})

    def test_stable_hash_ignores_whitespace_capitalization_and_order(self) -> None:
        first = (
            SimulationDeckCard(quantity=1, name="  Sol Ring "),
            SimulationDeckCard(quantity=1, name="Rhystic Study"),
        )
        second = (
            SimulationDeckCard(quantity=1, name="rhystic study"),
            SimulationDeckCard(quantity=1, name="sol   ring"),
        )

        self.assertEqual(stable_deck_hash(first), stable_deck_hash(second))

    def test_target_condition_parses_valid_input(self) -> None:
        parsed = parse_target_condition(
            {
                "target_card": "Rhystic Study",
                "target_card_id": "rhystic_study",
                "target_zone": "stack",
                "turn": 2,
                "condition_type": "cast_or_access",
                "required_support_tags": ["mana"],
            }
        )

        self.assertEqual(parsed.issues, ())
        self.assertIsNotNone(parsed.target_condition)
        assert parsed.target_condition is not None
        self.assertEqual(parsed.target_condition.target_card, "Rhystic Study")
        self.assertEqual(parsed.target_condition.turn, 2)

    def test_target_condition_rejects_invalid_inputs(self) -> None:
        parsed = parse_target_condition({"target_card": "", "target_zone": "sideboard", "turn": 0, "condition_type": "win"})

        self.assertIsNone(parsed.target_condition)
        issue_types = [issue.issue_type for issue in parsed.issues]
        self.assertIn("missing_card_name", issue_types)
        self.assertIn("invalid_quantity", issue_types)
        self.assertIn("unsupported_section", issue_types)
        self.assertIn("malformed_row", issue_types)

    def test_issue_serialization(self) -> None:
        issue = DeckParseIssue(1, "0 Sol Ring", "invalid_quantity", "Quantity must be positive.", "error")

        self.assertEqual(issue.to_dict()["line_number"], 1)
        with self.assertRaises(ValueError):
            DeckParseIssue(None, None, "bad", "bad", "fatal")

    def test_parser_has_no_forbidden_imports(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "deck_parser.py"
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
        forbidden = {
            "codie." + "prov" + "iders",
            "codie." + "db",
            "codie." + "analytics",
            "codie." + "recommendations",
            "codie." + "ingestion",
            "sql" + "ite3",
            "req" + "uests",
            "ht" + "tpx",
        }

        self.assertFalse(forbidden.intersection(imports))

    def test_no_strategic_claim_language_in_parser_code(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "deck_parser.py"
        text = path.read_text(encoding="utf-8").lower()
        forbidden = (
            "should " + "play",
            "must " + "include",
            "correct " + "card",
            "breaks " + "the format",
            "secretly " + "opti" + "mal",
            "cut " + "this",
            "you " + "should",
            "keep" + "able",
        )

        self.assertFalse([phrase for phrase in forbidden if phrase in text])


if __name__ == "__main__":
    unittest.main()
