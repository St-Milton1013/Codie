# Phase51M Documentation Record Evidence Safety Amendment

Status: documentation-only implementation-safety amendment

## Validation Tuple

```text
phase_id: Phase51M
phase_part: documentation-record-evidence-implementation-safety-amendment
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase51M
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

## Superseded Mechanism

This amendment supersedes only Phase51L's per-finding `record_assertions`
mechanism. It does not reopen Phase51L's accepted purpose, Phase51K's
structured-disposition meaning, Phase51J, Phase44U, or any product boundary.

The per-finding shape is unsafe: a model could attach an otherwise valid record
assertion to an ordinary security, code, or other non-record finding. A
deterministic proof that the record assertion is false could then remove the
whole ordinary finding. That contradicts Phase51L's hard boundary that
non-record findings remain blocking.

## Required Two-Lane Response Shape

Phase51M replaces that shape with two independent top-level arrays:

```text
findings: ordinary architecture findings
documentation_record_assertions: documentation-record claims only
```

Every entry in `findings` keeps the existing validation path and remains
blocking unless an already-authorized, independent rule applies. The
documentation-record path must never remove, rewrite, downgrade, or suppress
an entry in `findings`.

Every `documentation_record_assertions` entry is exactly:

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

This lane has no severity, title, description, governing-rule, code, security,
or generic-finding field. The model must place a qualifying ledger
presence/status claim in this lane. A record claim left in `findings` remains
an ordinary blocking finding.

## Fail-Closed Deterministic Handling

The current target-tree protected-ledger index must retain the ledger path,
section anchor, table/block ordinal, exact inclusive line range, canonical
record key, normalized exact-line digest, and exact current line.

- An assertion disproved by exactly one current target-tree record is retained
  in immutable assertion-audit evidence and creates no ordinary finding.
- An absent, malformed, duplicate, contradictory, wrong-file, wrong-section,
  wrong-block, wrong-phase, insufficient-evidence, or otherwise unresolved
  assertion creates a deterministic blocking finding.
- Assertion handling never examines or changes ordinary `findings`.
- No code may infer an assertion, a disposition, or a security exception from
  free-text finding prose by keyword, phrase, stem, regex, or natural-language
  reclassification.

## Authorized Phase51M Boundary

```text
codie/validation/local_gate.py
tests/test_validation_local_gate.py
docs/PHASE51K_STRUCTURED_CONCRETE_DEFECT_DISPOSITION_CONTRACT.md
docs/PHASE51M_DOCUMENTATION_RECORD_EVIDENCE_IMPLEMENTATION_REPORT.md
```

Within this existing boundary, Phase51M may replace the held per-finding parser,
schema, prompt/context, filter, audit serialization, and focused tests with the
two-lane mechanism. It must preserve the required Phase51K-to-Phase51N
handoff. No other files or behavior are authorized.

## Required Tests

Phase51M must prove all of the following:

- the exact Phase51I ledger assertion relevant to PR #113 is separately audited
  as disproved when the exact indexed record is present;
- SQL injection, data exfiltration, authorization failure, and other ordinary
  security findings remain blocking while a separate record assertion is
  audited;
- a record claim mistakenly put in the ordinary findings lane remains blocking;
- genuine absence and status mismatch assertions, and every malformed or
  location-mismatched assertion, create deterministic blocking findings;
- ordinary findings and assertion audit evidence round-trip independently in
  immutable report serialization; and
- existing Phase51E/H/I tests, phase-status checks, schema bootstrap, and the
  full suite remain green.

## Hard Boundaries And Gate

This amendment does not accept, update, rerun, or merge PR #113; accept
Phase51K, Phase51J, or Phase44U; grant human authority; or alter provider,
database, card-truth, model-selection, severity, aggregate-policy, repair,
workflow, UI, CLI, source-registry, or scope authority behavior.

Theory and theory-skill review gates, official Scryfall card truth,
user-initiated public Moxfield input, Hareruya tournament-only provenance,
supplemental-only Stream Deck support, local-first/zero-cost execution,
evidence-class separation, and human roadmap/push/merge/promotion authority
remain unchanged.

Phase51M source work may resume only after this exact amendment receives
independent artifact-backed validation and human acceptance. PR #113 may be
revalidated only after accepted Phase51M implementation reaches `main`.
Phase51N remains blocked until both Phase51K and Phase51M are accepted.
