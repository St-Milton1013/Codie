# Outside Validation Prompt - Phase 37C Frequency Pool Packet Models

Validate Phase 37C as a local, in-memory Frequency Pool packet model and
validator implementation.

Return one of:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Only PASS or PASS WITH REVIEW NOTES may unblock Phase 37D.

## Required Files To Review

```text
docs/PHASE37B_FREQUENCY_POOLS_TAG_GRAPH_LAB_IMPLEMENTATION_CONTRACT.md
docs/PHASE37C_FREQUENCY_POOL_MODELS_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE37C_FREQUENCY_POOL_MODELS_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE37C_FREQUENCY_POOL_MODELS_IMPLEMENTATION_PROMPT.md
codie/frequency_pools/__init__.py
codie/frequency_pools/models.py
tests/test_frequency_pool_models.py
tests/fixtures/frequency_pools/frequency_pool_commander.json
tests/fixtures/frequency_pools/frequency_pool_partner_pair.json
tests/fixtures/frequency_pools/frequency_pool_user_local.json
tests/fixtures/frequency_pools/frequency_pool_invalid.json
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Required Validation

Run:

```powershell
git diff --check
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe scripts/check_schema.py
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest tests.test_frequency_pool_models -v
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest discover -s tests -v
```

## Required Checks

Confirm Phase 37C:

```text
implements only the allowed Phase 37C files
defines the required public interface
uses local fixtures only
serializes deterministically
round-trips through dictionaries
preserves immutable packet values
does not mutate input payloads
preserves canonical card identity
preserves scryfall_id when supplied
preserves oracle_id for analytics grouping
preserves tag source provenance
preserves source_ref_ids
preserves caveat_ids
preserves coverage values
serializes explicit unknown coverage markers
requires visible low-sample caveats
requires visible low-coverage caveats
labels user-local pools visibly
isolates user-local pools from commander/global/tournament/recommendation use
rejects private/raw metadata recursively
rejects recommendation metadata and strategic language
```

Reject Phase 37C if it implements:

```text
provider reads
source table reads
repository-backed builders
raw data gathering
frequency pool calculation from raw sources
Tag Graph metric packets
Tag Graph visualizations
exports
UI
LLM calls
simulator runtime
analytics recalculation
recommendation output
file writing
schema changes
dependency changes
```

Phase 37C is not accepted until this validation returns PASS or PASS WITH
REVIEW NOTES.
