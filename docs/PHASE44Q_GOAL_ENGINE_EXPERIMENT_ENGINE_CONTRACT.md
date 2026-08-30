# Phase 44Q Goal Experiment Engine Contract

Status: implementation contract only

## Validation Tuple

```text
phase_id: Phase44Q
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase44R
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase44R is reserved for a pure, immutable, caller-input Goal Experiment
Engine implementation. It remains blocked until this exact contract receives
artifact-backed outside validation and is merged through human authority.

## Purpose

Phase44Q defines the complete planning boundary for an experiment. The future
engine may validate and package an explicitly proposed experiment, its
question, hypothesis, bounded inputs, expected observations, safety limits,
approval references, stop criteria, cleanup plan, rollback analysis, and
caller-supplied observations or outcomes.

It is not an experiment runner. It cannot select an experiment, approve one,
obtain approval, execute a command, create data, inspect a repository, access
a provider, schedule work, collect observations, decide success, or promote an
outcome into a Goal, policy, decision, or authority.

Phase44Q is documentation-only. It changes no production code, tests, schema,
repositories, dependencies, workflows, active scope, providers, UI, CLI,
Stream Deck integration, model behavior, storage, or runtime authority.

## Governing Authority

```text
docs/CODIE_V2_CONSTITUTION.md
-> accepted constitutional ADRs and contracts
-> docs/GOAL_ENGINE_V1_SPEC.md
-> docs/GOAL_ENGINE_IMPLEMENTATION_PROGRAM_V1.md
-> this bounded Phase44Q contract
```

An experiment description, approval reference, planned outcome, or clean
validator result cannot grant authority or supersede that order.

## Accepted Baseline

Phase44Q begins only because Change / Impact Engine contract, implementation,
and checkpoint are accepted through Phase44N, Phase44O, and Phase44P.

Phase44P acceptance evidence:

```text
pull request: 98
validated SHA: 2210f03466b8b1fa6355a5acd63219a5f5427433
workflow run ID: 33296674722
validation job ID: 99217429479
artifact ID: 9727637007
artifact digest: sha256:9c4dcde550963f2b075d1cc10e05c2b27ffbaa70678eb9999469c3939fa63acf
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: CLEAN_PASS
aggregate: CLEAN_PASS
findings: 0
errors: 0
skipped validators: 0
merge commit: 2a3f790e03633e73e8f78a8b138eb054753459c3
post-merge main workflow run ID: 33296788341
post-merge main validation: PASS
```

The protected Phase44Q tuple must be established by a separate one-file active
scope transition. That transition is not part of this contract packet and must
reach `main` before a contract PR is published.

## Existing Architecture Reconciliation

```text
foundation.py owns canonical Goal, evidence, policy, risk, and rollback references
state_engine.py owns observational project-state reconciliation
health.py owns immutable in-memory subsystem-health Findings
idea_ledger.py owns immutable Findings, Ideas, relations, and history
impact.py owns caller-supplied expected impact, validation, rollback, and history records
experiment.py and tests/test_goal_engine_experiment.py do not exist
```

Phase44R may reuse accepted immutable records. It may not mutate them, discover
evidence, turn an experiment into a Goal, or reinterpret a planned or observed
result as permission.

## Future Phase44R Files

Phase44R may change only:

```text
codie/goal_engine/experiment.py
codie/goal_engine/__init__.py
tests/test_goal_engine_experiment.py
docs/PHASE44R_GOAL_ENGINE_EXPERIMENT_ENGINE_IMPLEMENTATION_REPORT.md
```

No schema, migration, fixture, repository, provider, dependency, workflow,
validator, CLI, UI, API, service, worker, queue, scheduler, configuration,
constitution, roadmap, active-scope, or Stream Deck file is authorized.

## Required Schema Versions and Vocabulary

Future Phase44R must use only these exact schema identifiers:

```text
codie.goal_engine.experiment_question.v1
codie.goal_engine.experiment_hypothesis.v1
codie.goal_engine.experiment_input.v1
codie.goal_engine.experiment_boundary.v1
codie.goal_engine.experiment_stop_criterion.v1
codie.goal_engine.experiment_cleanup_plan.v1
codie.goal_engine.experiment_approval_reference.v1
codie.goal_engine.experiment_observation.v1
codie.goal_engine.experiment_outcome.v1
codie.goal_engine.goal_experiment.v1
codie.goal_engine.goal_experiment_reference.v1
```

```text
experiment status: DRAFT, PROPOSED, APPROVED_REFERENCE_RECORDED, OBSERVED,
  STOPPED, CLOSED
input class: CALLER_SUPPLIED, FIXTURE, SYNTHETIC, PUBLIC_USER_INITIATED
boundary kind: SCOPE, DATA, PRIVACY, SECURITY, ZERO_COST, MANUAL_BURDEN,
  TIME, RESOURCE, NETWORK_DENIED, PROVIDER_DENIED, WRITE_DENIED
stop criterion kind: SAFETY, PRIVACY, COST, SCOPE, EVIDENCE, HUMAN_REQUEST,
  TIME, RESOURCE, VALIDATION
observation disposition: OBSERVED, NOT_OBSERVED, INCONCLUSIVE, BLOCKED
outcome disposition: NOT_INTERPRETED, SUPPORTS_HYPOTHESIS,
  DOES_NOT_SUPPORT_HYPOTHESIS, INCONCLUSIVE, STOPPED
```

Vocabulary describes caller-supplied planning or observation. It does not
calculate probability, risk, confidence, priority, readiness, success,
permission, approval, or authority.

## Required Immutable Records

All future records are frozen dataclasses with exact-field parsing, canonical
serialization, immutable tuples, fail-closed validation, and caller-supplied
identifiers and timestamps.

```text
ExperimentQuestion:
  question_id, statement, evidence_ref_ids, limitations, schema_version

ExperimentHypothesis:
  hypothesis_id, statement, expected_observation, disconfirmation_criteria,
  evidence_ref_ids, limitations, schema_version

ExperimentInput:
  input_id, input_class, subject, description, evidence_ref_ids,
  limitations, schema_version

ExperimentBoundary:
  boundary_id, boundary_kind, statement, evidence_ref_ids, limitations,
  schema_version

ExperimentStopCriterion:
  criterion_id, criterion_kind, statement, human_review_required,
  limitations, schema_version

ExperimentCleanupPlan:
  cleanup_id, statement, preconditions, validation_requirement_ids,
  residual_risk_summary, limitations, schema_version

ExperimentApprovalReference:
  approval_ref_id, authority_kind, decision_ref, scope_statement,
  recorded_at, limitations, schema_version

ExperimentObservation:
  observation_id, statement, disposition, observed_at, evidence_ref_ids,
  limitations, schema_version

ExperimentOutcome:
  outcome_id, disposition, statement, observation_ref_ids,
  limitations, schema_version

GoalExperiment:
  experiment_id, revision, question, hypothesis, inputs, boundaries,
  stop_criteria, cleanup_plan, rollback, approval_references, observations,
  outcome, impact_assessment_ref, evidence_snapshot, as_of,
  supersedes_experiment, schema_version
```

An approval reference records a caller-supplied human decision. It does not
prove that approval exists, authorize execution, or substitute for the
separate human gate. An observation records what the caller states was seen;
it cannot prove execution, causality, outcome, safety, or success.

## Required Construction and Validation Rules

Future Phase44R may expose only validation, construction, canonical
serialization, parsing, semantic-hash, and revision-validation helpers for the
records above. A builder must:

1. accept only caller inputs and a caller-supplied UTC `as_of` value;
2. require an explicit question, hypothesis, bounded inputs, boundaries, stop
   criteria, cleanup plan, rollback analysis, limitations, and evidence links;
3. keep expected observations separate from observations and outcomes;
4. require each scope, data, privacy, security, zero-cost, manual-burden, and
   resource boundary to be explicit or visibly absent;
5. record approval references without treating them as executable permission;
6. reject duplicate IDs, dangling references, malformed hashes, hidden raw
   content, cross-owner private leakage, mutable collections, revision rewrite,
   and revision deletion; and
7. canonically sort unordered collections and return byte-stable immutable data.

Revision one forbids a predecessor. Later revisions require the same identity,
the next exact revision, and the immediately prior semantic hash. Observations
and outcomes are append-only caller records; they cannot silently overwrite a
prior record.

## Hard Boundaries

Phase44R must preserve:

```text
fact != human decision != policy != authority
proposal != approval reference != execution permission
hypothesis != expected observation != observed fact != outcome interpretation
stop criterion != stop detection != stopping an experiment
cleanup plan != cleanup execution != cleanup success
rollback analysis != rollback execution or recovery success
validation requirement != validation execution or result
passing validation != Build acceptance != Goal success
```

It is local-only, in-memory, deterministic, zero-cost, standard-library-only
apart from accepted Goal Engine helpers, and caller-input only. It performs no
filesystem, repository, worktree, database, process, environment, provider,
network, model, telemetry, analytics, clock, UUID, random, test, validator,
retrieval, simulation, persistence, notification, UI, CLI, API, service,
worker, queue, scheduler, execution, or Stream Deck operation.

Theory and theory-skill review remain external and mandatory. Rules, legality,
Corrections, policy mutation, and source authority remain external. Official
Scryfall remains card truth; public Moxfield and pasted decks remain
user-initiated non-tournament inputs; Hareruya remains tournament-only
provenance; Stream Deck remains absent and supplemental-only.

## Deferred Work

Phase44Q and Phase44R implement no experiment execution, autonomous
experiment authority, Goal Contract creation or revision, decision core,
recommendation, corpus, validator, shadow mode, Stage 1 work-order authority,
Stage 2 experiment authority, Stage 3 Build Graph, CCPM execution, agents, or
autonomous implementation. The human-authored roadmap remains canonical.

## Authorized Phase44Q Files

This contract packet may change only:

```text
docs/PHASE44Q_GOAL_ENGINE_EXPERIMENT_ENGINE_CONTRACT.md
docs/CHECKPOINT_PHASE44Q_GOAL_ENGINE_EXPERIMENT_ENGINE_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE44Q_GOAL_ENGINE_EXPERIMENT_ENGINE_CONTRACT_PROMPT.md
docs/GOAL_ENGINE_IMPLEMENTATION_PROGRAM_V1.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Gate

Phase44R remains blocked until this exact Phase44Q contract SHA receives
artifact-backed `PASS` or `PASS WITH REVIEW NOTES` and Phase44Q is merged by
human authority. Phase44R must implement only this accepted contract.
