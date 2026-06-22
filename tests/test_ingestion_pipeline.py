from __future__ import annotations

import unittest

from codie.cards.lookup import CardLookup
from codie.db.bootstrap import bootstrap_database
from codie.db.repositories.core import CoreRepository
from codie.db.repositories.source import SourceRepository
from codie.ingestion.pipeline import DeckIngestionPipeline
from codie.ingestion.validation import validate_candidate
from codie.providers.base import Provider
from codie.providers.errors import MissingRequiredFieldError, ParseError, SchemaValidationError
from codie.providers.models import (
    RawPayload,
    SourceDeckCandidate,
    SourceDeckCardCandidate,
    SourceEventCandidate,
)


NOW = "2026-06-21T00:00:00+00:00"


class MockProvider(Provider):
    provider_name = "mock_provider"

    def __init__(self, parsed=None, error=None) -> None:
        self.parsed = parsed
        self.error = error

    def fetch(self):
        return {"fixture": True}

    def parse(self, payload):
        if self.error:
            raise self.error
        return self.parsed


def raw_payload(object_type: str, provider_id: str, payload: dict) -> RawPayload:
    return RawPayload(
        provider="mock_provider",
        object_type=object_type,
        provider_id=provider_id,
        source_url=f"https://example.test/{provider_id}",
        retrieved_at=NOW,
        payload=payload,
    )


def event_candidate() -> SourceEventCandidate:
    return SourceEventCandidate(
        provider="mock_provider",
        provider_event_id="event-1",
        source_url="https://example.test/event-1",
        original_source="Mock",
        original_source_url="https://example.test",
        event_name="Mock Open",
        event_date="2026-06-21",
        format="commander",
        region="north_america",
        country="US",
        store_tag="fixture",
        language="en",
        player_count=16,
        deck_count=16,
        raw_payload=raw_payload("event", "event-1", {"event": True}),
        event_key="event-1",
    )


def deck_candidate(card_name: str = "Tymna the Weaver") -> SourceDeckCandidate:
    card = SourceDeckCardCandidate(
        source_deck_key="deck-1",
        raw_name=card_name,
        quantity=1,
        source_zone="mainboard",
        source_order=1,
        raw_entry=f"1 {card_name}",
    )
    return SourceDeckCandidate(
        provider="mock_provider",
        provider_deck_id="deck-1",
        source_event_key="event-1",
        source_url="https://example.test/deck-1",
        download_url="https://example.test/deck-1.txt",
        deck_title="Mock Deck",
        commander_text="Tymna the Weaver",
        pilot_name="Fixture Pilot",
        rank=1,
        rank_label="1st",
        record="4-0",
        win_rate=1.0,
        archetype_name="Source Label",
        raw_payload=raw_payload("deck", "deck-1", {"deck": True}),
        deck_key="deck-1",
        cards=(card,),
    )


class DeckIngestionPipelineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = bootstrap_database()
        self.core = CoreRepository(self.connection)
        self.source = SourceRepository(self.connection)
        self.core.insert_card(
            {
                "scryfall_id": "tymna-card",
                "oracle_id": "tymna-oracle",
                "name": "Tymna the Weaver",
                "normalized_name": "tymna the weaver",
                "raw_json": "{}",
                "imported_at": NOW,
            }
        )

    def tearDown(self) -> None:
        self.connection.close()

    def pipeline(self, provider: Provider) -> DeckIngestionPipeline:
        return DeckIngestionPipeline(provider, self.source, CardLookup(self.core))

    def test_successful_mock_provider_persists_source_records_and_run_log(self) -> None:
        provider = MockProvider({"events": (event_candidate(),), "decks": (deck_candidate(),)})
        result = self.pipeline(provider).run()
        run = self.source.get_ingestion_run(result.run_id)
        self.assertEqual(result.status, "completed")
        self.assertEqual(result.objects_processed, 2)
        self.assertEqual(result.objects_failed, 0)
        self.assertEqual(run["status"], "completed")
        self.assertEqual(run["objects_processed"], 2)
        deck_card = self.connection.execute("SELECT * FROM source_deck_cards").fetchone()
        provider_object = self.connection.execute(
            "SELECT * FROM provider_objects WHERE object_type = ?",
            ("deck",),
        ).fetchone()
        self.assertEqual(deck_card["scryfall_id"], "tymna-card")
        self.assertEqual(deck_card["resolution_status"], "exact")
        self.assertTrue(provider_object["payload_hash"].startswith("sha256:"))
        self.assertEqual(provider_object["raw_payload_json"], '{"deck":true}')

    def test_parse_failure_is_logged_as_structured_failure(self) -> None:
        provider = MockProvider(error=ParseError("malformed payload"))
        result = self.pipeline(provider).run()
        run = self.source.get_ingestion_run(result.run_id)
        self.assertEqual(result.status, "failed")
        self.assertEqual(result.objects_failed, 1)
        failure = result.failures[0]
        self.assertEqual(failure.provider, "mock_provider")
        self.assertEqual(failure.pipeline, "deck_ingestion")
        self.assertIsNone(failure.source_url)
        self.assertEqual(failure.object_type, "provider")
        self.assertEqual(failure.error_type, "ParseError")
        self.assertEqual(failure.error_message, "malformed payload")
        self.assertIsNone(failure.raw_payload_hash)
        self.assertTrue(failure.occurred_at)
        self.assertEqual(failure.retryable, False)
        self.assertIn("malformed payload", run["error_summary"])

    def test_missing_required_field_validation_fails_cleanly(self) -> None:
        invalid = SourceDeckCardCandidate(
            source_deck_key="deck-1",
            raw_name="",
            quantity=1,
            source_zone="mainboard",
            source_order=1,
            raw_entry=None,
        )
        with self.assertRaises(MissingRequiredFieldError):
            validate_candidate(invalid)

    def test_invalid_card_quantity_fails_schema_validation(self) -> None:
        invalid = SourceDeckCardCandidate(
            source_deck_key="deck-1",
            raw_name="Tymna the Weaver",
            quantity=0,
            source_zone="mainboard",
            source_order=1,
            raw_entry=None,
        )
        with self.assertRaises(SchemaValidationError):
            validate_candidate(invalid)

    def test_card_resolution_failure_marks_run_completed_with_errors(self) -> None:
        provider = MockProvider({"events": (event_candidate(),), "decks": (deck_candidate("Unknown Card"),)})
        result = self.pipeline(provider).run()
        run = self.source.get_ingestion_run(result.run_id)
        self.assertEqual(result.status, "completed_with_errors")
        self.assertEqual(result.objects_failed, 1)
        failure = result.failures[0]
        self.assertEqual(failure.provider, "mock_provider")
        self.assertEqual(failure.pipeline, "deck_ingestion")
        self.assertEqual(failure.source_url, "https://example.test/deck-1")
        self.assertEqual(failure.object_type, "deck")
        self.assertEqual(failure.error_type, "CardResolutionError")
        self.assertIn("Unknown Card", failure.error_message)
        self.assertTrue(failure.raw_payload_hash.startswith("sha256:"))
        self.assertTrue(failure.occurred_at)
        self.assertEqual(failure.retryable, False)
        self.assertEqual(run["objects_failed"], 1)
        self.assertEqual(
            self.connection.execute("SELECT COUNT(*) AS count FROM source_deck_cards").fetchone()["count"],
            0,
        )
        self.assertEqual(
            self.connection.execute("SELECT COUNT(*) AS count FROM source_decks").fetchone()["count"],
            0,
        )
        self.assertEqual(
            self.connection.execute("SELECT COUNT(*) AS count FROM provider_objects WHERE object_type = ?", ("deck",)).fetchone()["count"],
            0,
        )


if __name__ == "__main__":
    unittest.main()
