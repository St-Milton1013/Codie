# Outside Validation — Phase51A Validation Gate Context Correction Contract

Validate the exact pull-request head from a clean checkout.

## Validation Tuple

```text
phase_id: Phase51A
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase51B
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

## Required Review

Confirm that Phase51A:

```text
is documentation-only and separately gated from Phase44R
preserves PR #100 and run 33316542885 as historical evidence
defines only deterministic changed-test import evidence plus one prompt rule
requires direct imports, changed test files, and a CLEAN_PASS deterministic
  full-suite result before preventing a “no validation” claim
still permits any specific, supported test-coverage or architecture finding
does not change models, severities, aggregation, cost policy, repair limits,
  protected repair prefixes, product code/data, schemas, workflow, providers,
  UI, CLI, API, persistence, network, or authority
does not modify the Phase44R Experiment Engine boundary
requires explicit deterministic tests for positive, negative, and absent
  direct-import coverage cases
keeps Theory review, hard evidence, local-first/zero-cost, Scryfall,
  Moxfield/pasted-deck, Hareruya, and Stream Deck boundaries unchanged
changes exactly the eight authorized Phase51A documentation files
keeps Phase51B and Phase44S blocked pending their respective gates
```

Reject the packet if it weakens validator policy, hides a finding, treats a
test name as proof of coverage, alters PR #100, authorizes product behavior, or
advances Phase44R without its own clean exact-SHA validation and human merge.

## Commands

```text
git diff --check
python scripts/check_schema.py
python -m unittest tests.test_validation_local_gate -v
python -m unittest discover -s tests -p "test_*.py"
```

## Allowed Verdicts

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Phase51B remains blocked until `PASS` or `PASS WITH REVIEW NOTES` and human
merge.
