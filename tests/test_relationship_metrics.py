from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
import json
import math
from pathlib import Path
import unittest

from codie.analytics.relationship_metrics import (
    RELATIONSHIP_METRIC_VERSION,
    RelationshipCountPacket,
    RelationshipMetricBuildError,
    build_relationship_metric_bundle,
    relationship_metric_bundle_to_dict,
    validate_relationship_count_packet,
    validate_relationship_metric_bundle,
)


CALCULATED_AT = "2026-07-24T01:00:00Z"


def count_packet(**overrides):
    values = {
        "count_packet_version": "relationship-count.v1",
        "population_manifest_id": "population-1",
        "population_manifest_version": "population-manifest.v1",
        "population_spec_hash": "spec-hash-1",
        "source_endpoint_type": "card",
        "source_endpoint_id": "oracle-a",
        "target_endpoint_type": "card",
        "target_endpoint_id": "oracle-b",
        "directionality": "undirected",
        "N": 100,
        "nA": 20,
        "nB": 25,
        "nAB": 10,
        "candidate_population_count": 120,
        "usable_population_count": 100,
        "unknown_or_excluded_count": 20,
        "deduplicated_population_count": 2,
        "matching_deck_count": 80,
        "available_deck_count": 100,
        "coverage_ratio": 0.8,
        "low_sample_threshold": 25,
        "low_coverage_threshold": 0.6,
        "provenance_ref_ids": ("source-1", "source-2"),
        "caveat_ids": ("caveat-1",),
    }
    values.update(overrides)
    return RelationshipCountPacket(**values)


def metric_bundle(packet=None):
    return build_relationship_metric_bundle(
        packet or count_packet(),
        measurement_version="relationship-measurement.v1",
        metric_bundle_version="relationship-metric-bundle.v1",
        calculated_at=CALCULATED_AT,
    )


def metric_map(bundle):
    return {
        (metric.metric_name, metric.orientation): metric
        for metric in bundle.metrics
    }


class RelationshipMetricTests(unittest.TestCase):
    def test_constitutional_formulas_match_hand_calculation(self) -> None:
        bundle = metric_bundle()
        metrics = metric_map(bundle)

        self.assertAlmostEqual(metrics[("support", "undirected")].value, 0.1)
        self.assertAlmostEqual(
            metrics[("directional_confidence", "A_to_B")].value, 0.5
        )
        self.assertAlmostEqual(
            metrics[("directional_confidence", "B_to_A")].value, 0.4
        )
        self.assertAlmostEqual(
            metrics[("dependence_delta", "A_to_B")].value, 0.25
        )
        self.assertAlmostEqual(
            metrics[("dependence_delta", "B_to_A")].value, 0.2
        )
        self.assertAlmostEqual(metrics[("lift", "undirected")].value, 2.0)
        self.assertAlmostEqual(metrics[("leverage", "undirected")].value, 0.05)
        self.assertAlmostEqual(
            metrics[("jaccard_similarity", "undirected")].value,
            10 / 35,
        )
        self.assertAlmostEqual(metrics[("pmi", "undirected")].value, 1.0)
        self.assertEqual(bundle.observed_co_occurrence, 10)
        self.assertAlmostEqual(bundle.expected_co_occurrence, 5.0)

    def test_metric_order_versions_and_orientations_are_stable(self) -> None:
        bundle = metric_bundle()
        self.assertEqual(
            tuple((metric.metric_name, metric.orientation) for metric in bundle.metrics),
            (
                ("support", "undirected"),
                ("directional_confidence", "A_to_B"),
                ("directional_confidence", "B_to_A"),
                ("dependence_delta", "A_to_B"),
                ("dependence_delta", "B_to_A"),
                ("lift", "undirected"),
                ("leverage", "undirected"),
                ("jaccard_similarity", "undirected"),
                ("pmi", "undirected"),
            ),
        )
        self.assertTrue(
            all(
                metric.metric_version == RELATIONSHIP_METRIC_VERSION
                for metric in bundle.metrics
            )
        )

    def test_serialization_is_deterministic_and_preserves_evidence_fields(self) -> None:
        first = relationship_metric_bundle_to_dict(metric_bundle())
        second = relationship_metric_bundle_to_dict(metric_bundle())
        encoded_first = json.dumps(first, sort_keys=True, separators=(",", ":"))
        encoded_second = json.dumps(second, sort_keys=True, separators=(",", ":"))

        self.assertEqual(encoded_first, encoded_second)
        self.assertEqual(first["N"], 100)
        self.assertEqual(first["nA"], 20)
        self.assertEqual(first["nB"], 25)
        self.assertEqual(first["nAB"], 10)
        self.assertEqual(first["coverage_ratio"], 0.8)
        self.assertEqual(first["provenance_ref_ids"], ["source-1", "source-2"])
        self.assertEqual(first["caveat_ids"], ["caveat-1"])
        self.assertEqual(first["calculated_at"], CALCULATED_AT)

    def test_packets_are_immutable_and_do_not_mutate_caller_lists(self) -> None:
        refs = ["source-1"]
        packet = count_packet(provenance_ref_ids=refs)
        refs.append("source-2")
        bundle = metric_bundle(packet)

        self.assertEqual(packet.provenance_ref_ids, ("source-1",))
        self.assertEqual(bundle.provenance_ref_ids, ("source-1",))
        with self.assertRaises(FrozenInstanceError):
            packet.N = 10
        with self.assertRaises(FrozenInstanceError):
            bundle.metrics = ()

    def test_count_invariants_fail_closed(self) -> None:
        invalid_overrides = (
            {"N": 0, "nA": 0, "nB": 0, "nAB": 0},
            {"nA": 101},
            {"nB": 101},
            {"nAB": 21},
            {"matching_deck_count": 101},
            {"coverage_ratio": 0.7},
            {"directionality": "sometimes"},
            {"low_coverage_threshold": 1.1},
        )
        for overrides in invalid_overrides:
            with self.subTest(overrides=overrides):
                with self.assertRaises(RelationshipMetricBuildError):
                    count_packet(**overrides)

    def test_boolean_counts_and_non_finite_values_are_rejected(self) -> None:
        for overrides in (
            {"N": True},
            {"nA": False},
            {"coverage_ratio": math.nan},
            {"coverage_ratio": math.inf},
            {"low_coverage_threshold": math.nan},
        ):
            with self.subTest(overrides=overrides):
                with self.assertRaises(RelationshipMetricBuildError):
                    count_packet(**overrides)

    def test_duplicate_and_invalid_reference_ids_are_rejected(self) -> None:
        for overrides in (
            {"provenance_ref_ids": ("source-1", "source-1")},
            {"caveat_ids": ("",)},
            {"provenance_ref_ids": "source-1"},
        ):
            with self.subTest(overrides=overrides):
                with self.assertRaises(RelationshipMetricBuildError):
                    count_packet(**overrides)

    def test_zero_endpoint_a_preserves_defined_and_undefined_states(self) -> None:
        bundle = metric_bundle(count_packet(nA=0, nAB=0))
        metrics = metric_map(bundle)

        self.assertEqual(metrics[("support", "undirected")].value, 0.0)
        self.assertEqual(metrics[("leverage", "undirected")].value, 0.0)
        self.assertIsNone(
            metrics[("directional_confidence", "A_to_B")].value
        )
        self.assertEqual(
            metrics[("directional_confidence", "A_to_B")].undefined_reason,
            "ENDPOINT_A_NOT_OBSERVED",
        )
        self.assertIsNone(metrics[("dependence_delta", "A_to_B")].value)
        self.assertIsNone(metrics[("lift", "undirected")].value)
        self.assertIsNone(metrics[("pmi", "undirected")].value)

    def test_zero_endpoint_b_preserves_directional_reason(self) -> None:
        metrics = metric_map(metric_bundle(count_packet(nB=0, nAB=0)))
        self.assertEqual(
            metrics[("directional_confidence", "B_to_A")].undefined_reason,
            "ENDPOINT_B_NOT_OBSERVED",
        )
        self.assertEqual(
            metrics[("dependence_delta", "B_to_A")].undefined_reason,
            "ENDPOINT_B_NOT_OBSERVED",
        )

    def test_zero_union_and_zero_joint_reasons_are_visible(self) -> None:
        metrics = metric_map(
            metric_bundle(count_packet(nA=0, nB=0, nAB=0))
        )
        self.assertEqual(
            metrics[("jaccard_similarity", "undirected")].undefined_reason,
            "ZERO_UNION_JACCARD_UNDEFINED",
        )
        self.assertEqual(
            metrics[("pmi", "undirected")].undefined_reason,
            "ZERO_JOINT_PMI_UNDEFINED",
        )

    def test_zero_joint_with_observed_endpoints_keeps_finite_metrics(self) -> None:
        bundle = metric_bundle(count_packet(nAB=0))
        metrics = metric_map(bundle)
        self.assertEqual(metrics[("support", "undirected")].value, 0.0)
        self.assertAlmostEqual(metrics[("leverage", "undirected")].value, -0.05)
        self.assertTrue(
            all(
                metric.value is None or math.isfinite(metric.value)
                for metric in bundle.metrics
            )
        )

    def test_sample_and_coverage_labels_do_not_change_formulas(self) -> None:
        low = metric_bundle(
            count_packet(
                usable_population_count=10,
                matching_deck_count=20,
                coverage_ratio=0.2,
            )
        )
        normal = metric_bundle()
        self.assertEqual(low.sample_label, "low_sample")
        self.assertEqual(low.availability_label, "low_coverage")
        self.assertEqual(
            tuple(metric.value for metric in low.metrics),
            tuple(metric.value for metric in normal.metrics),
        )
        self.assertEqual(low.low_sample_threshold, 25)
        self.assertEqual(low.low_coverage_threshold, 0.6)

    def test_zero_available_population_is_explicitly_unavailable(self) -> None:
        bundle = metric_bundle(
            count_packet(
                available_deck_count=0,
                matching_deck_count=0,
                coverage_ratio=None,
            )
        )
        self.assertIsNone(bundle.coverage_ratio)
        self.assertEqual(bundle.availability_label, "unavailable")

    def test_zero_matching_population_is_insufficient_coverage(self) -> None:
        bundle = metric_bundle(
            count_packet(matching_deck_count=0, coverage_ratio=0.0)
        )
        self.assertEqual(bundle.availability_label, "insufficient_coverage")

    def test_direct_card_to_tag_measurement_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            RelationshipMetricBuildError,
            "anti-tautology",
        ):
            count_packet(target_endpoint_type="functional_tag")

    def test_public_validators_reject_wrong_packet_types(self) -> None:
        with self.assertRaises(RelationshipMetricBuildError):
            validate_relationship_count_packet({})
        with self.assertRaises(RelationshipMetricBuildError):
            validate_relationship_metric_bundle({})

    def test_bundle_validator_rejects_reordered_metrics(self) -> None:
        bundle = metric_bundle()
        with self.assertRaises(RelationshipMetricBuildError):
            replace(bundle, metrics=tuple(reversed(bundle.metrics)))

    def test_module_has_no_forbidden_runtime_coupling(self) -> None:
        source = (
            Path(__file__).parents[1]
            / "codie"
            / "analytics"
            / "relationship_metrics.py"
        ).read_text(encoding="utf-8")
        forbidden = (
            "codie.db",
            "repository",
            "sqlite3",
            "requests",
            "httpx",
            "openai",
            "anthropic",
            "datetime.now",
            "time.time",
            "open(",
            "recommendation",
            "simulator",
        )
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, source.lower())


if __name__ == "__main__":
    unittest.main()
