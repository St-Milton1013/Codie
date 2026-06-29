# Phase 12Q - Share Bundle Zip Export Contract

## Purpose

Define how Codie may package a local share bundle into a zip file before any
outbound delivery feature can use that bundle as a payload.

This is a contract-only packet. It does not add zip export code.

## Reason

Outbound delivery should not send arbitrary directories or raw project files.
It needs a reviewed, deterministic package format first.

## Future Scope

Potential future files:

```text
codie/exports/share_bundle_zip.py
tests/test_exports_share_bundle_zip.py
docs/PHASE12R_SHARE_BUNDLE_ZIP_EXPORT_IMPLEMENTATION_CONTRACT.md
```

## Public Interface Shape

Future classes/functions:

```text
ShareBundleZipResult
build_share_bundle_zip_manifest(...)
write_share_bundle_zip(...)
validate_share_bundle_zip_payload(...)
```

Future CLI command:

```text
zip-share-bundle
```

Possible flags:

```text
--bundle-dir
--output
--output-root
--generated-at
```

## Required Input

Input must be an existing share bundle directory containing:

```text
index.html
manifest.json
```

Optional accepted files:

```text
print.html
assets/
```

## Required Output

Output:

```text
<name>.zip
```

The zip must contain:

```text
index.html
manifest.json
print.html, if present
assets/<selected files>
zip-manifest.json
```

## Zip Manifest

`zip-manifest.json` must include:

```text
zip_manifest_version
generated_at
source_bundle_dir
entry_file
file_count
total_bytes
files
rejected_files
privacy_notes
```

Each file entry must include:

```text
bundle_path
byte_size
sha256
content_type_guess
```

## Determinism Rules

- Zip entries must be sorted by relative path.
- Zip entry names must use forward slashes.
- Zip metadata timestamps should be deterministic where practical.
- The generated `zip-manifest.json` must be deterministic for the same input
  and `generated_at`.

## Output Root Rules

- Zip output must respect `output_root` containment.
- Input bundle root must be resolved before scanning.
- Only files under the selected bundle directory may be included.
- Symlink handling must be conservative:
  - either reject symlinks entirely
  - or resolve and include only if still under the bundle root

The recommended first implementation should reject symlinks.

## Forbidden Payloads

The zip must reject:

```text
*.sqlite
*.sqlite3
*.db
.env
*.env
*.key
*.pem
*.p12
*.pfx
ignored local config files
raw provider payload archives
source database files
files outside the selected bundle root
```

## Required Safety Behavior

- Reject path traversal.
- Reject absolute archive paths.
- Reject duplicate archive names.
- Reject empty bundle output.
- Record rejected files in `zip-manifest.json` when safe to do so.
- Do not delete source bundle files.
- Do not send the zip anywhere.

## Future Tests

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
path traversal is rejected
output_root containment is enforced
no network calls occur
CLI returns zip path and byte size
```

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

## Do Not Do In Phase 12Q

- Do not add zip code.
- Do not add dependencies.
- Do not add outbound delivery.
- Do not add Discord/email/cloud integrations.
- Do not create public links.
- Do not change schema.
- Do not change recommendation logic.
