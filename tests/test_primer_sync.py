from __future__ import annotations

import json
from pathlib import Path
import unittest
from dataclasses import replace

from codie.db.bootstrap import bootstrap_database
from codie.db.repositories.analytics import AnalyticsRepository
from codie.db.repositories.curated import CuratedRepository
from codie.db.repositories.source import SourceRepository
from codie.primers import PrimerMetadataSync, score_primer_candidate
from codie.providers.moxfield.parser import MoxfieldProvider


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "moxfield"


def load_fixture(name: str):
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


class PrimerMetadataSyncTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = bootstrap_database()
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.source = SourceRepository(self.connection)
        self.curated = CuratedRepository(self.connection)
        self.analytics = AnalyticsRepository(self.connection)

    def _candidates(self):
        provider = MoxfieldProvider()
        return (
            provider.parse_deck(load_fixture("deck_with_primer.json")),
            provider.parse_deck(load_fixture("deck_without_primer.json")),
        )

    def _sync(self):
        return PrimerMetadataSync(self.source, self.curated, self.analytics).sync_candidates(self._candidates())

    def test_sync_persists_source_primers_and_registry_metadata(self) -> None:
        result = self._sync()
        self.assertEqual(result.source_primer_count, 2)
        self.assertEqual(result.registry_primer_count, 1)
        self.assertEqual(result.evidence_count_count, 1)
        self.assertEqual(result.skipped_registry_count, 1)

        source_primer = self.source.get_source_primer(
            "moxfield",
            "https://moxfield.com/decks/mox-primer-1/primer",
        )
        self.assertEqual(source_primer["primer_title"], "Tymna Kraum Primer")
        self.assertEqual(source_primer["author_url"], "https://moxfield.com/users/PrimerAuthor")
        self.assertNotIn("DO NOT STORE", source_primer["raw_metadata_json"])

        registry_primer = self.curated.get_primer("https://moxfield.com/decks/mox-primer-1/primer")
        self.assertEqual(registry_primer["primer_title"], "Tymna Kraum Primer")
        self.assertEqual(registry_primer["author"], "PrimerAuthor")
        self.assertEqual(registry_primer["commander_key"], "kraum, ludevic's opus|tymna the weaver")
        self.assertEqual(registry_primer["has_primer_route"], 1)
        self.assertGreater(registry_primer["primer_quality_score"], 0)

    def test_sync_keeps_no_primer_deck_out_of_registry(self) -> None:
        self._sync()
        source_primer = self.source.get_source_primer(
            "moxfield",
            "https://moxfield.com/decks/mox-no-primer",
        )
        self.assertEqual(source_primer["deck_title"], "Casual Metadata Only Deck")
        self.assertIsNone(self.curated.get_primer("https://moxfield.com/decks/mox-no-primer"))

    def test_sync_updates_primer_evidence_count(self) -> None:
        self._sync()
        evidence = self.analytics.get_evidence_count(
            "primer",
            "https://moxfield.com/decks/mox-primer-1/primer",
        )
        self.assertEqual(evidence["primer_evidence_count"], 1)
        self.assertEqual(evidence["tournament_evidence_count"], 0)

    def test_sync_is_idempotent_for_registry_and_evidence(self) -> None:
        first = self._sync()
        second = self._sync()
        self.assertEqual(first.registry_primer_count, 1)
        self.assertEqual(second.registry_primer_count, 1)
        registry_count = self.connection.execute("SELECT COUNT(*) AS count FROM primer_registry").fetchone()
        evidence_count = self.connection.execute("SELECT COUNT(*) AS count FROM evidence_counts").fetchone()
        source_count = self.connection.execute("SELECT COUNT(*) AS count FROM source_primers").fetchone()
        self.assertEqual(registry_count["count"], 1)
        self.assertEqual(evidence_count["count"], 1)
        self.assertEqual(source_count["count"], 4)

    def test_repeated_sync_updates_existing_primer_registry_record(self) -> None:
        candidate = self._candidates()[0]
        sync = PrimerMetadataSync(self.source, self.curated, self.analytics)
        sync.sync_candidates((candidate,))
        updated = replace(candidate, primer_title="Updated Primer Title", likes=99)
        sync.sync_candidates((updated,))

        registry_count = self.connection.execute("SELECT COUNT(*) AS count FROM primer_registry").fetchone()
        registry_primer = self.curated.get_primer("https://moxfield.com/decks/mox-primer-1/primer")
        self.assertEqual(registry_count["count"], 1)
        self.assertEqual(registry_primer["primer_title"], "Updated Primer Title")
        self.assertEqual(registry_primer["likes"], 99)

    def test_evidence_only_storage_excludes_body_and_strategy_text(self) -> None:
        self._sync()
        forbidden_fragments = (
            "DO NOT STORE",
            "MULLIGAN GUIDE",
            "STRATEGY TEXT",
            "DESCRIPTION BODY",
        )
        rows = list(
            self.connection.execute(
                """
                SELECT raw_metadata_json FROM source_primers
                UNION ALL
                SELECT raw_metadata_json FROM primer_registry
                """
            )
        )
        self.assertGreater(len(rows), 0)
        for row in rows:
            raw_metadata = row["raw_metadata_json"] or ""
            for fragment in forbidden_fragments:
                self.assertNotIn(fragment, raw_metadata)

    def test_partner_pair_signature_requires_exact_pair_and_is_order_insensitive(self) -> None:
        provider = MoxfieldProvider()
        base = provider.parse_deck(load_fixture("deck_with_primer.json"))
        reversed_pair = replace(
            base,
            primer_url="https://moxfield.com/decks/reversed-pair/primer",
            deck_url="https://moxfield.com/decks/reversed-pair",
            commander_text="Kraum, Ludevic's Opus / Tymna the Weaver",
            partner_text=None,
        )
        single_commander = replace(
            base,
            primer_url="https://moxfield.com/decks/single-tymna/primer",
            deck_url="https://moxfield.com/decks/single-tymna",
            commander_text="Tymna the Weaver",
            partner_text=None,
        )
        explicit_partner = replace(
            base,
            primer_url="https://moxfield.com/decks/explicit-partner/primer",
            deck_url="https://moxfield.com/decks/explicit-partner",
            commander_text="Tymna the Weaver",
            partner_text="Kraum, Ludevic's Opus",
        )

        PrimerMetadataSync(self.source, self.curated, self.analytics).sync_candidates(
            (base, reversed_pair, single_commander, explicit_partner)
        )

        base_row = self.curated.get_primer("https://moxfield.com/decks/mox-primer-1/primer")
        reversed_row = self.curated.get_primer("https://moxfield.com/decks/reversed-pair/primer")
        single_row = self.curated.get_primer("https://moxfield.com/decks/single-tymna/primer")
        explicit_row = self.curated.get_primer("https://moxfield.com/decks/explicit-partner/primer")
        expected_pair = "kraum, ludevic's opus|tymna the weaver"
        self.assertEqual(base_row["commander_key"], expected_pair)
        self.assertEqual(reversed_row["commander_key"], expected_pair)
        self.assertEqual(explicit_row["commander_key"], expected_pair)
        self.assertEqual(single_row["commander_key"], "tymna the weaver")
        self.assertNotEqual(single_row["commander_key"], expected_pair)
        self.assertEqual(explicit_row["partner_key"], "kraum, ludevic's opus")

    def test_primer_score_output_is_reproducible_and_explained(self) -> None:
        candidate = self._candidates()[0]
        score = score_primer_candidate(candidate, generated_at="2026-06-22T00:00:00+00:00")
        self.assertEqual(score.generated_at, "2026-06-22T00:00:00+00:00")
        self.assertGreater(score.score, 0)
        self.assertIn("has_primer_route", score.component_breakdown)
        self.assertIn("primer_heading_count", score.component_breakdown)
        self.assertAlmostEqual(score.score, sum(score.component_breakdown.values()))

    def test_sync_does_not_create_recommendations_packages_or_combos(self) -> None:
        self._sync()
        recommendation_count = self.connection.execute("SELECT COUNT(*) AS count FROM recommendation_runs").fetchone()
        package_count = self.connection.execute("SELECT COUNT(*) AS count FROM package_registry").fetchone()
        combo_count = self.connection.execute("SELECT COUNT(*) AS count FROM combos").fetchone()
        self.assertEqual(recommendation_count["count"], 0)
        self.assertEqual(package_count["count"], 0)
        self.assertEqual(combo_count["count"], 0)

    def test_sync_rolls_back_all_tables_when_evidence_update_fails(self) -> None:
        def fail_evidence_update(evidence):
            raise RuntimeError("evidence write failed")

        self.analytics.upsert_evidence_count = fail_evidence_update
        candidate = MoxfieldProvider().parse_deck(load_fixture("deck_with_primer.json"))
        with self.assertRaises(RuntimeError):
            PrimerMetadataSync(self.source, self.curated, self.analytics).sync_candidates((candidate,))

        self.assertEqual(self.connection.execute("SELECT COUNT(*) AS count FROM source_primers").fetchone()["count"], 0)
        self.assertEqual(self.connection.execute("SELECT COUNT(*) AS count FROM primer_registry").fetchone()["count"], 0)
        self.assertEqual(self.connection.execute("SELECT COUNT(*) AS count FROM evidence_counts").fetchone()["count"], 0)


if __name__ == "__main__":
    unittest.main()
