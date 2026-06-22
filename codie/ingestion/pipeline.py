"""Deck ingestion pipeline orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from codie.cards.lookup import CardLookup
from codie.cards.normalization import normalize_card_name
from codie.db.repositories.source import SourceRepository
from codie.providers.base import Provider
from codie.providers.errors import CardResolutionError, ParseError, ProviderError, SchemaValidationError
from codie.providers.models import SourceDeckCandidate, RawPayload

from .validation import validate_candidate


@dataclass(frozen=True)
class IngestionFailure:
    provider: str
    pipeline: str
    source_url: str | None
    object_type: str
    error_type: str
    error_message: str
    raw_payload_hash: str | None
    occurred_at: str
    retryable: bool


@dataclass(frozen=True)
class IngestionResult:
    run_id: int
    status: str
    objects_processed: int
    objects_inserted: int
    objects_failed: int
    failures: tuple[IngestionFailure, ...]


class DeckIngestionPipeline:
    """Run provider fetch/parse/validate/resolve/persist for source decks."""

    def __init__(
        self,
        provider: Provider,
        source_repository: SourceRepository,
        card_lookup: CardLookup,
        *,
        pipeline_name: str = "deck_ingestion",
    ) -> None:
        self.provider = provider
        self.source_repository = source_repository
        self.card_lookup = card_lookup
        self.pipeline_name = pipeline_name

    def run(self) -> IngestionResult:
        provider_name = self.provider.provider_name
        started_at = self.source_repository.now()
        run_id = self.source_repository.create_ingestion_run(
            {
                "provider": provider_name,
                "pipeline_name": self.pipeline_name,
                "started_at": started_at,
                "status": "running",
            }
        )
        processed = 0
        inserted = 0
        failures: list[IngestionFailure] = []

        try:
            payload = self.provider.fetch()
            parsed = self.provider.parse(payload)
        except ProviderError as exc:
            failure = self._failure(provider_name, None, "provider", exc)
            failures.append(failure)
            self._finish(run_id, "failed", processed, inserted, failures)
            return IngestionResult(run_id, "failed", processed, inserted, len(failures), tuple(failures))
        except Exception as exc:
            failure = self._failure(provider_name, None, "provider", ParseError(str(exc)))
            failures.append(failure)
            self._finish(run_id, "failed", processed, inserted, failures)
            return IngestionResult(run_id, "failed", processed, inserted, len(failures), tuple(failures))

        events_by_key: dict[str, int] = {}
        decks_by_key: dict[str, int] = {}

        for event in tuple(parsed.get("events", ())):
            processed += 1
            try:
                validate_candidate(event)
                provider_object_id = self._persist_raw_payload(event.raw_payload, run_id)
                source_event_id = self.source_repository.create_source_event(
                    {
                        "provider": event.provider,
                        "provider_event_id": event.provider_event_id,
                        "source_url": event.source_url,
                        "original_source": event.original_source,
                        "original_source_url": event.original_source_url,
                        "event_name": event.event_name,
                        "normalized_event_name": normalize_card_name(event.event_name or ""),
                        "event_date": event.event_date,
                        "format": event.format,
                        "source_region": event.region,
                        "source_country": event.country,
                        "source_store_tag": event.store_tag,
                        "source_language": event.language,
                        "source_reported_player_count": event.player_count,
                        "source_reported_deck_count": event.deck_count,
                        "raw_json": event.raw_payload.raw_payload_json,
                        "provider_object_id": provider_object_id,
                        "imported_at": self.source_repository.now(),
                    }
                )
                events_by_key[event.event_key or event.provider_event_id or str(source_event_id)] = source_event_id
                inserted += 2
            except ProviderError as exc:
                failures.append(self._failure(event.provider, event.raw_payload, "event", exc))

        for deck in tuple(parsed.get("decks", ())):
            processed += 1
            try:
                validate_candidate(deck)
                resolved_cards = self._resolve_deck_cards(deck)
                provider_object_id = self._persist_raw_payload(deck.raw_payload, run_id)
                source_event_id = events_by_key.get(deck.source_event_key or "")
                source_deck_id = self.source_repository.create_source_deck(
                    {
                        "provider": deck.provider,
                        "provider_deck_id": deck.provider_deck_id,
                        "source_event_id": source_event_id,
                        "source_url": deck.source_url,
                        "source_download_url": deck.download_url,
                        "deck_title": deck.deck_title,
                        "commander_text": deck.commander_text,
                        "source_archetype_name": deck.archetype_name,
                        "source_player_name": deck.pilot_name,
                        "source_rank": deck.rank,
                        "source_rank_label": deck.rank_label,
                        "source_record": deck.record,
                        "source_win_rate": deck.win_rate,
                        "raw_json": deck.raw_payload.raw_payload_json,
                        "provider_object_id": provider_object_id,
                        "imported_at": self.source_repository.now(),
                    }
                )
                deck_key = deck.deck_key or deck.provider_deck_id or str(source_deck_id)
                decks_by_key[deck_key] = source_deck_id
                inserted += 2
                inserted += self._persist_deck_cards(source_deck_id, resolved_cards)
            except ProviderError as exc:
                failures.append(self._failure(deck.provider, deck.raw_payload, "deck", exc))

        status = "completed" if not failures else "completed_with_errors"
        self._finish(run_id, status, processed, inserted, failures)
        return IngestionResult(run_id, status, processed, inserted, len(failures), tuple(failures))

    def _persist_raw_payload(self, raw_payload: RawPayload, run_id: int) -> int:
        return self.source_repository.create_provider_object(
            {
                "provider": raw_payload.provider,
                "object_type": raw_payload.object_type,
                "provider_id": raw_payload.provider_id,
                "source_url": raw_payload.source_url,
                "retrieved_at": raw_payload.retrieved_at,
                "payload_hash": raw_payload.payload_hash,
                "raw_payload_json": raw_payload.raw_payload_json,
                "raw_file_path": raw_payload.raw_file_path,
                "run_id": run_id,
            }
        )

    def _resolve_deck_cards(self, deck: SourceDeckCandidate) -> list[tuple[Any, Any]]:
        resolved_cards = []
        for card in deck.cards:
            validate_candidate(card)
            if card.source_deck_key != (deck.deck_key or deck.provider_deck_id):
                raise SchemaValidationError(f"Unknown source deck key: {card.source_deck_key}")
            resolved = self.card_lookup.resolve(card.raw_name)
            if resolved.card is None:
                raise CardResolutionError(f"Could not resolve card: {card.raw_name}")
            resolved_cards.append((card, resolved))
        return resolved_cards

    def _persist_deck_cards(self, source_deck_id: int, resolved_cards: list[tuple[Any, Any]]) -> int:
        inserted = 0
        for card, resolved in resolved_cards:
            self.source_repository.create_source_deck_card(
                {
                    "source_deck_id": source_deck_id,
                    "raw_name": card.raw_name,
                    "normalized_name": normalize_card_name(card.raw_name),
                    "quantity": card.quantity,
                    "source_zone": card.source_zone,
                    "source_order": card.source_order,
                    "scryfall_id": resolved.card["scryfall_id"],
                    "oracle_id": resolved.card["oracle_id"],
                    "resolution_status": resolved.status,
                    "raw_entry": card.raw_entry,
                }
            )
            inserted += 1
        return inserted

    def _finish(
        self,
        run_id: int,
        status: str,
        processed: int,
        inserted: int,
        failures: list[IngestionFailure],
    ) -> None:
        self.source_repository.update_ingestion_run(
            run_id,
            {
                "completed_at": self.source_repository.now(),
                "status": status,
                "objects_processed": processed,
                "objects_inserted": inserted,
                "objects_failed": len(failures),
                "error_summary": "\n".join(f"{failure.error_type}: {failure.error_message}" for failure in failures) or None,
            },
        )

    def _failure(
        self,
        provider: str,
        raw_payload: RawPayload | None,
        object_type: str,
        error: ProviderError,
    ) -> IngestionFailure:
        return IngestionFailure(
            provider=provider,
            pipeline=self.pipeline_name,
            source_url=raw_payload.source_url if raw_payload else None,
            object_type=object_type,
            error_type=type(error).__name__,
            error_message=str(error),
            raw_payload_hash=raw_payload.payload_hash if raw_payload else None,
            occurred_at=self.source_repository.now(),
            retryable=error.retryable,
        )
