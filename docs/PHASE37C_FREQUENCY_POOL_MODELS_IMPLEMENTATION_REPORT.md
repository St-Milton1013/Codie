# Phase 37C - Frequency Pool Packet Models Implementation Report

Status: implementation prepared; PR validation and outside validation required

Phase 37C implements the local, in-memory Frequency Pool packet models and
validators authorized by the accepted Phase 37B implementation contract.

Phase 37C is not externally accepted by this document. Phase 37D remains
blocked until Phase 37C receives PASS or PASS WITH REVIEW NOTES from the
required validation path.

## Validation Tuple

```text
phase_id: Phase37C
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase37D
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Implementation Files

```text
codie/frequency_pools/__init__.py
codie/frequency_pools/models.py
tests/test_frequency_pool_models.py
tests/fixtures/frequency_pools/frequency_pool_commander.json
tests/fixtures/frequency_pools/frequency_pool_partner_pair.json
tests/fixtures/frequency_pools/frequency_pool_user_local.json
tests/fixtures/frequency_pools/frequency_pool_invalid.json
```

## Public Interface

```text
FREQUENCY_POOL_PACKET_VERSION
FrequencyPoolBuildError
FrequencyPoolSubject
FrequencyPoolSourceWindow
FrequencyPoolSourceRef
FrequencyPoolCardIdentity
FrequencyPoolCardRow
FrequencyPoolTagRow
FrequencyPoolCoverageReport
FrequencyPoolCaveat
FrequencyPoolPacket
FrequencyPoolOptions
build_frequency_pool_packet(...)
validate_frequency_pool_packet(...)
frequency_pool_packet_to_dict(...)
```

## Behavior Implemented

```text
packet serialization is deterministic
packets round-trip through dictionary form
packet values are immutable after build
input payloads are not mutated
pool type values are validated
canonical card identity is preserved
scryfall_id is preserved when supplied
oracle_id remains the analytics grouping identity
tag source provenance remains visible
source_ref_ids remain visible
caveat_ids remain visible
coverage values remain visible
unknown coverage values serialize explicit unknown markers
low sample coverage requires visible caveat
low coverage ratio requires visible caveat
user-local pools require explicit isolation labels
user-local pools are labeled not tournament evidence
user-local pools are labeled not recommendation input
private/raw metadata is rejected recursively
recommendation-language fields and metadata are rejected
```

## Boundary

Phase 37C remains model/validator-only.

It does not implement:

```text
source gathering
raw provider reads
source table reads
repository-backed builders
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

## Local Validation

Focused tests:

```text
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest tests.test_frequency_pool_models -v
Ran 14 tests
OK
```

Schema bootstrap:

```text
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe scripts/check_schema.py
Schema bootstrap check passed.
```

Full suite:

```text
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest discover -s tests -v
Ran 1047 tests
OK (skipped=1)
```

Whitespace check:

```text
git diff --check
passed
```

## Environment Note

The system `python` executable in this worktree is missing existing project
dependencies such as `qrcode` and `bs4`. The meaningful Windows
validation result above uses the repaired configured Codie venv:

```text
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe
```
