# User Guide - Deck Memory CLI

## Purpose

The deck memory CLI lets you inspect user decks that were already imported into
your local Codie database.

It is for local recall and review:

```text
list remembered decks
show one remembered deck
see linked saved analysis metadata
see linked analysis session metadata
see imported card rows
```

It does not import new decks, call providers, call LLMs, run simulator logic,
rank cards, or generate recommendations.

## Privacy Warning

`raw_input` contains the original imported deck text.

By default, Codie omits `raw_input` from deck memory CLI output.

`raw_input` appears only when this flag is explicitly provided:

```text
--include-raw-input
```

Treat `raw_input` as private deck text. Do not paste it into chats, web tools,
or public reports unless that is your intended action.

## Database Path

Both deck memory commands require a local Codie SQLite database:

```text
--db PATH
```

Example:

```powershell
python -m codie.cli.user_deck_memory list-deck-memory --db .\codie.sqlite
```

The CLI reads an existing database. It does not create schema or mutate user
deck records.

## List Remembered Decks

Use `list-deck-memory` to list remembered user deck summaries:

```powershell
python -m codie.cli.user_deck_memory list-deck-memory --db .\codie.sqlite
```

Example output:

```json
{
  "decks": [
    {
      "card_count": 100,
      "commander_hash": "tymna|kraum",
      "created_at": "2026-07-01T00:00:00+00:00",
      "deck_hash": "deck-example-001",
      "deck_name": "Example Tymna Kraum",
      "is_temporary": false,
      "latest_analysis_generated_at": "2026-07-01T01:00:00+00:00",
      "saved_analysis_count": 2,
      "source_url": "https://example.test/decks/example",
      "updated_at": "2026-07-01T02:00:00+00:00",
      "user_deck_id": 1
    }
  ]
}
```

List output does not include:

```text
raw_input
full card rows
saved analysis summary_json
```

## List Filters

Filter by commander hash:

```powershell
python -m codie.cli.user_deck_memory list-deck-memory --db .\codie.sqlite --commander-hash "tymna|kraum"
```

Filter by deck hash:

```powershell
python -m codie.cli.user_deck_memory list-deck-memory --db .\codie.sqlite --deck-hash "deck-example-001"
```

Filter by created date window:

```powershell
python -m codie.cli.user_deck_memory list-deck-memory --db .\codie.sqlite --created-at-from "2026-07-01T00:00:00+00:00" --created-at-to "2026-07-31T23:59:59+00:00"
```

Exclude temporary deck records:

```powershell
python -m codie.cli.user_deck_memory list-deck-memory --db .\codie.sqlite --exclude-temporary
```

Exclude persistent deck records:

```powershell
python -m codie.cli.user_deck_memory list-deck-memory --db .\codie.sqlite --exclude-persistent
```

Limit the number of returned summaries:

```powershell
python -m codie.cli.user_deck_memory list-deck-memory --db .\codie.sqlite --limit 10
```

## Show One Remembered Deck

Use `show-deck-memory` to inspect one remembered user deck:

```powershell
python -m codie.cli.user_deck_memory show-deck-memory --db .\codie.sqlite --user-deck-id 1
```

Example output without raw input:

```json
{
  "deck": {
    "analysis_sessions": [
      {
        "analysis_session_id": 7,
        "commander_hash": "tymna|kraum",
        "completed_at": "2026-07-01T01:01:00+00:00",
        "deck_hash": "deck-example-001",
        "session_type": "evidence_comparison",
        "started_at": "2026-07-01T01:00:00+00:00",
        "status": "complete"
      }
    ],
    "cards": [
      {
        "oracle_id": "oracle-example-001",
        "quantity": 1,
        "raw_name": "Example Card",
        "resolution_status": "resolved",
        "scryfall_id": "scryfall-example-001",
        "zone": "mainboard"
      }
    ],
    "saved_analyses": [
      {
        "analysis_type": "user_deck_evidence_comparison",
        "deck_hash": "deck-example-001",
        "generated_at": "2026-07-01T01:02:00+00:00",
        "report_path": "reports/example.md",
        "saved_analysis_id": 3
      }
    ],
    "summary": {
      "card_count": 100,
      "commander_hash": "tymna|kraum",
      "created_at": "2026-07-01T00:00:00+00:00",
      "deck_hash": "deck-example-001",
      "deck_name": "Example Tymna Kraum",
      "is_temporary": false,
      "latest_analysis_generated_at": "2026-07-01T01:02:00+00:00",
      "saved_analysis_count": 1,
      "source_url": "https://example.test/decks/example",
      "updated_at": "2026-07-01T02:00:00+00:00",
      "user_deck_id": 1
    }
  }
}
```

## Show Raw Input Explicitly

To include the original imported deck text, pass:

```text
--include-raw-input
```

Example:

```powershell
python -m codie.cli.user_deck_memory show-deck-memory --db .\codie.sqlite --user-deck-id 1 --include-raw-input
```

Synthetic example output:

```json
{
  "deck": {
    "raw_input": "1 Example Card\n1 Another Example Card",
    "summary": {
      "deck_hash": "deck-example-001",
      "user_deck_id": 1
    },
    "cards": [],
    "analysis_sessions": [],
    "saved_analyses": []
  }
}
```

Use this flag deliberately. The raw input can contain the complete imported deck
text.

## Failure Examples

Missing database path:

```text
error: database path does not exist: .\missing.sqlite
```

Unknown user deck ID:

```text
error: Unknown user_deck_id: 999
```

Invalid limit:

```text
error: Deck memory limit must be at least 1
```

Both temporary and persistent records excluded:

```text
error: At least one deck memory visibility class must be included
```

Errors are written to stderr and return a non-zero exit code.

## What This CLI Does Not Do

The deck memory CLI:

```text
does not import new decks
does not create schema
does not mutate user deck records
does not call providers
does not call LLMs
does not run simulator logic
does not rank cards
does not generate recommendations
does not treat user decks as tournament records
does not read source/provider tables
```

Deck memory is local user data. It is useful for finding prior imports and
their linked local analyses, not for establishing metagame truth.
