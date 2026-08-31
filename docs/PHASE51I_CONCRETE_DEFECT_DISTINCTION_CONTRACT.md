# Phase51I Concrete Defect Distinction Contract

Status: implementation contract only

## Validation Tuple

```text
phase_id: Phase51I
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase51J
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase51I defines one bounded conformance correction to the accepted Phase51G
and Phase51H generic absence-of-validation rule. The correct-scope Phase44U
PR #105 artifact at `929e7dcf0d7f9de5f9a13ea45ff418e8a116aa32` claimed that
the new file was "without any validation" and generically needed validation
for "correctness and security." It named no vulnerability, threat, security
property, behavior, test, assertion, coverage gap, or other concrete defect.
Deterministic and adversarial validation were clean, and the changed test
directly imported the changed module.

Phase51H correctly preserved literal `security` language, but that is stricter
than Phase51G's required distinction between generic boilerplate and a named
concrete security defect. Phase51J may correct that classifier only. It does
not change Phase44U, reinterpret prior artifacts, accept a PR, or grant
authority.

## Authorized Phase51J Boundary

```text
codie/validation/local_gate.py
tests/test_validation_local_gate.py
docs/PHASE51J_CONCRETE_DEFECT_DISTINCTION_IMPLEMENTATION_REPORT.md
```

The existing audit schema, `suppressed_findings` representation, evidence
extractor, validator models, and workflow are reused unchanged. No product,
schema, provider, model selection, severity, aggregation, repair, UI, CLI,
source, or authority change is authorized.

## Required Deterministic Rule

Phase51J may classify generic references to correctness, reliability,
robustness, or security as boilerplate within an otherwise qualifying generic
absence-of-validation architecture claim. A word alone is not a concrete
defect. Every existing evidence condition remains required:

```text
validator is architecture
deterministic full suite is CLEAN_PASS
one or more changed tests directly import the one affected changed module
the finding's sole claim is generic absence of validation
```

The finding must remain open if it names any concrete deficiency, including a
missing or failing behavior, test, assertion, coverage area, security
vulnerability, threat, attack path, security property, data exposure,
authorization/authentication/control failure, injection class, architecture
defect, scope breach, source or policy violation, named report/artifact, human
decision, or outside review. Mixed or uncertain language, multiple affected
modules, and incomplete evidence remain blocking.

The original model finding must remain an immutable suppressed audit record
with its canonical hash and exact evidence. Suppression remains neither a
waiver nor a replacement for human outside validation.

## Required Tests

Phase51J must prove the exact Phase44U wording from run `33352581441` is
suppressed and audited only when every trusted evidence condition holds. It
must prove generic correctness/security boilerplate is insufficient to make a
claim concrete. It must retain as blocking a named vulnerability, threat,
attack, injection, data exposure, missing security property, behavior, test,
assertion, coverage, architecture, scope, source, policy, named artifact,
human decision, outside review, ambiguity, multi-file finding, unsupported
validator, missing direct import, and non-clean deterministic suite. Existing
Phase51E/H tests must remain intact. Full suite and schema bootstrap must pass.

## Hard Boundaries And Gate

This is separate protected validation-gate work. It does not accept Phase44U
or permit its merge. Theory/theory-skill, Scryfall, Moxfield, Hareruya,
supplemental-only Stream Deck, local-first/zero-cost, evidence, and human
authority boundaries remain unchanged. Phase51J and any further Phase44U rerun
remain blocked until this exact contract is artifact-validated and human-
merged.
