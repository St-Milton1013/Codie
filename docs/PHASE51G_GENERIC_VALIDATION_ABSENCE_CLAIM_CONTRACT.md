# Phase51G Generic Validation-Absence Claim Contract

Status: implementation contract only

## Validation Tuple

```text
phase_id: Phase51G
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase51H
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase51G defines one bounded follow-up to Phase51E. The accepted Phase51E
rule correctly preserved a later architecture-model finding on Phase44U PR
#105 because its wording differed from the recognized "no validation" forms.
The exact-head correct-scope artifact instead claimed only that a new file
"has not been validated according to the governance rules." Deterministic and
adversarial validation were clean, and the changed test directly imported the
changed production module.

Phase51H may recognize that same class of *generic absence-of-validation*
architecture claim without depending on one phrase. It does not change
Phase44U, reinterpret prior artifacts, accept a PR, or grant authority.

## Authorized Phase51H Boundary

```text
codie/validation/local_gate.py
tests/test_validation_local_gate.py
docs/PHASE51H_GENERIC_VALIDATION_ABSENCE_CLAIM_IMPLEMENTATION_REPORT.md
```

The existing `suppressed_findings` schema and audit representation are reused;
no report shape, schema, workflow, product, provider, model selection,
severity, aggregation, repair, UI, CLI, source, or authority change is
authorized.

## Required Deterministic Rule

Phase51H may suppress an architecture finding only when all of the following
are established from trusted review context:

```text
validator is architecture
deterministic full suite is CLEAN_PASS
one or more changed tests directly import the one affected changed module
the model finding's sole claim is generic absence of validation for that module
the finding names no missing behavior, test, assertion, coverage, security,
architecture, scope, source, policy, or other concrete defect
```

"Generic absence" may include conservative synonymous claims such as a file
being unvalidated, not validated, missing validation, or missing a generic
validation report. It must not include an assertion that a particular required
artifact, human decision, outside review, test, behavior, or method is absent.
If the text is mixed, ambiguous, multi-file, unsupported by exact direct test
evidence, or does not establish every condition, the finding remains open.

The original model finding must remain in immutable `suppressed_findings` with
the existing canonical hash and exact evidence basis. Suppression is not a
waiver, resolution, deferred finding, approval, or replacement for human
outside validation.

## Required Tests

Phase51H must prove that qualifying synonymous generic absence claims are
suppressed and audited, including the exact Phase44U wording from run
`33351194463`. It must prove all near misses remain blocking: no direct test,
non-clean deterministic suite, a different or multiple affected module,
non-architecture validator, a named report/artifact/outside-review requirement,
and any specific behavior, test, coverage, security, architecture, scope,
source, policy, or ambiguous claim. Existing Phase51E qualification, audit,
schema, parsing, and serialization tests must remain intact. Full suite and
schema bootstrap must pass.

## Hard Boundaries And Gate

This is separate protected validation-gate work. It does not accept Phase44U
or permit its merge. Theory/theory-skill, Scryfall, Moxfield, Hareruya,
supplemental-only Stream Deck, local-first/zero-cost, evidence, and human
authority boundaries remain unchanged. Phase51H and any further Phase44U rerun
remain blocked until this exact contract is artifact-validated and human-
merged.
