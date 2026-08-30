# Phase51C Validation Gate Test-Evidence Enforcement Contract

Status: implementation contract only

## Validation Tuple

```text
phase_id: Phase51C
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase51D
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase51C defines one protected validation-gate correction after Phase51B's
prompt-only changed-test evidence was correctly supplied yet ignored twice by
the architecture model on Phase44U PR #105. It does not change Phase44U,
reinterpret its failing artifacts, or grant merge authority.

Phase51D may deterministically suppress only a blanket architecture finding
that says a changed production module has *no validation*, when all of the
following are proven by the existing review context:

```text
validator is architecture
deterministic full suite is CLEAN_PASS
one or more changed tests directly import that exact changed module
the finding identifies no missing behavior, test case, or concrete defect
the finding's sole claim is absence of validation
```

The implementation must preserve the model finding as an auditable suppressed
record with the exact evidence basis. It must not suppress a specific coverage,
security, architecture, scope, or behavioral finding.

## Authorized Phase51D Boundary

```text
codie/validation/local_gate.py
tests/test_validation_local_gate.py
docs/PHASE51D_VALIDATION_GATE_TEST_EVIDENCE_ENFORCEMENT_REPORT.md
```

No product code, product tests, Phase44U file, schema, workflow, provider,
model selection, severity policy, aggregation policy, repair policy, UI, CLI,
network, or authority surface may change.

## Required Deterministic Rules

The filter must fail closed. It must retain a finding unless every listed
condition is established. Exact direct-import evidence remains necessary;
filename similarity, a passing focused test alone, a test outside the diff,
or a model assertion never qualifies. The filter applies to architecture output
only and must run before aggregation. It must record the original finding,
changed module, direct test paths, deterministic result, and reason.

It may not hide a finding that names a missing behavior, names a test deficiency,
contains an affected file beyond the evidenced module, alleges anything other
than absence of validation, or is emitted by deterministic/adversarial review.

## Required Tests

Phase51D must prove qualifying blanket findings are retained as suppressed
audit records and do not block aggregation; every near miss remains open:
no direct test, non-clean deterministic suite, different module, additional
defect claim, named missing behavior, multi-file finding, non-architecture
validator, and unknown wording. Existing Phase51B changed-test extraction and
prompt text must remain intact. Full suite and schema bootstrap must pass.

## Hard Boundaries And Gate

This is separate protected validator work. It does not accept Phase44U or
permit its merge. Theory/theory-skill, Scryfall, Moxfield, Hareruya,
supplemental-only Stream Deck, local-first/zero-cost, evidence, and human
authority boundaries remain unchanged. Phase51D and any Phase44U rerun remain
blocked until this exact contract is artifact-validated and human-merged.
