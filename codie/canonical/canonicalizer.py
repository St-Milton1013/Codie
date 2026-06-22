"""Source-to-canonical orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from codie.canonical.deck_hash import COMMANDER_ZONES, canonical_card_fingerprint, commander_hash, deck_hash
from codie.canonical.event_matcher import event_dedupe_key, normalize_event_name, normalize_format
from codie.db.repositories.canonical import CanonicalRepository
from codie.db.repositories.source import SourceRepository


class CanonicalizationError(ValueError):
    """Raised when source records cannot safely become canonical records."""


@dataclass(frozen=True)
class CanonicalizationResult:
    object_type: str
    source_id: int
    canonical_id: int
    created: bool
    linked: bool


class Canonicalizer:
    """Canonicalize source events and decks through repository boundaries."""

    def __init__(self, source_repository: SourceRepository, canonical_repository: CanonicalRepository) -> None:
        self.source = source_repository
        self.canonical = canonical_repository

    def canonicalize_event(self, source_event_id: int) -> CanonicalizationResult:
        source_event = self.source.get_source_event(source_event_id)
        if source_event is None:
            raise CanonicalizationError(f"Missing source event: {source_event_id}")
        if not source_event["event_name"]:
            raise CanonicalizationError(f"Source event {source_event_id} is missing event_name")
        dedupe_key = event_dedupe_key(source_event)
        now = self.canonical.now()
        existing = self.canonical.get_event_by_dedupe_key(dedupe_key)
        created = existing is None
        if created:
            canonical_event_id = self.canonical.create_event(
                {
                    "event_name": source_event["event_name"],
                    "normalized_event_name": normalize_event_name(source_event["event_name"]),
                    "event_date": source_event["event_date"],
                    "format": normalize_format(source_event["format"]),
                    "region": source_event["source_region"],
                    "country": source_event["source_country"],
                    "venue_or_store": source_event["source_store_tag"],
                    "player_count": source_event["source_reported_player_count"],
                    "deck_count": source_event["source_reported_deck_count"],
                    "event_size_bucket": source_event["tournament_size_bucket"],
                    "confidence_score": 1.0,
                    "dedupe_key": dedupe_key,
                    "created_at": now,
                    "updated_at": now,
                }
            )
        else:
            canonical_event_id = int(existing["canonical_event_id"])
            self.canonical.update_event(canonical_event_id, {"updated_at": now})
        linked = self._link_event_source(canonical_event_id, source_event)
        self.source.update_source_event(
            source_event_id,
            {"canonical_event_id": canonical_event_id, "dedupe_status": "canonicalized"},
        )
        return CanonicalizationResult("event", source_event_id, canonical_event_id, created, linked)

    def canonicalize_deck(self, source_deck_id: int) -> CanonicalizationResult:
        source_deck = self.source.get_source_deck(source_deck_id)
        if source_deck is None:
            raise CanonicalizationError(f"Missing source deck: {source_deck_id}")
        cards = [dict(card) for card in self.source.list_source_deck_cards(source_deck_id)]
        if not cards:
            raise CanonicalizationError(f"Source deck {source_deck_id} has no cards")
        unresolved = [card for card in cards if not card.get("scryfall_id")]
        if unresolved:
            names = ", ".join(str(card["raw_name"]) for card in unresolved)
            raise CanonicalizationError(f"Source deck {source_deck_id} has unresolved source card(s): {names}")
        commanders = [card for card in cards if self._zone(card) in COMMANDER_ZONES]
        if not commanders:
            raise CanonicalizationError(f"Source deck {source_deck_id} has no resolved commander cards")
        deck_hash_value = deck_hash(cards, commanders, format="commander")
        commander_hash_value = commander_hash(commanders)
        now = self.canonical.now()
        existing = self.canonical.get_deck_by_hash(deck_hash_value)
        created = existing is None
        if created:
            canonical_deck_id = self.canonical.create_deck(
                {
                    "deck_hash": deck_hash_value,
                    "commander_hash": commander_hash_value,
                    "format": "commander",
                    "card_count": self._card_count(cards),
                    "commander_count": len(commanders),
                    "color_identity_json": None,
                    "first_seen_at": source_deck["imported_at"],
                    "last_seen_at": source_deck["imported_at"],
                    "created_at": now,
                    "updated_at": now,
                }
            )
            self._persist_deck_cards(canonical_deck_id, cards)
            self._persist_commanders(canonical_deck_id, commanders)
        else:
            canonical_deck_id = int(existing["canonical_deck_id"])
            self.canonical.update_deck(
                canonical_deck_id,
                {"last_seen_at": source_deck["imported_at"], "updated_at": now},
            )
        linked = self._link_deck_source(canonical_deck_id, source_deck)
        self.source.update_source_deck(
            source_deck_id,
            {"canonical_deck_id": canonical_deck_id, "deck_hash": deck_hash_value, "dedupe_status": "canonicalized"},
        )
        self._create_event_deck_entry_if_ready(canonical_deck_id, source_deck)
        return CanonicalizationResult("deck", source_deck_id, canonical_deck_id, created, linked)

    def canonicalize_pending(self) -> tuple[CanonicalizationResult, ...]:
        results: list[CanonicalizationResult] = []
        for event in self.source.list_source_events_for_canonicalization():
            results.append(self.canonicalize_event(int(event["source_event_id"])))
        for deck in self.source.list_source_decks_for_canonicalization():
            results.append(self.canonicalize_deck(int(deck["source_deck_id"])))
        return tuple(results)

    def _link_event_source(self, canonical_event_id: int, source_event: Any) -> bool:
        source_event_id = int(source_event["source_event_id"])
        if self.canonical.get_event_source_link(canonical_event_id, source_event_id) is not None:
            return False
        self.canonical.link_event_source(
            {
                "canonical_event_id": canonical_event_id,
                "source_event_id": source_event_id,
                "provider": source_event["provider"],
                "source_url": source_event["source_url"],
                "source_confidence": 1.0,
                "merge_reason": "dedupe_key",
                "created_at": self.canonical.now(),
            }
        )
        return True

    def _link_deck_source(self, canonical_deck_id: int, source_deck: Any) -> bool:
        source_deck_id = int(source_deck["source_deck_id"])
        if self.canonical.get_deck_source_link(canonical_deck_id, source_deck_id) is not None:
            return False
        self.canonical.link_deck_source(
            {
                "canonical_deck_id": canonical_deck_id,
                "source_deck_id": source_deck_id,
                "source_event_id": source_deck["source_event_id"],
                "provider": source_deck["provider"],
                "source_url": source_deck["source_url"],
                "pilot_name": source_deck["source_player_name"],
                "placement": source_deck["source_rank"],
                "placement_label": source_deck["source_rank_label"],
                "record_text": source_deck["source_record"],
                "source_confidence": 1.0,
                "created_at": self.canonical.now(),
            }
        )
        return True

    def _persist_deck_cards(self, canonical_deck_id: int, cards: list[dict[str, Any]]) -> None:
        aggregate: dict[tuple[str, str], dict[str, Any]] = {}
        for card in cards:
            zone = self._zone(card)
            if zone == "auxiliary":
                continue
            key = (str(card["scryfall_id"]), zone)
            if key not in aggregate:
                aggregate[key] = dict(card)
                aggregate[key]["quantity"] = 0
            aggregate[key]["quantity"] += int(card["quantity"])
        for (_, zone), card in sorted(aggregate.items()):
            if self.canonical.get_deck_card(canonical_deck_id, card["scryfall_id"], zone) is not None:
                continue
            self.canonical.add_deck_card(
                {
                    "canonical_deck_id": canonical_deck_id,
                    "scryfall_id": card["scryfall_id"],
                    "oracle_id": card["oracle_id"],
                    "quantity": card["quantity"],
                    "zone": zone,
                    "is_commander": 1 if zone in COMMANDER_ZONES else 0,
                    "is_companion": 0,
                }
            )

    def _persist_commanders(self, canonical_deck_id: int, commanders: list[dict[str, Any]]) -> None:
        for index, commander in enumerate(sorted(commanders, key=lambda card: str(card["scryfall_id"])), start=1):
            if self.canonical.get_deck_commander(canonical_deck_id, commander["scryfall_id"]) is not None:
                continue
            self.canonical.add_deck_commander(
                {
                    "canonical_deck_id": canonical_deck_id,
                    "scryfall_id": commander["scryfall_id"],
                    "oracle_id": commander["oracle_id"],
                    "commander_order": index,
                    "commander_role": "commander",
                }
            )

    def _create_event_deck_entry_if_ready(self, canonical_deck_id: int, source_deck: Any) -> None:
        source_event_id = source_deck["source_event_id"]
        if source_event_id is None:
            return
        source_event = self.source.get_source_event(int(source_event_id))
        if source_event is None or source_event["canonical_event_id"] is None:
            return
        canonical_event_id = int(source_event["canonical_event_id"])
        source_deck_id = int(source_deck["source_deck_id"])
        if self.canonical.get_event_deck_entry(canonical_event_id, canonical_deck_id, source_deck_id) is not None:
            return
        self.canonical.create_event_deck_entry(
            {
                "canonical_event_id": canonical_event_id,
                "canonical_deck_id": canonical_deck_id,
                "source_deck_id": source_deck_id,
                "pilot_name": source_deck["source_player_name"],
                "placement": source_deck["source_rank"],
                "placement_label": source_deck["source_rank_label"],
                "record_text": source_deck["source_record"],
                "created_at": self.canonical.now(),
            }
        )

    def _card_count(self, cards: list[dict[str, Any]]) -> int:
        return len(canonical_card_fingerprint(cards))

    def _zone(self, card: dict[str, Any]) -> str:
        return str(card.get("source_zone") or "mainboard").lower().strip()
