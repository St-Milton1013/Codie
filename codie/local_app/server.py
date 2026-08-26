"""Loopback-only HTTP and static UI adapter for the Codie local application."""

from __future__ import annotations

import ipaddress
import json
import mimetypes
import re
from collections.abc import Mapping
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from typing import Any
from urllib.parse import parse_qs, unquote, urlsplit

from .service import LocalAppError, LocalAppService

DEFAULT_PORT = 8765
DEFAULT_MAX_PAYLOAD_BYTES = 256 * 1024 * 1024
LOOPBACK_HOSTS = frozenset({"127.0.0.1", "localhost", "::1"})
_DECK_RE = re.compile(r"^/local/decks/(?P<deck_id>\d+)$")
_COMPARISON_RE = re.compile(r"^/local/decks/(?P<deck_id>\d+)/comparisons$")
_ANALYSES_RE = re.compile(r"^/local/decks/(?P<deck_id>\d+)/analyses$")
_ANALYSIS_RE = re.compile(r"^/local/analyses/(?P<analysis_id>\d+)$")
_EXPORT_RE = re.compile(r"^/local/analyses/(?P<analysis_id>\d+)/export$")


@dataclass(frozen=True)
class LocalAppConfig:
    workspace_root: str
    ui_root: str
    database_name: str = "codie.sqlite3"
    host: str = "127.0.0.1"
    port: int = DEFAULT_PORT
    max_payload_bytes: int = DEFAULT_MAX_PAYLOAD_BYTES

    def __post_init__(self) -> None:
        if self.host not in LOOPBACK_HOSTS:
            raise ValueError("Codie local app host must be loopback-only")
        if self.port < 0 or self.port > 65535:
            raise ValueError("port must be between 0 and 65535")
        if self.max_payload_bytes < 1:
            raise ValueError("max_payload_bytes must be positive")
        workspace = Path(self.workspace_root).expanduser().resolve()
        database = (workspace / self.database_name).resolve()
        try:
            database.relative_to(workspace)
        except ValueError as exc:
            raise ValueError("database_name must remain inside workspace_root") from exc

    @property
    def resolved_workspace_root(self) -> Path:
        return Path(self.workspace_root).expanduser().resolve()

    @property
    def resolved_ui_root(self) -> Path:
        return Path(self.ui_root).expanduser().resolve()

    @property
    def database_path(self) -> Path:
        return (self.resolved_workspace_root / self.database_name).resolve()


class _LocalThreadingHTTPServer(ThreadingHTTPServer):
    daemon_threads = True


class LocalAppServer:
    """Serve the local API and built React UI from one loopback origin."""

    def __init__(self, config: LocalAppConfig, service: LocalAppService | None = None) -> None:
        self.config = config
        self.ui_root = config.resolved_ui_root
        self.service = service or LocalAppService(
            config.resolved_workspace_root,
            config.database_path,
        )
        handler = _handler_for(self)
        self._httpd = _LocalThreadingHTTPServer((config.host, config.port), handler)
        self._thread: Thread | None = None

    @property
    def host(self) -> str:
        return str(self._httpd.server_address[0])

    @property
    def port(self) -> int:
        return int(self._httpd.server_address[1])

    @property
    def url(self) -> str:
        return local_app_url(self.host, self.port)

    @property
    def ui_ready(self) -> bool:
        return (self.ui_root / "index.html").is_file()

    def start(self) -> LocalAppServer:
        if self._thread is not None:
            raise RuntimeError("local app server already started")
        self._thread = Thread(target=self._httpd.serve_forever, daemon=True)
        self._thread.start()
        return self

    def serve_forever(self) -> None:
        self._httpd.serve_forever()

    def stop(self) -> None:
        self._httpd.shutdown()
        self._httpd.server_close()
        if self._thread is not None:
            self._thread.join(timeout=5)
            self._thread = None

    def close(self) -> None:
        self._httpd.server_close()

    def __enter__(self) -> LocalAppServer:
        return self.start()

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        self.stop()


def local_app_url(host: str, port: int) -> str:
    if host not in LOOPBACK_HOSTS:
        raise ValueError("host must be loopback-only")
    if port < 1 or port > 65535:
        raise ValueError("port must be between 1 and 65535")
    visible_host = f"[{host}]" if ":" in host else host
    return f"http://{visible_host}:{port}/"


def _handler_for(app: LocalAppServer) -> type[BaseHTTPRequestHandler]:
    class LocalAppHandler(BaseHTTPRequestHandler):
        server_version = "CodieLocal/0.1"

        def do_GET(self) -> None:
            if not self._request_is_local():
                self._error(
                    LocalAppError("non_loopback_request", "Loopback requests only.", status=403)
                )
                return
            parts = urlsplit(self.path)
            if parts.path.startswith("/local/"):
                self._handle_local_get(parts.path, parse_qs(parts.query))
                return
            self._serve_static(parts.path, send_body=True)

        def do_HEAD(self) -> None:
            if not self._request_is_local():
                self._error(
                    LocalAppError("non_loopback_request", "Loopback requests only.", status=403)
                )
                return
            parts = urlsplit(self.path)
            if parts.path.startswith("/local/"):
                self._error(
                    LocalAppError(
                        "method_not_allowed", "HEAD is not allowed for this route.", status=405
                    )
                )
                return
            self._serve_static(parts.path, send_body=False)

        def do_POST(self) -> None:
            if not self._request_is_local():
                self._error(
                    LocalAppError("non_loopback_request", "Loopback requests only.", status=403)
                )
                return
            parts = urlsplit(self.path)
            if not parts.path.startswith("/local/"):
                self._error(
                    LocalAppError("method_not_allowed", "Static assets are read-only.", status=405)
                )
                return
            try:
                request = self._read_json_request()
                self._handle_local_post(parts.path, request)
            except LocalAppError as exc:
                self._error(exc)
            except Exception:
                self._error(
                    LocalAppError(
                        "internal_error",
                        "The local request failed without saving partial state.",
                        status=500,
                    )
                )

        def do_PUT(self) -> None:
            self._method_not_allowed()

        def do_PATCH(self) -> None:
            self._method_not_allowed()

        def do_DELETE(self) -> None:
            self._method_not_allowed()

        def do_OPTIONS(self) -> None:
            self._method_not_allowed()

        def _handle_local_get(self, path: str, query: dict[str, list[str]]) -> None:
            try:
                if path == "/local/health":
                    self._success(app.service.health(ui_ready=app.ui_ready))
                    return
                if path == "/local/workspace":
                    self._success(app.service.workspace_summary(ui_ready=app.ui_ready))
                    return
                if path == "/local/decks":
                    self._success(app.service.list_decks())
                    return
                match = _DECK_RE.fullmatch(path)
                if match:
                    include_raw = query.get("include_raw", ["false"])[0].lower() == "true"
                    self._success(
                        app.service.get_deck(int(match.group("deck_id")), include_raw=include_raw)
                    )
                    return
                match = _ANALYSES_RE.fullmatch(path)
                if match:
                    self._success(app.service.list_analyses(int(match.group("deck_id"))))
                    return
                match = _ANALYSIS_RE.fullmatch(path)
                if match:
                    self._success(app.service.get_analysis(int(match.group("analysis_id"))))
                    return
                match = _EXPORT_RE.fullmatch(path)
                if match:
                    export_format = query.get("format", [""])[0]
                    self._success(
                        app.service.export_analysis(int(match.group("analysis_id")), export_format)
                    )
                    return
                raise LocalAppError(
                    "route_not_found", "The requested local route was not found.", status=404
                )
            except LocalAppError as exc:
                self._error(exc)
            except Exception:
                self._error(
                    LocalAppError(
                        "internal_error",
                        "The local request failed without exposing private details.",
                        status=500,
                    )
                )

        def _handle_local_post(self, path: str, request: dict[str, Any]) -> None:
            if path == "/local/database/bootstrap":
                self._success(app.service.bootstrap())
                return
            if path == "/local/catalog/import":
                self._success(app.service.import_catalog(request))
                return
            if path == "/local/catalog/prepare":
                self._success(app.service.prepare_catalog(request))
                return
            if path == "/local/decks/import":
                self._success(app.service.import_deck(request))
                return
            match = _COMPARISON_RE.fullmatch(path)
            if match:
                self._success(app.service.compare_deck(int(match.group("deck_id")), request))
                return
            raise LocalAppError(
                "route_not_found", "The requested local route was not found.", status=404
            )

        def _read_json_request(self) -> dict[str, Any]:
            content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
            if content_type != "application/json":
                raise LocalAppError(
                    "unsupported_content_type",
                    "Local API requests must use application/json.",
                    status=415,
                    field="Content-Type",
                )
            raw_length = self.headers.get("Content-Length")
            if raw_length is None:
                raise LocalAppError(
                    "content_length_required",
                    "Content-Length is required.",
                    status=411,
                    field="Content-Length",
                )
            try:
                length = int(raw_length)
            except ValueError as exc:
                raise LocalAppError(
                    "invalid_content_length",
                    "Content-Length must be a non-negative integer.",
                    status=400,
                    field="Content-Length",
                ) from exc
            if length < 0:
                raise LocalAppError(
                    "invalid_content_length",
                    "Content-Length must be a non-negative integer.",
                    status=400,
                    field="Content-Length",
                )
            if length > app.config.max_payload_bytes:
                raise LocalAppError(
                    "payload_too_large",
                    "The selected local payload exceeds the configured size limit.",
                    status=413,
                )
            body = self.rfile.read(length)
            if len(body) != length:
                raise LocalAppError(
                    "incomplete_request", "The request body was incomplete.", status=400
                )
            try:
                decoded = body.decode("utf-8")
                payload = json.loads(decoded)
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise LocalAppError(
                    "malformed_json", "The request body is not valid JSON.", status=400
                ) from exc
            if not isinstance(payload, dict):
                raise LocalAppError(
                    "invalid_request", "The request body must be a JSON object.", status=422
                )
            return payload

        def _serve_static(self, path: str, *, send_body: bool) -> None:
            if not app.ui_ready:
                self._error(
                    LocalAppError(
                        "ui_not_built",
                        "The local UI has not been built. Run the documented setup command.",
                        status=503,
                    )
                )
                return
            requested = unquote(path)
            relative = "index.html" if requested in {"", "/"} else requested.lstrip("/")
            candidate = (app.ui_root / relative).resolve()
            try:
                candidate.relative_to(app.ui_root)
            except ValueError:
                self._error(
                    LocalAppError(
                        "static_path_escape", "Static path is outside the UI root.", status=403
                    )
                )
                return
            if not candidate.is_file():
                self._error(
                    LocalAppError("static_not_found", "Static asset was not found.", status=404)
                )
                return
            content = candidate.read_bytes()
            media_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
            self.send_response(200)
            self.send_header(
                "Content-Type",
                f"{media_type}; charset=utf-8" if media_type.startswith("text/") else media_type,
            )
            self.send_header("Content-Length", str(len(content)))
            self.send_header(
                "Cache-Control",
                "no-store" if candidate.name == "index.html" else "public, max-age=3600",
            )
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            if send_body:
                self.wfile.write(content)

        def _success(self, data: Mapping[str, Any], *, status: int = 200) -> None:
            self._json(status, {"ok": True, "data": data})

        def _error(self, error: LocalAppError) -> None:
            payload: dict[str, Any] = {
                "code": error.code,
                "message": error.message,
            }
            if error.field is not None:
                payload["field"] = error.field
            if error.details:
                payload["details"] = error.details
            self._json(error.status, {"ok": False, "error": payload})

        def _json(self, status: int, payload: Mapping[str, Any]) -> None:
            body = json.dumps(
                payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
            ).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.end_headers()
            self.wfile.write(body)

        def _request_is_local(self) -> bool:
            try:
                address = ipaddress.ip_address(self.client_address[0])
            except ValueError:
                return False
            if not address.is_loopback:
                return False
            host_header = self.headers.get("Host", "").strip().lower()
            if not host_header:
                return False
            host_name = host_header
            if host_header.startswith("["):
                host_name = host_header.split("]", 1)[0] + "]"
            elif ":" in host_header:
                host_name = host_header.split(":", 1)[0]
            return host_name in {"127.0.0.1", "localhost", "[::1]"}

        def _method_not_allowed(self) -> None:
            self._error(LocalAppError("method_not_allowed", "Method not allowed.", status=405))

        def log_message(self, format: str, *args: Any) -> None:
            return

    return LocalAppHandler
