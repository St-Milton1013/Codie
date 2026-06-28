# Phase 12H - Local Report Share Bundle Contract

## Purpose

Create a local static report bundle that can be opened from another trusted
device, such as a phone, after the user moves or shares the generated folder.

This is a convenience export surface, not hosting, recommendation generation,
or mobile app development.

## Scope

```text
codie/exports/share_bundle.py
codie/exports/__init__.py
codie/cli/user_deck.py
tests/test_exports_share_bundle.py
tests/test_cli_user_deck.py
docs/PHASE12H_LOCAL_REPORT_SHARE_BUNDLE_CONTRACT.md
docs/PHASE12H_LOCAL_REPORT_SHARE_BUNDLE_REPORT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Functions / Classes

```text
ShareBundleAsset
ShareBundleWriteResult
build_share_bundle_manifest(...)
share_bundle_index_html(...)
write_local_share_bundle(...)
```

## CLI Command

```text
build-share-bundle
```

Required arguments:

```text
--title
--generated-at
--asset
--output-dir
```

Optional arguments:

```text
--asset-label
--output-root
```

## Schema Impact

None.

## Dependencies

- Existing export files created by earlier workflows.
- Standard library only: `html`, `json`, `pathlib`, `shutil`.
- Existing CLI wrapper.

## Outputs

```text
index.html
manifest.json
assets/<copied export files>
```

Manifest fields:

```text
bundle_version
title
generated_at
entry_file
qr_ready_entry
assets
notes
```

## Rules

- Bundle writes must respect `output_root` containment when provided.
- Bundle must copy caller-supplied assets without modifying their contents.
- Bundle index must escape titles and labels for HTML.
- Bundle must be static and require no local server.
- Bundle must not read SQLite.
- Bundle must not import providers, analytics, recommendations, or source
  tables.
- Bundle must not generate strategic recommendation wording.

## Failure Modes

- Missing title: `ValueError`.
- Missing generated timestamp: `ValueError`.
- No assets: `ValueError`.
- Missing asset file: `ValueError`.
- Output directory outside `output_root`: `ValueError`.

## Tests

```text
manifest deterministic and QR-ready
index HTML escapes title and labels
bundle copies assets and writes index/manifest
output_root containment rejects outside bundle path
invalid inputs fail cleanly
CLI writes static index and manifest
```

## Do Not Do

- Do not add hosted sharing.
- Do not add QR image generation yet.
- Do not add PDF generation yet.
- Do not add Discord/mobile integrations yet.
- Do not change recommendation logic.
- Do not persist bundle metadata to SQLite.
