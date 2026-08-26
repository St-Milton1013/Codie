from __future__ import annotations

import http.client
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from codie.local_app import LocalAppConfig, LocalAppServer

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "scryfall"


class LocalWorkingIterationHttpTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.workspace = self.root / "workspace"
        self.ui = self.root / "ui"
        (self.ui / "assets").mkdir(parents=True)
        (self.ui / "index.html").write_text("<html>Codie local</html>", encoding="utf-8")
        (self.ui / "assets" / "app.js").write_text("console.log('local')", encoding="utf-8")
        config = LocalAppConfig(
            workspace_root=str(self.workspace),
            ui_root=str(self.ui),
            port=0,
            max_payload_bytes=1024 * 1024,
        )
        self.server = LocalAppServer(config).start()

    def tearDown(self) -> None:
        self.server.stop()
        self.temporary_directory.cleanup()

    def request(
        self,
        method: str,
        path: str,
        body: bytes | None = None,
        headers: dict[str, str] | None = None,
    ) -> tuple[int, dict]:
        connection = http.client.HTTPConnection(self.server.host, self.server.port, timeout=5)
        try:
            connection.request(method, path, body=body, headers=headers or {})
            response = connection.getresponse()
            payload = json.loads(response.read().decode("utf-8"))
            return response.status, payload
        finally:
            connection.close()

    def post(self, path: str, payload: dict) -> tuple[int, dict]:
        return self.request(
            "POST",
            path,
            json.dumps(payload).encode("utf-8"),
            {"Content-Type": "application/json"},
        )

    def test_config_and_host_header_enforce_loopback_only(self) -> None:
        with self.assertRaisesRegex(ValueError, "loopback-only"):
            LocalAppConfig(workspace_root=str(self.workspace), ui_root=str(self.ui), host="0.0.0.0")

        connection = http.client.HTTPConnection(self.server.host, self.server.port, timeout=5)
        try:
            connection.putrequest("GET", "/local/health", skip_host=True)
            connection.putheader("Host", "example.com")
            connection.endheaders()
            response = connection.getresponse()
            payload = json.loads(response.read())
        finally:
            connection.close()
        self.assertEqual(response.status, 403)
        self.assertEqual(payload["error"]["code"], "non_loopback_request")

    def test_page_load_is_read_only_and_static_paths_are_contained(self) -> None:
        connection = http.client.HTTPConnection(self.server.host, self.server.port, timeout=5)
        try:
            connection.request("GET", "/")
            index_response = connection.getresponse()
            index = index_response.read()
            connection.request("GET", "/assets/app.js")
            asset_response = connection.getresponse()
            asset = asset_response.read()
            connection.request("GET", "/%2e%2e/private.txt")
            escaped_response = connection.getresponse()
            escaped_response.read()
        finally:
            connection.close()

        self.assertEqual(index_response.status, 200)
        self.assertIn(b"Codie local", index)
        self.assertEqual(asset_response.status, 200)
        self.assertIn(b"console.log", asset)
        self.assertIn(escaped_response.status, {403, 404})
        self.assertFalse((self.workspace / "codie.sqlite3").exists())

    def test_request_contract_rejects_method_content_type_json_and_size_failures(self) -> None:
        status, payload = self.request("PUT", "/local/workspace")
        self.assertEqual(status, 405)
        self.assertEqual(payload["error"]["code"], "method_not_allowed")

        status, payload = self.request(
            "POST",
            "/local/database/bootstrap",
            b"{}",
            {"Content-Type": "text/plain"},
        )
        self.assertEqual(status, 415)
        self.assertEqual(payload["error"]["code"], "unsupported_content_type")

        status, payload = self.request(
            "POST",
            "/local/database/bootstrap",
            b"{",
            {"Content-Type": "application/json"},
        )
        self.assertEqual(status, 400)
        self.assertEqual(payload["error"]["code"], "malformed_json")

        connection = http.client.HTTPConnection(self.server.host, self.server.port, timeout=5)
        try:
            connection.putrequest("POST", "/local/database/bootstrap")
            connection.putheader("Content-Type", "application/json")
            connection.endheaders()
            response = connection.getresponse()
            missing_length = json.loads(response.read())
        finally:
            connection.close()
        self.assertEqual(response.status, 411)
        self.assertEqual(missing_length["error"]["code"], "content_length_required")

        small_server = LocalAppServer(
            LocalAppConfig(
                workspace_root=str(self.root / "small-workspace"),
                ui_root=str(self.ui),
                port=0,
                max_payload_bytes=8,
            )
        ).start()
        try:
            connection = http.client.HTTPConnection(small_server.host, small_server.port, timeout=5)
            connection.request(
                "POST",
                "/local/database/bootstrap",
                body=b'{"long":true}',
                headers={"Content-Type": "application/json"},
            )
            response = connection.getresponse()
            payload = json.loads(response.read())
            connection.close()
        finally:
            small_server.stop()
        self.assertEqual(response.status, 413)
        self.assertEqual(payload["error"]["code"], "payload_too_large")

    def test_http_vertical_slice_persists_and_exports_evidence(self) -> None:
        status, _ = self.post("/local/database/bootstrap", {})
        self.assertEqual(status, 200)
        cards = json.loads((FIXTURE_DIR / "bulk_cards.json").read_text(encoding="utf-8"))
        status, catalog = self.post("/local/catalog/import", {"snapshot": cards})
        self.assertEqual(status, 200)
        self.assertEqual(catalog["data"]["imported_count"], 4)

        status, imported = self.post(
            "/local/decks/import",
            {"deck_name": "HTTP Deck", "decklist": "Mainboard\n1 Command Tower"},
        )
        self.assertEqual(status, 200)
        deck_id = imported["data"]["user_deck_id"]

        status, comparison = self.post(
            f"/local/decks/{deck_id}/comparisons",
            {
                "candidates": [
                    {
                        "oracle_id": "44444444-4444-4444-4444-444444444444",
                        "card_name": "Command Tower",
                        "evidence_type": "tournament_evidence",
                        "sample_size": 5,
                        "source_record_id": "event:5:tower",
                    }
                ]
            },
        )
        self.assertEqual(status, 200)
        analysis_id = comparison["data"]["saved_analysis_id"]

        status, decks = self.request("GET", "/local/decks")
        self.assertEqual(status, 200)
        self.assertEqual(decks["data"]["decks"][0]["saved_analysis_count"], 1)
        self.assertNotIn("raw_input", decks["data"]["decks"][0])

        status, detail = self.request("GET", f"/local/analyses/{analysis_id}")
        self.assertEqual(status, 200)
        self.assertEqual(
            detail["data"]["comparison"]["rows"][0]["evidence_type"], "tournament_evidence"
        )

        status, exported = self.request(
            "GET", f"/local/analyses/{analysis_id}/export?format=markdown"
        )
        self.assertEqual(status, 200)
        self.assertEqual(exported["data"]["media_type"], "text/markdown")
        self.assertIn("event:5:tower", exported["data"]["content"])

    def test_prepare_route_requires_explicit_network_consent(self) -> None:
        status, rejected = self.post("/local/catalog/prepare", {"refresh": False})
        self.assertEqual(status, 422)
        self.assertEqual(rejected["error"]["code"], "network_consent_required")
        self.assertFalse((self.workspace / "codie.sqlite3").exists())

    def test_unresolved_deck_and_internal_error_are_redacted(self) -> None:
        self.post("/local/database/bootstrap", {})
        status, not_ready = self.post(
            "/local/decks/import",
            {"deck_name": "Rejected", "decklist": "Mainboard\n1 Missing Card"},
        )
        self.assertEqual(status, 409)
        self.assertEqual(not_ready["error"]["code"], "catalog_not_ready")
        self.assertNotIn("details", not_ready["error"])

        cards = json.loads((FIXTURE_DIR / "bulk_cards.json").read_text(encoding="utf-8"))
        self.post("/local/catalog/import", {"snapshot": cards})
        status, unresolved = self.post(
            "/local/decks/import",
            {"deck_name": "Rejected", "decklist": "Mainboard\n1 Missing Card"},
        )
        self.assertEqual(status, 422)
        self.assertEqual(unresolved["error"]["details"]["unresolved_names"], ["Missing Card"])
        status, decks = self.request("GET", "/local/decks")
        self.assertEqual(decks["data"]["decks"], [])

        original = self.server.service.health
        self.server.service.health = Mock(side_effect=RuntimeError("private traceback secret"))
        try:
            status, failure = self.request("GET", "/local/health")
        finally:
            self.server.service.health = original
        serialized = json.dumps(failure).lower()
        self.assertEqual(status, 500)
        self.assertNotIn("traceback", serialized)
        self.assertNotIn("secret", serialized)

    def test_server_stop_releases_the_loopback_listener(self) -> None:
        stopped_server = LocalAppServer(
            LocalAppConfig(
                workspace_root=str(self.root / "stopped-workspace"),
                ui_root=str(self.ui),
                port=0,
            )
        ).start()
        host, port = stopped_server.host, stopped_server.port
        stopped_server.stop()

        connection = http.client.HTTPConnection(host, port, timeout=1)
        try:
            with self.assertRaises(OSError):
                connection.request("GET", "/local/health")
        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main()
