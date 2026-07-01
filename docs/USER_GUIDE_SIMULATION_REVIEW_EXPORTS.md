# User Guide - Simulation Review Exports

This guide shows how to write simulator review export bundles to local files.

Simulation review exports are QA and training artifacts. They help inspect
reviewed simulator lines, reviewed accuracy summaries, unsupported-card issues,
and regression fixtures. They are not tournament evidence and they do not
generate recommendations.

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
$out = "$HOME\Documents\CodieSimulationReviews"
New-Item -ItemType Directory -Force $out
```

## Build A Bundle JSON

Phase 13Z creates export bundles from already-built reviewed accuracy summaries
and line review fixtures.

The normal application flow should build these objects from persisted simulator
review data. The CLI does not query the database and does not build summaries.
It only writes a local bundle JSON that already exists.

Minimal Python shape:

```python
import json
from pathlib import Path

from codie.probability_engine import build_simulation_review_export_bundle

# summary: ReviewedAccuracySummary
# fixtures: tuple[LineReviewFixture, ...]

bundle = build_simulation_review_export_bundle(
    summary,
    fixtures,
    exported_at="2026-07-01T00:00:00Z",
)

Path(r"C:\Users\Main\Documents\CodieSimulationReviews\simulation-review-bundle.json").write_text(
    json.dumps(bundle.to_dict(), sort_keys=True, indent=2) + "\n",
    encoding="utf-8",
)
```

The bundle JSON contains:

```text
kind
schema_version
bundle_id
summary_path
markdown_path
fixture_paths
generated_at
exported_at
files
```

Every file path inside the bundle is relative.

## Write The Bundle Files

Run the Phase 14B CLI:

```powershell
$bundleJson = "$out\simulation-review-bundle.json"
$exportRoot = "$out\review-export"

& $python -m codie.cli.simulation_review export-review-bundle `
  --bundle-json $bundleJson `
  --output-root $exportRoot
```

The command prints deterministic JSON containing:

```text
root
bundle_id
files
bytes_written
```

## Output Layout

The export root contains:

```text
manifest.json
reviewed_accuracy_summary.json
reviewed_accuracy_summary.md
fixtures/
```

Each fixture normally has:

```text
fixtures/<review-id>.json
fixtures/<review-id>.md
```

## Inspect The Manifest

Open the manifest:

```powershell
Get-Content "$exportRoot\manifest.json"
```

Check:

```text
bundle_id
schema_version
generated_at
exported_at
files
```

The manifest is the portable index for the export.

## Inspect The Summary

Open the Markdown summary:

```powershell
Get-Content "$exportRoot\reviewed_accuracy_summary.md"
```

The summary reports reviewed simulator accuracy counts and filters. It does not
change simulator history and does not rewrite line review annotations.

## Inspect A Line Review Fixture

List fixture files:

```powershell
Get-ChildItem "$exportRoot\fixtures"
```

Open a fixture:

```powershell
Get-Content "$exportRoot\fixtures\<review-id>.md"
```

The JSON fixture preserves the action trace payload for regression work. The
Markdown fixture is for human review.

## Share As A Local Report Bundle

You may pass generated Markdown or JSON files into the existing local share
bundle workflow.

Example:

```powershell
$shareBundle = "$out\share-bundle"

& $python -m codie.cli.user_deck build-share-bundle `
  --title "Codie Simulation Review" `
  --generated-at "2026-07-01T00:00:00+00:00" `
  --asset "$exportRoot\reviewed_accuracy_summary.md" `
  --asset-label "Reviewed accuracy summary" `
  --output-dir $shareBundle `
  --output-root $out
```

The share bundle remains local unless you explicitly move or serve it.

## Privacy And Evidence Rules

Before sharing simulator review exports:

```text
inspect the manifest
inspect the Markdown summary
inspect any fixture trace you plan to share
confirm private deck or trace data is safe to disclose
do not upload private exports unless you explicitly choose to share them
```

Remember:

```text
simulation review exports are QA/training metadata
simulation results are not tournament evidence
review annotations do not rewrite historical simulation records
unsupported cards must remain visible
cEDHData reference material remains reference-only
```

## Troubleshooting

If the CLI says the bundle JSON is not a `simulation_review_export_bundle`, make
sure the input file came from `SimulationReviewExportBundle.to_dict()`.

If the CLI rejects an export path, inspect the bundle JSON for absolute paths,
drive-letter paths, backslashes, duplicate paths, or traversal segments.

If the CLI says the output path cannot be written, confirm the output root
exists or that the parent folder is writable:

```powershell
Test-Path $out
```

If Python cannot import `codie`, confirm you are running the command from the
project checkout.
