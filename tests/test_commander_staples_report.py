from __future__ import annotations

import unittest

from codie.db.bootstrap import bootstrap_database
from codie.recommendations import StapleObservation, build_commander_staples_report


GENERATED_AT = "2026-06-22T00:00:00+00:00"


def observation(**overrides) -> StapleObservation:
    data = {
        "deck_id": "deck-1",
        "oracle_id": "oracle-remora",
        "scryfall_id": "scryfall-remora",
        "card_name": "Mystic Remora",
        "quantity": 1,
        "type_line": "Enchantment",
        "color_identity": ("U",),
        "entry_weight": 1.0,
        "placement": 1,
        "top_cut": True,
        "winner": False,
        "event_date": "2026-06-01",
        "deck_url": "https://example.test/decks/1",
        "event_url": "https://example.test/events/1",
        "provider": "topdeck",
        "region": "NA",
        "country": "US",
    }
    data.update(overrides)
    return StapleObservation(**data)


class CommanderStaplesReportTest(unittest.TestCase):
    def staple_observations(self):
        return (
            observation(
                oracle_id="oracle-mana-crypt",
                scryfall_id="scryfall-mana-crypt",
                card_name="Mana Crypt",
                type_line="Artifact",
                color_identity=(),
                deck_id="deck-1",
                entry_weight=1.0,
                placement=1,
                winner=True,
                event_date="2026-06-01",
                deck_url="https://example.test/decks/1",
                event_url="https://example.test/events/1",
                provider="topdeck",
                region="NA",
                country="US",
            ),
            observation(
                oracle_id="oracle-mana-crypt",
                scryfall_id="scryfall-mana-crypt",
                card_name="Mana Crypt",
                type_line="Artifact",
                color_identity=(),
                deck_id="deck-2",
                entry_weight=0.5,
                placement=8,
                winner=False,
                event_date="2026-06-15",
                deck_url="https://example.test/decks/2",
                event_url="https://example.test/events/2",
                provider="mtgdecks",
                region="EU",
                country="DE",
            ),
            observation(
                oracle_id="oracle-mana-crypt",
                scryfall_id="scryfall-mana-crypt",
                card_name="Mana Crypt",
                type_line="Artifact",
                color_identity=(),
                deck_id="deck-3",
                entry_weight=0.2,
                placement=24,
                top_cut=False,
                winner=False,
                event_date="2026-06-20",
                deck_url="https://example.test/decks/3",
                event_url="https://example.test/events/3",
                provider="topdeck",
                region="NA",
                country="CA",
            ),
            observation(
                deck_id="deck-1",
                entry_weight=1.0,
                placement=1,
                winner=True,
                event_date="2026-06-01",
                deck_url="https://example.test/decks/1",
                event_url="https://example.test/events/1",
                provider="topdeck",
                region="NA",
                country="US",
            ),
            observation(
                deck_id="deck-2",
                entry_weight=0.5,
                placement=8,
                winner=False,
                event_date="2026-06-15",
                deck_url="https://example.test/decks/2",
                event_url="https://example.test/events/2",
                provider="mtgdecks",
                region="EU",
                country="DE",
            ),
            observation(
                oracle_id="oracle-dockside",
                scryfall_id="scryfall-dockside",
                card_name="Dockside Extortionist",
                type_line="Creature",
                color_identity=("R",),
                deck_id="deck-3",
                entry_weight=0.2,
                placement=24,
                top_cut=False,
                winner=False,
                event_date="2026-06-20",
                deck_url="https://example.test/decks/3",
                event_url="https://example.test/events/3",
                provider="topdeck",
                region="NA",
                country="CA",
            ),
        )

    def test_report_aggregates_required_output_fields(self) -> None:
        report = build_commander_staples_report(
            commander_signature="kraum, ludevic's opus|tymna the weaver",
            observations=self.staple_observations(),
            time_window="180d",
            generated_at=GENERATED_AT,
        )

        self.assertEqual(report.commander_signature, "kraum, ludevic's opus|tymna the weaver")
        self.assertEqual(report.total_matching_decks, 3)
        self.assertEqual([row.oracle_id for row in report.rows], ["oracle-mana-crypt", "oracle-remora", "oracle-dockside"])

        remora = next(row for row in report.rows if row.oracle_id == "oracle-remora")
        self.assertEqual(remora.card_name, "Mystic Remora")
        self.assertEqual(remora.scryfall_id, "scryfall-remora")
        self.assertEqual(remora.type_line, "Enchantment")
        self.assertEqual(remora.color_identity, ("U",))
        self.assertEqual(remora.matching_deck_count, 2)
        self.assertEqual(remora.total_matching_decks, 3)
        self.assertAlmostEqual(remora.inclusion_percentage, 2 / 3)
        self.assertEqual(remora.total_copies_observed, 2)
        self.assertEqual(remora.average_copies_per_deck, 1.0)
        self.assertAlmostEqual(remora.placement_weighted_usage, 1.5 / 1.7)
        self.assertEqual(remora.best_finish_observed, 1)
        self.assertEqual(remora.top16_count, 2)
        self.assertEqual(remora.winner_count, 1)
        self.assertEqual(remora.first_appearance_date, "2026-06-01")
        self.assertEqual(remora.most_recent_appearance_date, "2026-06-15")
        self.assertEqual(remora.deck_urls, ("https://example.test/decks/1", "https://example.test/decks/2"))
        self.assertEqual(remora.event_urls, ("https://example.test/events/1", "https://example.test/events/2"))
        self.assertEqual(remora.provider_breakdown, {"mtgdecks": 1, "topdeck": 1})
        self.assertEqual(remora.region_breakdown, {"EU/DE": 1, "NA/US": 1})

    def test_minimum_inclusion_filter_and_total_override(self) -> None:
        report = build_commander_staples_report(
            commander_signature="kraum, ludevic's opus|tymna the weaver",
            observations=self.staple_observations(),
            time_window="180d",
            generated_at=GENERATED_AT,
            total_matching_decks=4,
            minimum_inclusion_percentage=0.70,
        )
        self.assertEqual([row.oracle_id for row in report.rows], ["oracle-mana-crypt"])
        self.assertEqual(report.rows[0].total_matching_decks, 4)
        self.assertEqual(report.rows[0].inclusion_percentage, 0.75)

    def test_empty_observations_return_empty_report(self) -> None:
        report = build_commander_staples_report(
            commander_signature="tymna the weaver",
            observations=(),
            time_window="180d",
            generated_at=GENERATED_AT,
        )
        self.assertEqual(report.total_matching_decks, 0)
        self.assertEqual(report.rows, ())

    def test_invalid_inputs_fail_cleanly(self) -> None:
        self.assertEqual(observation(color_identity=("g", "W", "U", "U")).color_identity, ("W", "U", "G"))
        with self.assertRaises(ValueError):
            observation(deck_id="")
        with self.assertRaises(ValueError):
            observation(oracle_id="")
        with self.assertRaises(ValueError):
            observation(card_name="")
        with self.assertRaises(ValueError):
            observation(quantity=0)
        with self.assertRaises(ValueError):
            observation(entry_weight=-0.1)
        with self.assertRaises(ValueError):
            build_commander_staples_report(
                commander_signature="",
                observations=self.staple_observations(),
                time_window="180d",
                generated_at=GENERATED_AT,
            )
        with self.assertRaises(ValueError):
            build_commander_staples_report(
                commander_signature="tymna the weaver",
                observations=self.staple_observations(),
                time_window="180d",
                generated_at=GENERATED_AT,
                total_matching_decks=2,
            )

    def test_phase8c_does_not_create_recommendation_rows(self) -> None:
        connection = bootstrap_database()
        build_commander_staples_report(
            commander_signature="kraum, ludevic's opus|tymna the weaver",
            observations=self.staple_observations(),
            time_window="180d",
            generated_at=GENERATED_AT,
        )
        run_count = connection.execute("SELECT COUNT(*) AS count FROM recommendation_runs").fetchone()
        candidate_count = connection.execute("SELECT COUNT(*) AS count FROM recommendation_candidates").fetchone()
        self.assertEqual(run_count["count"], 0)
        self.assertEqual(candidate_count["count"], 0)


if __name__ == "__main__":
    unittest.main()
