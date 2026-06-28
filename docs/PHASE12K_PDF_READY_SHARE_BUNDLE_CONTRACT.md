# Phase 12K - PDF-Ready Share Bundle Output Contract

## Purpose

Add PDF-ready static output to local share bundles without adding a PDF
generation dependency or external conversion service.

This phase supports the browser Print / Save as PDF workflow.

## Scope

```text
codie/exports/share_bundle.py
codie/exports/__init__.py
codie/cli/user_deck.py
tests/test_exports_share_bundle.py
tests/test_cli_user_deck.py
docs/PHASE12K_PDF_READY_SHARE_BUNDLE_CONTRACT.md
docs/PHASE12K_PDF_READY_SHARE_BUNDLE_REPORT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Functions / Classes

```text
share_bundle_print_html(...)
```

Existing public class extended:

```text
ShareBundleWriteResult.print_path
```

Existing public functions extended:

```text
build_share_bundle_manifest(..., include_print_entry=False, print_entry="print.html")
write_local_share_bundle(..., include_print_entry=True)
```

## CLI Impact

Existing command extended:

```text
build-share-bundle --no-print-entry
```

By default, `build-share-bundle` writes:

```text
index.html
print.html
manifest.json
assets/
```

## Schema Impact

None.

## Dependency Impact

None.

## Manifest Impact

Fields:

```text
print_entry
pdf_assets
```

No PDF binary is generated in this phase.

## Rules

- `print.html` must be static.
- `print.html` requires print-friendly CSS.
- Output must remain inside `output_root` through the existing bundle directory
  containment.
- No remote PDF conversion service is allowed.
- No hosted sharing is allowed.
- No report upload is allowed.
- No recommendation logic is changed.

## Tests

```text
manifest records print entry when requested
print HTML includes @media print CSS
print HTML supports browser Save as PDF
bundle writes print.html by default
bundle can disable print.html
CLI reports print_path
```

## Do Not Do

- Do not generate PDF files.
- Do not add PDF dependencies.
- Do not invoke browser automation.
- Do not upload files.
- Do not add hosted/mobile delivery integrations.
- Do not change schema.
