from __future__ import annotations

import json
import unittest

from codie.db.bootstrap import bootstrap_database
from codie.db.repositories import CoreRepository, RecommendationRepository
from codie.recommendations import (
    RecommendationCandidateSource,
    RecommendationGenerationConfig,
    RecommendationRunSpec,
    build_candidate_packet,
    persist_recommendation_packets,
    recommendation_candidate_row,
    recommendation_run_row,
)


GENERATED_AT = "2026-06-22T00:00:00+00:00"


def add_card(connection, scryfall_id: str = "scryfall-remora", oracle_id: str = "oracle-remora") -> None:
    CoreRepository(connection).upsert_card(
        {
            "scryfall_id": scryfall_id,
            "oracle_id": oracle_id,
            "name": "Mystic Remora",
            "normalized_name": "mystic remora",
            "type_line": "Enchantment",
            "color_identity_json": '["U"]',
            "is_legal_commander": 1,
            "raw_json": "{}",
            "imported_at": GENERATED_AT,
        }
    )


def packet(
    *,
    oracle_id: str = "oracle-remora",
    scryfall_id: str | None = "scryfall-remora",
    source_record_id: str = "metric:oracle-remora:180d",
):
    return build_candidate_packet(
        source=RecommendationCandidateSource(
            oracle_id=oracle_id,
            scryfall_id=scryfall_id,
            card_name="Mystic Remora",
            sample_size=42,
            inclusion_rate=0.75,
            commander_lift=1.4,
            similarity_score=0.25,
            tournament_performance_score=0.15,
            generic_staple_penalty=0.05,
            source_record_id=source_record_id,
        ),
        config=RecommendationGenerationConfig(
            generated_at=GENERATED_AT,
            time_window="180d",
            minimum_sample_size=10,
        ),
    )


def run_spec() -> RecommendationRunSpec:
    return RecommendationRunSpec(
        input_deck_hash="deck-hash-1",
        commander_hash="kraum-ludevics-opus|tymna-the-weaver",
        generated_at=GENERATED_AT,
        config={"window": "180d", "minimum_sample_size": 10},
        notes="fixture run",
    )


class RecommendationPersistenceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = bootstrap_database()
        add_card(self.connection)
        self.repository = RecommendationRepository(self.connection)

    def test_row_mappers_preserve_config_evidence_and_scores(self) -> None:
        run_row = recommendation_run_row(run_spec())
        candidate_row = recommendation_candidate_row(packet())

        self.assertEqual(run_row["input_deck_hash"], "deck-hash-1")
        self.assertEqual(json.loads(str(run_row["config_json"])), {"minimum_sample_size": 10, "window": "180d"})
        self.assertEqual(candidate_row["scryfall_id"], "scryfall-remora")
        self.assertEqual(candidate_row["oracle_id"], "oracle-remora")
        self.assertEqual(candidate_row["candidate_type"], "commander_specific")
        self.assertAlmostEqual(float(candidate_row["inclusion_rate"]), 0.75)
        self.assertAlmostEqual(float(candidate_row["lift_score"]), 1.4)
        evidence = json.loads(str(candidate_row["evidence_json"]))
        self.assertEqual(evidence["scryfall_id"], "scryfall-remora")
        self.assertEqual(evidence["candidate"]["entity_id"], "oracle-remora")
        self.assertIn("comparable canonical decks", str(candidate_row["explanation_text"]))

    def test_persist_recommendation_packets_writes_run_and_candidates(self) -> None:
        result = persist_recommendation_packets(
            repository=self.repository,
            run=run_spec(),
            packets=(packet(),),
        )

        run = self.repository.get_recommendation_run(result.recommendation_run_id)
        candidates = self.repository.list_run_candidates(result.recommendation_run_id)
        self.assertEqual(result.candidate_count, 1)
        self.assertEqual(run["input_deck_hash"], "deck-hash-1")
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["scryfall_id"], "scryfall-remora")
        self.assertEqual(candidates[0]["oracle_id"], "oracle-remora")

    def test_repeated_persistence_replaces_existing_run_for_same_key(self) -> None:
        first = persist_recommendation_packets(
            repository=self.repository,
            run=run_spec(),
            packets=(packet(),),
        )
        second_packet = packet(oracle_id="oracle-other", scryfall_id=None, source_record_id="metric:oracle-other:180d")
        second = persist_recommendation_packets(
            repository=self.repository,
            run=run_spec(),
            packets=(second_packet,),
        )

        runs = self.repository.find_recommendation_runs(input_deck_hash="deck-hash-1", generated_at=GENERATED_AT)
        candidates = self.repository.list_run_candidates(second.recommendation_run_id)
        orphan_count = self.connection.execute(
            "SELECT COUNT(*) AS count FROM recommendation_candidates WHERE recommendation_run_id = ?",
            (first.recommendation_run_id,),
        ).fetchone()
        self.assertEqual(len(runs), 1)
        self.assertNotEqual(first.recommendation_run_id, second.recommendation_run_id)
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["oracle_id"], "oracle-other")
        self.assertEqual(orphan_count["count"], 0)

    def test_failed_candidate_insert_rolls_back_run_and_candidates(self) -> None:
        bad_packet = packet(scryfall_id="missing-scryfall")

        with self.assertRaises(Exception):
            persist_recommendation_packets(
                repository=self.repository,
                run=run_spec(),
                packets=(bad_packet,),
            )

        run_count = self.connection.execute("SELECT COUNT(*) AS count FROM recommendation_runs").fetchone()
        candidate_count = self.connection.execute("SELECT COUNT(*) AS count FROM recommendation_candidates").fetchone()
        self.assertEqual(run_count["count"], 0)
        self.assertEqual(candidate_count["count"], 0)

    def test_invalid_run_spec_fails_cleanly(self) -> None:
        with self.assertRaises(ValueError):
            RecommendationRunSpec(input_deck_hash="", generated_at=GENERATED_AT)
        with self.assertRaises(ValueError):
            RecommendationRunSpec(input_deck_hash="deck", generated_at="")
        with self.assertRaises(ValueError):
            RecommendationRunSpec(input_deck_hash="deck", generated_at=GENERATED_AT, source_snapshot_id=-1)


if __name__ == "__main__":
    unittest.main()
