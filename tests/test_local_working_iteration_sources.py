from __future__ import annotations

import gzip
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from codie.local_app.sources import (
    LocalSourceError,
    MoxfieldDeckSource,
    ScryfallCatalogSource,
    read_catalog_payloads,
)
from codie.providers.errors import NetworkError, RateLimitError

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "scryfall"


class FakeResponse:
    def __init__(self, body: bytes, *, content_length: int | None = None) -> None:
        self.body = body
        self.offset = 0
        self.headers = {}
        if content_length is not None:
            self.headers["Content-Length"] = str(content_length)

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self, size: int = -1) -> bytes:
        if size < 0:
            size = len(self.body) - self.offset
        chunk = self.body[self.offset : self.offset + size]
        self.offset += len(chunk)
        return chunk


class StubMoxfieldClient:
    def __init__(self, result: dict | Exception) -> None:
        self.result = result
        self.calls: list[str] = []

    def fetch_deck(self, public_id: str) -> dict:
        self.calls.append(public_id)
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


class LocalWorkingIterationSourceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temporary_directory.name) / "workspace"
        self.cards = (FIXTURE_DIR / "bulk_cards.json").read_bytes()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def metadata(self, download_uri: str = "https://data.scryfall.io/oracle-cards.json") -> bytes:
        return json.dumps(
            {
                "data": [
                    {
                        "type": "oracle_cards",
                        "download_uri": download_uri,
                        "updated_at": "2026-08-25T00:00:00+00:00",
                    }
                ]
            }
        ).encode()

    def test_catalog_download_is_bounded_hashed_contained_and_cached(self) -> None:
        source = ScryfallCatalogSource()
        responses = [
            FakeResponse(self.metadata()),
            FakeResponse(self.cards, content_length=len(self.cards)),
        ]
        with patch("codie.local_app.sources.urlopen", side_effect=responses) as fetch:
            first = source.prepare(self.workspace, refresh=False)
            second = source.prepare(self.workspace, refresh=False)

        expected_hash = "sha256:" + hashlib.sha256(self.cards).hexdigest()
        self.assertEqual(fetch.call_count, 2)
        self.assertEqual(first.content_hash, expected_hash)
        self.assertFalse(first.from_cache)
        self.assertTrue(second.from_cache)
        self.assertEqual(second.content_hash, expected_hash)
        self.assertEqual(first.path.read_bytes(), self.cards)
        self.assertEqual(
            first.path.relative_to(self.workspace).parts[:2], ("cache", "card-catalog")
        )
        self.assertFalse(first.path.with_suffix(".json.part").exists())

    def test_catalog_rejects_untrusted_download_and_oversize_without_partial_file(self) -> None:
        source = ScryfallCatalogSource(max_catalog_bytes=10)
        with patch(
            "codie.local_app.sources.urlopen",
            return_value=FakeResponse(self.metadata("https://example.test/cards.json")),
        ):
            with self.assertRaisesRegex(LocalSourceError, "not trusted"):
                source.prepare(self.workspace, refresh=True)

        with patch(
            "codie.local_app.sources.urlopen",
            side_effect=[
                FakeResponse(self.metadata()),
                FakeResponse(self.cards, content_length=len(self.cards)),
            ],
        ):
            with self.assertRaisesRegex(LocalSourceError, "size limit"):
                source.prepare(self.workspace, refresh=True)
        cache_root = self.workspace / "cache" / "card-catalog"
        self.assertFalse((cache_root / "oracle_cards.json").exists())
        self.assertFalse((cache_root / "oracle_cards.json.part").exists())

    def test_cached_catalog_integrity_failure_requires_refresh(self) -> None:
        source = ScryfallCatalogSource()
        with patch(
            "codie.local_app.sources.urlopen",
            side_effect=[
                FakeResponse(self.metadata()),
                FakeResponse(self.cards, content_length=len(self.cards)),
            ],
        ):
            snapshot = source.prepare(self.workspace, refresh=False)
        snapshot.path.write_bytes(b"[]")
        with self.assertRaisesRegex(LocalSourceError, "integrity check"):
            source.prepare(self.workspace, refresh=False)

    def test_current_scryfall_jsonl_gzip_shape_is_streamed_and_parsed(self) -> None:
        jsonl = (
            b"\n".join(
                json.dumps(card, separators=(",", ":")).encode() for card in json.loads(self.cards)
            )
            + b"\n"
        )
        compressed = gzip.compress(jsonl)
        metadata = json.dumps(
            {
                "data": [
                    {
                        "type": "oracle_cards",
                        "jsonl_download_uri": (
                            "https://data.scryfall.io/oracle-cards/oracle-cards-fixture.jsonl.gz"
                        ),
                        "updated_at": "2026-08-25T00:00:00+00:00",
                    }
                ]
            }
        ).encode()
        with patch(
            "codie.local_app.sources.urlopen",
            side_effect=[
                FakeResponse(metadata),
                FakeResponse(compressed, content_length=len(compressed)),
            ],
        ):
            snapshot = ScryfallCatalogSource().prepare(self.workspace, refresh=False)

        self.assertEqual(snapshot.content_format, "jsonl_gzip")
        self.assertEqual(snapshot.path.name, "oracle_cards.jsonl.gz")
        self.assertEqual(len(read_catalog_payloads(snapshot)), 4)

    def test_moxfield_source_falls_back_between_approved_endpoints(self) -> None:
        first = StubMoxfieldClient(NetworkError("primary unavailable"))
        second = StubMoxfieldClient(
            {
                "name": "Fallback Deck",
                "boards": {
                    "mainboard": {
                        "cards": {"tower": {"quantity": 1, "card": {"name": "Command Tower"}}}
                    }
                },
            }
        )
        fetched = MoxfieldDeckSource(clients=(first, second)).fetch(
            "https://www.moxfield.com/decks/public-id"
        )
        self.assertEqual(fetched.deck_name, "Fallback Deck")
        self.assertEqual(first.calls, ["public-id"])
        self.assertEqual(second.calls, ["public-id"])

    def test_moxfield_rate_limit_has_manual_export_fallback(self) -> None:
        source = MoxfieldDeckSource(clients=(StubMoxfieldClient(RateLimitError("limited")),))
        with self.assertRaisesRegex(LocalSourceError, "paste an export") as context:
            source.fetch("https://moxfield.com/decks/public-id")
        self.assertEqual(context.exception.code, "moxfield_rate_limited")
        self.assertTrue(context.exception.retryable)


if __name__ == "__main__":
    unittest.main()
