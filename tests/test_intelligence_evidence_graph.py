from __future__ import annotations

import json
import unittest
from pathlib import Path

from codie.intelligence import (
    EvidenceCaveat,
    EvidenceCitation,
    EvidenceEdge,
    EvidenceGraphBuildError,
    EvidenceGraphInput,
    EvidenceNode,
    build_evidence_graph,
    evidence_graph_to_dict,
)


GENERATED_AT = "2026-07-01T00:00:00+00:00"


def citation(**overrides) -> EvidenceCitation:
    data = {
        "citation_id": "citation:b",
        "source_type": "analytics",
        "source_name": "canonical card performance metrics",
        "source_record_id": "card_performance_metrics:oracle-remora:90d",
        "source_url": None,
        "observed_at": GENERATED_AT,
    }
    data.update(overrides)
    return EvidenceCitation(**data)


def node(**overrides) -> EvidenceNode:
    data = {
        "node_id": "node:b",
        "node_type": "card",
        "label": "Mystic Remora",
        "summary": "Card appeared in 12 of 40 comparable canonical decks.",
        "confidence": 0.8,
        "citations": (citation(),),
        "privacy_scope": "public",
        "metadata": {"oracle_id": "oracle-remora"},
    }
    data.update(overrides)
    return EvidenceNode(**data)


def edge(**overrides) -> EvidenceEdge:
    data = {
        "edge_id": "edge:b",
        "source_node_id": "node:a",
        "target_node_id": "node:b",
        "edge_type": "supports",
        "summary": "The analytics node supports the card evidence claim.",
        "confidence": 0.7,
        "metadata": {"formula": "included_decks / total_decks"},
    }
    data.update(overrides)
    return EvidenceEdge(**data)


def caveat(**overrides) -> EvidenceCaveat:
    data = {
        "caveat_id": "caveat:b",
        "caveat_type": "low_sample",
        "message": "The selected scope has limited data.",
        "severity": "warning",
        "related_node_ids": ("node:b",),
        "metadata": {"sample_size": 12},
    }
    data.update(overrides)
    return EvidenceCaveat(**data)


def graph_input(**overrides) -> EvidenceGraphInput:
    nodes = (
        node(
            node_id="node:b",
            citations=(
                citation(citation_id="citation:b"),
                citation(citation_id="citation:a", source_record_id="card_performance_metrics:oracle-remora:30d"),
            ),
        ),
        node(
            node_id="node:a",
            node_type="tournament_stat",
            label="90-day inclusion",
            summary="Card appeared in 30.0% of comparable canonical decks.",
            metadata={"sample_size": 40},
        ),
    )
    data = {
        "graph_id": "graph:oracle-remora",
        "claim_type": "card_evidence",
        "claim_text": "Mystic Remora has observed inclusion evidence.",
        "subject_type": "card",
        "subject_id": "oracle-remora",
        "generated_at": GENERATED_AT,
        "nodes": nodes,
        "edges": (
            edge(edge_id="edge:b"),
            edge(edge_id="edge:a", summary="The tournament node is linked to the card node."),
        ),
        "caveats": (
            caveat(caveat_id="caveat:b"),
            caveat(caveat_id="caveat:a", caveat_type="missing_data", message="Some sources are missing data."),
        ),
        "metadata": {"scope": "90d", "entity": {"type": "card"}},
    }
    data.update(overrides)
    return EvidenceGraphInput(**data)


class IntelligenceEvidenceGraphTest(unittest.TestCase):
    def test_valid_graph_serializes_deterministically(self) -> None:
        graph = build_evidence_graph(graph_input())
        payload = evidence_graph_to_dict(graph)

        self.assertEqual(payload["graph_id"], "graph:oracle-remora")
        self.assertEqual([item["node_id"] for item in payload["nodes"]], ["node:a", "node:b"])
        self.assertEqual([item["edge_id"] for item in payload["edges"]], ["edge:a", "edge:b"])
        self.assertEqual([item["caveat_id"] for item in payload["caveats"]], ["caveat:a", "caveat:b"])
        self.assertEqual(
            [item["citation_id"] for item in payload["nodes"][1]["citations"]],
            ["citation:a", "citation:b"],
        )
        json.dumps(payload, sort_keys=True)

    def test_duplicate_node_ids_fail_cleanly(self) -> None:
        duplicate_nodes = (node(node_id="node:a"), node(node_id="node:a"))

        with self.assertRaises(EvidenceGraphBuildError):
            build_evidence_graph(graph_input(nodes=duplicate_nodes, edges=(), caveats=()))

    def test_duplicate_edge_ids_fail_cleanly(self) -> None:
        duplicate_edges = (
            edge(edge_id="edge:a"),
            edge(edge_id="edge:a"),
        )

        with self.assertRaises(EvidenceGraphBuildError):
            build_evidence_graph(graph_input(edges=duplicate_edges))

    def test_edge_referencing_missing_node_fails_cleanly(self) -> None:
        with self.assertRaises(EvidenceGraphBuildError):
            build_evidence_graph(graph_input(edges=(edge(source_node_id="missing"),)))

    def test_caveat_referencing_missing_node_fails_cleanly(self) -> None:
        with self.assertRaises(EvidenceGraphBuildError):
            build_evidence_graph(graph_input(caveats=(caveat(related_node_ids=("missing",)),)))

    def test_unsupported_node_type_fails_cleanly(self) -> None:
        with self.assertRaises(EvidenceGraphBuildError):
            node(node_type="unsupported")

    def test_unsupported_edge_type_fails_cleanly(self) -> None:
        with self.assertRaises(EvidenceGraphBuildError):
            edge(edge_type="unsupported")

    def test_unsupported_source_type_fails_cleanly(self) -> None:
        with self.assertRaises(EvidenceGraphBuildError):
            citation(source_type="unsupported")

    def test_unsupported_caveat_type_fails_cleanly(self) -> None:
        with self.assertRaises(EvidenceGraphBuildError):
            caveat(caveat_type="unsupported")

    def test_invalid_confidence_fails_cleanly(self) -> None:
        with self.assertRaises(EvidenceGraphBuildError):
            node(confidence=1.1)
        with self.assertRaises(EvidenceGraphBuildError):
            edge(confidence=-0.1)

    def test_forbidden_strategic_claim_text_fails_cleanly(self) -> None:
        forbidden = (
            "This card should be " + "played.",
            "This card should be " + "cut.",
            "This card is optimal.",
            "This deck must " + "include this package.",
        )
        for claim_text in forbidden:
            with self.subTest(claim_text=claim_text):
                with self.assertRaises(EvidenceGraphBuildError):
                    build_evidence_graph(graph_input(claim_text=claim_text))

    def test_manual_note_may_omit_citation(self) -> None:
        manual = node(
            node_id="node:manual",
            node_type="manual_note",
            label="Manual review note",
            summary="Manual review is required for this evidence.",
            citations=(),
        )
        graph = build_evidence_graph(graph_input(nodes=(manual,), edges=(), caveats=()))

        self.assertEqual(evidence_graph_to_dict(graph)["nodes"][0]["citations"], [])

    def test_non_manual_nodes_require_citation(self) -> None:
        with self.assertRaises(EvidenceGraphBuildError):
            node(citations=())

    def test_raw_input_metadata_is_rejected_by_default(self) -> None:
        blocked_keys = (
            "raw_input",
            "private_deck_text",
            "full_primer_body",
            "raw_provider_payload",
            "provider_payload",
            "original_import_text",
        )
        for blocked_key in blocked_keys:
            with self.subTest(blocked_key=blocked_key):
                with self.assertRaises(EvidenceGraphBuildError):
                    node(metadata={blocked_key: "1 Example Card"})
                with self.assertRaises(EvidenceGraphBuildError):
                    build_evidence_graph(graph_input(metadata={blocked_key: "1 Example Card"}))

    def test_local_user_data_node_is_preserved_with_privacy_scope(self) -> None:
        local_node = node(
            node_id="node:deck-memory",
            node_type="user_deck_memory",
            privacy_scope="local_user_data",
            label="Remembered user deck",
            summary="This node is derived from a saved local deck analysis.",
            citations=(citation(source_type="deck_memory", source_record_id="user_decks:1"),),
        )
        graph = build_evidence_graph(graph_input(nodes=(local_node,), edges=(), caveats=()))

        self.assertEqual(evidence_graph_to_dict(graph)["nodes"][0]["privacy_scope"], "local_user_data")

    def test_blocking_caveat_is_preserved_in_serialized_output(self) -> None:
        graph = build_evidence_graph(
            graph_input(
                caveats=(
                    caveat(
                        caveat_id="caveat:blocking",
                        caveat_type="unsupported_card",
                        severity="blocking",
                        message="Unsupported card behavior blocks this simulation evidence.",
                    ),
                )
            )
        )

        self.assertEqual(evidence_graph_to_dict(graph)["caveats"][0]["severity"], "blocking")

    def test_self_edge_requires_qualifies_type(self) -> None:
        with self.assertRaises(EvidenceGraphBuildError):
            build_evidence_graph(graph_input(edges=(edge(source_node_id="node:a", target_node_id="node:a"),)))

        graph = build_evidence_graph(
            graph_input(
                edges=(
                    edge(
                        source_node_id="node:a",
                        target_node_id="node:a",
                        edge_type="qualifies",
                    ),
                )
            )
        )
        self.assertEqual(evidence_graph_to_dict(graph)["edges"][0]["edge_type"], "qualifies")

    def test_non_json_metadata_fails_cleanly(self) -> None:
        with self.assertRaises(EvidenceGraphBuildError):
            node(metadata={"bad": object()})

    def test_module_has_no_forbidden_imports_or_raw_sql(self) -> None:
        import codie.intelligence.evidence_graph as evidence_graph_module

        source = Path(evidence_graph_module.__file__).read_text(encoding="utf-8")
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
