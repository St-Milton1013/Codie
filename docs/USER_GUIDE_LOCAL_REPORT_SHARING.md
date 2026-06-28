# User Guide - Local Report Sharing

This guide shows how to build a local Codie report bundle and view it on your
PC or phone.

The current workflow is local and manual. It does not upload reports, post to
Discord, create public links, or start a server.

## Requirements

Use the project checkout:

```powershell
cd "C:\Users\Main\Documents\Codex\2026-06-22\next-phase-contract-recommended-next-task"
```

Use the bundled Python runtime:

```powershell
$python = "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
```

Choose an output folder:

```powershell
$out = "$HOME\Documents\CodieReports"
New-Item -ItemType Directory -Force $out
```

## Build A Basic Share Bundle

Start with one or more existing Codie export files. For example:

```powershell
$report = "$out\comparison.md"
$bundle = "$out\share-bundle"
```

Build the bundle:

```powershell
& $python -m codie.cli.user_deck build-share-bundle `
  --title "Codie Evidence Report" `
  --generated-at "2026-06-28T00:00:00+00:00" `
  --asset $report `
  --asset-label "Evidence comparison" `
  --output-dir $bundle `
  --output-root $out
```

The bundle folder contains:

```text
index.html
print.html
manifest.json
assets/
```

## Build A QR-Enabled Bundle

A QR code encodes only the target you provide. It does not encode the report
contents.

Example with a local target:

```powershell
& $python -m codie.cli.user_deck build-share-bundle `
  --title "Codie Evidence Report" `
  --generated-at "2026-06-28T00:00:00+00:00" `
  --asset $report `
  --asset-label "Evidence comparison" `
  --output-dir $bundle `
  --output-root $out `
  --qr-target "index.html"
```

The QR image is written to:

```text
assets/bundle-entry-qr.png
```

## Open The Bundle On Your PC

Open the main bundle page:

```powershell
Start-Process "$bundle\index.html"
```

Open the print-friendly page:

```powershell
Start-Process "$bundle\print.html"
```

## Save As PDF

Open `print.html` in your browser.

Then use:

```text
Ctrl+P
Destination: Save as PDF
```

Save the PDF somewhere under your report folder, for example:

```text
C:\Users\Main\Documents\CodieReports\Codie Evidence Report.pdf
```

## Move The Report To Your Phone

Safe manual options:

```text
copy the generated PDF to your phone
copy the whole share-bundle folder to your phone
send the PDF manually through your preferred app
open index.html after moving the folder
open print.html after moving the folder
```

Avoid uploading private deck reports to public link services unless you
intentionally want that file to leave your machine.

## QR Notes

The QR image is useful when the target is something your phone can actually
open.

Examples:

```text
index.html
file path copied to your phone
future local LAN URL, after a separate LAN-preview feature exists
```

Current Codie does not start a local web server. LAN preview is a future
optional feature and requires a separate contract.

## Optional Local LAN Preview

Codie can serve one existing share bundle through a local read-only preview
server.

Localhost-only preview:

```powershell
& $python -m codie.cli.user_deck serve-share-bundle `
  --bundle-dir $bundle
```

The command prints JSON containing:

```text
bundle_dir
host
port
url
privacy_warning
```

Open the printed `url` from the same PC.

LAN-visible preview requires an explicit host and opt-in flag:

```powershell
& $python -m codie.cli.user_deck serve-share-bundle `
  --bundle-dir $bundle `
  --host "0.0.0.0" `
  --allow-lan
```

Only use LAN-visible preview on a trusted network. Anyone who can reach the
bound host and port may be able to read the bundle files while the command is
running.

Stop the preview with:

```text
Ctrl+C
```

## Troubleshooting

If the command says an asset does not exist, check the report path:

```powershell
Test-Path $report
```

If the command says the output path is outside `output_root`, make sure
`--output-dir` is inside the folder passed to `--output-root`.

If your phone cannot open the QR target, move the bundle or PDF to the phone
first, or wait for the future local LAN preview feature.

If `qrcode` is missing, install project requirements into the bundled runtime:

```powershell
& $python -m pip install -r requirements.txt
```

## Privacy Checklist

Before sharing:

```text
confirm the report file is the one you intend to share
open print.html locally and inspect it
save a PDF only if you want a portable copy
do not post private reports publicly by accident
remember QR targets are paths or URLs, not report contents
```
