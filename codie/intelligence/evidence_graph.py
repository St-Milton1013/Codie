"""In-memory evidence graph primitives for interactive intelligence."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


ALLOWED_NODE_TYPES = frozenset(
    {
        "card",
        "commander",
        "deck",
        "package",
        "tournament_stat",
        "regional_stat",
        "historical_stat",
        "innovation_signal",
        "primer_metadata",
        "combo_evidence",
        "simulation_result",
        "unsupported_card",
        "source_conflict",
        "user_deck_memory",
        "saved_analysis",
        "manual_note",
    }
)

ALLOWED_PRIVACY_SCOPES = frozenset({"public", "local", "local_user_data", "sensitive"})

ALLOWED_EDGE_TYPES = frozenset(
    {
        "supports",
        "contradicts",
        "qualifies",
        "derived_from",
        "same_card_as",
        "same_commander_as",
        "observed_in",
        "linked_to",
        "requires_caveat",
    }
)

ALLOWED_SOURCE_TYPES = frozenset(
    {
        "canonical",
        "analytics",
        "recommendation_candidate",
        "innovation_snapshot",
        "combo",
        "primer_metadata",
        "simulation",
        "deck_memory",
        "saved_analysis",
        "curated",
        "manual",
    }
)

ALLOWED_CAVEAT_TYPES = frozenset(
    {
        "low_sample",
        "missing_data",
        "unsupported_card",
        "unsupported_simulator_behavior",
        "source_conflict",
        "privacy_redaction",
        "stale_data",
        "manual_review_required",
    }
)

ALLOWED_SEVERITIES = frozenset({"info", "warning", "blocking"})

FORBIDDEN_CLAIM_FRAGMENTS = (
    "this deck is trying to",
    "the game plan is",
    "this deck should",
    "should " + "play",
    "should be " + "played",
    "should be " + "cut",
    "must " + "include",
    "strictly better",
    "correct " + "card",
    "is optimal",
    "cut " + "this",
    "always include",
)

FORBIDDEN_METADATA_KEYS = frozenset(
    {
        "raw_input",
        "full_primer_body",
        "raw_provider_payload",
        "private_deck_text",
        "provider_payload",
        "original_import_text",
    }
)


class EvidenceGraphBuildError(ValueError):
    """Raised when an evidence graph cannot be built safely."""


@dataclass(frozen=True)
class EvidenceCitation:
    citation_id: str
    source_type: str
    source_name: str
    observed_at: str
    source_record_id: str | None = None
    source_url: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.citation_id, "citation_id")
        object.__setattr__(self, "source_type", _normalize_allowed(self.source_type, ALLOWED_SOURCE_TYPES, "source_type"))
        _require_text(self.source_name, "source_name")
        _require_text(self.observed_at, "observed_at")
        if self.source_record_id in (None, "") and self.source_url in (None, ""):
            raise EvidenceGraphBuildError("source_record_id or source_url is required")


@dataclass(frozen=True)
class EvidenceCaveat:
    caveat_id: str
    caveat_type: str
    message: str
    severity: str
    related_node_ids: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.caveat_id, "caveat_id")
        object.__setattr__(self, "caveat_type", _normalize_allowed(self.caveat_type, ALLOWED_CAVEAT_TYPES, "caveat_type"))
        object.__setattr__(self, "message", _validate_text(self.message, "message"))
        object.__setattr__(self, "severity", _normalize_allowed(self.severity, ALLOWED_SEVERITIES, "severity"))
        object.__setattr__(self, "related_node_ids", tuple(self.related_node_ids))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class EvidenceNode:
    node_id: str
    node_type: str
    label: str
    summary: str
    confidence: float
    citations: tuple[EvidenceCitation, ...] = ()
    privacy_scope: str = "public"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.node_id, "node_id")
        object.__setattr__(self, "node_type", _normalize_allowed(self.node_type, ALLOWED_NODE_TYPES, "node_type"))
        _require_text(self.label, "label")
        object.__setattr__(self, "summary", _validate_text(self.summary, "summary"))
        _validate_confidence(self.confidence, "confidence")
        object.__setattr__(
            self,
            "privacy_scope",
            _normalize_allowed(self.privacy_scope, ALLOWED_PRIVACY_SCOPES, "privacy_scope"),
        )
        object.__setattr__(self, "citations", tuple(sorted(self.citations, key=lambda item: item.citation_id)))
        if self.node_type != "manual_note" and not self.citations:
            raise EvidenceGraphBuildError("non-manual evidence nodes require at least one citation")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class EvidenceEdge:
    edge_id: str
    source_node_id: str
    target_node_id: str
    edge_type: str
    summary: str
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.edge_id, "edge_id")
        _require_text(self.source_node_id, "source_node_id")
        _require_text(self.target_node_id, "target_node_id")
        object.__setattr__(self, "edge_type", _normalize_allowed(self.edge_type, ALLOWED_EDGE_TYPES, "edge_type"))
        object.__setattr__(self, "summary", _validate_text(self.summary, "summary"))
        _validate_confidence(self.confidence, "confidence")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class EvidenceGraph:
    graph_id: str
    claim_type: str
    claim_text: str
    subject_type: str
    subject_id: str
    generated_at: str
    nodes: tuple[EvidenceNode, ...]
    edges: tuple[EvidenceEdge, ...] = ()
    caveats: tuple[EvidenceCaveat, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.graph_id, "graph_id")
        _require_text(self.claim_type, "claim_type")
        object.__setattr__(self, "claim_text", _validate_text(self.claim_text, "claim_text"))
        _require_text(self.subject_type, "subject_type")
        _require_text(self.subject_id, "subject_id")
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "nodes", tuple(sorted(self.nodes, key=lambda item: item.node_id)))
        object.__setattr__(self, "edges", tuple(sorted(self.edges, key=lambda item: item.edge_id)))
        object.__setattr__(self, "caveats", tuple(sorted(self.caveats, key=lambda item: item.caveat_id)))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        validate_evidence_graph(self)


@dataclass(frozen=True)
class EvidenceGraphInput:
    graph_id: str
    claim_type: str
    claim_text: str
    subject_type: str
    subject_id: str
    generated_at: str
    nodes: tuple[EvidenceNode, ...]
    edges: tuple[EvidenceEdge, ...] = ()
    caveats: tuple[EvidenceCaveat, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


def build_evidence_graph(graph_input: EvidenceGraphInput) -> EvidenceGraph:
    """Build and validate one deterministic in-memory evidence graph."""

    return EvidenceGraph(
        graph_id=graph_input.graph_id,
        claim_type=graph_input.claim_type,
        claim_text=graph_input.claim_text,
        subject_type=graph_input.subject_type,
        subject_id=graph_input.subject_id,
        generated_at=graph_input.generated_at,
        nodes=graph_input.nodes,
        edges=graph_input.edges,
        caveats=graph_input.caveats,
        metadata=graph_input.metadata,
    )


def validate_evidence_graph(graph: EvidenceGraph) -> EvidenceGraph:
    """Validate graph-level references and uniqueness."""

    if not graph.nodes:
        raise EvidenceGraphBuildError("EvidenceGraph requires at least one node")

    node_ids = [node.node_id for node in graph.nodes]
    duplicate_node_ids = _duplicates(node_ids)
    if duplicate_node_ids:
        raise EvidenceGraphBuildError(f"duplicate node_id: {duplicate_node_ids[0]}")
    node_id_set = set(node_ids)

    edge_ids = [edge.edge_id for edge in graph.edges]
    duplicate_edge_ids = _duplicates(edge_ids)
    if duplicate_edge_ids:
        raise EvidenceGraphBuildError(f"duplicate edge_id: {duplicate_edge_ids[0]}")
    for edge in graph.edges:
        if edge.source_node_id not in node_id_set:
            raise EvidenceGraphBuildError(f"edge references missing source node: {edge.source_node_id}")
        if edge.target_node_id not in node_id_set:
            raise EvidenceGraphBuildError(f"edge references missing target node: {edge.target_node_id}")
        if edge.source_node_id == edge.target_node_id and edge.edge_type != "qualifies":
            raise EvidenceGraphBuildError("self-edges require edge_type qualifies")

    for caveat in graph.caveats:
        for node_id in caveat.related_node_ids:
            if node_id not in node_id_set:
                raise EvidenceGraphBuildError(f"caveat references missing node: {node_id}")

    return graph


def evidence_graph_to_dict(graph: EvidenceGraph) -> dict[str, Any]:
    """Serialize one evidence graph to deterministic JSON-compatible data."""

    validated = validate_evidence_graph(graph)
    return {
        "graph_id": validated.graph_id,
        "claim_type": validated.claim_type,
        "claim_text": validated.claim_text,
        "subject_type": validated.subject_type,
        "subject_id": validated.subject_id,
        "generated_at": validated.generated_at,
        "nodes": [_node_to_dict(node) for node in validated.nodes],
        "edges": [_edge_to_dict(edge) for edge in validated.edges],
        "caveats": [_caveat_to_dict(caveat) for caveat in validated.caveats],
        "metadata": _sorted_json_object(validated.metadata),
    }


def _node_to_dict(node: EvidenceNode) -> dict[str, Any]:
    return {
        "node_id": node.node_id,
        "node_type": node.node_type,
        "label": node.label,
        "summary": node.summary,
        "confidence": node.confidence,
        "citations": [_citation_to_dict(citation) for citation in node.citations],
        "privacy_scope": node.privacy_scope,
        "metadata": _sorted_json_object(node.metadata),
    }


def _edge_to_dict(edge: EvidenceEdge) -> dict[str, Any]:
    return {
        "edge_id": edge.edge_id,
        "source_node_id": edge.source_node_id,
        "target_node_id": edge.target_node_id,
        "edge_type": edge.edge_type,
        "summary": edge.summary,
        "confidence": edge.confidence,
        "metadata": _sorted_json_object(edge.metadata),
    }


def _citation_to_dict(citation: EvidenceCitation) -> dict[str, Any]:
    return {
        "citation_id": citation.citation_id,
        "source_type": citation.source_type,
        "source_name": citation.source_name,
        "source_record_id": citation.source_record_id,
        "source_url": citation.source_url,
        "observed_at": citation.observed_at,
    }


def _caveat_to_dict(caveat: EvidenceCaveat) -> dict[str, Any]:
    return {
        "caveat_id": caveat.caveat_id,
        "caveat_type": caveat.caveat_type,
        "message": caveat.message,
        "severity": caveat.severity,
        "related_node_ids": list(caveat.related_node_ids),
        "metadata": _sorted_json_object(caveat.metadata),
    }


def _validate_text(text: str, field_name: str) -> str:
    _require_text(text, field_name)
    normalized = " ".join(text.strip().lower().split())
    for fragment in FORBIDDEN_CLAIM_FRAGMENTS:
        if fragment in normalized:
            raise EvidenceGraphBuildError(f"unsupported strategic claim text: {fragment}")
    return text.strip()


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise EvidenceGraphBuildError(f"{field_name} is required")


def _normalize_allowed(value: str, allowed: frozenset[str], field_name: str) -> str:
    _require_text(value, field_name)
    normalized = value.strip().lower()
    if normalized not in allowed:
        raise EvidenceGraphBuildError(f"unsupported {field_name}: {value}")
    return normalized


def _validate_confidence(value: float, field_name: str) -> None:
    if not isinstance(value, int | float):
        raise EvidenceGraphBuildError(f"{field_name} must be numeric")
    if value < 0 or value > 1:
        raise EvidenceGraphBuildError(f"{field_name} must be between 0 and 1")


def _validate_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise EvidenceGraphBuildError("metadata must be an object")
    _reject_forbidden_metadata(metadata)
    try:
        encoded = json.dumps(metadata, sort_keys=True)
        decoded = json.loads(encoded)
    except (TypeError, ValueError) as exc:
        raise EvidenceGraphBuildError("metadata must be JSON-compatible") from exc
    if not isinstance(decoded, dict):
        raise EvidenceGraphBuildError("metadata must be an object")
    return decoded


def _reject_forbidden_metadata(value: Any) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized_key = str(key).strip().lower().replace(" ", "_").replace("-", "_")
            if normalized_key in FORBIDDEN_METADATA_KEYS:
                raise EvidenceGraphBuildError(f"metadata contains forbidden private field: {key}")
            _reject_forbidden_metadata(nested)
    elif isinstance(value, list):
        for item in value:
            _reject_forbidden_metadata(item)


def _sorted_json_object(value: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(value, sort_keys=True))


def _duplicates(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for value in values:
        if value in seen and value not in duplicates:
            duplicates.append(value)
        seen.add(value)
    return duplicates
