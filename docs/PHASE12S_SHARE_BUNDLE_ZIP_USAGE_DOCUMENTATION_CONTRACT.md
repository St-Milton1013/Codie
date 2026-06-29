# Phase 12S - Share Bundle Zip Usage Documentation Contract

## Purpose

Document the completed local/mobile report sharing workflow for Codie share
bundles, including deterministic zip export.

This is a documentation-only packet.

## Scope

Files created:

```text
docs/PHASE12S_SHARE_BUNDLE_ZIP_USAGE_DOCUMENTATION_CONTRACT.md
docs/PHASE12S_SHARE_BUNDLE_ZIP_USAGE_DOCUMENTATION_REPORT.md
```

Files modified:

```text
docs/USER_GUIDE_LOCAL_REPORT_SHARING.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Functions / Classes

None.

## Schema Impact

None.

## Dependency Impact

None.

## Documentation Requirements

The user guide must explain:

- how to build a local share bundle
- how to include a QR asset
- how to open the bundle on the PC
- how to use the print-friendly page for browser Save as PDF
- how to zip a share bundle with `zip-share-bundle`
- how to move the zip/PDF/folder to a phone manually
- how to use local LAN preview
- privacy notes for QR, LAN preview, zip files, and manual sharing

## Boundary Rules

Documentation must not claim that Codie:

- uploads reports
- posts to Discord
- creates public links
- sends files to a phone automatically
- hosts reports outside the user's machine
- performs recommendation generation as part of report sharing

## Validation Requirements

Run:

```powershell
git diff --check
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests
rg -n "uploads reports|posts to Discord|creates public links|sends files to a phone automatically|hosts reports outside" docs\USER_GUIDE_LOCAL_REPORT_SHARING.md docs\PHASE12S_SHARE_BUNDLE_ZIP_USAGE_DOCUMENTATION_CONTRACT.md docs\PHASE12S_SHARE_BUNDLE_ZIP_USAGE_DOCUMENTATION_REPORT.md
```

## Do Not Do

- Do not add code.
- Do not change schema.
- Do not add delivery integrations.
- Do not add public tunnels.
- Do not add simulator integration.
- Do not add recommendation output.
