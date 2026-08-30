# Phase44T Goal Engine Read-Only Decision Core Contract

Status: implementation contract only

## Validation Tuple

```text
phase_id: Phase44T
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase44U
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase44T defines the only Phase44U implementation boundary: a pure,
deterministic, immutable, caller-input Read-Only Decision Core v1. It may
evaluate a caller-supplied bounded packet and return either `HEALTHY_IDLE` or
an advisory Goal Candidate and draft Goal Contract. A result is an explanation,
not a work order, approval, current fact, persistence request, or authority.

This documentation-only packet changes no production code, tests, schema,
repositories, dependencies, workflows, active validation scope, providers, UI,
CLI, Stream Deck behavior, model behavior, or runtime authority.

## Governing Authority And Baseline

Authority remains `docs/CODIE_V2_CONSTITUTION.md`, accepted constitutional
ADRs/contracts, `docs/GOAL_ENGINE_V1_SPEC.md`, the implementation program, then
this bounded contract. Phase44A through Phase44S are accepted in sequence;
Phase44S is accepted through merged PR #103. Phase51A/B are accepted validator
context infrastructure only. The human-authored roadmap remains canonical until
validated Stage 1 plus explicit human promotion.

The existing accepted inputs are caller-owned immutable records from Foundation,
State Engine, Health, Findings + Idea Ledger, Change/Impact, and Experiment
Engine. Phase44U must not change or reinterpret them. It creates no storage,
lookup, source registry, provider fetch, repository scan, or historical search.

## Future Phase44U Files

Only these files may change:

```text
codie/goal_engine/decision_core.py
codie/goal_engine/__init__.py
tests/test_goal_engine_decision_core.py
docs/PHASE44U_GOAL_ENGINE_READ_ONLY_DECISION_CORE_IMPLEMENTATION_REPORT.md
```

No schema, migration, fixture, database, repository, provider, dependency,
workflow, validator, CLI, UI, API, service, worker, scheduler, configuration,
constitution, or Stream Deck file is authorized.

## Required Vocabulary And Schemas

```text
codie.goal_engine.decision_input.v1
codie.goal_engine.decision_assessment.v1
codie.goal_engine.goal_candidate.v1
codie.goal_engine.draft_goal_contract.v1
codie.goal_engine.decision_evidence_reference.v1
codie.goal_engine.decision_limitation.v1
```

Assessment values are exactly `HEALTHY_IDLE` and `GOAL_CANDIDATE`. A candidate
is not a Goal, active work, a selected next task, or an approved contract.
All records are frozen dataclasses, strict exact-field parsed, canonically
serialized, semantic-hashed with Foundation v1 conventions, and use immutable
tuples. Unknown fields, mutable values, duplicate IDs, dangling references,
unknown vocabulary, secret material, or malformed hashes fail closed.

## Required Inputs And Outputs

`DecisionInput` must contain caller-supplied immutable references for the
observed problem (if any), evidence, conflicts, limitations, historical
attempts, accepted policy/human-decision references, state/health/findings/idea
ledger/change-impact/experiment assessments as applicable, and caller-supplied
`as_of`. Every input preserves its source semantic hash and evidence ceiling.

`DecisionAssessment` must separately and visibly report these nine questions:

```text
Necessity: concrete meaningful consequence if nothing is done
Evidence: support, conflict, freshness, and limitations
Root Cause: caller-supplied hypothesis and confidence only
History: relevant supplied attempts, failures, rewinds, and outcomes
Actionability: whether supplied evidence supports a bounded next investigation
Experiment Need: whether a bounded experiment is needed before any intervention
Intervention: smallest caller-supplied plausible intervention, if any
Impact: supplied expected affected and unaffected systems only
Priority: bounded advisory rationale only; never a queue position or selection
```

The core must return `HEALTHY_IDLE` whenever no concrete evidence-backed,
actionable problem survives these gates. It must prefer that outcome to
manufacturing work. A non-idle output may include one `GoalCandidate` and one
`DraftGoalContract`, each visibly labelled advisory and non-authoritative.

A draft contract retains only caller-supplied or mechanically derived bounded
fields: originating references, observed problem, acceptable result, maximum
acceptable regressions, root-cause hypothesis/confidence, alternatives,
disconfirmation, expected affected/unaffected systems, dependencies, evidence
snapshot, history, limitations, and approval requirements. It cannot claim
approval, approval readiness, activation, implementation authorization, or
current truth.

## Required Pure Interfaces

```text
validate_decision_input(...)
validate_decision_assessment(...)
evaluate_read_only_decision(...)
build_healthy_idle_assessment(...)
build_goal_candidate(...)
build_draft_goal_contract(...)
*_to_dict(...) / *_from_dict(...) / *_semantic_hash(...)
```

Every interface uses caller inputs only and returns new immutable values. It
does not read time, filesystem, environment, process, repository, network,
provider, model, database, or prior storage; it performs no I/O, telemetry,
analytics, retry, monitoring, persistence, export, or mutation.

## Hard Decision And Authority Boundaries

```text
fact != human decision != policy != authority
candidate != Goal != selected work != active work
draft Goal Contract != approved Goal Contract != implementation authority
priority rationale != rank != queue position != work order
support != truth; conflict/limitation remains visible
history reference != retry permission
experiment need != experiment authorization
intervention proposal != execution permission
passing validation != Goal success or promotion
```

The core may not select, rank, schedule, activate, execute, retry, close,
promote, modify, merge, release, or approve work; create a real Goal or revise
an accepted Goal Contract; grant a CAP level; admit policy; bypass a human wait;
or make a human roadmap non-canonical. It must not infer missing evidence,
causality, consent, novelty, relation, source authority, universal priority, or
approval from text, confidence, recurrence, recency, user preference, or a
model.

Theory and theory-skill review stay external and mandatory. Rules, Corrections,
and source authority remain external. Official Scryfall remains card truth;
public Moxfield and pasted decks remain explicit user-initiated non-tournament
inputs; Hareruya remains tournament-only. No source is fetched or promoted.
Stream Deck remains absent and supplemental-only in any future separately
accepted display surface.

## Required Phase44U Tests

Tests must prove exact schemas/fields, immutable canonical values and hashes,
visible support/conflict/limitation separation, each assessment question,
`HEALTHY_IDLE` for no meaningful evidenced problem, no candidate from a health
finding alone, candidate/draft non-authority, no Goal or work-order output,
draft field provenance and evidence ceilings, no hidden ranking/selection,
fail-closed malformed references, and no I/O/imports or later-phase authority.
They must preserve all prior Goal Engine regression tests.

## Forbidden Work

Phase44U must not implement the Regression Corpus (44W-Y), independent
validator/shadow mode (45), Stage 1 work-order authority (46), experiment
authority (47), Build Graph/CCPM work (48), or later autonomy. It must not add
providers, source registry routing, UI, CLI, Stream Deck, persistence, schema,
network, models, or runtime orchestration.

## Authorized Phase44T Files And Gate

This contract packet may change only:

```text
docs/PHASE44T_GOAL_ENGINE_READ_ONLY_DECISION_CORE_CONTRACT.md
docs/CHECKPOINT_PHASE44T_GOAL_ENGINE_READ_ONLY_DECISION_CORE_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE44T_GOAL_ENGINE_READ_ONLY_DECISION_CORE_CONTRACT_PROMPT.md
docs/GOAL_ENGINE_IMPLEMENTATION_PROGRAM_V1.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

The separately published one-file scope transition is not part of this packet.
Phase44U remains blocked until the exact Phase44T contract has artifact-backed
`PASS` or `PASS WITH REVIEW NOTES` and is merged by human authority.
