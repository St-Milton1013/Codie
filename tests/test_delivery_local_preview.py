from __future__ import annotations

import http.client
import tempfile
import unittest
from pathlib import Path

from codie.delivery import (
    LocalPreviewConfig,
    LocalPreviewServer,
    preview_url,
    validate_preview_root,
)


class LocalPreviewDeliveryTest(unittest.TestCase):
    def test_validate_preview_root_accepts_bundle_with_index(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text("ok", encoding="utf-8")

            self.assertEqual(validate_preview_root(root), root.resolve())

    def test_validate_preview_root_rejects_missing_index(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                validate_preview_root(directory)

    def test_config_defaults_to_localhost_and_requires_explicit_lan(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text("ok", encoding="utf-8")

            config = LocalPreviewConfig(bundle_dir=str(root))

            self.assertEqual(config.host, "127.0.0.1")
            self.assertEqual(config.port, 0)
            with self.assertRaises(ValueError):
                LocalPreviewConfig(bundle_dir=str(root), host="0.0.0.0")
            lan_config = LocalPreviewConfig(bundle_dir=str(root), host="0.0.0.0", allow_lan=True)
            self.assertTrue(lan_config.allow_lan)

    def test_preview_url_validates_inputs(self) -> None:
        self.assertEqual(preview_url("127.0.0.1", 8000), "http://127.0.0.1:8000/index.html")
        with self.assertRaises(ValueError):
            preview_url("", 8000)
        with self.assertRaises(ValueError):
            preview_url("127.0.0.1", 0)
        with self.assertRaises(ValueError):
            preview_url("127.0.0.1", 8000, "index.html")

    def test_server_serves_selected_bundle_files_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            root = parent / "bundle"
            assets = root / "assets"
            assets.mkdir(parents=True)
            (root / "index.html").write_text("bundle index", encoding="utf-8")
            (assets / "report.md").write_text("report", encoding="utf-8")
            (parent / "sibling.txt").write_text("sibling", encoding="utf-8")

            with LocalPreviewServer(LocalPreviewConfig(bundle_dir=str(root))) as server:
                index = _request(server, "GET", "/index.html")
                asset = _request(server, "GET", "/assets/report.md")
                sibling = _request(server, "GET", "/../sibling.txt")
                encoded_sibling = _request(server, "GET", "/%2e%2e/sibling.txt")

            self.assertEqual(index.status, 200)
            self.assertEqual(index.body, b"bundle index")
            self.assertEqual(asset.status, 200)
            self.assertEqual(asset.body, b"report")
            self.assertIn(sibling.status, {403, 404})
            self.assertIn(encoded_sibling.status, {403, 404})

    def test_server_allows_head_and_rejects_write_methods(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text("bundle index", encoding="utf-8")

            with LocalPreviewServer(LocalPreviewConfig(bundle_dir=str(root))) as server:
                head = _request(server, "HEAD", "/index.html")
                post = _request(server, "POST", "/index.html")
                put = _request(server, "PUT", "/index.html")
                delete = _request(server, "DELETE", "/index.html")

            self.assertEqual(head.status, 200)
            self.assertEqual(post.status, 405)
            self.assertEqual(put.status, 405)
            self.assertEqual(delete.status, 405)

    def test_directory_listing_is_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            assets = root / "assets"
            assets.mkdir()
            (root / "index.html").write_text("bundle index", encoding="utf-8")
            (assets / "report.md").write_text("report", encoding="utf-8")

            with LocalPreviewServer(LocalPreviewConfig(bundle_dir=str(root))) as server:
                response = _request(server, "GET", "/assets/")

            self.assertEqual(response.status, 403)

    def test_delivery_module_has_no_forbidden_imports(self) -> None:
        import codie.delivery.local_preview as local_preview

        source = Path(local_preview.__file__).read_text(encoding="utf-8")
        forbidden = (
            "codie.providers",
            "codie.db",
            "codie.analytics",
            "codie.recommendations",
            "sqlite3",
            "source_events",
            "source_decks",
            "provider_objects",
        )
        for pattern in forbidden:
            self.assertNotIn(pattern, source)


class Response:
    def __init__(self, status: int, body: bytes) -> None:
        self.status = status
        self.body = body


def _request(server: LocalPreviewServer, method: str, path: str) -> Response:
    connection = http.client.HTTPConnection(server.host, server.port, timeout=5)
    try:
        connection.request(method, path)
        response = connection.getresponse()
        return Response(response.status, response.read())
    finally:
        connection.close()


if __name__ == "__main__":
    unittest.main()
