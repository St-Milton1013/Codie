"""Read-only local preview server for a single Codie share bundle."""

from __future__ import annotations

from dataclasses import dataclass
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from typing import Any


LAN_VISIBLE_HOSTS = {"0.0.0.0", "::"}


@dataclass(frozen=True)
class LocalPreviewConfig:
    bundle_dir: str
    host: str = "127.0.0.1"
    port: int = 0
    allow_lan: bool = False
    open_browser: bool = False

    def __post_init__(self) -> None:
        validate_preview_root(self.bundle_dir)
        if not isinstance(self.host, str) or not self.host.strip():
            raise ValueError("host is required")
        if self.port < 0 or self.port > 65535:
            raise ValueError("port must be between 0 and 65535")
        if self.host in LAN_VISIBLE_HOSTS and not self.allow_lan:
            raise ValueError("LAN-visible host requires allow_lan=True")
        if self.open_browser:
            raise ValueError("open_browser is reserved for a later contract")


class LocalPreviewServer:
    """Serve one share bundle directory through a read-only local HTTP server."""

    def __init__(self, config: LocalPreviewConfig) -> None:
        self.config = config
        self.root = validate_preview_root(config.bundle_dir)
        handler_class = _handler_for_root(self.root)
        self._httpd = ThreadingHTTPServer((config.host, config.port), handler_class)
        self._thread: Thread | None = None

    @property
    def host(self) -> str:
        return str(self._httpd.server_address[0])

    @property
    def port(self) -> int:
        return int(self._httpd.server_address[1])

    @property
    def url(self) -> str:
        return preview_url(self.host, self.port)

    def start(self) -> "LocalPreviewServer":
        if self._thread is not None:
            raise RuntimeError("preview server already started")
        self._thread = Thread(target=self._httpd.serve_forever, daemon=True)
        self._thread.start()
        return self

    def serve_forever(self) -> None:
        """Serve in the current thread until interrupted by the caller."""

        self._httpd.serve_forever()

    def stop(self) -> None:
        self._httpd.shutdown()
        self._httpd.server_close()
        if self._thread is not None:
            self._thread.join(timeout=5)
            self._thread = None

    def close(self) -> None:
        self._httpd.server_close()

    def __enter__(self) -> "LocalPreviewServer":
        return self.start()

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        self.stop()


def validate_preview_root(bundle_dir: str | Path) -> Path:
    """Return a resolved bundle root if it contains a share-bundle index."""

    root = Path(bundle_dir).expanduser().resolve()
    if not root.is_dir():
        raise ValueError("bundle_dir must be an existing directory")
    if not (root / "index.html").is_file():
        raise ValueError("bundle_dir must contain index.html")
    return root


def preview_url(host: str, port: int, path: str = "/index.html") -> str:
    if not isinstance(host, str) or not host.strip():
        raise ValueError("host is required")
    if port <= 0 or port > 65535:
        raise ValueError("port must be between 1 and 65535")
    if not path.startswith("/"):
        raise ValueError("path must start with /")
    return f"http://{host}:{port}{path}"


def _handler_for_root(root: Path) -> type[SimpleHTTPRequestHandler]:
    class BundlePreviewHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, directory=str(root), **kwargs)

        def translate_path(self, path: str) -> str:
            translated = Path(super().translate_path(path)).resolve()
            try:
                translated.relative_to(root)
            except ValueError:
                return str(root / "__codie_forbidden__")
            return str(translated)

        def list_directory(self, path: str):
            self.send_error(403, "Directory listing disabled")
            return None

        def do_POST(self) -> None:
            self._reject_write_method()

        def do_PUT(self) -> None:
            self._reject_write_method()

        def do_PATCH(self) -> None:
            self._reject_write_method()

        def do_DELETE(self) -> None:
            self._reject_write_method()

        def do_OPTIONS(self) -> None:
            self._reject_write_method()

        def _reject_write_method(self) -> None:
            self.send_error(405, "Codie preview is read-only")

        def log_message(self, format: str, *args: Any) -> None:
            return

    return BundlePreviewHandler
