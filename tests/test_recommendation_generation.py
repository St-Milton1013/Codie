from __future__ import annotations

import unittest

from codie.db.bootstrap import bootstrap_database
from codie.recommendations import (
    RecommendationCandidateSource,
    RecommendationGenerationConfig,
    StapleReportRow,
    build_candidate_packet,
    build_commander_staples_report,
    candidate_sources_from_staples_report,
    generate_candidate_packets,
)
from codie.recommendations.generation import RecommendationCandidatePacket


GENERATED_AT = "2026-06-22T00:00:00+00:00"


def config(minimum_sample_size: int = 10) -> RecommendationGenerationConfig:
    return RecommendationGenerationConfig(
        generated_at=GENERATED_AT,
        time_window="180d",
        minimum_sample_size=minimum_sample_size,
    )


def source(
    oracle_id: str = "oracle-remora",
    *,
    card_name: str = "Mystic Remora",
    sample_size: int = 42,
    inclusion_rate: float | None = 0.75,
    commander_lift: float | None = 1.4,
    source_record_id: str = "metric:oracle-remora:180d",
) -> RecommendationCandidateSource:
    return RecommendationCandidateSource(
        oracle_id=oracle_id,
        card_name=card_name,
        sample_size=sample_size,
        inclusion_rate=inclusion_rate,
        commander_lift=commander_lift,
        similarity_score=0.25,
        tournament_performance_score=0.15,
        generic_staple_penalty=0.05,
        source_record_id=source_record_id,
    )


class RecommendationGenerationTest(unittest.TestCase):
    def test_build_candidate_packet_creates_draft_and_audit_in_memory(self) -> None:
        packet = build_candidate_packet(source=source(), config=config())

        self.assertIsInstance(packet, RecommendationCandidatePacket)
        self.assertEqual(packet.candidate.entity_type, "card")
        self.assertEqual(packet.candidate.entity_id, "oracle-remora")
        self.assertEqual(packet.candidate.candidate_type, "commander_specific")
        self.assertTrue(packet.audit.is_valid)
        self.assertTrue(packet.audit.rank_eligible)
        self.assertEqual(packet.audit.evidence_count, 1)
        self.assertEqual(packet.candidate.evidence.items[0].source_record_id, "metric:oracle-remora:180d")
        self.assertIn("comparable canonical decks", packet.audit.explanation_lines[1])

    def test_generate_candidate_packets_sorts_rankable_score_then_identity(self) -> None:
        packets = generate_candidate_packets(
            sources=(
                source("oracle-low", card_name="Low Card", inclusion_rate=0.10, commander_lift=0.1),
                source("oracle-high", card_name="High Card", inclusion_rate=0.80, commander_lift=2.0),
                source("oracle-sample", card_name="Small Sample", sample_size=4, inclusion_rate=1.0, commander_lift=3.0),
            ),
            config=config(),
        )

        self.assertEqual([packet.candidate.entity_id for packet in packets], ["oracle-high", "oracle-low", "oracle-sample"])
        self.assertFalse(packets[-1].audit.rank_eligible)
        self.assertEqual(packets[-1].audit.issues[0].code, "low_sample_size")

    def test_candidate_sources_from_staples_report_feed_generation(self) -> None:
        report = build_commander_staples_report(
            commander_signature="kraum-ludevics-opus|tymna-the-weaver",
            time_window="180d",
            placement_scope="top_16",
            generated_at=GENERATED_AT,
            total_matching_decks=20,
            observations=(),
        )
        row = StapleReportRow(
            card_name="Ranger-Captain of Eos",
            scryfall_id="scryfall-ranger",
            oracle_id="oracle-ranger",
            type_line="Creature - Human Soldier",
            color_identity=("W",),
            matching_deck_count=8,
            total_matching_decks=20,
            inclusion_percentage=0.40,
            total_copies_observed=8,
            average_copies_per_deck=1.0,
            placement_weighted_usage=0.45,
            best_finish_observed=2,
            top16_count=8,
            winner_count=1,
            most_recent_appearance_date="2026-06-01",
            first_appearance_date="2026-04-01",
            deck_urls=("https://example.test/deck",),
            event_urls=("https://example.test/event",),
            provider_breakdown={"topdeck": 8},
            region_breakdown={"NA/US": 8},
        )
        report = type(report)(
            commander_signature=report.commander_signature,
            time_window=report.time_window,
            placement_scope=report.placement_scope,
            generated_at=report.generated_at,
            total_matching_decks=report.total_matching_decks,
            rows=(row,),
        )

        sources = candidate_sources_from_staples_report(report)
        packets = generate_candidate_packets(sources=sources, config=config())

        self.assertEqual(sources[0].oracle_id, "oracle-ranger")
        self.assertEqual(sources[0].source_record_id, "commander_staples:kraum-ludevics-opus|tymna-the-weaver:180d:oracle-ranger")
        self.assertEqual(packets[0].candidate.entity_id, "oracle-ranger")
        self.assertGreater(packets[0].candidate.score.recommendation_score, 0)

    def test_invalid_generation_inputs_fail_cleanly(self) -> None:
        with self.assertRaises(ValueError):
            RecommendationGenerationConfig(generated_at="", time_window="180d")
        with self.assertRaises(ValueError):
            RecommendationGenerationConfig(generated_at=GENERATED_AT, time_window="180d", minimum_sample_size=0)
        with self.assertRaises(ValueError):
            source(inclusion_rate=1.2)
        with self.assertRaises(ValueError):
            RecommendationCandidateSource(
                oracle_id="oracle-no-source",
                card_name="No Source",
                sample_size=1,
                inclusion_rate=0.1,
            )

    def test_phase8h_does_not_create_recommendation_rows(self) -> None:
        connection = bootstrap_database()

        build_candidate_packet(source=source(), config=config())

        run_count = connection.execute("SELECT COUNT(*) AS count FROM recommendation_runs").fetchone()
        candidate_count = connection.execute("SELECT COUNT(*) AS count FROM recommendation_candidates").fetchone()
        self.assertEqual(run_count["count"], 0)
        self.assertEqual(candidate_count["count"], 0)


if __name__ == "__main__":
    unittest.main()
