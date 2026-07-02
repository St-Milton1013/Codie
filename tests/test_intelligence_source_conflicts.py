from __future__ import annotations

import json
import unittest
from pathlib import Path

from codie.intelligence import (
    SourceConflictBuildError,
    SourceConflictEvidenceRef,
    SourceConflictItem,
    SourceConflictReport,
    SourceConflictReportOptions,
    source_conflict_report_to_dict,
    source_conflict_report_to_input_records,
)


GENERATED_AT = "2026-07-01T00:00:00+00:00"


def evidence_ref(**overrides) -> SourceConflictEvidenceRef:
    data = {
        "evidence_id": "evidence:b",
        "source_type": "analytics",
        "source_name": "canonical metrics",
        "source_record_id": "analytics:1",
        "source_url": None,
        "observed_at": GENERATED_AT,
        "field_name": "commander_signature",
        "field_value": "Tymna the Weaver|Kraum, Ludevic's Opus",
        "privacy_scope": "public",
        "metadata": {"source": "canonical"},
    }
    data.update(overrides)
    return SourceConflictEvidenceRef(**data)


def conflict(**overrides) -> SourceConflictItem:
    data = {
        "conflict_id": "conflict-b",
        "conflict_type": "identity_mismatch",
        "summary": "Two sanitized evidence records disagree on commander identity.",
        "severity": "warning",
        "resolution_status": "unresolved",
        "evidence_refs": (
            evidence_ref(evidence_id="evidence:b"),
            evidence_ref(evidence_id="evidence:a", source_record_id="analytics:2", field_value="Tymna the Weaver"),
        ),
        "caveats": (),
        "metadata": {"field_names": ["commander_signature"]},
    }
    data.update(overrides)
    return SourceConflictItem(**data)


def report(**overrides) -> SourceConflictReport:
    data = {
        "report_id": "source-conflict-report:1",
        "subject_type": "commander",
        "subject_id": "tymna-kraum",
        "generated_at": GENERATED_AT,
        "conflicts": (conflict(),),
        "metadata": {"scope": "input-assembly"},
    }
    data.update(overrides)
    return SourceConflictReport(**data)


class IntelligenceSourceConflictsTest(unittest.TestCase):
    def test_valid_conflict_report_serializes_deterministically(self) -> None:
        payload = source_conflict_report_to_dict(
            report(
                conflicts=(
                    conflict(conflict_id="conflict:b"),
                    conflict(conflict_id="conflict:a"),
                )
            )
        )

        self.assertEqual([item["conflict_id"] for item in payload["conflicts"]], ["conflict:a", "conflict:b"])
        self.assertEqual(
            [item["evidence_id"] for item in payload["conflicts"][0]["evidence_refs"]],
            ["evidence:a", "evidence:b"],
        )
        json.dumps(payload, sort_keys=True)

    def test_valid_conflict_report_converts_to_input_records(self) -> None:
        records = source_conflict_report_to_input_records(report())

        self.assertEqual(records[0].record_type, "source_conflict")
        self.assertEqual(records[0].references[0].source_type, "analytics")

    def test_conflict_metadata_is_preserved(self) -> None:
        records = source_conflict_report_to_input_records(report())
        metadata = records[0].metadata

        self.assertEqual(metadata["conflict_type"], "identity_mismatch")
        self.assertEqual(metadata["severity"], "warning")
        self.assertEqual(metadata["resolution_status"], "unresolved")

    def test_blocking_conflicts_are_preserved(self) -> None:
        records = source_conflict_report_to_input_records(report(conflicts=(conflict(severity="blocking"),)))

        self.assertEqual(records[0].metadata["severity"], "blocking")
        self.assertEqual(records[0].confidence, 1.0)

    def test_resolved_conflicts_excluded_by_default(self) -> None:
        open_conflict = conflict(conflict_id="open")
        resolved_conflict = conflict(conflict_id="resolved", resolution_status="resolved_externally")

        records = source_conflict_report_to_input_records(report(conflicts=(open_conflict, resolved_conflict)))

        self.assertEqual([item.record_id for item in records], ["source-conflict:open", "source-conflict-filtered:source-conflict-report:1"])

    def test_resolved_conflicts_included_only_with_option(self) -> None:
        resolved_conflict = conflict(conflict_id="resolved", resolution_status="resolved_externally")

        records = source_conflict_report_to_input_records(
            report(conflicts=(resolved_conflict,)),
            SourceConflictReportOptions(include_resolved=True),
        )

        self.assertEqual(records[0].record_id, "source-conflict:resolved")

    def test_sensitive_evidence_excluded_by_default(self) -> None:
        public_ref = evidence_ref(evidence_id="public")
        sensitive_ref = evidence_ref(evidence_id="sensitive", privacy_scope="sensitive")

        records = source_conflict_report_to_input_records(
            report(conflicts=(conflict(evidence_refs=(public_ref, sensitive_ref)),))
        )

        self.assertEqual([item.source_record_id for item in records[0].references], ["analytics:1"])
        self.assertEqual(records[0].caveats[0]["metadata"]["filtered_evidence_ids"], ["sensitive"])

    def test_sensitive_evidence_included_only_with_option(self) -> None:
        sensitive_ref = evidence_ref(evidence_id="sensitive", privacy_scope="sensitive")

        records = source_conflict_report_to_input_records(
            report(conflicts=(conflict(evidence_refs=(sensitive_ref,)),)),
            SourceConflictReportOptions(include_sensitive=True),
        )

        self.assertEqual(records[0].privacy_scope, "sensitive")

    def test_duplicate_conflict_ids_fail_cleanly(self) -> None:
        with self.assertRaises(SourceConflictBuildError):
            report(conflicts=(conflict(conflict_id="duplicate"), conflict(conflict_id="duplicate")))

    def test_unsupported_conflict_type_fails_cleanly(self) -> None:
        with self.assertRaises(SourceConflictBuildError):
            conflict(conflict_type="unsupported")

    def test_unsupported_severity_fails_cleanly(self) -> None:
        with self.assertRaises(SourceConflictBuildError):
            conflict(severity="unsupported")

    def test_unsupported_resolution_status_fails_cleanly(self) -> None:
        with self.assertRaises(SourceConflictBuildError):
            conflict(resolution_status="unsupported")

    def test_conflict_missing_evidence_refs_fails_cleanly(self) -> None:
        with self.assertRaises(SourceConflictBuildError):
            conflict(evidence_refs=())

    def test_evidence_ref_missing_required_fields_fails_cleanly(self) -> None:
        with self.assertRaises(SourceConflictBuildError):
            evidence_ref(source_name="")
        with self.assertRaises(SourceConflictBuildError):
            evidence_ref(observed_at="")
        with self.assertRaises(SourceConflictBuildError):
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
                with self.assertRaises(SourceConflictBuildError):
                    evidence_ref(metadata={blocked_key: "secret"})
                with self.assertRaises(SourceConflictBuildError):
                    conflict(metadata={blocked_key: "secret"})
                with self.assertRaises(SourceConflictBuildError):
                    report(metadata={blocked_key: "secret"})

    def test_nested_private_metadata_keys_fail_cleanly(self) -> None:
        with self.assertRaises(SourceConflictBuildError):
            conflict(metadata={"safe": [{"private-deck-text": "secret"}]})

    def test_forbidden_strategic_language_fails_cleanly(self) -> None:
        with self.assertRaises(SourceConflictBuildError):
            conflict(summary="This card should be " + "played.")

    def test_conversion_emits_source_conflict_record_type(self) -> None:
        records = source_conflict_report_to_input_records(report())

        self.assertEqual(records[0].record_type, "source_conflict")

    def test_filtered_report_with_no_remaining_conflicts_fails_cleanly(self) -> None:
        with self.assertRaises(SourceConflictBuildError):
            source_conflict_report_to_input_records(
                report(conflicts=(conflict(resolution_status="resolved_externally"),))
            )

    def test_minimum_severity_filters_lower_severity_conflicts(self) -> None:
        info_conflict = conflict(conflict_id="info", severity="info")
        warning_conflict = conflict(conflict_id="warning", severity="warning")

        records = source_conflict_report_to_input_records(
            report(conflicts=(info_conflict, warning_conflict)),
            SourceConflictReportOptions(minimum_severity="warning"),
        )

        self.assertEqual(records[0].record_id, "source-conflict:warning")
        self.assertEqual(records[1].metadata["filtered_conflict_ids"], ["info"])

    def test_module_has_no_forbidden_imports_raw_sql_or_file_writes(self) -> None:
        import codie.intelligence.source_conflicts as source_conflicts_module

        source = Path(source_conflicts_module.__file__).read_text(encoding="utf-8")
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
