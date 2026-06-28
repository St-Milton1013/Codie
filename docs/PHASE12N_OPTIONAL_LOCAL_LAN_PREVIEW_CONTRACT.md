# Phase 12N - Optional Local LAN Preview Contract

## Purpose

Define the rules for a future optional local LAN preview command that can serve
one generated Codie share bundle to another device on the same trusted network.

This is a planning-only packet. It does not add a server.

## Intended Future Behavior

A future command may:

```text
serve one selected share bundle directory
print the local URL
print the LAN URL when available
optionally generate or update a QR target for that URL
stop when the command exits
```

## Scope For Future Implementation

Potential future files:

```text
codie/delivery/local_preview.py
codie/delivery/__init__.py
tests/test_delivery_local_preview.py
docs/PHASE12O_OPTIONAL_LOCAL_LAN_PREVIEW_IMPLEMENTATION_CONTRACT.md
```

No files are created in those paths during Phase 12N.

## Public Interface Shape

Future Python API:

```text
LocalPreviewConfig
LocalPreviewServer
validate_preview_root(...)
preview_url(...)
```

Future CLI command:

```text
serve-share-bundle
```

Possible flags:

```text
--bundle-dir
--host
--port
--open-browser
--qr-target-out
```

## Required Defaults

```text
host = 127.0.0.1
port = 0
open_browser = false
serve_selected_bundle_only = true
read_only = true
```

`port = 0` means the operating system chooses an available port.

LAN binding such as `0.0.0.0` must be explicit.

## Hard Safety Rules

The future server must:

```text
serve only the selected bundle directory
refuse paths outside the bundle root
serve files read-only
reject upload methods
reject path traversal
not import providers
not import database/repositories
not import analytics
not import recommendations
not read source/provider tables
not start automatically
not run in the background unless explicitly requested by a later contract
```

## Allowed HTTP Methods

Allowed:

```text
GET
HEAD
```

Rejected:

```text
POST
PUT
PATCH
DELETE
OPTIONS for state-changing behavior
```

## Privacy Rules

- Serving a bundle exposes its files to clients that can reach the bound host
  and port.
- The command must print a privacy warning before serving on a LAN-visible
  address.
- The command must display the exact directory being served.
- The command must display the exact URL.
- No public tunnel or hosted link may be created.
- No credentials are accepted or stored.

## Test Requirements For Future Implementation

```text
validate_preview_root accepts bundle directory with index.html
validate_preview_root rejects missing index.html
path traversal is rejected
POST/PUT/DELETE are rejected
server serves index.html
server serves assets inside bundle
server does not serve sibling files
default host is 127.0.0.1
0.0.0.0 requires explicit user selection
no forbidden imports in delivery module
```

## Recommended Implementation Plan

1. Create `codie/delivery/local_preview.py`.
2. Use Python standard library HTTP serving where possible.
3. Resolve and lock the bundle root before serving.
4. Override request handling to enforce root containment.
5. Add focused tests using localhost only.
6. Add CLI command after the module has tests.
7. Update local sharing guide with the LAN preview workflow.

## Do Not Do In Phase 12N

- Do not add server code.
- Do not add dependencies.
- Do not add CLI command.
- Do not open firewall ports.
- Do not start background processes.
- Do not add public tunnels.
- Do not add Discord/email/cloud delivery.
- Do not change schema.
- Do not change recommendation logic.
