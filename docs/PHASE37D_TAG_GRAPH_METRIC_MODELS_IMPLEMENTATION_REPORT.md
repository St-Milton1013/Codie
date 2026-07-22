# Phase 37D - Tag Graph Metric Packet Models Implementation Report

Status: implementation prepared; PR validation and outside validation required

Phase 37D implements the local, in-memory Tag Graph metric packet models and
validators described by the accepted Phase 37A split.

Phase 37D is not externally accepted by this document. Phase 37E remains
blocked until Phase 37D receives PASS or PASS WITH REVIEW NOTES from the
required validation path.

## Validation Tuple

```text
phase_id: Phase37D
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase37E
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Implementation Files

```text
codie/tag_graphs/__init__.py
codie/tag_graphs/models.py
tests/test_tag_graph_models.py
tests/fixtures/tag_graphs/tag_graph_comparison.json
tests/fixtures/tag_graphs/tag_graph_trend.json
tests/fixtures/tag_graphs/tag_graph_invalid.json
```

## Public Interface

```text
TAG_GRAPH_PACKET_VERSION
TagGraphBuildError
TagGraphSubject
TagGraphComparisonRef
TagGraphSelectedTag
TagGraphMetricRow
TagGraphContributorRow
TagGraphOverlapRow
TagGraphCorrelationRow
TagGraphTrendRow
TagGraphNumericTable
TagGraphCardList
TagGraphCaveat
TagGraphPacket
TagGraphOptions
build_tag_graph_packet(...)
validate_tag_graph_packet(...)
tag_graph_packet_to_dict(...)
```

## Behavior Implemented

```text
packet serialization is deterministic
packets round-trip through dictionary form
packet values are immutable after build
input payloads are not mutated
graph type values are validated
selected tags are limited to one through six
duplicate selected tags are rejected
tag source provenance remains visible
source_packet_ids remain visible
caveat_ids remain visible
underlying numeric tables remain visible
underlying card lists remain visible
metric rows preserve required tag metrics
trend rows preserve window and delta fields
overlap rows preserve overlap metrics
correlation rows preserve sample size and bounded correlation
contributor rows preserve oracle IDs and card names
unknown coverage values serialize explicit unknown markers
private/raw metadata is rejected recursively
action-advice metadata and language are rejected
```

## Boundary

Phase 37D remains model/validator-only.

It does not implement:

```text
metric calculation from raw sources
source gathering
raw provider reads
source table reads
repository-backed builders
chart rendering
Tag Graph exports
UI
LLM calls
simulator runtime
analytics recalculation
action advice
file writing
schema changes
dependency changes
```

## Local Validation

Schema bootstrap:

```text
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe scripts/check_schema.py
Schema bootstrap check passed.
```

Focused tests:

```text
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest tests.test_tag_graph_models -v
Ran 13 tests
OK
```

Full suite:

```text
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest discover -s tests -v
Ran 1060 tests
OK (skipped=1)
```

Static whitespace check:

```text
git diff --check
passed
```
