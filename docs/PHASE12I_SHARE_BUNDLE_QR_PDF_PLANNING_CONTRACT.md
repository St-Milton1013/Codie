# Phase 12I - Share Bundle QR/PDF Planning Contract

## Purpose

Define the safe path for adding phone-friendly report access to Codie share
bundles.

This phase is a planning gate only. It does not add QR generation, PDF
generation, hosted links, Discord delivery, or mobile app behavior.

## Background

Phase 12H created local static report bundles:

```text
index.html
manifest.json
assets/<copied export files>
```

The next useful layer is making those bundles easier to open on a phone or
export as a document. That can be done several ways, and each option has
different privacy and dependency implications.

## Accepted Direction

Proceed in small packets:

```text
Phase 12J - QR Code Asset Generation
Phase 12K - PDF-Ready Share Bundle Output
Phase 12L - Optional Delivery Integrations Planning
```

## Feature Boundaries

### QR Code Asset Generation

Purpose:

Generate a local QR code image that points at the bundle entry path or a
caller-supplied local/private URL.

Allowed:

```text
local file path guidance
local LAN URL supplied by user
static QR PNG/SVG asset
manifest reference to QR asset
explicit disclosure of encoded target
```

Forbidden:

```text
uploading reports to third-party services
creating public links automatically
shortening links through external services
encoding private deck data directly in QR payload
network calls during tests
```

Dependency decision:

```text
Prefer a small explicit QR dependency only after approved:
- qrcode
- pillow, only if required for PNG output
```

The dependency must be added to `requirements.txt` in the implementation
packet if used.

### PDF-Ready Share Bundle Output

Purpose:

Make share bundles easy to print, save as PDF, or generate a local PDF artifact.

Allowed first step:

```text
print-friendly HTML/CSS
stable report title and metadata
asset links preserved
page-break friendly layout
browser Save as PDF workflow
```

Optional later step:

```text
local PDF generation using an explicit dependency or bundled PDF tooling
```

Forbidden:

```text
remote PDF conversion services
uploading private report files
embedding private user deck data in external URLs
browser automation dependency without a contract
```

### Optional Delivery Integrations

Purpose:

Plan ways to move the report to a phone after local bundle generation.

Possible options:

```text
open static folder on LAN
copy folder to phone
send generated PDF manually
send generated summary file manually
Discord webhook, only if explicitly configured by user
```

Forbidden by default:

```text
automatic Discord posting
automatic cloud upload
automatic public hosting
implicit external network calls
storing delivery credentials in source control
```

## Required Privacy Rules

- Private user deck contents must remain local unless the user explicitly
  exports or sends them.
- QR payloads must encode only a path or URL, not report contents.
- Generated PDFs must be local files.
- No third-party conversion service is allowed without a separate privacy
  review.
- Delivery integrations must be opt-in and disabled by default.

## Required Manifest Extensions

Future QR/PDF implementation packets may extend `manifest.json` with:

```text
qr_assets
pdf_assets
print_entry
encoded_targets
privacy_notes
generated_files
```

Existing fields must remain stable:

```text
bundle_version
title
generated_at
entry_file
qr_ready_entry
assets
notes
```

## Recommended Implementation Order

1. Phase 12J - QR Code Asset Generation
   - Add QR dependency explicitly.
   - Generate QR asset from `qr_ready_entry` or user-supplied local URL.
   - Store encoded target in manifest.
   - Add tests for deterministic output metadata, no private data encoding, and
     output-root containment.

2. Phase 12K - PDF-Ready Share Bundle Output
   - Add print stylesheet and PDF-ready HTML structure first.
   - Prefer browser Save as PDF guidance before adding PDF generation
     dependencies.
   - If local PDF generation is added, define dependency and rendering tests.

3. Phase 12L - Optional Delivery Integrations Planning
   - Decide whether Discord/manual send/LAN server belongs in Codie.
   - Require opt-in config and no credentials in repository.

## Test Requirements For Future Implementation

QR packet:

```text
QR target is explicit
QR target is recorded in manifest
QR asset is written inside output_root
private report contents are not encoded
missing/empty target fails cleanly
no network calls in tests
```

PDF-ready packet:

```text
print entry is generated
manifest records print/PDF-ready output
report assets remain linked
private data is not sent externally
output_root containment holds
```

Delivery packet:

```text
integration disabled by default
credentials are never committed
network calls are mock-only in tests
user must explicitly provide destination
```

## Do Not Do In Phase 12I

- Do not add dependencies.
- Do not generate QR codes.
- Do not generate PDFs.
- Do not add hosted links.
- Do not add Discord sending.
- Do not add a local server.
- Do not change schema.
- Do not change recommendation logic.
