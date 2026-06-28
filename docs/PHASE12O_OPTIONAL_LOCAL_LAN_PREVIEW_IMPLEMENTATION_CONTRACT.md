# Phase 12O - Optional Local LAN Preview Implementation Contract

## Purpose

Implement an optional local static preview server for one selected Codie share
bundle.

This is not hosted sharing, outbound delivery, a public tunnel, or a backend
API.

## Scope

```text
codie/delivery/__init__.py
codie/delivery/local_preview.py
codie/cli/user_deck.py
tests/test_delivery_local_preview.py
tests/test_cli_user_deck.py
docs/USER_GUIDE_LOCAL_REPORT_SHARING.md
docs/PHASE12O_OPTIONAL_LOCAL_LAN_PREVIEW_IMPLEMENTATION_CONTRACT.md
docs/PHASE12O_OPTIONAL_LOCAL_LAN_PREVIEW_IMPLEMENTATION_REPORT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Functions / Classes

```text
LocalPreviewConfig
LocalPreviewServer
validate_preview_root(...)
preview_url(...)
```

## CLI Command

```text
serve-share-bundle
```

Arguments:

```text
--bundle-dir
--host
--port
--allow-lan
```

Defaults:

```text
host = 127.0.0.1
port = 0
allow_lan = false
```

## Schema Impact

None.

## Dependency Impact

None.

## Rules

- Serve only the selected bundle directory.
- Require `index.html` in the bundle root.
- Reject LAN-visible hosts such as `0.0.0.0` unless `--allow-lan` is supplied.
- Allow only `GET` and `HEAD`.
- Reject write methods with `405`.
- Disable directory listing.
- Reject path traversal by resolving paths against the locked bundle root.
- Print the served directory and URL before serving.
- Print a privacy warning in the CLI result.
- Use standard library HTTP serving.

## Forbidden Behavior

- No provider imports.
- No database/repository imports.
- No analytics imports.
- No recommendation imports.
- No upload endpoint.
- No public tunnel.
- No outbound delivery.
- No background daemon.
- No schema changes.

## Tests

```text
validate_preview_root accepts bundle directory with index.html
validate_preview_root rejects missing index.html
default host is 127.0.0.1
0.0.0.0 requires allow_lan=True
server serves index.html
server serves assets inside bundle
server does not serve sibling files
HEAD works
POST/PUT/DELETE are rejected
directory listing is disabled
delivery module has no forbidden imports
CLI parser defaults to localhost
```
