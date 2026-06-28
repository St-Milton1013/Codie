# Phase 12L - Optional Delivery Integrations Planning Contract

## Purpose

Define how Codie may eventually move local report bundles to a phone or other
device without creating hidden network behavior or leaking private deck data.

This is a planning-only packet. It does not add delivery code.

## Background

Phase 12H created static local share bundles.
Phase 12J added optional local QR image generation.
Phase 12K added PDF-ready print HTML.

The remaining question is delivery: how a generated bundle gets from the PC to
another device.

## Delivery Options

### Tier 1 - Recommended Near-Term

Manual local transfer:

```text
copy folder to phone
copy generated PDF to phone
open index.html or print.html locally
scan QR that points at a user-supplied local path or LAN URL
```

Allowed:

```text
documentation
bundle manifest metadata
local file paths
manual copy guidance
```

No new code is required unless a future convenience command is useful.

### Tier 2 - Possible With Explicit Contract

Local LAN preview:

```text
serve one generated bundle directory on localhost/LAN
display LAN URL
generate QR for LAN URL
stop server when user exits
```

Required future guardrails:

```text
explicit user command
bind address must be visible
read-only static file serving
serve only selected bundle directory
no directory traversal
no upload endpoint
no provider/db/recommendation access
```

### Tier 3 - Deferred Until Privacy Review

Outbound delivery:

```text
Discord webhook
email
cloud upload
file sync provider
public link generation
URL shortener
```

These require a separate contract before implementation.

## Forbidden Defaults

Codie must not:

```text
send reports automatically
upload reports automatically
post to Discord automatically
start a LAN server automatically
store credentials in source control
write tokens into logs
embed private deck contents in QR payloads
create public links without explicit user action
```

## Credential Rules

If a later packet adds credentials:

```text
credentials must come from environment variables or an ignored local config
credentials must never be committed
tests must use fakes/mocks only
logs must redact secrets
missing credentials must fail cleanly
```

## Recommended Implementation Order

1. Phase 12M - Delivery Usage Documentation
   - Add a user-facing local workflow doc for:
     - building a bundle
     - opening `index.html`
     - opening `print.html`
     - scanning QR
     - moving files to a phone

2. Phase 12N - Optional Local LAN Preview Contract
   - Planning only unless explicitly approved.
   - Define bind address, port behavior, output-root containment, and static
     serving scope.

3. Phase 12O - Optional Local LAN Preview Implementation
   - Only if approved after Phase 12N.
   - Use standard library static serving if possible.
   - No database or provider access.

4. Phase 12P - Optional Outbound Delivery Contract
   - Planning only for Discord/email/cloud.
   - Requires credential and privacy rules.

## Acceptance Requirements For Future Delivery Code

Local LAN preview:

```text
explicit command starts server
server serves selected bundle only
server is read-only
server refuses paths outside bundle root
URL is printed for user
QR target is explicit
tests do not require live network outside localhost
```

Outbound delivery:

```text
disabled by default
explicit destination required
credentials not committed
network calls mocked in tests
dry-run mode available
payload summary shown before send
no automatic public link creation
```

## Do Not Do In Phase 12L

- Do not add delivery code.
- Do not start a local server.
- Do not add Discord/webhook code.
- Do not add email/cloud upload code.
- Do not add dependencies.
- Do not change schema.
- Do not change recommendation logic.
