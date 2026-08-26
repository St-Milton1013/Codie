"""Command-line launcher for the Codie local working iteration."""

from __future__ import annotations

import argparse
import os
import webbrowser
from pathlib import Path

from .server import DEFAULT_PORT, LocalAppConfig, LocalAppServer

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Codie on a loopback-only local server.")
    parser.add_argument(
        "--workspace-root",
        default=str(REPOSITORY_ROOT / "work" / "local-codie"),
        help="Contained directory for Codie's local SQLite workspace.",
    )
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--open-browser", action="store_true")
    args = parser.parse_args()

    config = LocalAppConfig(
        workspace_root=args.workspace_root,
        ui_root=str(REPOSITORY_ROOT / "ui" / "dist"),
        port=args.port,
    )
    server = LocalAppServer(config)
    if not server.ui_ready:
        parser.error("ui/dist/index.html is missing; run scripts/setup-codie-ui.ps1 first")

    print("Codie Local Working Iteration v0.1")
    print(f"URL: {server.url}")
    print(f"Workspace: {config.resolved_workspace_root}")
    print(f"Database: {config.database_path}")
    print(f"Process ID: {os.getpid()}")
    print("Privacy: loopback-only, local persistence, no telemetry or background fetches")
    print("Remote access: only after Prepare/Refresh or public Moxfield import")
    print("Stop: press Ctrl+C in this PowerShell window")
    if args.open_browser:
        webbrowser.open(server.url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping Codie.")
    finally:
        server.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
