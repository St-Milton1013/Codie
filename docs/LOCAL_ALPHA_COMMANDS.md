# Local Alpha Commands

Status: local alpha command guide

Run commands from the repository root. Use `python -m ...` module invocation.

## Validate Repository

```powershell
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

## Recommendation Output Report Rendering

Module:

```text
codie.cli.recommendation_output
```

Purpose:

```text
Render an already-built RecommendationOutputBundle JSON into local JSON and/or
Markdown report files.
```

Example:

```powershell
python -m codie.cli.recommendation_output render `
  --bundle-json work/recommendation_output_bundle.json `
  --format both `
  --output-root outputs/recommendation-report `
  --basename local-alpha-report `
  --create-output-root
```

Important:

```text
This command does not discover cards.
This command does not rank cards.
This command does not choose cuts or additions.
This command does not generate recommendations.
Input must already be a RecommendationOutputBundle JSON.
Output-root containment and overwrite rules are enforced by the writer.
```

Useful options:

```text
--format json|markdown|md|both
--basename <name without extension>
--overwrite
--create-output-root
--no-provenance
```

## Simulation Review Export Bundle

Module:

```text
codie.cli.simulation_review
```

Purpose:

```text
Write an accepted simulator review export bundle under an output root.
```

Example:

```powershell
python -m codie.cli.simulation_review export-review-bundle `
  --bundle-json work/simulation_review_export_bundle.json `
  --output-root outputs/simulation-review
```

Important:

```text
Input must already be a simulation_review_export_bundle JSON.
This command writes export files only.
This command does not run simulator search.
This command does not alter historical simulator records.
```

## User Deck Workflow

Module:

```text
codie.cli.user_deck
```

### Initialize A Local Database

```powershell
python -m codie.cli.user_deck init-db --db work/codie.sqlite
```

This bootstraps schema only. Card resolution workflows still require relevant
card rows to exist in the local database.

### Import A User Deck

```powershell
python -m codie.cli.user_deck import-user-deck `
  --db work/codie.sqlite `
  --deck-file work/my-deck.txt `
  --deck-name "Local Test Deck" `
  --output-root outputs/user-deck `
  --json-out outputs/user-deck/comparison.json `
  --markdown-out outputs/user-deck/comparison.md
```

Important:

```text
This is a local user-layer workflow.
Cards must resolve before persistence.
Unresolved cards should not leave partial user_decks, user_deck_cards, or analysis_sessions.
Comparison output is evidence-only.
```

### Saved Analyses

```powershell
python -m codie.cli.user_deck list-saved-analyses `
  --db work/codie.sqlite `
  --user-deck-id 1

python -m codie.cli.user_deck show-saved-analysis `
  --db work/codie.sqlite `
  --saved-analysis-id 1
```

### UI Page Model Exports

```powershell
python -m codie.cli.user_deck export-ui-saved-analysis-list `
  --db work/codie.sqlite `
  --user-deck-id 1 `
  --output outputs/ui/saved-analysis-list.json `
  --output-root outputs/ui

python -m codie.cli.user_deck export-ui-saved-analysis-detail `
  --db work/codie.sqlite `
  --saved-analysis-id 1 `
  --output outputs/ui/saved-analysis-detail.json `
  --output-root outputs/ui
```

## Share Bundle Commands

Module:

```text
codie.cli.user_deck
```

### Build A Static Share Bundle

```powershell
python -m codie.cli.user_deck build-share-bundle `
  --title "Local Alpha Report" `
  --generated-at "2026-07-10T00:00:00+00:00" `
  --asset outputs/user-deck/comparison.json `
  --asset-label "Comparison JSON" `
  --asset outputs/user-deck/comparison.md `
  --asset-label "Comparison Markdown" `
  --output-dir outputs/share/local-alpha `
  --output-root outputs/share
```

### Serve A Share Bundle Locally

```powershell
python -m codie.cli.user_deck serve-share-bundle `
  --bundle-dir outputs/share/local-alpha `
  --host 127.0.0.1 `
  --port 0
```

LAN-visible serving requires explicit `--allow-lan`.

### Zip A Share Bundle

```powershell
python -m codie.cli.user_deck zip-share-bundle `
  --bundle-dir outputs/share/local-alpha `
  --output outputs/share/local-alpha.zip `
  --output-root outputs/share `
  --generated-at "2026-07-10T00:00:00+00:00"
```

## Deck Memory

Module:

```text
codie.cli.user_deck_memory
```

List remembered decks:

```powershell
python -m codie.cli.user_deck_memory list-deck-memory `
  --db work/codie.sqlite `
  --limit 20
```

Show one remembered deck:

```powershell
python -m codie.cli.user_deck_memory show-deck-memory `
  --db work/codie.sqlite `
  --user-deck-id 1
```

Privacy note:

```text
show-deck-memory omits raw_input unless --include-raw-input is explicitly used.
```

