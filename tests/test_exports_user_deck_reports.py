from __future__ import annotations

import unittest

from codie.exports import user_deck_comparison_export, user_deck_comparison_markdown
from codie.user_decks import (
    UserDeckEvidenceComparison,
    UserDeckEvidenceComparisonRow,
)


GENERATED_AT = "2026-06-22T00:00:00+00:00"


def comparison() -> UserDeckEvidenceComparison:
    return UserDeckEvidenceComparison(
        user_deck_id=7,
        deck_hash="deck-hash",
        commander_hash="tymna the weaver",
        generated_at=GENERATED_AT,
        present_count=1,
        absent_count=1,
        rows=(
            UserDeckEvidenceComparisonRow(
                oracle_id="oracle-lotus",
                card_name="Jeweled Lotus",
                evidence_type="generic_staple",
                presence_status="present",
                quantity_in_deck=1,
                zones=("mainboard",),
                score=0.9,
                sample_size=100,
                source_record_id="staple:lotus",
                source_url=None,
                evidence_line="Jeweled Lotus is present in the imported user deck; evidence type generic_staple; sample size 100.",
            ),
            UserDeckEvidenceComparisonRow(
                oracle_id="oracle-remora",
                card_name="Mystic Remora",
                evidence_type="commander_staple",
                presence_status="absent",
                quantity_in_deck=0,
                zones=(),
                score=0.8,
                sample_size=42,
                source_record_id="staple:remora",
                source_url=None,
                evidence_line="Mystic Remora is absent in the imported user deck; evidence type commander_staple; sample size 42.",
            ),
        ),
    )


class UserDeckReportExportTest(unittest.TestCase):
    def test_user_deck_comparison_export_is_json_compatible(self) -> None:
        payload = user_deck_comparison_export(comparison())

        self.assertEqual(payload["user_deck_id"], 7)
        self.assertEqual(payload["present_count"], 1)
        self.assertEqual(payload["absent_count"], 1)
        self.assertEqual(payload["rows"][0]["oracle_id"], "oracle-lotus")
        self.assertEqual(payload["rows"][0]["zones"], ["mainboard"])
        self.assertEqual(payload["rows"][1]["presence_status"], "absent")

    def test_user_deck_comparison_markdown_is_evidence_only(self) -> None:
        markdown = user_deck_comparison_markdown(comparison())

        self.assertIn("# User Deck Evidence Comparison", markdown)
        self.assertIn("| Jeweled Lotus | generic_staple | present | 1 | mainboard | 100 | staple:lotus |", markdown)
        self.assertIn("Mystic Remora is absent in the imported user deck", markdown)
        forbidden = ("should play", "must include", "correct card", "secretly optimal")
        for phrase in forbidden:
            self.assertNotIn(phrase, markdown.lower())

    def test_export_table_escapes_pipe_characters(self) -> None:
        row = UserDeckEvidenceComparisonRow(
            oracle_id="oracle-pipe",
            card_name="Card | Name",
            evidence_type="fixture",
            presence_status="absent",
            quantity_in_deck=0,
            zones=(),
            score=None,
            sample_size=None,
            source_record_id="source|record",
            source_url=None,
            evidence_line="Card Name is absent in the imported user deck; evidence type fixture; sample size 0.",
        )
        payload = comparison()
        report = UserDeckEvidenceComparison(
            user_deck_id=payload.user_deck_id,
            deck_hash=payload.deck_hash,
            commander_hash=payload.commander_hash,
            rows=(row,),
            present_count=0,
            absent_count=1,
            generated_at=payload.generated_at,
        )

        markdown = user_deck_comparison_markdown(report)

        self.assertIn("Card \\| Name", markdown)
        self.assertIn("source\\|record", markdown)


if __name__ == "__main__":
    unittest.main()
