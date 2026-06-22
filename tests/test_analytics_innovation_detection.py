from __future__ import annotations

import json
import unittest

from codie.analytics import (
    InnovationFilter,
    InnovationObservation,
    detect_innovations,
    innovation_evidence_line,
)
from codie.db.bootstrap import bootstrap_database


GENERATED_AT = "2026-06-22T00:00:00+00:00"
COMMANDER = "kraum-card|tymna-card"


def observation(
    oracle_id: str,
    deck_id: str,
    event_id: str,
    event_date: str,
    **overrides,
) -> InnovationObservation:
    data = {
        "oracle_id": oracle_id,
        "scryfall_id": f"scryfall-{oracle_id}",
        "card_name": oracle_id.replace("oracle-", "").replace("-", " ").title(),
        "type_line": "Artifact",
        "color_identity": (),
        "source_deck_id": deck_id,
        "source_event_id": event_id,
        "event_date": event_date,
        "commander_signature": COMMANDER,
        "region_code": "NA",
        "country_code": "US",
        "placement": 8,
        "top_cut": True,
        "winner": False,
        "player_count": 64,
    }
    data.update(overrides)
    return InnovationObservation(**data)


def innovation_dataset() -> list[InnovationObservation]:
    observations: list[InnovationObservation] = []
    for index in range(1, 11):
        observations.append(
            observation(
                "oracle-common",
                f"recent-deck-{index}",
                "recent-event",
                "2026-06-20",
            )
        )
    for index in range(1, 21):
        observations.append(
            observation(
                "oracle-common",
                f"baseline-deck-{index}",
                "baseline-event",
                "2026-04-15",
            )
        )
    for index in range(1, 3):
        observations.append(
            observation(
                "oracle-new-innovation",
                f"recent-deck-{index}",
                "recent-event",
                "2026-06-20",
                winner=index == 1,
            )
        )
        observations.append(
            observation(
                "oracle-breakout",
                f"recent-deck-{index + 2}",
                "recent-event",
                "2026-06-20",
            )
        )
        observations.append(
            observation(
                "oracle-resurgence",
                f"recent-deck-{index + 4}",
                "recent-event",
                "2026-06-20",
            )
        )
        observations.append(
            observation(
                "oracle-new-release",
                f"recent-deck-{index + 6}",
                "recent-event",
                "2026-06-20",
                card_released_at="2026-06-01",
            )
        )
        observations.append(
            observation(
                "oracle-regional",
                f"recent-deck-{index + 8}",
                "recent-event",
                "2026-06-20",
                region_code="JP",
                country_code="JP",
                type_line="Instant",
                color_identity=("u", "W"),
            )
        )
    observations.append(
        observation(
            "oracle-breakout",
            "baseline-deck-1",
            "baseline-event",
            "2026-04-15",
        )
    )
    observations.append(
        observation(
            "oracle-resurgence",
            "old-deck-1",
            "old-event",
            "2025-01-15",
        )
    )
    return observations


class InnovationDetectionTest(unittest.TestCase):
    def signals(self, **filter_overrides):
        filters = InnovationFilter(
            window_end_date="2026-06-30",
            low_baseline_inclusion_threshold=0.10,
            breakout_delta_threshold=0.05,
            **filter_overrides,
        )
        return detect_innovations(innovation_dataset(), filters, generated_at=GENERATED_AT)

    def test_low_historical_usage_recent_topcut_flags_new_innovation(self) -> None:
        signals = self.signals()
        new_signal = next(
            signal
            for signal in signals
            if signal.oracle_id == "oracle-new-innovation" and signal.innovation_type == "new_innovation"
        )
        self.assertEqual(new_signal.recent_window, "30d")
        self.assertEqual(new_signal.baseline_window, "180d")
        self.assertEqual(new_signal.sample_size, 2)
        self.assertAlmostEqual(new_signal.recent_inclusion_rate, 0.2)
        self.assertEqual(new_signal.baseline_inclusion_rate, 0)
        self.assertEqual(new_signal.recent_topcut_count, 2)
        self.assertEqual(new_signal.recent_winner_count, 1)
        self.assertEqual(new_signal.first_recent_seen_at, "2026-06-20")
        self.assertEqual(json.loads(new_signal.source_deck_ids_json), ["recent-deck-1", "recent-deck-2"])
        self.assertEqual(json.loads(new_signal.source_event_ids_json), ["recent-event"])

    def test_historically_common_card_does_not_flag_as_innovation(self) -> None:
        signals = self.signals()
        common_signals = [signal for signal in signals if signal.oracle_id == "oracle-common"]
        self.assertEqual(common_signals, [])

    def test_breakout_new_release_and_old_resurgence_are_separate_signals(self) -> None:
        signals = self.signals()
        signal_types = {(signal.oracle_id, signal.innovation_type) for signal in signals}
        self.assertIn(("oracle-breakout", "recent_breakout"), signal_types)
        self.assertIn(("oracle-new-release", "new_release_adoption"), signal_types)
        self.assertIn(("oracle-resurgence", "old_card_resurgence"), signal_types)

        release = next(signal for signal in signals if signal.innovation_type == "new_release_adoption")
        self.assertTrue(release.is_new_release)
        self.assertEqual(release.card_released_at, "2026-06-01")

        resurgence = next(signal for signal in signals if signal.innovation_type == "old_card_resurgence")
        self.assertEqual(resurgence.last_seen_before_recent_window, "2025-01-15")

    def test_commander_specific_and_regional_innovations_work(self) -> None:
        signals = self.signals()
        commander_signal = next(
            signal
            for signal in signals
            if signal.oracle_id == "oracle-new-innovation"
            and signal.innovation_type == "commander_specific_innovation"
        )
        self.assertEqual(commander_signal.commander_signature, COMMANDER)

        regional_signal = next(
            signal
            for signal in signals
            if signal.oracle_id == "oracle-regional" and signal.innovation_type == "regional_innovation"
        )
        self.assertEqual(regional_signal.region_code, "JP")

    def test_filters_and_minimum_sample_guardrail_work(self) -> None:
        no_signals = self.signals(minimum_sample_size=3)
        self.assertNotIn(
            ("oracle-new-innovation", "new_innovation"),
            {(signal.oracle_id, signal.innovation_type) for signal in no_signals},
        )

        regional = self.signals(
            region_code="JP",
            card_type_contains=("instant",),
            color_identity=("W", "U"),
        )
        self.assertEqual({signal.oracle_id for signal in regional}, {"oracle-regional"})
        self.assertEqual(InnovationFilter(window_end_date="2026-06-30", color_identity=("u", "W")).color_identity, ("W", "U"))

    def test_evidence_output_uses_allowed_language(self) -> None:
        forbidden = (
            "new tech",
            "is correct",
            "breaks the format",
            "secretly optimal",
            "should play",
        )
        for signal in self.signals():
            line = innovation_evidence_line(signal)
            lowered = line.lower()
            self.assertTrue(line.startswith("Card "))
            self.assertFalse(any(fragment in lowered for fragment in forbidden))

    def test_invalid_inputs_fail_cleanly(self) -> None:
        with self.assertRaises(ValueError):
            InnovationFilter(window_end_date="", baseline_window="180d")
        with self.assertRaises(ValueError):
            InnovationFilter(window_end_date="2026-06-30", baseline_window="45d")
        with self.assertRaises(ValueError):
            InnovationObservation(
                oracle_id="",
                source_deck_id="deck",
                source_event_id="event",
                event_date="2026-06-20",
            )
        with self.assertRaises(ValueError):
            detect_innovations(innovation_dataset(), InnovationFilter(window_end_date="2026-06-30"), generated_at="")

    def test_phase8b_patch_does_not_create_recommendation_rows(self) -> None:
        connection = bootstrap_database()
        self.signals()
        run_count = connection.execute("SELECT COUNT(*) AS count FROM recommendation_runs").fetchone()
        candidate_count = connection.execute("SELECT COUNT(*) AS count FROM recommendation_candidates").fetchone()
        self.assertEqual(run_count["count"], 0)
        self.assertEqual(candidate_count["count"], 0)


if __name__ == "__main__":
    unittest.main()
