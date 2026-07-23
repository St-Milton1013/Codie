# Phase 39D - Cockatrice Interoperability Checkpoint Contract

Status: checkpoint contract only

## Validation Tuple

```text
phase_id: Phase39D
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase40A
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase 39D closes the Cockatrice Interoperability track as a checkpoint and
freeze packet. It records the accepted Phase 39C implementation evidence,
confirms the implementation remains local and fixture-first, and prepares the
roadmap to begin the V2 Relationship Intelligence program contract-first.

Phase 39D adds no runtime behavior. It does not authorize production code,
tests for new behavior, fixtures, schema, repositories, providers, analytics,
recommendations, simulator execution, UI, LLM calls, live network access, file
writing, dependencies, validator changes, workflow changes, active-scope
changes, or constitution changes.

## Accepted Phase 39C Evidence

```text
workflow run ID: 30017208205
validated SHA: c121330f8332f022049eea207079c511e5096873
artifact: codie-phase_ledger-validation-c121330f8332f022049eea207079c511e5096873
validation scope: phase_ledger
validator profile: all
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: CLEAN_PASS
aggregate: CLEAN_PASS
severity totals: BLOCKER 0, CRITICAL 0, HIGH 0, MEDIUM 0, LOW 0, INFORMATIONAL 0
skipped validators: none
unresolved findings: none
errors: none
final governance verdict: PASS
required corrections: none
```

## Authorized Files

Phase 39D may create or modify only:

```text
docs/PHASE39D_COCKATRICE_INTEROPERABILITY_CHECKPOINT_CONTRACT.md
docs/CHECKPOINT_PHASE39D_COCKATRICE_INTEROPERABILITY_CHECKPOINT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE39D_COCKATRICE_INTEROPERABILITY_CHECKPOINT_PROMPT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Checkpoint Requirements

Phase 39D must verify:

```text
Phase 39A is accepted with review notes and no required corrections
Phase 39B is accepted
Phase 39C is accepted
Phase 39C artifact metadata matches the exact merged main SHA
all three Phase 39C validators returned CLEAN_PASS
Phase 39C aggregate is CLEAN_PASS
Phase 39C has no findings, skipped validators, or errors
Cockatrice import/export remains local and fixture-first
Cockatrice XML parsing accepts supplied payload text only
Cockatrice export accepts supplied card rows only
unsupported zones, cards, and formats remain visible
unsafe XML remains rejected
user-local packets remain not_tournament_evidence
no live Cockatrice, provider, repository, or database access exists
no analytics, recommendations, simulator, CLI, or UI behavior exists
future file writing and CLI work remain separately contracted
Phase 40A begins Relationship Intelligence contract-first only
```

## Track Completion Boundary

The accepted Phase 39 implementation provides deterministic in-memory packet
models, validators, supplied XML parsing, and supplied-row export packet
building. It does not complete every possible Cockatrice integration.

Still deferred unless separately contracted:

```text
Cockatrice client automation
live Cockatrice network access
filesystem import or export writers
CLI commands
UI surfaces
collection synchronization
match tracking
repository persistence
provider adapters
analytics consumption
recommendation output
```

## Next Roadmap Gate

After Phase 39D returns PASS or PASS WITH REVIEW NOTES, Phase 40A may begin as
the Relationship Intelligence Core Contract. Phase 40A must remain
contract-only and must preserve the metric-only Class 2 evidence boundary in
`docs/CODIE_V2_CONSTITUTION.md`, Section 17.

Phase 40A must not authorize production implementation until a later accepted
implementation contract names the files, formulas, population rules,
provenance, caveats, and tests.

## Active Scope Handling

This PR must not modify `docs/CODIE_ACTIVE_VALIDATION_SCOPE.json`. The protected
scope remains Phase39C until this checkpoint packet is merged. Any transition
to Phase39D must use the approved protected-scope governance path after merge.

## Forbidden Work

Phase 39D must not add or change:

```text
production or test behavior
fixtures
schema or repositories
providers or live network access
Cockatrice runtime integration
filesystem writers
CLI or UI behavior
analytics or metrics
recommendations or deck-health output
simulator runtime
LLM calls
dependencies
validators or workflows
active validation scope
either constitution
```

## Outside Validation Packet

Review:

```text
docs/PHASE39D_COCKATRICE_INTEROPERABILITY_CHECKPOINT_CONTRACT.md
docs/CHECKPOINT_PHASE39D_COCKATRICE_INTEROPERABILITY_CHECKPOINT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE39D_COCKATRICE_INTEROPERABILITY_CHECKPOINT_PROMPT.md
docs/PHASE39C_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE39C_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE39C_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_PROMPT.md
docs/PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT.md
docs/PHASE39A_COCKATRICE_INTEROPERABILITY_CONTRACT.md
codie/cockatrice/interoperability.py
codie/cockatrice/__init__.py
tests/test_cockatrice_interoperability.py
tests/fixtures/cockatrice/
docs/CODIE_V2_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

## Required Validation

```text
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -v
```

Phase 40A remains blocked until Phase 39D receives artifact-backed PASS or
PASS WITH REVIEW NOTES.
