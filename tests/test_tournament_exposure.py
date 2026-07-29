from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
import json
from pathlib import Path
import unittest

from codie.analytics.tournament_exposure import (
    INDEPENDENT_SEAT_MODEL_ID,
    TOURNAMENT_EXPOSURE_VERSION,
    TournamentExposureAssumptions,
    TournamentExposureBuildError,
    TournamentExposurePopulationManifest,
    TournamentExposureTarget,
    build_tournament_exposure_bundle,
    build_tournament_exposure_comparison,
    build_tournament_exposure_estimate,
    build_tournament_exposure_preparation_brief,
    tournament_exposure_bundle_to_dict,
    tournament_exposure_estimate_to_dict,
)


WARNING = (
    "Independent-seat approximation; this is not a Swiss-pairing model."
)
NOW = "2026-07-29T18:00:00-05:00"


class TournamentExposureTest(unittest.TestCase):
    def target(
        self,
        *,
        target_type: str = "commander",
        target_id: str = "commander:kinnan",
        components: tuple[str, ...] = (),
    ) -> TournamentExposureTarget:
        return TournamentExposureTarget(
            target_type=target_type,
            target_id=target_id,
            target_version="identity.v1",
            display_label="Kinnan, Bonder Prodigy",
            component_ids=components,
            provenance_ref_ids=("identity:1",),
        )

    def manifest(
        self,
        *,
        scope_type: str = "global",
        scope_key: str = "global",
        matching: int = 25,
        available: int = 100,
        coverage_numerator: int = 4,
        coverage_denominator: int = 5,
        coverage_ratio: str = "0.8",
        low_sample_threshold: int = 10,
        low_coverage_threshold: str = "0.75",
        target: TournamentExposureTarget | None = None,
    ) -> TournamentExposurePopulationManifest:
        return TournamentExposurePopulationManifest(
            population_manifest_id=f"population:{scope_type}:{scope_key}",
            population_version="population.v1",
            population_spec_hash=f"hash:{scope_type}:{scope_key}",
            observation_unit="canonical_tournament_deck_instance",
            scope_type=scope_type,
            scope_key=scope_key,
            date_start="2026-01-01",
            date_end="2026-06-30",
            source_snapshot_ids=("snapshot:1",),
            source_record_count=120,
            available_population_count=available,
            matching_population_count=matching,
            excluded_record_count=10,
            deduplicated_record_count=10,
            target=target or self.target(),
            deduplication_policy="canonical_snapshot",
            deduplication_version="dedupe.v1",
            coverage_numerator=coverage_numerator,
            coverage_denominator=coverage_denominator,
            coverage_ratio=coverage_ratio,
            low_sample_threshold=low_sample_threshold,
            low_coverage_threshold=low_coverage_threshold,
            generated_at=NOW,
            provenance_ref_ids=("source:1",),
            caveat_ids=("caveat:independent",),
            region="North America" if scope_type == "region" else None,
            store="Local Store" if scope_type == "store" else None,
        )

    def assumptions(
        self,
        *,
        attendance: int = 64,
        seats: int = 3,
        rounds: int = 2,
        model_id: str = INDEPENDENT_SEAT_MODEL_ID,
    ) -> TournamentExposureAssumptions:
        return TournamentExposureAssumptions(
            model_id=model_id,
            model_version=TOURNAMENT_EXPOSURE_VERSION,
            formula_version="independent-seat-formula.v1",
            numeric_policy_version="decimal-12-half-even.v1",
            expected_attendance=attendance,
            event_size_class="medium",
            opponent_seats_per_round=seats,
            round_count=rounds,
            approximation_label="INDEPENDENT_SEAT_APPROXIMATION",
            approximation_warning=WARNING,
        )

    def estimate(self, **manifest_kwargs):
        return build_tournament_exposure_estimate(
            population_manifest=self.manifest(**manifest_kwargs),
            assumptions=self.assumptions(),
            calculated_at=NOW,
        )

    def test_fractional_formulas_and_fixed_precision(self) -> None:
        estimate = self.estimate()
        self.assertEqual(estimate.metagame_share, "0.250000000000")
        self.assertEqual(estimate.per_round_encounter_probability, "0.578125000000")
        self.assertEqual(estimate.event_wide_encounter_probability, "0.822021484375")
        self.assertEqual(estimate.expected_encounter_count, "1.500000000000")
        self.assertEqual(estimate.seat_opportunities_per_event, 6)

    def test_zero_and_one_share_boundaries(self) -> None:
        zero = self.estimate(matching=0)
        one = self.estimate(matching=100)
        self.assertEqual(zero.event_wide_encounter_probability, "0.000000000000")
        self.assertEqual(zero.expected_encounter_count, "0.000000000000")
        self.assertEqual(one.per_round_encounter_probability, "1.000000000000")
        self.assertEqual(one.event_wide_encounter_probability, "1.000000000000")

    def test_half_even_rounding_and_determinism(self) -> None:
        estimate = self.estimate(matching=1, available=6)
        first = json.dumps(
            tournament_exposure_estimate_to_dict(estimate),
            sort_keys=True,
            separators=(",", ":"),
        )
        second = json.dumps(
            tournament_exposure_estimate_to_dict(
                self.estimate(matching=1, available=6)
            ),
            sort_keys=True,
            separators=(",", ":"),
        )
        self.assertEqual(estimate.metagame_share, "0.166666666667")
        self.assertEqual(estimate.coverage_ratio, "0.800000000000")
        self.assertEqual(first, second)

    def test_expected_attendance_is_formula_neutral(self) -> None:
        manifest = self.manifest()
        low = build_tournament_exposure_estimate(
            population_manifest=manifest,
            assumptions=self.assumptions(attendance=32),
            calculated_at=NOW,
        )
        high = build_tournament_exposure_estimate(
            population_manifest=manifest,
            assumptions=self.assumptions(attendance=256),
            calculated_at=NOW,
        )
        self.assertEqual(
            low.event_wide_encounter_probability,
            high.event_wide_encounter_probability,
        )
        self.assertNotEqual(low.exposure_id, high.exposure_id)

    def test_partner_pair_is_order_normalized(self) -> None:
        first = self.target(
            target_type="partner_pair",
            target_id="pair:thrasios-tymna",
            components=("commander:tymna", "commander:thrasios"),
        )
        second = self.target(
            target_type="partner_pair",
            target_id="pair:thrasios-tymna",
            components=("commander:thrasios", "commander:tymna"),
        )
        self.assertEqual(first, second)
        with self.assertRaises(TournamentExposureBuildError):
            self.target(target_type="partner_pair", components=("only-one",))

    def test_all_target_and_scope_types_are_supported(self) -> None:
        for target_type in (
            "commander",
            "archetype",
            "card",
            "package",
            "functional_tag",
        ):
            self.manifest(target=self.target(target_type=target_type))
        for scope_type, scope_key in (
            ("global", "global"),
            ("region", "region:na"),
            ("country", "country:us"),
            ("store", "store:1"),
            ("organizer", "organizer:1"),
            ("tournament_size", "size:large"),
        ):
            self.manifest(scope_type=scope_type, scope_key=scope_key)

    def test_population_invariants_fail_closed(self) -> None:
        with self.assertRaises(TournamentExposureBuildError):
            self.manifest(matching=101)
        with self.assertRaises(TournamentExposureBuildError):
            self.manifest(available=True)
        with self.assertRaises(TournamentExposureBuildError):
            self.manifest(coverage_ratio="0.7")
        with self.assertRaises(TournamentExposureBuildError):
            replace(self.manifest(), date_end="2025-01-01")
        with self.assertRaises(TournamentExposureBuildError):
            replace(self.manifest(), source_snapshot_ids=("same", "same"))
        with self.assertRaises(TournamentExposureBuildError):
            replace(self.manifest(), source_snapshot_ids=())
        with self.assertRaises(TournamentExposureBuildError):
            replace(self.manifest(), available_population_count=121)
        with self.assertRaises(TournamentExposureBuildError):
            replace(self.manifest(), scope_key=" global")

    def test_hand_constructed_packet_tampering_fails_validation(self) -> None:
        estimate = self.estimate()
        with self.assertRaises(TournamentExposureBuildError):
            replace(estimate, per_round_encounter_probability="0.000000000000")
        with self.assertRaises(TournamentExposureBuildError):
            replace(estimate, exposure_id="exposure:tampered")

    def test_unsupported_model_and_weak_warning_fail(self) -> None:
        with self.assertRaises(TournamentExposureBuildError):
            self.assumptions(model_id="swiss")
        with self.assertRaises(TournamentExposureBuildError):
            replace(self.assumptions(), approximation_warning="Approximation.")

    def test_confidence_labels_preserve_sample_and_coverage(self) -> None:
        sufficient = self.estimate()
        low_sample = self.estimate(matching=2)
        low_coverage = self.estimate(
            coverage_numerator=1,
            coverage_denominator=2,
            coverage_ratio="0.5",
        )
        both = self.estimate(
            matching=2,
            coverage_numerator=1,
            coverage_denominator=2,
            coverage_ratio="0.5",
        )
        self.assertEqual(sufficient.confidence_label, "SUFFICIENT")
        self.assertEqual(low_sample.confidence_label, "LIMITED_SAMPLE")
        self.assertEqual(low_coverage.confidence_label, "LIMITED_COVERAGE")
        self.assertEqual(both.confidence_label, "LIMITED_SAMPLE_AND_COVERAGE")

    def test_local_and_regional_comparisons(self) -> None:
        global_estimate = self.estimate()
        local_estimate = self.estimate(
            scope_type="store", scope_key="store:1", matching=50
        )
        regional_estimate = self.estimate(
            scope_type="region", scope_key="region:na", matching=40
        )
        local = build_tournament_exposure_comparison(
            comparison_type="local_versus_global",
            selected_estimate=local_estimate,
            global_estimate=global_estimate,
            calculated_at=NOW,
        )
        regional = build_tournament_exposure_comparison(
            comparison_type="regional_versus_global",
            selected_estimate=regional_estimate,
            global_estimate=global_estimate,
            calculated_at=NOW,
        )
        self.assertEqual(local.event_wide_probability_delta, "0.162353515625")
        self.assertEqual(regional.selected_scope_type, "region")

    def test_incompatible_comparison_fails(self) -> None:
        selected = build_tournament_exposure_estimate(
            population_manifest=self.manifest(
                scope_type="store", scope_key="store:1"
            ),
            assumptions=self.assumptions(rounds=3),
            calculated_at=NOW,
        )
        with self.assertRaises(TournamentExposureBuildError):
            build_tournament_exposure_comparison(
                comparison_type="local_versus_global",
                selected_estimate=selected,
                global_estimate=self.estimate(),
                calculated_at=NOW,
            )

    def test_preparation_brief_is_evidence_only(self) -> None:
        estimate = self.estimate()
        brief = build_tournament_exposure_preparation_brief(
            estimate=estimate, generated_at=NOW
        )
        payload = json.dumps(brief.__dict__, default=list).casefold()
        for forbidden in ("replace card", "cut card", "add card", "matchup plan"):
            self.assertNotIn(forbidden, payload)
        self.assertIn("not a swiss-pairing model", brief.approximation_warning.casefold())

    def test_bundle_orders_packets_and_rejects_dangling_refs(self) -> None:
        global_estimate = self.estimate()
        local_estimate = self.estimate(
            scope_type="store", scope_key="store:1", matching=50
        )
        comparison = build_tournament_exposure_comparison(
            comparison_type="local_versus_global",
            selected_estimate=local_estimate,
            global_estimate=global_estimate,
            calculated_at=NOW,
        )
        brief = build_tournament_exposure_preparation_brief(
            estimate=local_estimate,
            comparisons=(comparison,),
            generated_at=NOW,
        )
        bundle = build_tournament_exposure_bundle(
            population_manifests=(
                local_estimate.population_manifest,
                global_estimate.population_manifest,
            ),
            estimates=(local_estimate, global_estimate),
            comparisons=(comparison,),
            preparation_briefs=(brief,),
            generated_at=NOW,
        )
        payload = tournament_exposure_bundle_to_dict(bundle)
        self.assertEqual(
            [item["exposure_id"] for item in payload["estimates"]],
            sorted(item["exposure_id"] for item in payload["estimates"]),
        )
        with self.assertRaises(TournamentExposureBuildError):
            build_tournament_exposure_bundle(
                population_manifests=(),
                estimates=(global_estimate,),
                generated_at=NOW,
            )
        with self.assertRaises(TournamentExposureBuildError):
            replace(bundle, bundle_id="bundle:tampered")
        with self.assertRaises(TournamentExposureBuildError):
            replace(comparison, comparison_id="comparison:tampered")
        with self.assertRaises(TournamentExposureBuildError):
            replace(brief, brief_id="brief:tampered")

    def test_packets_are_immutable_and_inputs_are_unchanged(self) -> None:
        manifest = self.manifest()
        source_refs = manifest.source_snapshot_ids
        estimate = build_tournament_exposure_estimate(
            population_manifest=manifest,
            assumptions=self.assumptions(),
            calculated_at=NOW,
        )
        with self.assertRaises(FrozenInstanceError):
            estimate.sample_size = 1
        self.assertEqual(manifest.source_snapshot_ids, source_refs)

    def test_timestamps_normalize_to_utc(self) -> None:
        estimate = self.estimate()
        self.assertEqual(estimate.calculated_at, "2026-07-29T23:00:00Z")
        with self.assertRaises(TournamentExposureBuildError):
            build_tournament_exposure_estimate(
                population_manifest=self.manifest(),
                assumptions=self.assumptions(),
                calculated_at="2026-07-29T23:00:00",
            )

    def test_module_has_no_forbidden_runtime_coupling(self) -> None:
        source = (
            Path(__file__).parents[1]
            / "codie"
            / "analytics"
            / "tournament_exposure.py"
        ).read_text(encoding="utf-8")
        for forbidden in (
            "import sqlite3",
            "import requests",
            "import httpx",
            "codie.db",
            "codie.providers",
            "codie.recommendations",
            "openai",
            "ollama",
        ):
            self.assertNotIn(forbidden, source)
        self.assertNotIn("datetime.now", source)
        self.assertNotIn("random.", source)


if __name__ == "__main__":
    unittest.main()
