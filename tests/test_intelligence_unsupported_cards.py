from __future__ import annotations

import json
import unittest
from pathlib import Path

from codie.intelligence import (
    UnsupportedCardEvidenceRef,
    UnsupportedCardQueue,
    UnsupportedCardQueueBuildError,
    UnsupportedCardQueueItem,
    UnsupportedCardQueueOptions,
    unsupported_card_queue_to_dict,
    unsupported_card_queue_to_input_records,
)


GENERATED_AT = "2026-07-02T00:00:00+00:00"


def evidence_ref(**overrides) -> UnsupportedCardEvidenceRef:
    data = {
        "evidence_id": "evidence:b",
        "source_type": "simulation",
        "source_name": "Challenge line review",
        "source_record_id": "review:1",
        "source_url": None,
        "observed_at": GENERATED_AT,
        "card_name": "Thundertrap Trainer",
        "oracle_id": "oracle-thundertrap",
        "scryfall_id": "scryfall-thundertrap",
        "context": {"action_type": "cast"},
        "privacy_scope": "public",
        "metadata": {"source": "line-review"},
    }
    data.update(overrides)
    return UnsupportedCardEvidenceRef(**data)


def item(**overrides) -> UnsupportedCardQueueItem:
    data = {
        "item_id": "item-b",
        "card_name": "Thundertrap Trainer",
        "oracle_id": "oracle-thundertrap",
        "scryfall_id": "scryfall-thundertrap",
        "reason": "simulator_unsupported",
        "severity": "warning",
        "status": "open",
        "evidence_refs": (
            evidence_ref(evidence_id="evidence:b"),
            evidence_ref(evidence_id="evidence:a", source_record_id="review:2"),
        ),
        "first_seen_at": "2026-07-01T00:00:00+00:00",
        "last_seen_at": GENERATED_AT,
        "caveats": (),
        "metadata": {"component": "mana-model"},
    }
    data.update(overrides)
    return UnsupportedCardQueueItem(**data)


def queue(**overrides) -> UnsupportedCardQueue:
    data = {
        "queue_id": "unsupported-card-queue:1",
        "subject_type": "deck",
        "subject_id": "deck-hash-1",
        "generated_at": GENERATED_AT,
        "items": (item(),),
        "metadata": {"scope": "interactive-intelligence"},
    }
    data.update(overrides)
    return UnsupportedCardQueue(**data)


class IntelligenceUnsupportedCardsTest(unittest.TestCase):
    def test_valid_queue_serializes_deterministically(self) -> None:
        payload = unsupported_card_queue_to_dict(
            queue(
                items=(
                    item(item_id="item:b"),
                    item(item_id="item:a"),
                )
            )
        )

        self.assertEqual([record["item_id"] for record in payload["items"]], ["item:a", "item:b"])
        self.assertEqual(
            [ref["evidence_id"] for ref in payload["items"][0]["evidence_refs"]],
            ["evidence:a", "evidence:b"],
        )
        json.dumps(payload, sort_keys=True)

    def test_valid_queue_converts_to_input_records(self) -> None:
        records = unsupported_card_queue_to_input_records(queue())

        self.assertEqual(records[0].record_type, "unsupported_card")
        self.assertEqual(records[0].references[0].source_type, "simulation")

    def test_item_metadata_is_preserved(self) -> None:
        records = unsupported_card_queue_to_input_records(queue())
        metadata = records[0].metadata

        self.assertEqual(metadata["reason"], "simulator_unsupported")
        self.assertEqual(metadata["severity"], "warning")
        self.assertEqual(metadata["status"], "open")
        self.assertEqual(metadata["card_name"], "Thundertrap Trainer")
        self.assertEqual(metadata["oracle_id"], "oracle-thundertrap")
        self.assertEqual(metadata["scryfall_id"], "scryfall-thundertrap")

    def test_blocking_items_are_preserved(self) -> None:
        records = unsupported_card_queue_to_input_records(queue(items=(item(severity="blocking"),)))

        self.assertEqual(records[0].metadata["severity"], "blocking")
        self.assertEqual(records[0].confidence, 1.0)

    def test_resolved_items_excluded_by_default(self) -> None:
        open_item = item(item_id="open")
        resolved_item = item(item_id="resolved", status="resolved")

        records = unsupported_card_queue_to_input_records(queue(items=(open_item, resolved_item)))

        self.assertEqual([record.record_id for record in records], ["unsupported-card:open", "unsupported-card-filtered:unsupported-card-queue:1"])

    def test_ignored_by_policy_items_use_same_inactive_filter(self) -> None:
        open_item = item(item_id="open")
        ignored_item = item(item_id="ignored", status="ignored_by_policy")

        records = unsupported_card_queue_to_input_records(queue(items=(open_item, ignored_item)))

        self.assertEqual([record.record_id for record in records], ["unsupported-card:open", "unsupported-card-filtered:unsupported-card-queue:1"])
        self.assertEqual(records[1].metadata["filtered_item_ids"], ["ignored"])

    def test_resolved_items_included_only_with_option(self) -> None:
        resolved_item = item(item_id="resolved", status="resolved")

        records = unsupported_card_queue_to_input_records(
            queue(items=(resolved_item,)),
            UnsupportedCardQueueOptions(include_resolved=True),
        )

        self.assertEqual(records[0].record_id, "unsupported-card:resolved")

    def test_sensitive_evidence_excluded_by_default(self) -> None:
        public_ref = evidence_ref(evidence_id="public")
        sensitive_ref = evidence_ref(evidence_id="sensitive", privacy_scope="sensitive")

        records = unsupported_card_queue_to_input_records(queue(items=(item(evidence_refs=(public_ref, sensitive_ref)),)))

        self.assertEqual([ref.source_record_id for ref in records[0].references], ["review:1"])
        self.assertEqual(records[0].caveats[0]["metadata"]["filtered_evidence_ids"], ["sensitive"])

    def test_sensitive_evidence_included_only_with_option(self) -> None:
        sensitive_ref = evidence_ref(evidence_id="sensitive", privacy_scope="sensitive")

        records = unsupported_card_queue_to_input_records(
            queue(items=(item(evidence_refs=(sensitive_ref,)),)),
            UnsupportedCardQueueOptions(include_sensitive=True),
        )

        self.assertEqual(records[0].privacy_scope, "sensitive")

    def test_minimum_severity_filters_lower_severity_items(self) -> None:
        info_item = item(item_id="info", severity="info")
        warning_item = item(item_id="warning", severity="warning")

        records = unsupported_card_queue_to_input_records(
            queue(items=(info_item, warning_item)),
            UnsupportedCardQueueOptions(minimum_severity="warning"),
        )

        self.assertEqual(records[0].record_id, "unsupported-card:warning")
        self.assertEqual(records[1].metadata["filtered_item_ids"], ["info"])

    def test_deduplicates_by_card_identity_by_default(self) -> None:
        first = item(item_id="first", scryfall_id="same-card")
        second = item(item_id="second", scryfall_id="same-card")

        records = unsupported_card_queue_to_input_records(queue(items=(first, second)))

        self.assertEqual(records[0].record_id, "unsupported-card:first")
        self.assertEqual(records[1].metadata["deduplicated_item_ids"], ["second"])

    def test_deduplication_can_be_disabled(self) -> None:
        first = item(item_id="first", scryfall_id="same-card")
        second = item(item_id="second", scryfall_id="same-card")

        records = unsupported_card_queue_to_input_records(
            queue(items=(first, second)),
            UnsupportedCardQueueOptions(deduplicate_by="none"),
        )

        self.assertEqual([record.record_id for record in records], ["unsupported-card:first", "unsupported-card:second"])

    def test_duplicate_item_ids_fail_cleanly(self) -> None:
        with self.assertRaises(UnsupportedCardQueueBuildError):
            queue(items=(item(item_id="duplicate"), item(item_id="duplicate")))

    def test_unsupported_reason_fails_cleanly(self) -> None:
        with self.assertRaises(UnsupportedCardQueueBuildError):
            item(reason="unsupported")

    def test_unsupported_severity_fails_cleanly(self) -> None:
        with self.assertRaises(UnsupportedCardQueueBuildError):
            item(severity="unsupported")

    def test_unsupported_status_fails_cleanly(self) -> None:
        with self.assertRaises(UnsupportedCardQueueBuildError):
            item(status="unsupported")

    def test_item_missing_evidence_refs_fails_cleanly(self) -> None:
        with self.assertRaises(UnsupportedCardQueueBuildError):
            item(evidence_refs=())

    def test_evidence_ref_missing_required_fields_fails_cleanly(self) -> None:
        with self.assertRaises(UnsupportedCardQueueBuildError):
            evidence_ref(source_name="")
        with self.assertRaises(UnsupportedCardQueueBuildError):
            evidence_ref(observed_at="")
        with self.assertRaises(UnsupportedCardQueueBuildError):
            evidence_ref(card_name="")
        with self.assertRaises(UnsupportedCardQueueBuildError):
            evidence_ref(source_record_id=None, source_url=None)

    def test_private_metadata_keys_fail_cleanly(self) -> None:
        blocked_keys = (
            "raw_input",
            "private_deck_text",
            "full_primer_body",
            "raw_" + "provider_payload",
            "provider_payload",
            "original_import_text",
        )
        for blocked_key in blocked_keys:
            with self.subTest(blocked_key=blocked_key):
                with self.assertRaises(UnsupportedCardQueueBuildError):
                    evidence_ref(metadata={blocked_key: "secret"})
                with self.assertRaises(UnsupportedCardQueueBuildError):
                    evidence_ref(context={blocked_key: "secret"})
                with self.assertRaises(UnsupportedCardQueueBuildError):
                    item(metadata={blocked_key: "secret"})
                with self.assertRaises(UnsupportedCardQueueBuildError):
                    queue(metadata={blocked_key: "secret"})

    def test_nested_private_metadata_keys_fail_cleanly(self) -> None:
        with self.assertRaises(UnsupportedCardQueueBuildError):
            item(metadata={"safe": [{"private-deck-text": "secret"}]})

    def test_forbidden_strategic_language_fails_cleanly(self) -> None:
        with self.assertRaises(UnsupportedCardQueueBuildError):
            item(card_name="This card should be " + "played.")

    def test_conversion_emits_unsupported_card_record_type(self) -> None:
        records = unsupported_card_queue_to_input_records(queue())

        self.assertEqual(records[0].record_type, "unsupported_card")

    def test_filtered_queue_with_no_remaining_items_fails_cleanly(self) -> None:
        with self.assertRaises(UnsupportedCardQueueBuildError):
            unsupported_card_queue_to_input_records(queue(items=(item(status="resolved"),)))

    def test_module_has_no_forbidden_imports_raw_sql_or_file_writes(self) -> None:
        import codie.intelligence.unsupported_cards as unsupported_cards_module

        source = Path(unsupported_cards_module.__file__).read_text(encoding="utf-8")
        forbidden = (
            "codie." + "db",
            "codie." + "providers",
            "codie." + "analytics",
            "codie." + "recommendations.generation",
            "codie." + "recommendations.persistence",
            "codie." + "ingestion",
            "codie." + "cards",
            "codie." + "probability_engine",
            "codie." + "canonical",
            "req" + "uests",
            "ht" + "tpx",
            "sqlite" + "3",
            "SEL" + "ECT ",
            "INS" + "ERT ",
            "UPD" + "ATE ",
            "DEL" + "ETE ",
            "exec" + "ute(",
            "execute" + "script(",
            "open(",
            "write_text(",
            "write_bytes(",
            "Path(",
            "mkdir(",
            "touch(",
            "unlink(",
        )
        for pattern in forbidden:
            self.assertNotIn(pattern, source)


if __name__ == "__main__":
    unittest.main()
