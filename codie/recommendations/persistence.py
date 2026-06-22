"""Persistence mappers for validated recommendation candidate packets."""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import asdict, dataclass

from codie.db.repositories import RecommendationRepository

from .generation import RecommendationCandidatePacket
from .scoring import ScoreComponent


@dataclass(frozen=True)
class RecommendationRunSpec:
    input_deck_hash: str
    generated_at: str
    commander_hash: str | None = None
    config: dict[str, object] | None = None
    source_snapshot_id: int | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.input_deck_hash, "input_deck_hash")
        _require_text(self.generated_at, "generated_at")
        if self.source_snapshot_id is not None and self.source_snapshot_id < 0:
            raise ValueError("source_snapshot_id must be non-negative")


@dataclass(frozen=True)
class PersistedRecommendationRun:
    recommendation_run_id: int
    candidate_count: int


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required")


def _component_value(components: tuple[ScoreComponent, ...], name: str) -> float | None:
    for component in components:
        if component.name == name:
            return component.value
    return None


def _config_json(config: dict[str, object] | None) -> str | None:
    if config is None:
        return None
    return json.dumps(config, sort_keys=True, separators=(",", ":"))


def _evidence_json(packet: RecommendationCandidatePacket) -> str:
    payload = {
        "candidate": asdict(packet.candidate),
        "audit": asdict(packet.audit),
        "scryfall_id": packet.scryfall_id,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _explanation_text(packet: RecommendationCandidatePacket) -> str:
    return "\n".join(packet.audit.explanation_lines)


def recommendation_run_row(spec: RecommendationRunSpec) -> dict[str, object | None]:
    return {
        "input_deck_hash": spec.input_deck_hash,
        "commander_hash": spec.commander_hash,
        "generated_at": spec.generated_at,
        "config_json": _config_json(spec.config),
        "source_snapshot_id": spec.source_snapshot_id,
        "notes": spec.notes,
    }


def recommendation_candidate_row(packet: RecommendationCandidatePacket) -> dict[str, object | None]:
    components = packet.candidate.score.components
    return {
        "scryfall_id": packet.scryfall_id,
        "oracle_id": packet.candidate.entity_id if packet.candidate.entity_type == "card" else None,
        "candidate_type": packet.candidate.candidate_type,
        "recommendation_score": packet.candidate.score.recommendation_score,
        "inclusion_rate": _component_value(components, "inclusion_rate_score"),
        "lift_score": _component_value(components, "commander_lift_score"),
        "confidence_score": _component_value(components, "confidence_score"),
        "similarity_score": _component_value(components, "similarity_score"),
        "package_completion_score": _component_value(components, "package_completion_score"),
        "generic_staple_penalty": _component_value(components, "generic_staple_penalty"),
        "evidence_json": _evidence_json(packet),
        "explanation_text": _explanation_text(packet),
    }


def persist_recommendation_packets(
    *,
    repository: RecommendationRepository,
    run: RecommendationRunSpec,
    packets: Iterable[RecommendationCandidatePacket],
) -> PersistedRecommendationRun:
    packet_tuple = tuple(packets)
    recommendation_run_id = repository.replace_recommendation_run(
        run=recommendation_run_row(run),
        candidates=tuple(recommendation_candidate_row(packet) for packet in packet_tuple),
    )
    return PersistedRecommendationRun(
        recommendation_run_id=recommendation_run_id,
        candidate_count=len(packet_tuple),
    )
