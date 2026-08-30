# Phase 44O Goal Engine Change / Impact Engine Implementation Report

Status: local implementation packet; not externally validated or accepted

## Scope

Phase44O implements only the accepted Phase44N Change / Impact Engine v1
contract. It provides pure immutable caller-input records, exact-field parsers,
canonical serialization, semantic hashes, reference validation, and revision
validation. It is a planning representation, not a decision or execution
surface.

## Changed Files

```text
codie/goal_engine/impact.py
codie/goal_engine/__init__.py
tests/test_goal_engine_impact.py
docs/PHASE44O_GOAL_ENGINE_CHANGE_IMPACT_ENGINE_IMPLEMENTATION_REPORT.md
```

## Implemented Boundary

The implementation adds the exact Phase44N v1 schemas for change candidates,
impact subjects and effects, dependencies, assumptions, rollback analyses,
validation requirements, historical attempts, assessments, and assessment
references. It preserves explicit `DIRECT`, `INDIRECT`, and `POSSIBLE`
likelihoods and explicit `EXPECTED_AFFECTED`, `EXPECTED_UNTOUCHED`, and
`UNKNOWN` subject expectations without converting any of them into causality,
truth, score, priority, decision, readiness, recommendation, or permission.

`build_change_impact_assessment(...)` consumes only supplied values. It checks
UTC timestamps without consulting a clock; resolves supplied evidence,
assumption, and validation-requirement identifiers against supplied immutable
snapshots; rejects dangling and duplicate identities; keeps supporting and
conflicting evidence separate; preserves visible limitations and assumption
disconfirmation criteria; and validates immediate, hash-linked revisions.
Later revisions cannot remove or rewrite prior caller-supplied records.

Rollback analyses and validation requirements are declarations only. They do
not perform, approve, schedule, or report rollback or validation. Historical
attempt records preserve `NOT_COMPARED` gaps and require text when callers use
`MATERIAL_DIFFERENCE_DOCUMENTED`.

## Explicit Non-Goals

This packet does not discover scope, retrieve history, infer effects or
causality, calculate risk or priority, select work, create or revise Goal
Contracts, grant authority, execute changes, run validation, observe results,
persist data, access a filesystem, repository, environment, process, network,
provider, model, clock, UUID, random source, UI, CLI, API, scheduler, worker,
or Stream Deck integration.

Hard evidence boundaries remain unchanged:

```text
fact != human decision != policy != authority
expected impact != observed outcome
validation requirement != validation result
rollback plan != rollback execution or success
```

Theory and theory-skill review gates remain external and mandatory. Official
Scryfall card truth, user-initiated public Moxfield inputs, Hareruya
tournament-only provenance, local-first behavior, zero-cost behavior, and
supplemental-only Stream Deck policy are unchanged.

## Local Verification

The focused Phase44O test suite covers canonical round trips, exact-field
parsing, evidence separation and resolution, explicit subject coverage,
history-gap handling, immediate hash-linked revisions, append-only revision
protection, immutable record fields, and import boundaries.

The implementation is not accepted until it has an exact-SHA pull-request
artifact with the required validators and a separate human merge approval.
