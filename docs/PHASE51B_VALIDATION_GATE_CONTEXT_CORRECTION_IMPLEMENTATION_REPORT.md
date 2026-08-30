# Phase51B Validation Gate Context Correction Implementation Report

Status: local implementation packet; not externally validated or accepted

## Scope

Phase51B implements only the accepted Phase51A Validation Gate Context
Correction contract. It adds bounded, deterministic changed-test import
evidence to model-review context so a bounded diff cannot support the specific
unsupported claim that a changed production module has no validation when a
changed test directly imports it and the deterministic full suite is clean.

## Changed Files

```text
codie/validation/local_gate.py
tests/test_validation_local_gate.py
docs/PHASE51B_VALIDATION_GATE_CONTEXT_CORRECTION_IMPLEMENTATION_REPORT.md
```

The separate local active-scope transition is limited to
`docs/CODIE_ACTIVE_VALIDATION_SCOPE.json`.

## Implemented Boundary

`run_validation_gate(...)` now carries its already-collected deterministic
validator report into the architecture and adversarial prompt construction.
The review context adds `changed_test_evidence` for changed `codie/*.py`
modules only. For each such module, it names only changed `tests/test_*.py`
files that directly import the module according to parsed Python import
syntax, and it records the deterministic full-suite result when that result is
available.

The exact Phase51A evidence-scoped prompt instruction is added before the
untrusted bounded review material. It does not create a waiver: reviewers may
still report a concrete missing behavior, inadequate test, architecture or
security defect, scope violation, or another supported finding.

## Preserved Boundaries

This packet makes no change to model selection, severity, aggregation,
cost policy, repair limits, protected repair paths or prefixes, product code,
product data, schema, workflow, provider, UI, CLI, API, service, network,
persistence, or authority. It does not modify Phase44R files, PR #100, or the
historical run `33316542885`.

Existing trusted prompt instructions remain present and are asserted by the
validation-gate test. Changed-test evidence is based on direct parsed imports,
not file-name inference; without a directly importing changed test or an
available clean deterministic full-suite result, no coverage credit is given.

Hard evidence separation, local-first and zero-cost constraints, mandatory
external Theory/theory-skill review, official Scryfall truth,
user-initiated Moxfield/pasted-deck scope, Hareruya tournament-only
provenance, absent/supplemental-only Stream Deck policy, and human promotion
and merge authority remain unchanged.

## Local Verification

The focused tests cover a direct changed-test import, an unrelated changed
test, no changed test, the exact new prompt rule, preservation of existing
trusted prompt instructions, and the pre-existing bounded review-context
limits. The exact implementation head must also pass schema bootstrap and the
complete Codie suite in an isolated local clone before publication.

This packet is not accepted until its exact-SHA pull-request artifact has
clean deterministic, architecture, adversarial, and aggregate validation
results and a human explicitly approves merging it. After acceptance, a
separate one-file scope restoration may return the active tuple to Phase44R;
only then may PR #100 be revalidated at its unchanged head.
