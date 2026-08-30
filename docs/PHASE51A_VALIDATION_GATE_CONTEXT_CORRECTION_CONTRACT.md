# Phase51A Validation Gate Context Correction Contract

Status: local documentation-only contract packet; outside validation pending

## Validation Tuple

```text
phase_id: Phase51A
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase51B
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase51A is a separately gated validation-infrastructure contract. It does not
reclassify, widen, modify, or accept Phase44R. PR #100 remains open, unmerged,
and blocked until this contract and its separately implemented correction have
been accepted, after which PR #100 must be revalidated under the restored
Phase44R validation scope.

## Purpose

Add one deterministic, bounded evidence signal to architecture and adversarial
review context. It prevents the specific unsupported claim that a changed
production module has no validation when the same pull request contains a
changed `tests/test_*.py` module that directly imports it and the
deterministic full suite is clean.

The triggering evidence is preserved: PR #100 exact head
`1164a11f6406ad689a0a912acfacbdfcdcc4914a` received `REPAIR_REQUIRED` in
self-hosted run `33316542885`. Its architecture model reported one CRITICAL
“no validation” finding for `codie/goal_engine/experiment.py`, although the
same PR added `tests/test_goal_engine_experiment.py`, its focused 79 tests
passed, the deterministic full suite passed, and both PR unit-test checks
passed.

## Authorized Phase51B Implementation Boundary

Only the future Phase51B implementation may modify:

```text
codie/validation/local_gate.py
tests/test_validation_local_gate.py
docs/PHASE51B_VALIDATION_GATE_CONTEXT_CORRECTION_IMPLEMENTATION_REPORT.md
```

Its separate active-scope transition is one file only:

```text
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

No Phase44R file, PR #100 commit, product code, product data, schema,
workflow, provider, model profile, or repair-controller file is authorized.

## Required Behavior

Phase51B must add a deterministic `changed_test_evidence` value to
`_review_context()` before the bounded `pr_diff` is presented to a model. For
each changed Python production module, it must list only changed
`tests/test_*.py` files whose import statements directly reference that
module's dotted path. The value must also carry the already collected
deterministic full-suite result.

`_validator_prompt()` must add exactly this evidence-scoped instruction before
the bounded diff material:

```text
When changed_test_evidence identifies a changed test file that directly imports
a changed production module, and the deterministic full suite is CLEAN_PASS,
do not report that production module as having no validation. You may still
report a specific insufficiency only by identifying the missing behavior and
the supplied test evidence that does not cover it.
```

The implementation may not infer coverage from file names alone, treat a test
as passing without the deterministic result, or convert the evidence into a
waiver. A model may still report a concrete missing behavior, inadequate test,
architecture defect, security defect, scope violation, or any other supported
finding.

## Hard Boundaries

```text
No model selection change.
No severity, aggregation, cost-policy, or repair-attempt-limit change.
No PROTECTED_REPAIR_PATHS or PROTECTED_REPAIR_PREFIXES change.
No removal or weakening of an existing trusted prompt instruction.
No product code, product data, schema, workflow, provider, UI, CLI, API,
service, network, persistence, or authority change.
No change to Phase44R's authorized three-file boundary.
No rewrite, suppression, or retroactive alteration of validation run 33316542885.
No automated repair of codie/validation/; this is the separately gated,
human-authorized path required by the existing protected-repair boundary.
```

Hard evidence, local-first, zero-cost, Theory and theory-skill review, official
Scryfall truth, user-initiated Moxfield/pasted-deck scope, Hareruya
tournament-only provenance, absent/supplemental-only Stream Deck policy, and
human promotion and merge authority are unchanged.

## Required Deterministic Tests

Phase51B must prove:

1. a changed test directly importing a changed production module is recorded;
2. a changed test not importing that module receives no coverage credit;
3. a changed production module with no directly importing changed test remains
   uncredited;
4. existing bounded-diff and review-context limits remain unchanged;
5. the new prompt instruction is present and every existing trusted instruction
   remains unchanged; and
6. validation-gate tests, schema bootstrap, and the complete Codie suite pass.

## Gate and Continuation

Phase51A requires its own exact-SHA PR, deterministic, architecture,
adversarial, and aggregate validation artifact, and explicit human merge
authority. Phase51B remains blocked until then. Phase51B requires the same
separate process. Only after an accepted Phase51B implementation may a
one-file scope restoration return the protected active validation tuple to
Phase44R / implementation; PR #100 must then be revalidated at its unchanged
exact head. Phase44S remains blocked until Phase44R itself has a clean
exact-SHA artifact and human merge.
