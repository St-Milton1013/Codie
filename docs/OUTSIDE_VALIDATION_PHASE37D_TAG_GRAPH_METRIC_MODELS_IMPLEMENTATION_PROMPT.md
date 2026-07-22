# Outside Validation Prompt - Phase 37D Tag Graph Metric Packet Models

Validate Phase 37D as a local, in-memory Tag Graph metric packet model and
validator implementation.

Return one of:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Only PASS or PASS WITH REVIEW NOTES may unblock Phase 37E.

## Required Files To Review

```text
docs/PHASE37A_FREQUENCY_POOLS_TAG_GRAPH_LAB_CONTRACT.md
docs/PHASE37C_FREQUENCY_POOL_MODELS_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE37C_FREQUENCY_POOL_MODELS_IMPLEMENTATION_REPORT.md
docs/PHASE37D_TAG_GRAPH_METRIC_MODELS_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE37D_TAG_GRAPH_METRIC_MODELS_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE37D_TAG_GRAPH_METRIC_MODELS_IMPLEMENTATION_PROMPT.md
codie/frequency_pools/__init__.py
codie/frequency_pools/models.py
codie/tag_graphs/__init__.py
codie/tag_graphs/models.py
tests/test_frequency_pool_models.py
tests/test_tag_graph_models.py
tests/fixtures/tag_graphs/tag_graph_comparison.json
tests/fixtures/tag_graphs/tag_graph_trend.json
tests/fixtures/tag_graphs/tag_graph_invalid.json
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
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest tests.test_tag_graph_models -v
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest discover -s tests -v
```

## Required Checks

Confirm Phase 37D:

```text
implements only local Tag Graph metric packet models and validators
uses local fixtures only
serializes deterministically
round-trips through dictionaries
preserves immutable packet values
does not mutate input payloads
limits selected tags to one through six
rejects duplicate selected tags
preserves tag source provenance
preserves source_packet_ids
preserves caveat_ids
preserves numeric tables
preserves card lists
preserves required metric row fields
preserves trend row fields
preserves overlap row fields
preserves correlation row fields
preserves contributor row fields
serializes explicit unknown markers
rejects private/raw metadata recursively
rejects action-advice metadata and language
```

Reject Phase 37D if it implements:

```text
metric calculation from raw sources
provider reads
source table reads
repository-backed builders
chart rendering
exports
UI
LLM calls
simulator runtime
analytics recalculation
action advice
file writing
schema changes
dependency changes
```

Phase 37D is not accepted until this validation returns PASS or PASS WITH
REVIEW NOTES.
