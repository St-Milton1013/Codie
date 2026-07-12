from __future__ import annotations

from dataclasses import FrozenInstanceError
import json
from pathlib import Path
import unittest

from codie.cards.scryfall_bulk_snapshots import (
    ScryfallBulkSnapshotError,
    load_scryfall_bulk_snapshot_fixture,
)
from codie.cards.scryfall_migration_monitoring import (
    SCRYFALL_MIGRATION_MONITOR_VERSION,
    ScryfallMigrationMonitoringError,
    ScryfallMigrationOptions,
    build_scryfall_migration_report,
    scryfall_migration_report_to_dict,
    validate_scryfall_migration_report,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "scryfall"


class ScryfallMigrationMonitoringTest(unittest.TestCase):
    def _snapshot(self, name: str):
        return load_scryfall_bulk_snapshot_fixture(FIXTURE_DIR / name)

    def test_snapshot_to_snapshot_report_serializes_deterministically(self) -> None:
        previous = self._snapshot("migration_previous_snapshot.json")
        next_snapshot = self._snapshot("migration_next_snapshot.json")

        report = build_scryfall_migration_report(previous, next_snapshot)
        first = scryfall_migration_report_to_dict(report)
        second = scryfall_migration_report_to_dict(report)

        self.assertEqual(first, second)
        self.assertEqual(first["monitor_version"], SCRYFALL_MIGRATION_MONITOR_VERSION)
        self.assertEqual(first["previous_snapshot_id"], "migration_previous_snapshot")
        self.assertEqual(first["next_snapshot_id"], "migration_next_snapshot")
        self.assertRegex(first["previous_content_hash"], r"^[0-9a-f]{64}$")
        self.assertRegex(first["next_content_hash"], r"^[0-9a-f]{64}$")

    def test_report_round_trips_through_dictionary_compatible_form(self) -> None:
        previous = self._snapshot("migration_previous_snapshot.json")
        next_snapshot = self._snapshot("migration_next_snapshot.json")
        report = build_scryfall_migration_report(previous, next_snapshot)
        encoded = json.dumps(scryfall_migration_report_to_dict(report), sort_keys=True)
        decoded = json.loads(encoded)

        self.assertEqual(decoded, scryfall_migration_report_to_dict(report))
        self.assertIn("affected_consumers", decoded)
        self.assertIn("manual_review_items", decoded)

    def test_required_missing_scryfall_id_and_name_block_activation(self) -> None:
        previous = self._snapshot("migration_previous_snapshot.json")
        breaking = self._snapshot("migration_breaking_snapshot.json")
        report = build_scryfall_migration_report(previous, breaking)

        self.assertTrue(report.activation_blocked)
        self.assertTrue(any("missing required Scryfall id" in value for value in report.required_field_failures))
        self.assertTrue(any("missing required name" in value for value in report.required_field_failures))
        self.assertIn("missing required Scryfall id", report.activation_block_reasons)
        self.assertIn("missing required card name", report.activation_block_reasons)
        self.assertTrue(any(item.review_type == "missing_required_field" for item in report.manual_review_items))

    def test_duplicate_scryfall_id_blocks_activation(self) -> None:
        previous = self._snapshot("migration_previous_snapshot.json")
        breaking = self._snapshot("migration_breaking_snapshot.json")
        report = build_scryfall_migration_report(previous, breaking)

        self.assertTrue(report.activation_blocked)
        self.assertIn("duplicate Scryfall ID within next snapshot", report.activation_block_reasons)
        self.assertTrue(any("duplicate Scryfall id" in value for value in report.schema_breaking_conditions))

    def test_same_oracle_id_split_across_incompatible_identities_blocks_activation(self) -> None:
        previous = self._snapshot("migration_previous_snapshot.json")
        breaking = self._snapshot("migration_breaking_snapshot.json")
        report = build_scryfall_migration_report(previous, breaking)

        self.assertTrue(report.activation_blocked)
        self.assertIn("same oracle ID split across incompatible card identities", report.activation_block_reasons)
        self.assertTrue(any("oracle_id oracle-split is split" in value for value in report.schema_breaking_conditions))
        self.assertTrue(any(item.review_type == "oracle_id_split" for item in report.manual_review_items))

    def test_oracle_id_continuity_change_and_renamed_card_are_visible(self) -> None:
        previous = self._snapshot("migration_previous_snapshot.json")
        next_snapshot = self._snapshot("migration_next_snapshot.json")
        report = build_scryfall_migration_report(previous, next_snapshot)
        changes = scryfall_migration_report_to_dict(report)["identity_changes"]

        self.assertTrue(any(change["change_type"] == "oracle_id_change" for change in changes))
        self.assertTrue(any(change["change_type"] == "renamed_card" for change in changes))
        self.assertTrue(report.activation_blocked)
        self.assertIn("same Scryfall ID mapped to conflicting oracle IDs", report.activation_block_reasons)

    def test_scryfall_id_replacement_is_visible(self) -> None:
        previous = self._snapshot("migration_previous_snapshot.json")
        next_snapshot = self._snapshot("migration_next_snapshot.json")
        report = build_scryfall_migration_report(previous, next_snapshot)
        changes = scryfall_migration_report_to_dict(report)["identity_changes"]

        replacements = [change for change in changes if change["change_type"] == "scryfall_id_replacement"]
        self.assertEqual(len(replacements), 1)
        self.assertEqual(replacements[0]["previous_scryfall_id"], "sf-003")
        self.assertEqual(replacements[0]["next_scryfall_id"], "sf-005")

    def test_optional_field_changes_are_visible(self) -> None:
        previous = self._snapshot("migration_previous_snapshot.json")
        next_snapshot = self._snapshot("migration_next_snapshot.json")
        report = build_scryfall_migration_report(previous, next_snapshot)

        self.assertTrue(
            any(change.field_name == "legalities" and change.scryfall_id == "sf-001" for change in report.optional_field_changes)
        )

    def test_unknown_additive_fields_are_reported_but_not_blocking_by_default(self) -> None:
        previous = self._snapshot("migration_previous_snapshot.json")
        unknown_fields = self._snapshot("migration_unknown_fields_snapshot.json")
        report = build_scryfall_migration_report(previous, unknown_fields)

        self.assertFalse(report.activation_blocked)
        self.assertEqual(report.unknown_field_changes[0].field_name, "future_scryfall_field")
        self.assertEqual(report.unknown_field_changes[0].change_type, "added_unknown_field")
        self.assertTrue(any(item.review_type == "unknown_field" for item in report.manual_review_items))

    def test_unknown_fields_can_be_policy_blocking(self) -> None:
        previous = self._snapshot("migration_previous_snapshot.json")
        unknown_fields = self._snapshot("migration_unknown_fields_snapshot.json")
        report = build_scryfall_migration_report(
            previous,
            unknown_fields,
            options=ScryfallMigrationOptions(unknown_fields_block_activation=True),
        )

        self.assertTrue(report.activation_blocked)
        self.assertIn("unknown field policy blocks activation", report.activation_block_reasons)

    def test_unknown_enum_values_are_reported(self) -> None:
        previous = self._snapshot("migration_previous_snapshot.json")
        unknown_enums = self._snapshot("migration_unknown_enums_snapshot.json")
        report = build_scryfall_migration_report(previous, unknown_enums)
        enum_values = {(change.field_name, change.enum_value) for change in report.unknown_enum_changes}

        self.assertIn(("layout", "future_layout"), enum_values)
        self.assertIn(("legalities", "temporarily_legal"), enum_values)
        self.assertIn(("rarity", "experimental"), enum_values)
        self.assertTrue(any(item.review_type == "unknown_enum_value" for item in report.manual_review_items))

    def test_unknown_enum_policy_can_block_activation(self) -> None:
        previous = self._snapshot("migration_previous_snapshot.json")
        unknown_enums = self._snapshot("migration_unknown_enums_snapshot.json")
        report = build_scryfall_migration_report(
            previous,
            unknown_enums,
            options=ScryfallMigrationOptions(unknown_enums_block_activation=True),
        )

        self.assertTrue(report.activation_blocked)
        self.assertIn("unknown enum policy blocks activation", report.activation_block_reasons)

    def test_schema_breaking_conditions_report_affected_consumers(self) -> None:
        previous = self._snapshot("migration_previous_snapshot.json")
        breaking = self._snapshot("migration_breaking_snapshot.json")
        report = build_scryfall_migration_report(previous, breaking)
        consumers = {consumer.consumer_key for consumer in report.affected_consumers}

        self.assertIn("card_lookup", consumers)
        self.assertIn("canonicalization", consumers)
        self.assertIn("analytics", consumers)
        self.assertIn("scryfall_tagger_oracle_mappings", consumers)

    def test_input_snapshots_are_not_mutated_and_report_value_is_frozen(self) -> None:
        previous = self._snapshot("migration_previous_snapshot.json")
        next_snapshot = self._snapshot("migration_next_snapshot.json")
        before = [dict(card) for card in previous.raw_cards]
        report = build_scryfall_migration_report(previous, next_snapshot)

        with self.assertRaises(FrozenInstanceError):
            report.activation_blocked = False  # type: ignore[misc]
        self.assertEqual([dict(card) for card in previous.raw_cards], before)

    def test_malformed_inputs_fail_cleanly(self) -> None:
        with self.assertRaises(ScryfallBulkSnapshotError):
            load_scryfall_bulk_snapshot_fixture(FIXTURE_DIR / "malformed_bulk_snapshot.json")
        with self.assertRaises(ScryfallMigrationMonitoringError):
            build_scryfall_migration_report(object(), object())  # type: ignore[arg-type]
        with self.assertRaises(ScryfallMigrationMonitoringError):
            validate_scryfall_migration_report(object())  # type: ignore[arg-type]

    def test_no_live_network_sqlite_or_recommendation_imports(self) -> None:
        module_text = (Path(__file__).parents[1] / "codie" / "cards" / "scryfall_migration_monitoring.py").read_text(
            encoding="utf-8"
        )
        for forbidden in (
            "import req" + "uests",
            "import ht" + "tpx",
            "import sql" + "ite3",
            "from codie" + ".db",
            "import codie" + ".db",
            "from codie" + ".prov" + "iders",
            "from codie" + ".analytics",
            "from codie" + ".recommendations",
            "import op" + "enai",
            "import anth" + "ropic",
        ):
            self.assertNotIn(forbidden, module_text)


if __name__ == "__main__":
    unittest.main()
