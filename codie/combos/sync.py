"""Persist Commander Spellbook combo evidence."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Iterable, Protocol

from codie.cards.lookup import CardLookup
from codie.cards.normalization import normalize_card_name
from codie.db.repositories.analytics import AnalyticsRepository
from codie.db.repositories.base import BaseRepository
from codie.db.repositories.curated import CuratedRepository
from codie.db.repositories.source import SourceRepository


class ComboCandidate(Protocol):
    provider: str
    provider_combo_id: str | None
    combo_url: str | None
    combo_name: str | None
    components: tuple[str, ...]
    outputs: tuple[str, ...]
    raw_payload: Any
    cards: tuple[Any, ...]


@dataclass(frozen=True)
class ComboSyncResult:
    source_combo_count: int
    combo_count: int
    combo_card_count: int
    resolved_card_count: int
    unresolved_card_count: int
    evidence_count_count: int


class ComboEvidenceSync:
    """Sync provider combo candidates into source/curated evidence tables."""

    def __init__(
        self,
        source: SourceRepository,
        curated: CuratedRepository,
        analytics: AnalyticsRepository,
        card_lookup: CardLookup,
    ) -> None:
        self.source = source
        self.curated = curated
        self.analytics = analytics
        self.card_lookup = card_lookup

    def sync_candidates(self, candidates: Iterable[ComboCandidate]) -> ComboSyncResult:
        now = BaseRepository.now()
        source_count = combo_count = card_count = resolved_count = unresolved_count = evidence_count = 0
        card_evidence: dict[str, int] = {}
        combo_evidence: dict[str, int] = {}

        for candidate in candidates:
            self.source.create_source_combo(
                {
                    "provider": candidate.provider,
                    "provider_combo_id": candidate.provider_combo_id,
                    "combo_url": candidate.combo_url,
                    "combo_name": candidate.combo_name,
                    "components_json": json.dumps(candidate.components, sort_keys=True, ensure_ascii=False),
                    "outputs_json": json.dumps(candidate.outputs, sort_keys=True, ensure_ascii=False),
                    "raw_json": candidate.raw_payload.raw_payload_json,
                    "imported_at": now,
                }
            )
            source_count += 1

            combo_id = self.curated.upsert_combo(
                {
                    "provider": candidate.provider,
                    "provider_combo_id": candidate.provider_combo_id,
                    "combo_url": candidate.combo_url,
                    "combo_name": candidate.combo_name,
                    "normalized_name": normalize_card_name(candidate.combo_name or candidate.provider_combo_id or ""),
                    "outputs_json": json.dumps(candidate.outputs, sort_keys=True, ensure_ascii=False),
                    "raw_json": candidate.raw_payload.raw_payload_json,
                    "created_at": now,
                    "updated_at": now,
                }
            )
            combo_count += 1
            self.curated.delete_combo_cards(combo_id)

            for component in candidate.cards:
                lookup = self.card_lookup.resolve(component.raw_name, fuzzy_threshold=1.0)
                card = lookup.card if lookup.status in {"exact", "alias"} else None
                if card is None:
                    unresolved_count += 1
                    scryfall_id = None
                    oracle_id = None
                else:
                    resolved_count += 1
                    scryfall_id = card["scryfall_id"]
                    oracle_id = card["oracle_id"]
                    evidence_id = oracle_id or scryfall_id
                    card_evidence[evidence_id] = card_evidence.get(evidence_id, 0) + 1
                self.curated.add_combo_card(
                    {
                        "combo_id": combo_id,
                        "scryfall_id": scryfall_id,
                        "oracle_id": oracle_id,
                        "card_name": component.raw_name,
                        "role": component.role,
                        "required": 1 if component.required else 0,
                    }
                )
                card_count += 1

            combo_id_key = candidate.provider_combo_id or str(combo_id)
            combo_evidence[combo_id_key] = len(candidate.cards)

        for entity_id, count in card_evidence.items():
            self.analytics.upsert_evidence_count(
                {
                    "entity_type": "card",
                    "entity_id": entity_id,
                    "combo_evidence_count": count,
                    "updated_at": now,
                }
            )
            evidence_count += 1
        for entity_id, count in combo_evidence.items():
            self.analytics.upsert_evidence_count(
                {
                    "entity_type": "combo",
                    "entity_id": entity_id,
                    "combo_evidence_count": count,
                    "updated_at": now,
                }
            )
            evidence_count += 1

        return ComboSyncResult(
            source_combo_count=source_count,
            combo_count=combo_count,
            combo_card_count=card_count,
            resolved_card_count=resolved_count,
            unresolved_card_count=unresolved_count,
            evidence_count_count=evidence_count,
        )
