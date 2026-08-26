from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from codie.db.connection import connect
from codie.local_app import LocalAppError, LocalAppService
from codie.local_app.sources import (
    CatalogSnapshotRef,
    FetchedDeck,
    LocalSourceError,
    moxfield_payload_to_deck,
)

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "scryfall"


class FixtureCatalogSource:
    def __init__(self, cards: list[dict]) -> None:
        self.cards = cards
        self.calls: list[bool] = []

    def prepare(self, workspace_root: Path, *, refresh: bool) -> CatalogSnapshotRef:
        cache = workspace_root / "cache" / "fixture-cards.json"
        cache.parent.mkdir(parents=True, exist_ok=True)
        was_cached = cache.exists() and not refresh
        cache.write_text(json.dumps(self.cards), encoding="utf-8")
        self.calls.append(refresh)
        return CatalogSnapshotRef(
            path=cache,
            content_hash="sha256:fixture-card-catalog",
            source_uri="https://data.scryfall.io/fixture.json",
            source_updated_at="2026-08-25T00:00:00+00:00",
            from_cache=was_cached,
        )


class FixtureMoxfieldSource:
    def __init__(self, *, failure: LocalSourceError | None = None) -> None:
        self.failure = failure
        self.calls: list[str] = []

    def fetch(self, source_url: str) -> FetchedDeck:
        self.calls.append(source_url)
        if self.failure is not None:
            raise self.failure
        return FetchedDeck(
            deck_name="Linked Partners",
            decklist=(
                "Commander\n"
                "1 Tymna the Weaver\n"
                "1 Kraum, Ludevic's Opus\n\n"
                "Mainboard\n"
                "1 Command Tower\n"
            ),
            source_url="https://www.moxfield.com/decks/public-id",
        )


class LocalWorkingIterationServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.workspace = self.root / "workspace"
        self.database = self.workspace / "codie.sqlite3"
        self.catalog_source = FixtureCatalogSource(self.fixture_cards())
        self.moxfield_source = FixtureMoxfieldSource()
        self.service = LocalAppService(
            self.workspace,
            self.database,
            catalog_source=self.catalog_source,
            moxfield_source=self.moxfield_source,
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def bootstrap_and_catalog(self) -> None:
        self.service.bootstrap()
        self.service.import_catalog({"snapshot": self.fixture_cards()})

    @staticmethod
    def fixture_cards() -> list[dict]:
        return json.loads((FIXTURE_DIR / "bulk_cards.json").read_text(encoding="utf-8"))

    def test_workspace_path_must_remain_contained(self) -> None:
        with self.assertRaisesRegex(LocalAppError, "inside the workspace"):
            LocalAppService(self.workspace, self.root / "outside.sqlite3")

    def test_bootstrap_is_idempotent_and_reports_contained_paths(self) -> None:
        first = self.service.bootstrap()
        second = self.service.bootstrap()
        summary = self.service.workspace_summary(ui_ready=True)

        self.assertTrue(first["created"])
        self.assertFalse(second["created"])
        self.assertTrue(summary["database_ready"])
        self.assertEqual(summary["database_path"], str(self.database.resolve()))
        self.assertEqual(summary["counts"], {"cards": 0, "decks": 0, "saved_analyses": 0})

    def test_catalog_import_is_card_truth_and_blocking_error_writes_nothing(self) -> None:
        self.service.bootstrap()
        result = self.service.import_catalog(
            {"snapshot": {"object": "list", "data": self.fixture_cards()}}
        )

        self.assertEqual(result["imported_count"], 4)
        self.assertEqual(result["rejected_count"], 0)
        self.assertEqual(result["evidence_class"], "card_truth")
        self.assertTrue(result["snapshot_hash"].startswith("sha256:"))

        valid_new = dict(self.fixture_cards()[0])
        valid_new["id"] = "10000000-0000-0000-0000-000000000001"
        with self.assertRaisesRegex(LocalAppError, "invalid card record"):
            self.service.import_catalog({"snapshot": [valid_new, {"name": "Missing ID"}]})

        connection = connect(self.database)
        try:
            count = connection.execute("SELECT COUNT(*) AS count FROM cards").fetchone()["count"]
            missing = connection.execute(
                "SELECT * FROM cards WHERE scryfall_id = ?", (valid_new["id"],)
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(count, 4)
        self.assertIsNone(missing)

    def test_prepare_catalog_requires_explicit_action_then_bootstraps_and_reuses_cache(
        self,
    ) -> None:
        with self.assertRaisesRegex(LocalAppError, "explicit user action") as context:
            self.service.prepare_catalog({})
        self.assertEqual(context.exception.code, "network_consent_required")
        self.assertFalse(self.database.exists())

        first = self.service.prepare_catalog({"allow_network": True, "refresh": False})
        second = self.service.prepare_catalog({"allow_network": True, "refresh": False})
        refreshed = self.service.prepare_catalog({"allow_network": True, "refresh": True})

        self.assertEqual(first["imported_count"], 4)
        self.assertFalse(first["from_cache"])
        self.assertTrue(second["from_cache"])
        self.assertFalse(refreshed["from_cache"])
        self.assertEqual(self.catalog_source.calls, [False, False, True])
        self.assertTrue(self.service.health(ui_ready=True)["catalog_ready"])

    def test_catalog_skips_only_structurally_valid_names_that_cannot_be_matched(self) -> None:
        self.service.bootstrap()
        unmatchable = dict(self.fixture_cards()[0])
        unmatchable.update(
            {
                "id": "10000000-0000-0000-0000-000000000002",
                "oracle_id": "oracle-unmatchable",
                "name": "_____",
            }
        )
        result = self.service.import_catalog({"snapshot": [self.fixture_cards()[0], unmatchable]})
        self.assertEqual(result["imported_count"], 1)
        self.assertEqual(result["rejected_count"], 1)
        self.assertEqual(len(result["warnings"]), 1)
        self.assertEqual(self.service.workspace_summary(ui_ready=True)["counts"]["cards"], 1)

    def test_deck_import_without_card_data_reports_preparation_not_every_card(self) -> None:
        self.service.bootstrap()
        with self.assertRaisesRegex(LocalAppError, "Prepare Codie's card data") as context:
            self.service.import_deck({"decklist": "Mainboard\n1 Unknown Local Card"})
        self.assertEqual(context.exception.code, "catalog_not_ready")
        self.assertNotIn("unresolved_names", context.exception.details)

    def test_deck_import_is_atomic_and_default_detail_redacts_raw_input(self) -> None:
        self.bootstrap_and_catalog()
        result = self.service.import_deck(
            {
                "deck_name": "Local Partners",
                "decklist": (
                    "Commander\n"
                    "1 Tymna the Weaver\n"
                    "1 Kraum, Ludevic's Opus\n\n"
                    "Mainboard\n"
                    "1 Command Tower\n"
                    "1 Bala Ged Recovery // Bala Ged Sanctuary\n"
                ),
            }
        )
        detail = self.service.get_deck(result["user_deck_id"])

        self.assertEqual(result["card_count"], 4)
        self.assertEqual(detail["summary"]["deck_name"], "Local Partners")
        self.assertNotIn("raw_input", detail)
        self.assertFalse(detail["raw_input_included"])
        self.assertIn("raw_input", self.service.get_deck(result["user_deck_id"], include_raw=True))

        with self.assertRaisesRegex(LocalAppError, "could not be resolved") as context:
            self.service.import_deck(
                {"deck_name": "Rejected", "decklist": "Mainboard\n1 Unknown Local Card"}
            )
        self.assertEqual(context.exception.details["unresolved_names"], ["Unknown Local Card"])
        self.assertEqual(len(self.service.list_decks()["decks"]), 1)

    def test_public_moxfield_link_import_is_explicit_attributed_and_atomic(self) -> None:
        self.bootstrap_and_catalog()
        source_url = "https://www.moxfield.com/decks/public-id"
        with self.assertRaisesRegex(LocalAppError, "explicit user import action"):
            self.service.import_deck({"deck_input": source_url})

        result = self.service.import_deck({"deck_input": source_url, "allow_network": True})
        self.assertEqual(result["source_type"], "moxfield_public_link")
        self.assertEqual(result["source_url"], source_url)
        self.assertEqual(result["card_count"], 3)
        self.assertEqual(self.moxfield_source.calls, [source_url])

        connection = connect(self.database)
        try:
            stored = connection.execute(
                "SELECT deck_name, source_url FROM user_decks WHERE user_deck_id = ?",
                (result["user_deck_id"],),
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(stored["deck_name"], "Linked Partners")
        self.assertEqual(stored["source_url"], source_url)

        failing = LocalAppService(
            self.workspace,
            self.database,
            moxfield_source=FixtureMoxfieldSource(
                failure=LocalSourceError(
                    "moxfield_fetch_failed",
                    "The link could not be loaded; paste its text export instead.",
                )
            ),
        )
        with self.assertRaisesRegex(LocalAppError, "paste its text export"):
            failing.import_deck(
                {"deck_input": "https://moxfield.com/decks/failure", "allow_network": True}
            )
        self.assertEqual(len(self.service.list_decks()["decks"]), 1)

    def test_moxfield_payload_adapter_accepts_public_board_shape(self) -> None:
        fetched = moxfield_payload_to_deck(
            {
                "name": "Board Shape",
                "boards": {
                    "commanders": {
                        "cards": {"tymna": {"quantity": 1, "card": {"name": "Tymna the Weaver"}}}
                    },
                    "mainboard": {
                        "cards": {"tower": {"quantity": 1, "card": {"name": "Command Tower"}}}
                    },
                },
            },
            public_id="board-shape",
        )
        self.assertEqual(fetched.deck_name, "Board Shape")
        self.assertIn("Commander\n1 Tymna the Weaver", fetched.decklist)
        self.assertIn("Mainboard\n1 Command Tower", fetched.decklist)

    def test_comparison_persists_deterministically_and_exports_provenance(self) -> None:
        self.bootstrap_and_catalog()
        imported = self.service.import_deck(
            {"deck_name": "Evidence Deck", "decklist": "Mainboard\n1 Command Tower"}
        )
        request = {
            "candidates": [
                {
                    "oracle_id": "44444444-4444-4444-4444-444444444444",
                    "card_name": "Command Tower",
                    "evidence_type": "tournament_evidence",
                    "score": 0.8,
                    "sample_size": 24,
                    "source_record_id": "event:24:command-tower",
                    "source_url": "https://example.test/tournament/24",
                },
                {
                    "oracle_id": "oracle-absent",
                    "card_name": "Absent Evidence Card",
                    "evidence_type": "community_signal",
                    "sample_size": 3,
                    "source_record_id": "community:3:absent",
                },
            ]
        }

        result = self.service.compare_deck(imported["user_deck_id"], request)
        analyses = self.service.list_analyses(imported["user_deck_id"])["analyses"]
        detail = self.service.get_analysis(result["saved_analysis_id"])
        json_export = self.service.export_analysis(result["saved_analysis_id"], "json")
        markdown_export = self.service.export_analysis(result["saved_analysis_id"], "markdown")

        self.assertEqual(len(analyses), 1)
        self.assertEqual(detail["comparison"]["present_count"], 1)
        self.assertEqual(detail["comparison"]["absent_count"], 1)
        self.assertEqual(
            [row["evidence_type"] for row in detail["comparison"]["rows"]],
            ["community_signal", "tournament_evidence"],
        )
        self.assertIn("event:24:command-tower", json_export["content"])
        self.assertIn("tournament_evidence", markdown_export["content"])
        self.assertEqual(markdown_export["media_type"], "text/markdown")

    def test_evidence_packet_rejects_advice_and_hareruya_non_tournament_scope(self) -> None:
        self.bootstrap_and_catalog()
        imported = self.service.import_deck(
            {"deck_name": "Boundary Deck", "decklist": "Mainboard\n1 Command Tower"}
        )
        base = {
            "oracle_id": "oracle-card",
            "card_name": "Card",
            "sample_size": 2,
        }
        with self.assertRaisesRegex(LocalAppError, "strategic advice"):
            self.service.compare_deck(
                imported["user_deck_id"],
                {"candidates": [{**base, "evidence_type": "recommendation_candidate"}]},
            )
        with self.assertRaisesRegex(LocalAppError, "tournament evidence"):
            self.service.compare_deck(
                imported["user_deck_id"],
                {
                    "candidates": [
                        {
                            **base,
                            "evidence_type": "community_signal",
                            "source_url": "https://www.hareruya.com/deck/1",
                        }
                    ]
                },
            )
        self.assertEqual(self.service.list_analyses(imported["user_deck_id"])["analyses"], [])

    def test_unknown_records_and_unsafe_export_fail_closed(self) -> None:
        self.bootstrap_and_catalog()
        with self.assertRaisesRegex(LocalAppError, "not found"):
            self.service.get_deck(404)
        with self.assertRaisesRegex(LocalAppError, "not found"):
            self.service.get_analysis(404)
        with self.assertRaisesRegex(LocalAppError, "json or markdown"):
            self.service.export_analysis(404, "html")

    def test_local_app_limits_provider_coupling_to_approved_user_initiated_sources(self) -> None:
        local_app_root = Path(__file__).parents[1] / "codie" / "local_app"
        source = "\n".join(
            path.read_text(encoding="utf-8") for path in sorted(local_app_root.glob("*.py"))
        )
        forbidden = (
            "codie.providers.hareruya",
            "codie.providers.topdeck",
            "codie.recommendations",
            "requests.",
            "opentelemetry",
            "sentry_sdk",
            "StreamDeck",
        )
        for fragment in forbidden:
            self.assertNotIn(fragment, source)
        self.assertIn("codie.providers.moxfield", source)
        self.assertIn("urllib.request", source)


if __name__ == "__main__":
    unittest.main()
