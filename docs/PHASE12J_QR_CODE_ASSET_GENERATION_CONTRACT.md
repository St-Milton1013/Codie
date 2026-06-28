# Phase 12J - QR Code Asset Generation Contract

## Purpose

Generate a local QR image for a share bundle entry target so the user can open
a Codie report bundle from a phone more easily.

This is local asset generation only. It is not hosted sharing, Discord
delivery, PDF generation, or recommendation output.

## Scope

```text
requirements.txt
codie/exports/share_bundle.py
codie/exports/__init__.py
codie/cli/user_deck.py
tests/test_exports_share_bundle.py
tests/test_cli_user_deck.py
docs/PHASE12J_QR_CODE_ASSET_GENERATION_CONTRACT.md
docs/PHASE12J_QR_CODE_ASSET_GENERATION_REPORT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Dependency Impact

```text
qrcode[pil]==7.4.2
```

Reason:

Generate local QR PNG assets without relying on network services or external
QR conversion websites.

## Public Functions / Classes

```text
write_qr_png(...)
```

Existing public classes changed:

```text
ShareBundleWriteResult.qr_asset_path
```

Existing public functions extended:

```text
build_share_bundle_manifest(..., qr_target=None, qr_asset_path=None)
write_local_share_bundle(..., qr_target=None)
```

## CLI Impact

Existing command extended:

```text
build-share-bundle --qr-target <path-or-url>
```

## Schema Impact

None.

## Manifest Impact

Optional fields added when QR generation is requested:

```text
qr_assets
encoded_targets
privacy_notes
```

Stable existing fields remain:

```text
bundle_version
title
generated_at
entry_file
qr_ready_entry
assets
notes
```

## Privacy Rules

- QR target must be explicit.
- QR target must be a single line.
- QR target may be a local path, local URL, or caller-supplied private URL.
- QR payload must not contain report contents.
- QR payload must not contain private deck contents.
- Tests must not make network calls.

## Failure Modes

- Empty QR target: `ValueError`.
- Multiline QR target: `ValueError`.
- Overlong QR target: `ValueError`.
- QR output path outside `output_root`: `ValueError`.
- Non-PNG QR output path: `ValueError`.

## Tests

```text
manifest records explicit QR target
QR asset writes as PNG
QR asset path respects output_root
non-PNG QR path fails
empty/multiline QR target fails
share bundle can include QR asset
manifest does not include copied report contents as encoded target
CLI can build QR-enabled bundle
```

## Do Not Do

- Do not generate PDF files.
- Do not add hosted sharing.
- Do not add Discord delivery.
- Do not add a local server.
- Do not encode report or deck contents in QR payloads.
- Do not change recommendation logic.
- Do not change schema.
