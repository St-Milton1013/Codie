# Phase 12M - Delivery Usage Documentation Contract

## Purpose

Create user-facing instructions for using local share bundles from PowerShell.

The guide must explain how to build a bundle, open it locally, use the QR asset,
save a PDF through the browser, and move the report to a phone manually.

## Scope

```text
docs/USER_GUIDE_LOCAL_REPORT_SHARING.md
docs/PHASE12M_DELIVERY_USAGE_DOCUMENTATION_CONTRACT.md
docs/PHASE12M_DELIVERY_USAGE_DOCUMENTATION_REPORT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Schema Impact

None.

## Dependency Impact

None.

## Required Content

The guide requires:

```text
PowerShell setup commands
build-share-bundle example
QR-enabled bundle example
how to open index.html
how to open print.html
browser Save as PDF guidance
manual phone transfer options
privacy notes
troubleshooting
```

## Rules

- Do not add delivery code.
- Do not add a local server.
- Do not add Discord/webhook/email/cloud instructions as active commands.
- Do not ask the user to upload private reports to third-party services.
- Keep all commands local/manual.
- Make clear that QR payloads encode only the explicit target path or URL.

## Validation

```text
python -m unittest discover -s tests
git diff --check
forbidden strategic-language scan
forbidden active delivery command scan
```

## Do Not Do

- Do not implement Phase 12N/12O.
- Do not start a server.
- Do not add dependencies.
- Do not add hosted sharing.
- Do not change schema.
