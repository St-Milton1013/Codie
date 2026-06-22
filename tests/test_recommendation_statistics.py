from __future__ import annotations

import unittest

from codie.db.bootstrap import bootstrap_database
from codie.recommendations import (
    confidence_rating,
    frequency_stats,
    generic_staple_profile,
    inclusion_rate,
    jaccard_similarity,
    lift_score,
    safe_rate,
    weighted_inclusion_rate,
    weighted_jaccard_similarity,
)


class RecommendationStatisticsTest(unittest.TestCase):
    def test_inclusion_and_weighted_rates_calculate_safely(self) -> None:
        self.assertEqual(inclusion_rate(7, 10), 0.7)
        self.assertEqual(weighted_inclusion_rate(2.5, 5.0), 0.5)
        self.assertIsNone(safe_rate(1, 0))
        with self.assertRaises(ValueError):
            inclusion_rate(-1, 10)

    def test_frequency_stats_validate_counts(self) -> None:
        stats = frequency_stats(3, 12)
        self.assertEqual(stats.observed_count, 3)
        self.assertEqual(stats.total_count, 12)
        self.assertEqual(stats.frequency, 0.25)
        self.assertIsNone(frequency_stats(0, 0).frequency)
        with self.assertRaises(ValueError):
            frequency_stats(4, 3)
        with self.assertRaises(TypeError):
            frequency_stats(1.5, 3)

    def test_lift_score_calculates_caps_and_handles_missing_baseline(self) -> None:
        self.assertAlmostEqual(lift_score(0.42, 0.20), 2.1)
        self.assertEqual(lift_score(1.0, 0.01, cap=5.0), 5.0)
        self.assertIsNone(lift_score(None, 0.2))
        self.assertIsNone(lift_score(0.2, 0.0))
        with self.assertRaises(ValueError):
            lift_score(0.2, 0.1, cap=0)

    def test_confidence_rating_follows_constitution_thresholds(self) -> None:
        self.assertEqual(confidence_rating(9).label, "insufficient")
        self.assertEqual(confidence_rating(10).label, "low")
        self.assertEqual(confidence_rating(29).label, "low")
        self.assertEqual(confidence_rating(30).label, "medium")
        self.assertEqual(confidence_rating(99).label, "medium")
        high = confidence_rating(100)
        self.assertEqual(high.label, "high")
        self.assertEqual(high.score, 1.0)
        with self.assertRaises(ValueError):
            confidence_rating(10, low_threshold=30, medium_threshold=10, high_threshold=100)

    def test_jaccard_similarity_uses_oracle_identity_sets(self) -> None:
        self.assertEqual(jaccard_similarity([], []), 0.0)
        self.assertEqual(
            jaccard_similarity(
                ["oracle-a", "oracle-b", "oracle-c"],
                ["oracle-b", "oracle-c", "oracle-d"],
            ),
            0.5,
        )
        self.assertEqual(jaccard_similarity([" oracle-a ", ""], ["oracle-a"]), 1.0)

    def test_weighted_jaccard_uses_min_over_max_weights(self) -> None:
        score = weighted_jaccard_similarity(
            {"oracle-a": 2.0, "oracle-b": 1.0},
            {"oracle-a": 1.0, "oracle-c": 3.0},
        )
        self.assertEqual(score, 1 / 6)
        self.assertEqual(weighted_jaccard_similarity({}, {}), 0.0)
        with self.assertRaises(ValueError):
            weighted_jaccard_similarity({"oracle-a": -1}, {})

    def test_generic_staple_profile_requires_all_generic_signals(self) -> None:
        generic = generic_staple_profile(
            global_inclusion_rate=0.55,
            commander_lift=1.05,
            color_identity_baseline_rate=0.44,
            commander_frequency=12,
        )
        self.assertTrue(generic.is_generic_staple)
        self.assertEqual(generic.penalty, 0.25)
        self.assertEqual(
            set(generic.reasons),
            {
                "high_global_inclusion",
                "low_commander_lift",
                "high_color_identity_baseline",
                "broad_commander_frequency",
            },
        )

        commander_specific = generic_staple_profile(
            global_inclusion_rate=0.55,
            commander_lift=2.4,
            color_identity_baseline_rate=0.44,
            commander_frequency=12,
        )
        self.assertFalse(commander_specific.is_generic_staple)
        self.assertEqual(commander_specific.penalty, 0.0)

    def test_phase8a_does_not_create_recommendation_rows(self) -> None:
        connection = bootstrap_database()
        inclusion_rate(7, 10)
        lift_score(0.42, 0.20)
        jaccard_similarity(["oracle-a"], ["oracle-a"])
        run_count = connection.execute("SELECT COUNT(*) AS count FROM recommendation_runs").fetchone()
        candidate_count = connection.execute("SELECT COUNT(*) AS count FROM recommendation_candidates").fetchone()
        self.assertEqual(run_count["count"], 0)
        self.assertEqual(candidate_count["count"], 0)


if __name__ == "__main__":
    unittest.main()
