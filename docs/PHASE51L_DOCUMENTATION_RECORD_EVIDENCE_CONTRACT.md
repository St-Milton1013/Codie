# Phase51L Documentation Record Evidence Contract

Status: documentation-only contract

## Validation Tuple

```text
phase_id: Phase51L
phase_part: documentation-record-evidence-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase51M
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase51L addresses one independently disproved architecture-model finding from
Phase51K PR #113: the model said the Phase51I contract record was missing from
`docs/ACTIVE_ROADMAP_INDEX.md`, although the exact target-tree line says
`Phase51I Concrete Defect Distinction Contract: PASS through merged PR #112`.

This contract establishes a narrow, fail-closed structured record-evidence
path for architecture findings about a named phase record in a protected phase
ledger. It does not suppress a finding because a phase identifier appears
somewhere in a file, and it does not reinterpret free-text finding prose.

## Required Structured Record Assertion

For every architecture-model finding, the model response includes
`record_assertions`, an array that is empty unless the finding makes a claim
about the presence or status of a named phase record in a protected phase
ledger. Each assertion is exactly:

```text
record_kind: phase_contract
phase_id: Phase<digits><optional letter>
assertion: absent | status_mismatch
affected_file: protected phase-ledger path
record_location:
  section_anchor: exact target-tree section heading
  table_or_block_ordinal: positive integer within that section
  record_key: exact phase identifier
claimed_status: string | null
```

The assertion is mandatory when the model makes such a record claim. The
model may not use it for code, security, behavior, test, coverage, evidence,
policy, source, human-decision, outside-review, named-report, provider, UI,
database, or other non-record claims.

## Deterministic Record Index And Disposition

The implementation builds its index only from the current target tree and
protected phase ledgers. Every index entry records:

```text
ledger path
section anchor
table or block ordinal
exact inclusive line range
canonical record key
normalized exact-line digest
exact current line text
```

An architecture finding with one well-formed `absent` assertion is
audit-preservingly non-blocking only when all of the following are true:

```text
the asserted affected file is a protected phase ledger
the assertion resolves to exactly one target-tree index entry
the entry has the same phase_id and record_key
the entry has the same section anchor and table/block ordinal
the exact target-tree line proves the asserted phase record is present
```

File-level phase presence is never enough. A matching Phase51I record in a
different section or table must not clear a claim about another record slot.

Every `status_mismatch` assertion remains blocking unless the exact indexed
record at the asserted location proves the claimed status false. Missing,
malformed, duplicated, contradictory, wrong-file, wrong-section, wrong-block,
wrong-phase, unsupported, multi-assertion, non-architecture, or
insufficient-evidence cases remain blocking. The parser must never construct
or alter an assertion by searching finding prose for words, phrases, stems,
regexes, or natural-language equivalents.

When a supported record assertion is disproved by the deterministic index, the
immutable audit record retains the raw model finding, structured assertion,
canonical hash, target record location, exact line range, normalized digest,
exact target line, and machine-readable non-blocking reason.

## Authorized Phase51M Boundary

```text
codie/validation/local_gate.py
tests/test_validation_local_gate.py
docs/PHASE51K_STRUCTURED_CONCRETE_DEFECT_DISPOSITION_CONTRACT.md
docs/PHASE51M_DOCUMENTATION_RECORD_EVIDENCE_IMPLEMENTATION_REPORT.md
```

Phase51M may only add the structured record-assertion schema, prompt/context,
strict parser and deterministic exact-record index, immutable audit evidence,
and focused tests. It may update the Phase51K contract's `next_phase_id`,
Authorized Phase51L Boundary filename, and Hard Boundaries text from
Phase51L to Phase51N, as the required handoff before Phase51N is contracted.

It must not alter product behavior, database, provider, card truth, model
selection, severity, aggregate result policy, repair policy, workflow, UI,
CLI, source registry, scope authority, Phase51K's structured-disposition
meaning, held Phase51J, PR #113 content, or Phase44U.

## Required Tests

Phase51M must prove:

- the exact Phase51I absent assertion at the active-roadmap Current Work
  Packet block is audit-preserved and non-blocking when the indexed target line
  proves it present;
- the same phase identifier in a different section or block does not clear a
  finding about the asserted slot;
- absent record, genuine status mismatch, wrong phase, wrong file, wrong
  section, wrong ordinal, missing location, malformed fields, duplicate
  assertions, and contradictory assertions remain blocking;
- all non-record findings, including security, code, behavior, tests,
  coverage, named reports, human decisions, outside review, evidence, policy,
  source, and multi-file findings remain blocking;
- the exact original finding and target-tree evidence survive immutable audit
  serialization; and
- existing Phase51E/H/I, phase-status, deterministic, schema, and full-suite
  tests remain green.

## Hard Boundaries And Gate

Phase51L does not accept PR #113, Phase51K, Phase51J, or Phase44U; rerun a
workflow; open/update a PR; merge; or grant any human authority. Theory and
theory-skill review gates, official Scryfall card truth, user-initiated public
Moxfield input, Hareruya tournament-only provenance, supplemental-only Stream
Deck, local-first/zero-cost execution, evidence-class separation, and human
roadmap/push/merge/promotion authority remain unchanged.

Phase51M remains blocked until this exact contract receives independent
artifact-backed validation and human merge. PR #113 may be revalidated only
after accepted Phase51M implementation reaches `main`. Phase51N remains
blocked until both Phase51K and Phase51M are accepted.
