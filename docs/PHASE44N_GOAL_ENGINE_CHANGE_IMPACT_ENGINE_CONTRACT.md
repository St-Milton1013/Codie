# Phase 44N Goal Engine Change / Impact Engine Contract

Status: implementation contract only

## Validation Tuple

```text
phase_id: Phase44N
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase44O
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase44O is reserved for the pure Change / Impact Engine implementation. It remains blocked until Phase44N outside validation returns `PASS` or `PASS WITH REVIEW NOTES` and this contract is merged through human authority.

## Purpose

Phase44N defines the only implementation boundary permitted for Phase44O: a pure, immutable, deterministic, caller-input Change / Impact Engine v1.

The future engine may represent an explicitly proposed change, caller-supplied direct, indirect, and possible effects, expected untouched systems, dependencies, privacy/security/zero-cost/manual/operational considerations, rollback analysis, validation requirements, and historical-attempt comparison. It may not discover scope, search history, rank an intervention, select work, create or revise a Goal Contract, approve a change, execute a change, schedule validation, or claim an outcome.

Phase44N is documentation-only. It changes no production code, tests, schema, repositories, dependencies, workflows, active scope, providers, UI, CLI, Stream Deck integration, model behavior, storage, or runtime authority.

## Governing Authority

```text
docs/CODIE_V2_CONSTITUTION.md
-> accepted constitutional ADRs and contracts
-> docs/GOAL_ENGINE_V1_SPEC.md
-> docs/GOAL_ENGINE_IMPLEMENTATION_PROGRAM_V1.md
-> this bounded Phase44N contract
```

A proposed change, impact assessment, expected benefit, historical attempt, or clean validator result cannot grant authority or supersede this order.

## Accepted Baseline

Phase44N begins only because Phase44A-M, including the Findings + Idea Ledger contract, implementation, and checkpoint, are accepted; Phase50A-C remains accepted and frozen.

Phase44M acceptance evidence:

```text
pull request: 95
validated SHA: 4935e4c948f9526dce6d728606e419b96a35090b
workflow run ID: 33281202007
validation job ID: 99176558290
artifact ID: 9723039545
artifact digest: sha256:8aba56b408dba57f437114a3d25acdb35e57d21e6d39afd85979825f7570b1d4
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: CLEAN_PASS
aggregate: CLEAN_PASS
findings: 0
errors: 0
skipped validators: 0
merge commit: 94c945fcba2fccd6cc70b32e6f91217130ab68c8
post-merge main workflow run ID: 33294053568
post-merge main validation: PASS
```

The protected Phase44N tuple was established separately by local scope-transition commit `a947437`. That one-file transition is not part of this eight-document contract packet and must reach `main` before the contract PR is published.

## Existing Architecture Reconciliation

```text
foundation.py owns Goal identifiers, Goal Contract references, evidence and policy references,
  SIZE, RISK, ROLLBACK, and canonical hashing
state_engine.py owns observational project-state reconciliation
health.py owns immutable in-memory subsystem-health Findings
idea_ledger.py owns immutable Findings, Ideas, relations, and history
impact.py and tests/test_goal_engine_impact.py do not exist
```

Phase44O may reuse accepted immutable Foundation, State Engine, Health, and Ledger records. It may not repurpose them as mutable storage, evidence discovery, approval, execution, or authority surfaces.

## Future Phase44O Files

Phase44O may change only:

```text
codie/goal_engine/impact.py
codie/goal_engine/__init__.py
tests/test_goal_engine_impact.py
docs/PHASE44O_GOAL_ENGINE_CHANGE_IMPACT_ENGINE_IMPLEMENTATION_REPORT.md
```

No schema, migration, fixture, repository, provider, dependency, workflow, validator, CLI, UI, API, service, worker, queue, scheduler, Stream Deck, configuration, constitution, roadmap, or active-scope file is authorized.

## Required Schema Versions

Future Phase44O must use exact v1 schema identifiers:

```text
codie.goal_engine.change_candidate.v1
codie.goal_engine.impact_subject_reference.v1
codie.goal_engine.impact_effect.v1
codie.goal_engine.dependency_effect.v1
codie.goal_engine.impact_assumption.v1
codie.goal_engine.rollback_analysis.v1
codie.goal_engine.impact_validation_requirement.v1
codie.goal_engine.historical_attempt_reference.v1
codie.goal_engine.change_impact_assessment.v1
codie.goal_engine.change_impact_assessment_reference.v1
```

Existing `GoalIdentifier`, `GoalContractRevisionReference`, `GoalEvidenceReference`, policy references, `LedgerEntityReference`, and Foundation canonical helpers must be reused. Phase44O must not fork them or create a new evidence, authority, Goal, decision, execution, or approval class.

## Canonical Vocabulary

```text
effect likelihood: DIRECT, INDIRECT, POSSIBLE
subject expectation: EXPECTED_AFFECTED, EXPECTED_UNTOUCHED, UNKNOWN
impact dimension: FUNCTIONAL, DATA, ARCHITECTURE, DEPENDENCY, PRIVACY, SECURITY,
  ZERO_COST, MANUAL_BURDEN, OPERATIONAL_BURDEN, PERFORMANCE, RELIABILITY,
  COMPATIBILITY, VALIDATION, ROLLBACK
dependency effect: REQUIRES, CONSTRAINS, MAY_DEGRADE, BLOCKS, REPLACES,
  COMPATIBILITY_RISK
validation requirement: EVIDENCE_REVIEW, UNIT_TEST, REGRESSION_TEST, SCHEMA_CHECK,
  SECURITY_REVIEW, PRIVACY_REVIEW, ZERO_COST_REVIEW, MANUAL_REVIEW,
  OBSERVATION_WINDOW, ROLLBACK_REHEARSAL
historical comparison: NOT_COMPARED, SIMILAR_SUCCESS, SIMILAR_LIMITATION,
  SIMILAR_FAILURE, SIMILAR_REWIND, MATERIAL_DIFFERENCE_DOCUMENTED
```

Likelihood describes caller-supplied expected relationship, not causality, probability, priority, truth, or permission. `EXPECTED_UNTOUCHED` is a testable expectation, not a guarantee; `UNKNOWN` must retain its gap. No vocabulary value computes a score, rank, priority, confidence, readiness, approval, work order, experiment permission, implementation permission, or authority stage.

## Required Immutable Records

All records are frozen dataclasses with exact-field parsing, canonical serialization, fail-closed validation, and immutable tuples. IDs, timestamps, evidence, decisions, policy references, and authority references are caller supplied.

### ChangeCandidate

```text
change_id: str
subject: LedgerEntityReference
goal_ref: GoalIdentifier | None
goal_contract_ref: GoalContractRevisionReference | None
proposed_change_summary: str
baseline_summary: str
expected_result_summary: str
evidence_ref_ids: tuple[str, ...]
conflict_ref_ids: tuple[str, ...]
limitations: tuple[str, ...]
created_at: str
schema_version: str
```

A candidate is a bounded proposal description. It does not create a Goal, revise a Goal Contract, establish root cause, choose intervention, or claim authorization. Supporting and conflicting evidence remain separate.

### ImpactSubjectReference and ImpactEffect

```text
ImpactSubjectReference:
  subject: LedgerEntityReference
  expected_state: str
  evidence_ref_ids: tuple[str, ...]
  limitations: tuple[str, ...]
  schema_version: str

ImpactEffect:
  effect_id: str
  subject: LedgerEntityReference
  dimension: str
  likelihood: str
  expected_state: str
  statement: str
  evidence_ref_ids: tuple[str, ...]
  conflict_ref_ids: tuple[str, ...]
  assumption_ids: tuple[str, ...]
  limitations: tuple[str, ...]
  schema_version: str
```

Expected untouched subjects must be explicit; omission does not imply safety. Each effect remains an expectation and cannot claim an observed outcome or change state. `POSSIBLE` cannot be converted into direct impact by recency, source name, or absence of contradiction.

### DependencyEffect and ImpactAssumption

```text
DependencyEffect:
  dependency_effect_id: str
  subject: LedgerEntityReference
  dependency: LedgerEntityReference
  effect_kind: str
  statement: str
  evidence_ref_ids: tuple[str, ...]
  limitations: tuple[str, ...]
  schema_version: str

ImpactAssumption:
  assumption_id: str
  statement: str
  evidence_ref_ids: tuple[str, ...]
  disconfirmation_criteria: tuple[str, ...]
  limitations: tuple[str, ...]
  schema_version: str
```

Dependencies are recorded, not discovered. `BLOCKS` and `REQUIRES` do not schedule or activate work. Every assumption requires visible disconfirmation criteria and limitations; it does not become fact, policy, or authority merely by inclusion.

### RollbackAnalysis and ImpactValidationRequirement

```text
RollbackAnalysis:
  rollback_class: str
  known_good_reference: LedgerEntityReference | None
  rollback_summary: str
  preconditions: tuple[str, ...]
  validation_requirement_ids: tuple[str, ...]
  residual_risk_summary: str
  limitations: tuple[str, ...]
  schema_version: str

ImpactValidationRequirement:
  requirement_id: str
  requirement_kind: str
  statement: str
  evidence_ref_ids: tuple[str, ...]
  expected_subject_refs: tuple[LedgerEntityReference, ...]
  human_review_required: bool
  limitations: tuple[str, ...]
  schema_version: str
```

`rollback_class` reuses Foundation v1 ROLLBACK vocabulary. A rollback analysis is planning only: it cannot perform, approve, or verify a rollback, claim recoverability, or conceal residual risk. Requirements declare later checks; they do not run tests, fetch evidence, schedule review, grant approval, or assert a pass.

### HistoricalAttemptReference and ChangeImpactAssessment

```text
HistoricalAttemptReference:
  attempt_ref: LedgerEntityReference
  disposition: str
  material_difference_summary: str | None
  evidence_ref_ids: tuple[str, ...]
  limitations: tuple[str, ...]
  schema_version: str

ChangeImpactAssessment:
  assessment_id: str
  revision: int
  change: ChangeCandidate
  as_of: str
  affected_subjects: tuple[ImpactSubjectReference, ...]
  effects: tuple[ImpactEffect, ...]
  dependency_effects: tuple[DependencyEffect, ...]
  assumptions: tuple[ImpactAssumption, ...]
  rollback: RollbackAnalysis
  validation_requirements: tuple[ImpactValidationRequirement, ...]
  historical_attempts: tuple[HistoricalAttemptReference, ...]
  evidence_snapshot: tuple[GoalEvidenceReference, ...]
  supersedes_assessment: ChangeImpactAssessmentReference | None
  schema_version: str
```

The caller supplies the bounded history comparison set. `NOT_COMPARED` keeps the gap visible. Similar failed or rewound attempts need a documented material difference before they can be treated as distinguishable. Assessment revision one forbids a predecessor; later revisions require the same identity, next exact revision, and immediately prior semantic hash. The snapshot is immutable, caller-persistable, planning-only, and append-only under revision validation.

## Required Pure Interfaces

Future Phase44O may expose only:

```text
validate_effect_likelihood(...)
validate_subject_expectation(...)
validate_impact_dimension(...)
validate_dependency_effect_kind(...)
validate_validation_requirement_kind(...)
validate_historical_comparison_disposition(...)
validate_change_candidate(...)
validate_change_impact_assessment(...)
validate_change_impact_assessment_revision(...)
build_change_impact_assessment(...)
*_to_dict(...) / *_from_dict(...)
*_semantic_hash(...)
```

Every builder returns a new immutable value and uses only caller inputs. It may validate and package explicit records. It may not search a repository, infer scope, calculate priority, decide necessity, evaluate alternatives, use a model, poll dependencies, run validation, or mutate a system.

## Assessment Construction Algorithm

`build_change_impact_assessment(...)` must:

1. Validate caller-supplied UTC `as_of` without reading the wall clock.
2. Validate exact schemas, vocabularies, privacy, ownership, and immutable fields.
3. Resolve all effects, subjects, dependencies, assumptions, rollback requirements, historical attempts, and evidence references against supplied snapshots.
4. Require explicit expected untouched subjects where callers make that claim.
5. Keep direct, indirect, possible, unknown, supporting, conflicting, and historical evidence dimensions distinct.
6. Make privacy, security, zero-cost, manual burden, operational burden, validation, and rollback visible through explicit effects, assumptions, limitations, or requirements.
7. Preserve `NOT_COMPARED` history gaps and require material-difference text for a similar failed or rewound attempt considered distinguishable.
8. Reject duplicate IDs, dangling references, malformed hashes, hidden raw content, cross-owner private leakage, and revision rewrite or deletion.
9. Sort unordered collections canonically and return a byte-stable assessment.

The result contains no score, aggregate risk, priority, recommendation, decision, work order, Goal Contract, approval, execution, expected success, or authority output.

## Hard Evidence, Local-First, And Source Boundaries

Phase44O must preserve:

```text
fact != human decision != policy != authority
expected impact != observed outcome
direct != indirect != possible
expected untouched != unknown != absent
historical attempt != current applicability
rollback plan != rollback execution or success
validation requirement != validation result
confidence, likelihood, and risk != permission
passing validation != Build acceptance != Goal success
```

It is local-only, in-memory, deterministic, zero-cost, standard-library-only apart from accepted Goal Engine helpers, and caller-input only. It performs no filesystem, repository, worktree, database, process, environment, provider, network, model, telemetry, analytics, clock, UUID, random, test, validator, retrieval, simulation, persistence, notification, UI, CLI, API, service, worker, queue, scheduler, or Stream Deck operation.

Theory and theory-skill review gates remain external and mandatory. Rules, legality, Corrections, policy mutation, and source authority remain external. Official Scryfall remains card truth; public Moxfield and pasted decks remain user-initiated non-tournament inputs; Hareruya remains tournament-only provenance; Stream Deck remains absent and supplemental-only.

## Roadmap And Authority Boundary

Phase44N implements no:

```text
Phase44O implementation or Phase44P checkpoint work
Goal Experiment Engine, Read-Only Decision Core, Goal Regression Corpus,
Independent Goal Validator, or Shadow Mode
Stage 1 work-order authority, Stage 2 experiment authority, or Stage 3 Build Graph
CCPM-inspired execution, issue dispatch, agents, or autonomous implementation
Goal Contract creation or revision, necessity/ranking/actionability evaluation,
intervention selection, execution, rollback execution, or observation result
```

The human-authored roadmap remains canonical until later stages pass all gates and receive explicit human promotion.

## Authorized Phase44N Files

This contract packet may change only:

```text
docs/PHASE44N_GOAL_ENGINE_CHANGE_IMPACT_ENGINE_CONTRACT.md
docs/CHECKPOINT_PHASE44N_GOAL_ENGINE_CHANGE_IMPACT_ENGINE_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE44N_GOAL_ENGINE_CHANGE_IMPACT_ENGINE_CONTRACT_PROMPT.md
docs/GOAL_ENGINE_IMPLEMENTATION_PROGRAM_V1.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

The implementation-program edit is status-only. It does not change the accepted Phase44-49 sequence, capability roadmap, evidence rules, authority gates, Stage 4 disposition, or conditional Phase48 CCPM placement.

## Gate

Phase44O remains blocked until this exact Phase44N contract SHA receives artifact-backed `PASS` or `PASS WITH REVIEW NOTES` and Phase44N is merged by human authority. Phase44O must implement only this accepted contract.
