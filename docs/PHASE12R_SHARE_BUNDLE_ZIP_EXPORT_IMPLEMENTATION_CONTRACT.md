# Phase 12R - Share Bundle Zip Export Implementation Contract

## Purpose

Implement deterministic local zip packaging for Codie share bundles using the
Phase 12Q contract.

## Scope

Files created:

```text
codie/exports/share_bundle_zip.py
tests/test_exports_share_bundle_zip.py
docs/PHASE12R_SHARE_BUNDLE_ZIP_EXPORT_IMPLEMENTATION_CONTRACT.md
docs/PHASE12R_SHARE_BUNDLE_ZIP_EXPORT_IMPLEMENTATION_REPORT.md
```

Files modified:

```text
codie/exports/__init__.py
codie/cli/user_deck.py
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Functions / Classes

```text
ShareBundleZipResult
build_share_bundle_zip_manifest(...)
validate_share_bundle_zip_payload(...)
write_share_bundle_zip(...)
```

CLI command:

```text
zip-share-bundle
```

## Schema Impact

None.

## Dependency Impact

None. Uses Python standard library only.

## Required Behavior

- Accept an existing share bundle directory with `index.html` and
  `manifest.json`.
- Include optional `print.html` and accepted `assets/` files.
- Write a local `.zip` file.
- Include deterministic `zip-manifest.json`.
- Sort archive entries by relative path.
- Use forward-slash archive paths.
- Use deterministic zip entry timestamps.
- Enforce `output_root` containment when supplied.
- Reject symlinks from the payload.
- Exclude forbidden payloads and record them in `zip-manifest.json`.
- Avoid network calls and outbound delivery.

## Boundary Rules

Zip export code must not import:

```text
codie.providers
codie.db
codie.analytics
codie.recommendations
sqlite3
requests
httpx
discord
```

## Acceptance Tests

```text
valid bundle writes zip
zip contains index.html and manifest.json
zip contains print.html when present
zip contains assets with relative paths
zip includes deterministic zip-manifest.json
entries are sorted
SQLite files are rejected
secret-like files are rejected
symlinks are rejected
output_root containment is enforced
CLI returns zip path and byte size
no forbidden imports
```

## Do Not Do

- Do not send the zip anywhere.
- Do not add Discord/email/cloud upload behavior.
- Do not create public links.
- Do not change schema.
- Do not change recommendation logic.
- Do not read SQLite.
