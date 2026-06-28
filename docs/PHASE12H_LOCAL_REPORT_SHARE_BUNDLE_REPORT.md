# Phase 12H - Local Report Share Bundle Report

## Verdict

```text
Phase 12H Local Report Share Bundle: PASS
```

## Objective

Add a safe local export bundle so Codie reports can be gathered into a static
folder with an `index.html` entry point and manifest metadata suitable for
phone viewing after the user shares or opens the folder on another trusted
device.

## Files Created

```text
codie/exports/share_bundle.py
tests/test_exports_share_bundle.py
docs/PHASE12H_LOCAL_REPORT_SHARE_BUNDLE_CONTRACT.md
docs/PHASE12H_LOCAL_REPORT_SHARE_BUNDLE_REPORT.md
```

## Files Modified

```text
codie/exports/__init__.py
codie/cli/user_deck.py
tests/test_cli_user_deck.py
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Functions / Classes Added

```text
ShareBundleAsset
ShareBundleWriteResult
build_share_bundle_manifest(...)
share_bundle_index_html(...)
write_local_share_bundle(...)
```

## CLI Command Added

```text
build-share-bundle
```

## Schema Impact

None.

## Work Completed

- Added static bundle manifest generation.
- Added static `index.html` generation with escaped title/asset labels.
- Added asset copying into `assets/`.
- Added output-root containment for bundle output directories.
- Added CLI wrapper for building bundles from existing export files.
- Added focused tests for manifest, HTML escaping, copying, containment,
  invalid inputs, and CLI execution.

## Validation Performed

Focused tests:

```text
Ran 15 tests in 0.279s

OK
```

Full Python test suite:

```text
Ran 296 tests in 0.833s

OK
```

Frontend build:

```text
> codie-ui@0.1.0 build
> tsc --noEmit && vite build

36 modules transformed.
dist/index.html                 0.41 kB
dist/assets/index-B1kzUvjH.css  3.03 kB
dist/assets/index-BQRhkJmF.js   203.12 kB
built in 505ms
```

Static checks:

```text
git diff --check
```

passed.

Boundary scans:

```text
rg -n "sqlite3|source_events|source_decks|provider_objects|codie\.providers|codie\.db|codie\.analytics|codie\.recommendations" codie\exports\share_bundle.py
rg -n "source_events|source_decks|provider_objects|codie\.providers|codie\.analytics|codie\.recommendations" codie\cli\user_deck.py
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this" codie\exports\share_bundle.py docs\PHASE12H_LOCAL_REPORT_SHARE_BUNDLE_CONTRACT.md docs\PHASE12H_LOCAL_REPORT_SHARE_BUNDLE_REPORT.md
```

all returned no matches.

## Boundary Notes

- Share bundles use existing export files only.
- No SQLite reads.
- No provider imports.
- No analytics or recommendation imports.
- No strategic recommendation language added.
- No hosted/mobile/Discord integration added yet.

## Known Caveats

- QR image generation is not implemented yet.
- PDF generation is not implemented yet.
- Phone viewing still requires the user to move/open the static folder through
  a trusted local path or later sharing workflow.

## Recommended Next Step

```text
Phase 12I - Share Bundle QR/PDF Planning Contract
```

Purpose:

Define the optional next layer for PDF-ready output and QR-code generation
without adding hosted sharing or leaking private deck data.
