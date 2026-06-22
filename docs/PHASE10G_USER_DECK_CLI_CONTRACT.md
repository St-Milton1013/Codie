# Phase 10G - User Deck CLI Wrapper

## Purpose

Provide a small, repeatable command-line wrapper for the accepted Phase 10 user deck workflow.

The CLI imports a local deck text file, optionally compares it against evidence candidates from a JSON file, and optionally writes JSON/Markdown comparison exports.

This phase does not add UI, final recommendations, provider calls, schema, or source-table reads.

## Files Created Or Modified

- `codie/cli/__init__.py`
- `codie/cli/user_deck.py`
- `tests/test_cli_user_deck.py`
- `docs/PHASE10G_USER_DECK_CLI_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions

- `build_parser(...)`
- `main(...)`

## CLI Commands

### `init-db`

Bootstraps a Codie SQLite database file:

```powershell
python -m codie.cli.user_deck init-db --db codie.sqlite
```

### `import-user-deck`

Imports a user deck text file:

```powershell
python -m codie.cli.user_deck import-user-deck `
  --db codie.sqlite `
  --deck-file deck.txt `
  --deck-name "Fixture Deck"
```

Optional evidence comparison and exports:

```powershell
python -m codie.cli.user_deck import-user-deck `
  --db codie.sqlite `
  --deck-file deck.txt `
  --evidence-json evidence.json `
  --json-out comparison.json `
  --markdown-out comparison.md `
  --output-root .
```

## Evidence JSON Shape

Accepted input:

```json
{
  "candidates": [
    {
      "oracle_id": "oracle-remora",
      "card_name": "Mystic Remora",
      "evidence_type": "commander_staple",
      "score": 0.8,
      "sample_size": 42,
      "source_record_id": "staple:remora"
    }
  ]
}
```

A top-level list of candidate objects is also accepted.

## Schema Impact

None.

Existing tables used through Phase 10 APIs:

- `cards`
- `user_decks`
- `user_deck_cards`
- `analysis_sessions`

## Boundary Rules

The CLI may orchestrate:

- DB connection/bootstrap
- core card lookup
- user repository
- user deck import
- user deck analysis input
- user deck evidence comparison
- export writing

The CLI must not import:

- providers
- source repositories/tables
- analytics
- recommendations

## Failure Modes

- Missing required CLI arguments fail through `argparse`.
- Unresolved cards fail through the user deck importer.
- Invalid evidence JSON fails before comparison.
- `--json-out` and `--markdown-out` must be supplied together.
- Export paths respect existing output-root containment rules.

## Tests

Required test coverage:

- `init-db` bootstraps schema
- `import-user-deck` writes comparison exports
- inline comparison output works without export paths
- output paths must be supplied together
- CLI boundary import guard

## Do Not Do

- Do not generate final recommendations.
- Do not call providers.
- Do not read source/provider tables.
- Do not add schema.
- Do not build UI.
