# Outside Validation Prompt - Phase50B Local Working Iteration v0.1

Validate the exact Phase50B pull-request SHA under:

```text
phase_id: Phase50B
phase_part: implementation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase50C
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Required review

Confirm the implementation:

```text
matches docs/PHASE50A_LOCAL_WORKING_ITERATION_V0_1_CONTRACT.md except for the
  narrow owner-approved clauses superseded by
  docs/PHASE50B_LOCAL_WORKING_ITERATION_V0_1_USABILITY_OVERRIDE.md
uses a loopback-only Python standard-library server
serves the built React UI and local JSON API from one origin
contains every server-side read and write below the configured workspace
initializes the existing SQLite schema idempotently
downloads card data only after explicit Prepare/Refresh action
uses only official Scryfall bulk metadata and trusted Scryfall HTTPS downloads
keeps the card-data cache contained, bounded, hashed, reusable, and atomic
retains explicit local Scryfall JSON import as a compatibility/recovery path
parses every Scryfall record before a transaction commits
rolls back a blocking catalog record without partial import
labels Scryfall only as card truth
accepts pasted deck text and public Moxfield deck links
fetches Moxfield only after explicit deck-import action through the existing
  rate-limited client and approved public endpoints
preserves the canonical public Moxfield URL as deck-source attribution
provides a paste-export fallback for private/unavailable decks, rate limits,
  network failure, or schema drift
atomically imports resolved deck text through existing domain APIs
returns unresolved names without partial deck/session persistence
redacts raw deck input from listings and default detail
imports only explicitly selected evidence-candidate JSON
retains evidence type, score, sample size, source record ID, and source URL
uses the existing evidence-only comparison and saved-analysis paths
shows present and absent as observations, never strategic advice
retrieves the same saved state after page reload
returns JSON and Markdown download content through safe local envelopes
performs no mutation, provider fetch, or hidden action on page load
rejects non-loopback hosts, path escape, missing/malformed Content-Length,
unsupported content type, malformed JSON, oversized payload, unsafe method,
unknown IDs, unsafe export format, invalid candidate, and raw traceback leakage
keeps Hareruya references tournament-only
keeps Jin, Theory, Rules, Corrections, simulation, recommendations, Goal Engine,
and Stream Deck behavior absent
adds no schema, dependency, workflow, existing-provider-client, or authority change
keeps Phase44H-49 and conditional Phase48 roadmap placement unchanged
records the Phase50A exact-SHA acceptance evidence correctly
advances only the active validation tuple from Phase50A to Phase50B
keeps Phase50C blocked pending Phase50B acceptance and human merge
```

Reject the packet if card truth is promoted to evidence, absence becomes a cut
or addition, a remote URL is fetched without the explicit bounded actions in
the Phase50B usability override, Hareruya is used outside tournament
evidence, a page-load mutation occurs, a non-loopback request is accepted, raw
deck text or traceback data leaks, a partial database write survives a failed
request, Stream Deck becomes required, Theory review is bypassed, or Goal
Engine authority changes.

## Commands

```text
python scripts/check_schema.py
python -m pytest -q tests/test_local_working_iteration.py tests/test_local_working_iteration_http.py tests/test_local_working_iteration_sources.py
python -m unittest discover -s tests -p "test_*.py"
python -m ruff check codie/local_app tests/test_local_working_iteration.py tests/test_local_working_iteration_http.py tests/test_local_working_iteration_sources.py
python -m mypy --follow-imports=skip codie/local_app
npm.cmd --prefix ui run build
git diff --check
```

Also record the non-regression inventories without requiring inherited,
untouched debt to be repaired inside Phase50B:

```text
python -m ruff check .
python -m mypy codie
```

Allowed verdicts:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Phase50C remains blocked until `PASS` or `PASS WITH REVIEW NOTES` and human
merge.
