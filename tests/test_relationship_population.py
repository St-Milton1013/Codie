from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
import json
from pathlib import Path
from types import MappingProxyType
import unittest

from codie.analytics.relationship_metrics import RelationshipCountPacket
from codie.analytics.relationship_population import (
    RELATIONSHIP_POPULATION_VERSION,
    RelationshipDeckPresenceRecord,
    RelationshipEndpoint,
    RelationshipPopulationBuildError,
    RelationshipPopulationSpec,
    build_relationship_population_resolution,
    relationship_population_manifest_to_dict,
    relationship_population_resolution_to_dict,
    validate_relationship_population_manifest,
    validate_relationship_population_resolution,
    validate_relationship_population_spec,
)


CALCULATED_AT = "2026-07-29T22:30:00Z"


def population_spec(**overrides):
    values = {
        "population_spec_version": "population-spec.v1",
        "population_scope_type": "commander_average",
        "population_scope_key": "commander:alpha",
        "source_snapshot_ids": ("snapshot-source-1",),
        "analytics_version": "analytics.v1",
        "deduplication_policy": "canonical_snapshot",
        "inactive_status_policy": "exclude_inactive",
        "low_sample_threshold": 2,
        "low_coverage_threshold": 0.75,
        "calculated_at": CALCULATED_AT,
        "commander_key": "commander-alpha",
        "provenance_ref_ids": ("provenance-1",),
        "caveat_ids": ("caveat-1",),
    }
    values.update(overrides)
    return RelationshipPopulationSpec(**values)


def presence_record(deck_id, snapshot_id, cards=(), **overrides):
    values = {
        "deck_id": deck_id,
        "snapshot_id": snapshot_id,
        "observation_status": "active",
        "privacy_class": "public",
        "commander_key": "commander-alpha",
        "mainboard_oracle_ids": tuple(cards),
        "source_snapshot_ids": ("snapshot-source-1",),
        "provenance_ref_ids": (f"provenance-{deck_id}",),
    }
    values.update(overrides)
    return RelationshipDeckPresenceRecord(**values)


def card_endpoint(endpoint_id):
    return RelationshipEndpoint(
        endpoint_type="card",
        endpoint_id=endpoint_id,
        canonical_identity_ids=(endpoint_id,),
    )


def build_resolution(records, **overrides):
    return build_relationship_population_resolution(
        overrides.pop("spec", population_spec()),
        records,
        overrides.pop("source_endpoint", card_endpoint("oracle-a")),
        overrides.pop("target_endpoint", card_endpoint("oracle-b")),
        **overrides,
    )


class RelationshipPopulationTests(unittest.TestCase):
    def test_presence_counts_and_existing_count_packet_compatibility(self) -> None:
        resolution = build_resolution(
            (
                presence_record("deck-1", "snapshot-1", ("oracle-a", "oracle-b")),
                presence_record("deck-2", "snapshot-2", ("oracle-a",)),
                presence_record("deck-3", "snapshot-3", ("oracle-b",)),
            )
        )

        self.assertIsInstance(resolution.count_packet, RelationshipCountPacket)
        self.assertEqual(resolution.count_packet.N, 3)
        self.assertEqual(resolution.count_packet.nA, 2)
        self.assertEqual(resolution.count_packet.nB, 2)
        self.assertEqual(resolution.count_packet.nAB, 1)
        self.assertEqual(resolution.count_packet.candidate_population_count, 3)
        self.assertEqual(resolution.count_packet.usable_population_count, 3)
        self.assertEqual(resolution.count_packet.coverage_ratio, 1.0)

    def test_manifest_identity_and_serialization_ignore_input_order(self) -> None:
        records = (
            presence_record("deck-b", "snapshot-2", ("oracle-a",)),
            presence_record("deck-a", "snapshot-1", ("oracle-b",)),
        )
        forward = build_resolution(records)
        reverse = build_resolution(tuple(reversed(records)))

        self.assertEqual(
            forward.manifest.population_manifest_id,
            reverse.manifest.population_manifest_id,
        )
        self.assertEqual(
            relationship_population_resolution_to_dict(forward),
            relationship_population_resolution_to_dict(reverse),
        )
        self.assertEqual(
            json.dumps(
                relationship_population_resolution_to_dict(forward),
                sort_keys=True,
                separators=(",", ":"),
            ),
            json.dumps(
                relationship_population_resolution_to_dict(reverse),
                sort_keys=True,
                separators=(",", ":"),
            ),
        )

    def test_set_like_identity_and_reference_order_is_normalized(self) -> None:
        forward = build_relationship_population_resolution(
            population_spec(
                source_snapshot_ids=("source-b", "source-a"),
                provenance_ref_ids=("provenance-b", "provenance-a"),
                caveat_ids=("caveat-b", "caveat-a"),
            ),
            (
                presence_record(
                    "deck-1",
                    "snapshot-1",
                    ("oracle-b", "oracle-a"),
                    source_snapshot_ids=("source-b", "source-a"),
                    provenance_ref_ids=("provenance-b", "provenance-a"),
                ),
            ),
            RelationshipEndpoint(
                endpoint_type="card",
                endpoint_id="source-set",
                canonical_identity_ids=("oracle-b", "oracle-a"),
            ),
            card_endpoint("oracle-c"),
        )
        reverse = build_relationship_population_resolution(
            population_spec(
                source_snapshot_ids=("source-a", "source-b"),
                provenance_ref_ids=("provenance-a", "provenance-b"),
                caveat_ids=("caveat-a", "caveat-b"),
            ),
            (
                presence_record(
                    "deck-1",
                    "snapshot-1",
                    ("oracle-a", "oracle-b"),
                    source_snapshot_ids=("source-a", "source-b"),
                    provenance_ref_ids=("provenance-a", "provenance-b"),
                ),
            ),
            RelationshipEndpoint(
                endpoint_type="card",
                endpoint_id="source-set",
                canonical_identity_ids=("oracle-a", "oracle-b"),
            ),
            card_endpoint("oracle-c"),
        )

        self.assertEqual(
            relationship_population_resolution_to_dict(forward),
            relationship_population_resolution_to_dict(reverse),
        )

    def test_packets_freeze_nested_values_without_mutating_callers(self) -> None:
        cards = ["oracle-a"]
        metadata = {"source": {"kind": "fixture"}}
        record = presence_record(
            "deck-1",
            "snapshot-1",
            cards,
            metadata=metadata,
        )
        cards.append("oracle-b")
        metadata["source"]["kind"] = "changed"
        resolution = build_resolution((record,))

        self.assertEqual(record.mainboard_oracle_ids, ("oracle-a",))
        self.assertIsInstance(record.metadata, MappingProxyType)
        self.assertEqual(record.metadata["source"]["kind"], "fixture")
        with self.assertRaises(FrozenInstanceError):
            resolution.labels = ()

    def test_canonical_snapshot_deduplication_is_stable_and_visible(self) -> None:
        first = presence_record("deck-a", "snapshot-1", ("oracle-a",))
        duplicate = presence_record(
            "deck-z",
            "snapshot-1",
            ("oracle-a", "oracle-b"),
        )
        second = presence_record("deck-b", "snapshot-2", ("oracle-b",))

        resolution = build_resolution((duplicate, second, first))
        packet = resolution.count_packet

        self.assertEqual(resolution.presence_record_ids[0], "deck-a@snapshot-1")
        self.assertEqual(packet.candidate_population_count, 3)
        self.assertEqual(packet.usable_population_count, 2)
        self.assertEqual(packet.deduplicated_population_count, 1)
        self.assertEqual(packet.unknown_or_excluded_count, 0)
        self.assertEqual(
            tuple(item.reason_code for item in resolution.exclusions),
            ("DUPLICATE_CANONICAL_SNAPSHOT",),
        )

    def test_inactive_private_and_unapproved_records_are_visible_exclusions(self) -> None:
        records = (
            presence_record("active", "snapshot-1", ("oracle-a",)),
            presence_record(
                "resolved",
                "snapshot-2",
                ("oracle-a",),
                observation_status="resolved",
            ),
            presence_record(
                "ignored",
                "snapshot-3",
                ("oracle-a",),
                observation_status="ignored_by_policy",
            ),
            presence_record(
                "private",
                "snapshot-4",
                ("oracle-a",),
                privacy_class="private",
            ),
            presence_record(
                "unapproved",
                "snapshot-5",
                ("oracle-a",),
                observation_status="unapproved_observation",
            ),
        )
        resolution = build_resolution(records)

        self.assertEqual(resolution.count_packet.N, 1)
        self.assertEqual(resolution.count_packet.unknown_or_excluded_count, 4)
        self.assertEqual(
            {item.reason_code for item in resolution.exclusions},
            {
                "INACTIVE_RESOLVED",
                "INACTIVE_IGNORED_BY_POLICY",
                "PRIVATE_USER_RECORD",
                "UNAPPROVED_OBSERVATION",
            },
        )
        self.assertEqual(resolution.count_packet.coverage_ratio, 1.0)
        self.assertEqual(resolution.labels, ("low_sample",))

    def test_low_provenance_coverage_is_visible_without_changing_counts(self) -> None:
        records = (
            presence_record("deck-1", "snapshot-1", ("oracle-a",)),
            presence_record(
                "deck-2",
                "snapshot-2",
                ("oracle-b",),
                source_snapshot_ids=(),
                provenance_ref_ids=(),
            ),
        )
        resolution = build_resolution(records)

        self.assertEqual(resolution.count_packet.N, 2)
        self.assertEqual(resolution.count_packet.nA, 1)
        self.assertEqual(resolution.count_packet.nB, 1)
        self.assertEqual(resolution.count_packet.matching_deck_count, 1)
        self.assertEqual(resolution.count_packet.available_deck_count, 2)
        self.assertEqual(resolution.count_packet.coverage_ratio, 0.5)
        self.assertEqual(resolution.labels, ("low_coverage",))

    def test_explicitly_approved_private_observation_is_usable(self) -> None:
        record = presence_record(
            "private-approved",
            "snapshot-1",
            ("oracle-a",),
            privacy_class="private",
            observation_status="approved_observation",
        )
        resolution = build_resolution((record,))
        self.assertEqual(resolution.count_packet.N, 1)
        self.assertEqual(resolution.exclusions, ())

    def test_sideboard_and_auxiliary_require_explicit_flags(self) -> None:
        record = presence_record(
            "deck-1",
            "snapshot-1",
            (),
            sideboard_oracle_ids=("oracle-a",),
            auxiliary_oracle_ids=("oracle-b",),
        )
        default = build_resolution((record,))
        included = build_resolution(
            (record,),
            spec=population_spec(
                include_sideboard=True,
                include_auxiliary=True,
            ),
        )

        self.assertEqual((default.count_packet.nA, default.count_packet.nB), (0, 0))
        self.assertEqual((included.count_packet.nA, included.count_packet.nB), (1, 1))

    def test_tag_and_package_presence_use_already_built_ids(self) -> None:
        record = presence_record(
            "deck-1",
            "snapshot-1",
            (),
            tag_assignment_ids=("tag-draw",),
            package_ids=("package-breach",),
        )
        resolution = build_resolution(
            (record,),
            source_endpoint=RelationshipEndpoint(
                endpoint_type="tag",
                endpoint_id="draw",
                tag_assignment_ids=("tag-draw",),
            ),
            target_endpoint=RelationshipEndpoint(
                endpoint_type="package",
                endpoint_id="breach",
                package_member_ids=("package-breach",),
            ),
        )
        self.assertEqual(
            (resolution.count_packet.nA, resolution.count_packet.nB),
            (1, 1),
        )

    def test_commander_and_exact_partner_pair_matching(self) -> None:
        record = presence_record(
            "deck-1",
            "snapshot-1",
            (),
            commander_key="commander-beta",
            partner_key="commander-alpha",
        )
        resolution = build_resolution(
            (record,),
            source_endpoint=RelationshipEndpoint(
                endpoint_type="commander",
                endpoint_id="commander-beta",
            ),
            target_endpoint=RelationshipEndpoint(
                endpoint_type="commander_pair",
                endpoint_id="commander-alpha+commander-beta",
                canonical_identity_ids=(
                    "commander-alpha",
                    "commander-beta",
                ),
            ),
        )
        reversed_endpoint = replace(
            resolution.target_endpoint,
            canonical_identity_ids=(
                "commander-beta",
                "commander-alpha",
            ),
        )
        reversed_resolution = build_resolution(
            (record,),
            source_endpoint=resolution.source_endpoint,
            target_endpoint=reversed_endpoint,
        )

        self.assertEqual(
            (resolution.count_packet.nA, resolution.count_packet.nB),
            (1, 1),
        )
        self.assertEqual(reversed_resolution.count_packet.nB, 1)
        self.assertEqual(
            resolution.manifest.population_manifest_id,
            reversed_resolution.manifest.population_manifest_id,
        )

    def test_missing_and_unresolved_identities_fail_closed(self) -> None:
        for values in (
            {"deck_id": ""},
            {"snapshot_id": ""},
            {"mainboard_oracle_ids": ("unresolved:Card Name",)},
        ):
            with self.subTest(values=values):
                with self.assertRaises(RelationshipPopulationBuildError):
                    presence_record(
                        values.pop("deck_id", "deck-1"),
                        values.pop("snapshot_id", "snapshot-1"),
                        (),
                        **values,
                    )

    def test_endpoint_validation_and_anti_tautology_fail_closed(self) -> None:
        with self.assertRaises(RelationshipPopulationBuildError):
            RelationshipEndpoint(
                endpoint_type="mystery",
                endpoint_id="unknown",
            )
        with self.assertRaises(RelationshipPopulationBuildError):
            build_resolution(
                (presence_record("deck-1", "snapshot-1", ("oracle-a",)),),
                target_endpoint=RelationshipEndpoint(
                    endpoint_type="tag",
                    endpoint_id="draw",
                    tag_assignment_ids=("tag-draw",),
                ),
            )
        with self.assertRaises(RelationshipPopulationBuildError):
            build_resolution(
                (presence_record("deck-1", "snapshot-1", ("oracle-a",)),),
                target_endpoint=card_endpoint("oracle-a"),
            )

    def test_empty_population_and_invalid_policies_fail_closed(self) -> None:
        with self.assertRaises(RelationshipPopulationBuildError):
            build_resolution(())
        with self.assertRaises(RelationshipPopulationBuildError):
            population_spec(deduplication_policy="input_order")
        with self.assertRaises(RelationshipPopulationBuildError):
            population_spec(inactive_status_policy="include_all")

    def test_population_count_and_resolution_invariants_are_enforced(self) -> None:
        resolution = build_resolution(
            (presence_record("deck-1", "snapshot-1", ("oracle-a",)),)
        )
        with self.assertRaises(RelationshipPopulationBuildError):
            replace(
                resolution.manifest,
                candidate_population_count=2,
            )
        with self.assertRaises(RelationshipPopulationBuildError):
            replace(
                resolution,
                presence_record_ids=("wrong", "extra"),
            )
        validate_relationship_population_spec(population_spec())
        validate_relationship_population_manifest(resolution.manifest)
        validate_relationship_population_resolution(resolution)

    def test_caller_timestamp_and_evidence_references_remain_visible(self) -> None:
        resolution = build_resolution(
            (presence_record("deck-1", "snapshot-1", ("oracle-a",)),)
        )
        payload = relationship_population_resolution_to_dict(resolution)
        manifest = relationship_population_manifest_to_dict(
            resolution.manifest
        )

        self.assertEqual(manifest["calculated_at"], CALCULATED_AT)
        self.assertEqual(manifest["provenance_ref_ids"], ["provenance-1"])
        self.assertEqual(manifest["caveat_ids"], ["caveat-1"])
        self.assertEqual(
            payload["count_packet"]["population_manifest_id"],
            manifest["population_manifest_id"],
        )
        self.assertEqual(
            payload["count_packet"]["population_spec_hash"],
            manifest["population_spec_hash"],
        )

    def test_private_or_non_json_metadata_is_rejected_recursively(self) -> None:
        for metadata in (
            {"nested": {"private_notes": "secret"}},
            {"raw_payload": {"cards": []}},
            {"value": object()},
        ):
            with self.subTest(metadata=metadata):
                with self.assertRaises(RelationshipPopulationBuildError):
                    presence_record(
                        "deck-1",
                        "snapshot-1",
                        (),
                        metadata=metadata,
                    )

    def test_module_has_no_forbidden_runtime_dependencies_or_execution_helpers(self) -> None:
        source = (
            Path(__file__).resolve().parents[1]
            / "codie"
            / "analytics"
            / "relationship_population.py"
        ).read_text(encoding="utf-8")
        for forbidden in (
            "import sqlite3",
            "import requests",
            "import httpx",
            "codie.db",
            "codie.providers",
            "openai",
            "anthropic",
            "ollama",
            "def execute_",
            "def rank_",
            "def recommend_",
            "datetime.now",
            "datetime.utcnow",
            "open(",
            "write_text(",
            "write_bytes(",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source)
        self.assertEqual(
            RELATIONSHIP_POPULATION_VERSION,
            "relationship-population.v1",
        )


if __name__ == "__main__":
    unittest.main()
