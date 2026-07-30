# Outside Validation - Phase 42E Minimal User Correction Ledger Core

Validate Phase 42E from a clean checkout of the exact submitted commit.

## Required Review Files

```text
docs/CODIE_V2_CONSTITUTION.md
docs/ROADMAP_PATCH_V2_INTELLIGENCE_PROGRAM_INTAKE.md
docs/PHASE42A_JIN_THEORY_RULES_CORRECTIONS_CROSS_SPECIFICATION_BOUNDARY_CONTRACT.md
docs/PHASE42C_RULES_AUTHORITY_LEGALITY_BOUNDED_INTERACTION_CONTRACT.md
docs/PHASE42D_LOCAL_FIRST_MODEL_PROFILE_REDACTION_CONSENT_ROUTING_CONTRACT.md
docs/PHASE42E_MINIMAL_USER_CORRECTION_LEDGER_CORE_CONTRACT.md
docs/CHECKPOINT_PHASE42E_MINIMAL_USER_CORRECTION_LEDGER_CORE_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE42E_MINIMAL_USER_CORRECTION_LEDGER_CORE_PROMPT.md
docs/design_inputs/v2_intelligence_program/CODIE_V2_USER_CORRECTION_LEDGER_PROPOSAL.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

Treat the constitution and accepted contracts as authority. Treat the
Correction Ledger proposal as preserved design input only.

## Confirm Scope

Confirm Phase 42E:

```text
is contract-only
records Phase 42D artifact-backed acceptance
defines Phase42E / outside-validation / INTERMEDIATE_PACKET
defines Phase42F / outside-validation / INTERMEDIATE_PACKET as next
keeps Phase 42F blocked
changes no active validation scope in the PR
```

Reject if it adds production correction code, tests, fixtures, schema,
migrations, repositories, write services, consumers, providers, network
calls, models, Jin output, simulator or parser changes, UI, CLI, file writing,
dependencies, workflows, or constitution changes.

## Confirm Authority And Scope

Confirm:

```text
the ledger is an overlay, not a truth database
official authority and canonical truth remain hard external barriers
measured evidence is not rewritten
persisted recommendations are not written
corrections apply at the narrowest valid scope
scope selectors are explicit and fail closed
repetition does not promote authority
newest does not automatically win
Jin and models may propose A0 candidates but cannot activate them
```

## Confirm Lifecycle And Resolution

Confirm:

```text
the six ratified lifecycle states are preserved
only active, valid, effective, compatible corrections may apply
semantic history is append-only
semantic changes use explicit supersession
supersession cycles are invalid
safety-sensitive revalidation-required corrections stop enforcing
equal-rank incompatible corrections remain visible conflicts
authority, scope, time, exceptions, and supersession are deterministic
bundle serialization and hashing are deterministic
application receipts preserve exact bundle identity
```

## Confirm Privacy And Consumers

Confirm:

```text
the ledger is private and local by default
secret contents cannot be stored as correction data
users and private decks remain isolated
cloud transmission is governed by the accepted Phase 42D profile and consent
default exports omit private content
Jin, Rules, simulator, parsers, Decision Intelligence, Theory, and UI retain bounded roles
no consumer can use a correction to write canonical, measured, or recommendation records
acceptable_low_confidence_result cannot raise confidence
```

## Run

```text
git diff --check
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe scripts/check_schema.py
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest discover -s tests -v
```

Inspect the submitted diff for undeclared changes. Tests must not require live
network access or paid credentials.

## Verdict

Return one:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

List each finding with severity, affected file, governing rule, and required
correction. Phase 42F remains blocked unless the result is PASS or PASS WITH
REVIEW NOTES.
