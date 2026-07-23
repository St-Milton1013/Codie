from __future__ import annotations

import json
import sqlite3
import unittest

from codie.db.bootstrap import bootstrap_database
from codie.db.repositories.analytics import AnalyticsRepository
from codie.db.repositories.base import RepositoryError


class RelationshipPersistenceRepositoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = bootstrap_database()
        self.repository = AnalyticsRepository(self.connection)
        self.now = "2026-07-23T00:00:00+00:00"

    def tearDown(self) -> None:
        self.connection.close()

    def spec(self, **updates):
        value = {
            "population_spec_version": "relationship.population.v1",
            "population_spec_hash": "spec-hash-1",
            "observation_unit": "canonical_tournament_deck",
            "scope_type": "commander",
            "scope_key": "tymna-kraum",
            "zone_scope": "mainboard",
            "deduplication_policy": "canonical_deck",
            "concentration_policy": "visible_only",
            "spec_json": {"region": None, "placement": "top_16"},
            "created_at": self.now,
        }
        value.update(updates)
        return value

    def manifest(self, spec_id: int, **updates):
        value = {
            "population_manifest_version": "relationship.manifest.v1",
            "population_manifest_hash": "manifest-hash-1",
            "population_spec_id": spec_id,
            "population_spec_version": "relationship.population.v1",
            "population_spec_hash": "spec-hash-1",
            "source_snapshot_refs_json": ["snapshot-2", "snapshot-1"],
            "candidate_population_count": 12,
            "usable_population_count": 10,
            "unknown_or_excluded_count": 2,
            "deduplicated_population_count": 10,
            "generated_at": self.now,
        }
        value.update(updates)
        return value

    @staticmethod
    def members():
        return [
            {
                "member_sequence": 1,
                "observation_unit_type": "canonical_deck",
                "observation_unit_id": "deck-b",
                "inclusion_status": "included",
                "deduplication_key": "deck-b",
            },
            {
                "member_sequence": 0,
                "observation_unit_type": "canonical_deck",
                "observation_unit_id": "deck-a",
                "inclusion_status": "included",
                "deduplication_key": "deck-a",
            },
        ]

    def measurement(self, manifest_id: int, **updates):
        value = {
            "relationship_measurement_version": "relationship.measurement.v1",
            "relationship_measurement_hash": "measurement-hash-1",
            "relationship_type": "measured_co_occurrence",
            "source_endpoint_type": "card",
            "source_endpoint_id": "oracle-a",
            "target_endpoint_type": "card",
            "target_endpoint_id": "oracle-b",
            "directionality": "undirected",
            "population_manifest_id": manifest_id,
            "population_manifest_version": "relationship.manifest.v1",
            "N": 10,
            "nA": 5,
            "nB": 4,
            "nAB": 3,
            "candidate_population_count": 12,
            "usable_population_count": 10,
            "unknown_or_excluded_count": 2,
            "deduplicated_population_count": 10,
            "observed_co_occurrence": 3.0,
            "expected_co_occurrence": 2.0,
            "metric_bundle_version": "relationship.metrics.v1",
            "provenance_refs_json": ["snapshot-1"],
            "caveat_refs_json": [],
            "generated_at": self.now,
        }
        value.update(updates)
        return value

    @staticmethod
    def metrics():
        return [
            {
                "metric_name": "support",
                "metric_version": "v1",
                "orientation": "undirected",
                "metric_value": 0.3,
                "numerator": 3,
                "denominator": 10,
            },
            {
                "metric_name": "pmi",
                "metric_version": "v1",
                "orientation": "undirected",
                "metric_value": None,
                "undefined_reason": "ZERO_JOINT_PMI_UNDEFINED",
            },
        ]

    def create_manifest(self) -> int:
        spec_id = self.repository.insert_relationship_population_spec(self.spec())
        return self.repository.insert_relationship_population_manifest(
            self.manifest(spec_id), self.members()
        )

    def test_spec_json_is_deterministic_and_identity_is_idempotent(self) -> None:
        spec_id = self.repository.insert_relationship_population_spec(self.spec())
        repeated = self.repository.insert_relationship_population_spec(
            self.spec(spec_json='{"placement":"top_16","region":null}')
        )
        self.assertEqual(spec_id, repeated)
        row = self.repository.get_relationship_population_spec(
            "spec-hash-1", "relationship.population.v1"
        )
        self.assertEqual(row["spec_json"], '{"placement":"top_16","region":null}')

    def test_conflicting_immutable_spec_is_rejected(self) -> None:
        self.repository.insert_relationship_population_spec(self.spec())
        with self.assertRaises(RepositoryError):
            self.repository.insert_relationship_population_spec(
                self.spec(scope_key="different")
            )

    def test_private_global_population_metadata_is_rejected_recursively(self) -> None:
        with self.assertRaisesRegex(RepositoryError, "private user data"):
            self.repository.insert_relationship_population_spec(
                self.spec(spec_json={"nested": {"private_notes": "secret"}})
            )

    def test_manifest_members_round_trip_in_stable_order(self) -> None:
        manifest_id = self.create_manifest()
        rows = self.repository.list_relationship_population_members(manifest_id)
        self.assertEqual([row["observation_unit_id"] for row in rows], ["deck-a", "deck-b"])
        manifest = self.repository.get_relationship_population_manifest(manifest_id)
        self.assertEqual(json.loads(manifest["source_snapshot_refs_json"]), ["snapshot-2", "snapshot-1"])

    def test_manifest_child_failure_rolls_back_parent(self) -> None:
        spec_id = self.repository.insert_relationship_population_spec(self.spec())
        duplicate_members = [self.members()[0], self.members()[0]]
        with self.assertRaises(sqlite3.IntegrityError):
            self.repository.insert_relationship_population_manifest(
                self.manifest(spec_id), duplicate_members
            )
        count = self.connection.execute(
            "SELECT COUNT(*) AS count FROM relationship_population_manifests"
        ).fetchone()["count"]
        self.assertEqual(count, 0)

    def test_manifest_identity_rejects_changed_members(self) -> None:
        spec_id = self.repository.insert_relationship_population_spec(self.spec())
        self.repository.insert_relationship_population_manifest(
            self.manifest(spec_id), self.members()
        )
        changed = self.members()
        changed[0] = {**changed[0], "inclusion_status": "excluded"}
        with self.assertRaisesRegex(RepositoryError, "manifest members"):
            self.repository.insert_relationship_population_manifest(
                self.manifest(spec_id), changed
            )

    def test_measurement_and_metrics_preserve_counts_null_reasons_and_order(self) -> None:
        manifest_id = self.create_manifest()
        measurement_id = self.repository.insert_relationship_measurement(
            self.measurement(manifest_id), self.metrics()
        )
        row = self.repository.get_relationship_measurement(measurement_id)
        self.assertEqual((row["N"], row["nA"], row["nB"], row["nAB"]), (10, 5, 4, 3))
        metrics = self.repository.list_relationship_measurement_metrics(measurement_id)
        self.assertEqual([metric["metric_name"] for metric in metrics], ["pmi", "support"])
        self.assertEqual(metrics[0]["undefined_reason"], "ZERO_JOINT_PMI_UNDEFINED")

    def test_count_invariants_fail_before_write(self) -> None:
        manifest_id = self.create_manifest()
        with self.assertRaisesRegex(RepositoryError, "invariants"):
            self.repository.insert_relationship_measurement(
                self.measurement(manifest_id, nAB=6), self.metrics()
            )
        self.assertEqual(
            self.connection.execute(
                "SELECT COUNT(*) AS count FROM relationship_measurements"
            ).fetchone()["count"],
            0,
        )

    def test_invalid_metric_rolls_back_measurement(self) -> None:
        manifest_id = self.create_manifest()
        invalid = self.metrics() + [
            {
                "metric_name": "synergy_score",
                "metric_version": "v1",
                "orientation": "undirected",
                "metric_value": 1.0,
            }
        ]
        with self.assertRaisesRegex(RepositoryError, "Unsupported"):
            self.repository.insert_relationship_measurement(
                self.measurement(manifest_id), invalid
            )
        self.assertEqual(
            self.connection.execute(
                "SELECT COUNT(*) AS count FROM relationship_measurements"
            ).fetchone()["count"],
            0,
        )

    def test_measurement_identity_rejects_changed_metrics(self) -> None:
        manifest_id = self.create_manifest()
        self.repository.insert_relationship_measurement(
            self.measurement(manifest_id), self.metrics()
        )
        changed = self.metrics()
        changed[0] = {**changed[0], "metric_value": 0.4}
        with self.assertRaisesRegex(RepositoryError, "measurement metrics"):
            self.repository.insert_relationship_measurement(
                self.measurement(manifest_id), changed
            )

    def test_metric_value_and_undefined_reason_are_mutually_exclusive(self) -> None:
        manifest_id = self.create_manifest()
        with self.assertRaisesRegex(RepositoryError, "mutually exclusive"):
            self.repository.insert_relationship_measurement(
                self.measurement(manifest_id),
                [
                    {
                        "metric_name": "support",
                        "metric_version": "v1",
                        "orientation": "undirected",
                        "metric_value": None,
                    }
                ],
            )

    def test_foreign_keys_reject_dangling_manifest(self) -> None:
        with self.assertRaises(sqlite3.IntegrityError):
            self.repository.insert_relationship_population_manifest(
                self.manifest(999), self.members()
            )

    def test_list_measurements_filters_and_orders(self) -> None:
        manifest_id = self.create_manifest()
        first = self.repository.insert_relationship_measurement(
            self.measurement(manifest_id), self.metrics()
        )
        rows = self.repository.list_relationship_measurements(
            population_manifest_id=manifest_id,
            source_endpoint_id="oracle-a",
            target_endpoint_id="oracle-b",
        )
        self.assertEqual([row["relationship_measurement_id"] for row in rows], [first])


if __name__ == "__main__":
    unittest.main()
