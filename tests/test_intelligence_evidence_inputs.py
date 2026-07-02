from __future__ import annotations

import unittest
from pathlib import Path

from codie.intelligence import (
    EvidenceGraphAssemblyOptions,
    EvidenceInputBuildError,
    EvidenceInputBundle,
    EvidenceInputRecord,
    EvidenceRecordRef,
    build_graph_input_from_records,
    build_evidence_graph,
    evidence_graph_to_dict,
    evidence_record_from_dict,
)


GENERATED_AT = "2026-07-01T00:00:00+00:00"


def ref(**overrides) -> EvidenceRecordRef:
    data = {
        "source_type": "analytics",
        "source_name": "canonical card performance metrics",
        "source_record_id": "card_performance_metrics:oracle-remora:30d",
        "source_url": None,
        "observed_at": GENERATED_AT,
    }
    data.update(overrides)
    return EvidenceRecordRef(**data)


def record(**overrides) -> EvidenceInputRecord:
    data = {
        "record_id": "record-remora",
        "record_type": "recommendation_candidate",
        "label": "Mystic Remora",
        "summary": "Card appeared in 12 of 40 comparable canonical decks.",
        "confidence": 0.8,
        "privacy_scope": "public",
        "references": (ref(),),
        "caveats": (),
        "metadata": {"oracle_id": "oracle-remora"},
    }
    data.update(overrides)
    return EvidenceInputRecord(**data)


def bundle(**overrides) -> EvidenceInputBundle:
    data = {
        "bundle_id": "graph:oracle-remora",
        "claim_type": "card_evidence",
        "claim_text": "Mystic Remora has observed evidence.",
        "subject_type": "card",
        "subject_id": "oracle-remora",
        "generated_at": GENERATED_AT,
        "records": (record(),),
        "bundle_caveats": (),
        "metadata": {"scope": "30d"},
    }
    data.update(overrides)
    return EvidenceInputBundle(**data)


class IntelligenceEvidenceInputsTest(unittest.TestCase):
    def test_valid_input_bundle_builds_evidence_graph_input(self) -> None:
        graph_input = build_graph_input_from_records(bundle())
        graph = build_evidence_graph(graph_input)
        payload = evidence_graph_to_dict(graph)

        self.assertEqual(payload["graph_id"], "graph:oracle-remora")
        self.assertEqual(payload["nodes"][0]["node_type"], "card")
        self.assertEqual(payload["nodes"][0]["citations"][0]["source_type"], "analytics")
        self.assertEqual(payload["edges"], [])

    def test_record_type_maps_to_expected_node_type(self) -> None:
        expected = {
            "recommendation_candidate": "card",
            "innovation_signal": "innovation_signal",
            "combo_evidence": "combo_evidence",
            "primer_metadata": "primer_metadata",
            "simulation_review_summary": "simulation_result",
            "deck_memory_summary": "user_deck_memory",
            "saved_analysis_summary": "saved_analysis",
            "manual_note": "manual_note",
            "source_conflict": "source_conflict",
            "unsupported_card": "unsupported_card",
        }

        for record_type, node_type in expected.items():
            with self.subTest(record_type=record_type):
                references = () if record_type == "manual_note" else (ref(source_type="manual"),)
                graph_input = build_graph_input_from_records(
                    bundle(records=(record(record_type=record_type, references=references),))
                )
                self.assertEqual(graph_input.nodes[0].node_type, node_type)

    def test_evidence_record_from_dict_maps_references(self) -> None:
        parsed = evidence_record_from_dict(
            {
                "record_id": "record-dict",
                "record_type": "innovation_signal",
                "label": "Example card",
                "summary": "Card appeared in the selected recent evidence window.",
                "confidence": 0.5,
                "privacy_scope": "public",
                "references": [
                    {
                        "source_type": "innovation_snapshot",
                        "source_name": "innovation snapshot",
                        "source_record_id": "innovation:1",
                        "source_url": None,
                        "observed_at": GENERATED_AT,
                    }
                ],
                "metadata": {"window": "30d"},
            }
        )

        self.assertEqual(parsed.references[0].source_type, "innovation_snapshot")

    def test_manual_note_may_omit_references(self) -> None:
        graph_input = build_graph_input_from_records(
            bundle(records=(record(record_type="manual_note", references=(), metadata={}),))
        )

        self.assertEqual(graph_input.nodes[0].citations, ())

    def test_non_manual_record_requires_reference(self) -> None:
        with self.assertRaises(EvidenceInputBuildError):
            record(references=())

    def test_duplicate_record_ids_fail_cleanly(self) -> None:
        with self.assertRaises(EvidenceInputBuildError):
            bundle(records=(record(record_id="duplicate"), record(record_id="duplicate")))

    def test_unsupported_record_type_fails_cleanly(self) -> None:
        with self.assertRaises(EvidenceInputBuildError):
            record(record_type="unsupported")

    def test_invalid_confidence_fails_cleanly(self) -> None:
        with self.assertRaises(EvidenceInputBuildError):
            record(confidence=1.1)
        with self.assertRaises(EvidenceInputBuildError):
            EvidenceGraphAssemblyOptions(minimum_confidence=-0.1)

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
                with self.assertRaises(EvidenceInputBuildError):
                    record(metadata={blocked_key: "1 Example Card"})
                with self.assertRaises(EvidenceInputBuildError):
                    bundle(metadata={blocked_key: "1 Example Card"})

    def test_nested_private_metadata_keys_fail_cleanly(self) -> None:
        with self.assertRaises(EvidenceInputBuildError):
            record(metadata={"safe": [{"private-deck-text": "1 Example Card"}]})

    def test_sensitive_records_excluded_by_default(self) -> None:
        public_record = record(record_id="public")
        sensitive_record = record(record_id="sensitive", privacy_scope="sensitive")

        graph_input = build_graph_input_from_records(bundle(records=(public_record, sensitive_record)))

        self.assertEqual([node.node_id for node in graph_input.nodes], ["node:public"])
        self.assertEqual(graph_input.caveats[0].caveat_type, "privacy_redaction")

    def test_sensitive_records_included_only_with_option(self) -> None:
        sensitive_record = record(record_id="sensitive", privacy_scope="sensitive")

        graph_input = build_graph_input_from_records(
            bundle(records=(sensitive_record,)),
            EvidenceGraphAssemblyOptions(include_sensitive=True),
        )

        self.assertEqual(graph_input.nodes[0].privacy_scope, "sensitive")

    def test_local_user_data_privacy_scope_is_preserved(self) -> None:
        local_record = record(
            record_id="deck-memory",
            record_type="deck_memory_summary",
            privacy_scope="local_user_data",
            references=(ref(source_type="deck_memory", source_record_id="user_decks:1"),),
        )

        graph_input = build_graph_input_from_records(bundle(records=(local_record,)))

        self.assertEqual(graph_input.nodes[0].privacy_scope, "local_user_data")

    def test_minimum_confidence_filters_low_confidence_records(self) -> None:
        high = record(record_id="high", confidence=0.9)
        low = record(record_id="low", confidence=0.2)

        graph_input = build_graph_input_from_records(
            bundle(records=(high, low)),
            EvidenceGraphAssemblyOptions(minimum_confidence=0.5),
        )

        self.assertEqual([node.node_id for node in graph_input.nodes], ["node:high"])
        self.assertEqual(graph_input.caveats[0].metadata["filtered_record_ids"], ["low"])

    def test_filtered_records_create_caveats_when_interpretation_changes(self) -> None:
        manual = record(record_id="manual", record_type="manual_note", references=(), metadata={})
        kept = record(record_id="kept")

        graph_input = build_graph_input_from_records(
            bundle(records=(kept, manual)),
            EvidenceGraphAssemblyOptions(include_manual_notes=False),
        )

        self.assertEqual(graph_input.caveats[0].caveat_id, "caveat:filtered-records")
        self.assertEqual(graph_input.caveats[0].metadata["filtered_count"], 1)

    def test_filtered_bundle_with_no_remaining_records_fails_cleanly(self) -> None:
        with self.assertRaises(EvidenceInputBuildError):
            build_graph_input_from_records(
                bundle(records=(record(privacy_scope="sensitive"),)),
                EvidenceGraphAssemblyOptions(),
            )

    def test_bundle_and_record_caveats_are_preserved(self) -> None:
        graph_input = build_graph_input_from_records(
            bundle(
                records=(
                    record(
                        record_id="with-caveat",
                        caveats=(
                            {
                                "caveat_type": "low_sample",
                                "message": "The selected scope has limited data.",
                                "severity": "warning",
                            },
                        ),
                    ),
                ),
                bundle_caveats=(
                    {
                        "caveat_id": "caveat:bundle",
                        "caveat_type": "missing_data",
                        "message": "Some sources are missing data.",
                        "severity": "info",
                    },
                ),
            )
        )

        self.assertEqual([item.caveat_type for item in graph_input.caveats], ["missing_data", "low_sample"])
        self.assertEqual(graph_input.caveats[1].related_node_ids, ("node:with-caveat",))

    def test_forbidden_strategic_language_fails_cleanly(self) -> None:
        with self.assertRaises(EvidenceInputBuildError):
            record(summary="This card should be " + "played.")

    def test_module_has_no_forbidden_imports_raw_sql_or_file_writes(self) -> None:
        import codie.intelligence.evidence_inputs as evidence_inputs_module

        source = Path(evidence_inputs_module.__file__).read_text(encoding="utf-8")
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
