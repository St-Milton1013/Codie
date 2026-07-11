from __future__ import annotations

from dataclasses import FrozenInstanceError
import json
from pathlib import Path
import tempfile
import unittest

from codie.cards.scryfall_bulk_snapshots import (
    SCRYFALL_BULK_SNAPSHOT_VERSION,
    ScryfallBulkFileRef,
    ScryfallBulkSnapshotError,
    build_scryfall_bulk_snapshot_manifest,
    load_scryfall_bulk_snapshot_fixture,
    scryfall_bulk_snapshot_manifest_to_dict,
    validate_scryfall_bulk_snapshot_manifest,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "scryfall"


class ScryfallBulkSnapshotsTest(unittest.TestCase):
    def test_loads_valid_fixture_and_preserves_snapshot_fields(self) -> None:
        report = load_scryfall_bulk_snapshot_fixture(
            FIXTURE_DIR / "default_cards_snapshot.json",
            snapshot_id="fixture-default-cards-2026-06-21",
            imported_at="2026-07-11T00:00:00+00:00",
        )

        self.assertTrue(report.is_valid)
        self.assertEqual(report.validation_errors, ())
        self.assertEqual(report.manifest.snapshot_version, SCRYFALL_BULK_SNAPSHOT_VERSION)
        self.assertEqual(report.manifest.bulk_type, "default_cards")
        self.assertEqual(report.manifest.source_uri, "fixture://scryfall/default_cards_snapshot.json")
        self.assertEqual(report.manifest.generated_at, "2026-06-21T00:00:00+00:00")
        self.assertEqual(report.manifest.imported_at, "2026-07-11T00:00:00+00:00")
        self.assertEqual(report.manifest.card_count, 3)
        self.assertRegex(report.manifest.content_hash, r"^[0-9a-f]{64}$")
        self.assertEqual(report.manifest.file_refs[0].filename, "default_cards_snapshot.json")

    def test_manifest_serializes_deterministically_and_round_trips_through_dict(self) -> None:
        manifest = build_scryfall_bulk_snapshot_manifest(
            snapshot_id="snapshot-1",
            bulk_type="default_cards",
            source_uri="fixture://snapshot",
            generated_at="2026-06-21T00:00:00+00:00",
            imported_at="2026-07-11T00:00:00+00:00",
            file_refs=(
                ScryfallBulkFileRef(
                    filename="default_cards_snapshot.json",
                    content_hash="a" * 64,
                    card_count=1,
                    source_uri="fixture://snapshot",
                ),
            ),
            raw_metadata={"z": {"b": 2, "a": 1}, "a": ["kept"]},
            cards=[{"id": "00000000-0000-0000-0000-000000000001", "name": "A Card"}],
        )

        first = scryfall_bulk_snapshot_manifest_to_dict(manifest)
        second = scryfall_bulk_snapshot_manifest_to_dict(manifest)
        self.assertEqual(first, second)
        encoded = json.dumps(first, sort_keys=True)
        decoded = json.loads(encoded)
        rebuilt = build_scryfall_bulk_snapshot_manifest(
            snapshot_id=decoded["snapshot_id"],
            bulk_type=decoded["bulk_type"],
            source_uri=decoded["source_uri"],
            generated_at=decoded["generated_at"],
            imported_at=decoded["imported_at"],
            content_hash=decoded["content_hash"],
            card_count=decoded["card_count"],
            schema_version=decoded["schema_version"],
            file_refs=tuple(
                ScryfallBulkFileRef(
                    filename=file_ref["filename"],
                    content_hash=file_ref["content_hash"],
                    card_count=file_ref["card_count"],
                    source_uri=file_ref["source_uri"],
                )
                for file_ref in decoded["file_refs"]
            ),
            raw_metadata=decoded["raw_metadata"],
        )
        self.assertEqual(scryfall_bulk_snapshot_manifest_to_dict(rebuilt), first)
        self.assertEqual(first["raw_metadata"], {"a": ["kept"], "z": {"a": 1, "b": 2}})

    def test_manifest_value_object_is_frozen_and_builder_does_not_mutate_metadata(self) -> None:
        metadata = {"nested": {"kept": True}}
        manifest = build_scryfall_bulk_snapshot_manifest(
            snapshot_id="snapshot-immutable",
            bulk_type="default_cards",
            raw_metadata=metadata,
            cards=[],
        )
        metadata["nested"]["kept"] = False

        with self.assertRaises(FrozenInstanceError):
            manifest.card_count = 99  # type: ignore[misc]
        self.assertEqual(scryfall_bulk_snapshot_manifest_to_dict(manifest)["raw_metadata"]["nested"]["kept"], True)

    def test_content_hash_is_stable_and_changes_with_payload(self) -> None:
        first = build_scryfall_bulk_snapshot_manifest(
            snapshot_id="snapshot-a",
            bulk_type="default_cards",
            cards=[{"name": "A Card", "id": "00000000-0000-0000-0000-000000000001"}],
        )
        same = build_scryfall_bulk_snapshot_manifest(
            snapshot_id="snapshot-a",
            bulk_type="default_cards",
            cards=[{"id": "00000000-0000-0000-0000-000000000001", "name": "A Card"}],
        )
        changed = build_scryfall_bulk_snapshot_manifest(
            snapshot_id="snapshot-a",
            bulk_type="default_cards",
            cards=[{"id": "00000000-0000-0000-0000-000000000001", "name": "Different Card"}],
        )

        self.assertEqual(first.content_hash, same.content_hash)
        self.assertNotEqual(first.content_hash, changed.content_hash)

    def test_preserves_optional_scryfall_fields_and_raw_card_payload(self) -> None:
        report = load_scryfall_bulk_snapshot_fixture(FIXTURE_DIR / "default_cards_snapshot.json")
        cards = [dict(card) for card in report.raw_cards]
        self.assertEqual(cards[0]["oracle_id"], "11111111-1111-1111-1111-111111111111")
        self.assertEqual(cards[0]["released_at"], "2016-11-11")
        self.assertEqual(cards[0]["legalities"], {"commander": "legal"})
        self.assertEqual(cards[1]["card_faces"][1]["name"], "Bala Ged Sanctuary")
        self.assertEqual(cards[1]["produced_mana"], ("G",))
        self.assertNotIn("oracle_id", cards[2])

    def test_malformed_json_fails_cleanly(self) -> None:
        with self.assertRaises(ScryfallBulkSnapshotError):
            load_scryfall_bulk_snapshot_fixture(FIXTURE_DIR / "malformed_bulk_snapshot.json")

    def test_missing_scryfall_id_and_missing_name_fail_cleanly(self) -> None:
        manifest = build_scryfall_bulk_snapshot_manifest(
            snapshot_id="snapshot-errors",
            bulk_type="default_cards",
            cards=[{"name": "No ID"}, {"id": "00000000-0000-0000-0000-000000000002"}],
        )
        report = validate_scryfall_bulk_snapshot_manifest(
            manifest,
            cards=[{"name": "No ID"}, {"id": "00000000-0000-0000-0000-000000000002"}],
        )

        self.assertFalse(report.is_valid)
        self.assertIn("card[0] missing required Scryfall id", report.validation_errors)
        self.assertIn("card[1] missing required name", report.validation_errors)

    def test_fixture_loading_is_local_only_and_supports_object_shape(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "snapshot.json"
            path.write_text(
                json.dumps(
                    {
                        "bulk_type": "oracle_cards",
                        "source_uri": "fixture://local",
                        "cards": [
                            {
                                "scryfall_id": "00000000-0000-0000-0000-000000000001",
                                "name": "Local Card",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            report = load_scryfall_bulk_snapshot_fixture(path)

        self.assertTrue(report.is_valid)
        self.assertEqual(report.manifest.bulk_type, "oracle_cards")
        self.assertEqual(report.manifest.raw_metadata["source_uri"], "fixture://local")

    def test_explicit_bulk_type_overrides_fixture_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "snapshot.json"
            path.write_text(
                json.dumps(
                    {
                        "bulk_type": "oracle_cards",
                        "cards": [
                            {
                                "scryfall_id": "00000000-0000-0000-0000-000000000001",
                                "name": "Local Card",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            report = load_scryfall_bulk_snapshot_fixture(path, bulk_type="default_cards")

        self.assertTrue(report.is_valid)
        self.assertEqual(report.manifest.bulk_type, "default_cards")

    def test_hash_and_card_count_validation_mismatches_are_visible(self) -> None:
        manifest = build_scryfall_bulk_snapshot_manifest(
            snapshot_id="snapshot-mismatch",
            bulk_type="default_cards",
            content_hash="0" * 64,
            card_count=5,
        )
        report = validate_scryfall_bulk_snapshot_manifest(
            manifest,
            cards=[
                {
                    "id": "00000000-0000-0000-0000-000000000001",
                    "name": "A Card",
                }
            ],
        )

        self.assertFalse(report.is_valid)
        self.assertIn("manifest content_hash does not match card payload", report.validation_errors)
        self.assertIn("manifest card_count does not match card payload", report.validation_errors)

    def test_no_live_network_or_sqlite_imports_in_module(self) -> None:
        module_text = (Path(__file__).parents[1] / "codie" / "cards" / "scryfall_bulk_snapshots.py").read_text(
            encoding="utf-8"
        )
        for forbidden in ("requests", "httpx", "sqlite3", "codie.db", "repositories", "recommendations"):
            self.assertNotIn(forbidden, module_text)


if __name__ == "__main__":
    unittest.main()
