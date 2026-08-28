# Phase 44H Goal Engine Subsystem Health Foundation Contract

Status: implementation contract only

## Validation Tuple

```text
phase_id: Phase44H
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase44I
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase44H defines the only implementation boundary permitted for Phase44I: a
pure, immutable, deterministic, caller-input Subsystem Health Foundation v1.
It gives Codie a way to preserve evidence-backed health observations and
derive reviewable Findings without collapsing distinct subsystems, inventing a
universal score, selecting work, or producing a Goal.

No universal health score is authorized.

This packet is documentation-only. It does not implement health runtime or
change any accepted Foundation v1, State Engine v1, Local Working Iteration,
provider, evidence, recommendation, Jin, Theory, simulator, validation, or
authority behavior.

## Governing Authority

The authority order remains:

```text
docs/CODIE_V2_CONSTITUTION.md
-> accepted constitutional ADRs and contracts
-> docs/GOAL_ENGINE_V1_SPEC.md
-> docs/GOAL_ENGINE_IMPLEMENTATION_PROGRAM_V1.md
-> this bounded Phase44H contract
```

Goal Engine v1 remains subordinate to the Codie V2 Constitution. The V1
Constitution remains historical reference. Chat, generated text, local notes,
unreviewed Theory, user preference, health status, and a Finding cannot
supersede this authority order.

## Accepted Baseline

Phase44H begins only because all required predecessor gates are satisfied:

```text
Phase44A Goal Engine ratification: accepted
Phase44B-C Foundation v1 contract and implementation: accepted
Phase44D Foundation v1 checkpoint/freeze: accepted
Phase44E-F State Engine v1 contract and implementation: accepted
Phase44G State Engine v1 checkpoint/freeze: accepted through PR #86
Phase50A Local Working Iteration v0.1 contract: accepted through PR #87
Phase50B Local Working Iteration v0.1 implementation: accepted through PR #88
Phase50C Local Working Iteration v0.1 checkpoint/freeze: accepted through PR #89
```

Phase50C acceptance evidence:

```text
pull request: 89
validated SHA: ae32c9bc590274b7ef36ed1b388c38a811c6684d
workflow run ID: 32981468252
artifact ID: 9611629279
artifact digest: sha256:239592a38b9cd839688da51d79e7c7b97ee30237728e2af4b43b13d3b9e98969
merge commit: f814ad41e0863c95126c9d904bcbc00b5074d36e
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: CLEAN_PASS
aggregate: CLEAN_PASS
findings: 0
errors: 0
skipped validators: 0
```

The protected scope transition to Phase44H is a separate one-file commit. This
contract packet must not modify `docs/CODIE_ACTIVE_VALIDATION_SCOPE.json`.

## Existing Architecture Reconciliation

Repository inspection establishes:

```text
codie/goal_engine/foundation.py is the accepted Foundation v1 surface
codie/goal_engine/state_engine.py is the accepted State Engine v1 surface
codie/goal_engine/health.py does not exist
tests/test_goal_engine_health.py does not exist
FindingIdentifier already exists but no durable Finding ledger exists
GoalEvidenceReference already exists as the bounded evidence-reference record
Decision Intelligence remains the only persisted recommendation/deck-health authority
provider/source health records are not Goal Engine subsystem-health authority
deck-health conclusions are not project/Jin/Theory-Corpus health
repository validation is not the Independent Goal Validator
the evidence graph is not a Build Graph
```

Subsystem Health v1 must remain a new, isolated Goal Engine foundation. It may
reference accepted records but may not repurpose provider health, deck health,
validation findings, State Engine state, or user feedback as a universal
project-health conclusion.

## Future Phase44I Files

Phase44I may change only:

```text
codie/goal_engine/health.py
codie/goal_engine/__init__.py
tests/test_goal_engine_health.py
docs/PHASE44I_GOAL_ENGINE_SUBSYSTEM_HEALTH_FOUNDATION_IMPLEMENTATION_REPORT.md
```

No schema, migration, fixture, repository, provider, dependency, workflow,
validator, CLI, UI, API, service, worker, queue, scheduler, Stream Deck, or
constitutional file is authorized.

## Required Schema Versions

Future Phase44I must use exact v1 schema identifiers:

```text
codie.goal_engine.health_signal_definition.v1
codie.goal_engine.health_signal_observation.v1
codie.goal_engine.health_manifest.v1
codie.goal_engine.health_finding.v1
codie.goal_engine.subsystem_health_assessment.v1
codie.goal_engine.subsystem_health_assessment_reference.v1
```

Existing `GoalEvidenceReference` and `FindingIdentifier` schema versions must
be reused. Phase44I must not fork those records or create a new evidence class.

## Canonical Health Vocabulary

### Health domains

The exact v1 domains are:

```text
CODIE
JIN
THEORY_CORPUS
```

Every definition, observation, Finding, manifest, reference, and assessment
belongs to exactly one domain. A record cannot span domains. There is no
`GLOBAL`, `OVERALL`, `PROJECT`, `COMBINED`, or `UNIVERSAL` health domain.

Future domains such as Tournament Data, Simulator, Relationship Intelligence,
or Rules Layer health require later contracts and cannot be smuggled into an
existing domain.

### Assessment classes

```text
OBJECTIVE
SEMI_OBJECTIVE
SUBJECTIVE
```

Objective signals depend on reproducible facts. Semi-objective signals depend
on explicit reviewed interpretation plus evidence. Subjective signals are
limited to user-experience judgments and must name their human-feedback basis.

CODIE signals are objective in v1. JIN factual correctness, citation, and
privacy signals are objective; correction-handling and retrieval-quality
signals may be semi-objective; clarity and usefulness may be subjective.
THEORY_CORPUS manifest, ingestion, representation, attribution, contradiction,
and graph-integrity signals are objective; retrieval-quality and discovered-
gap interpretation may be semi-objective. No subjective signal may make or
weaken a factual claim.

### Signal statuses

```text
PASS
DEGRADED
FAIL
UNKNOWN
CONFLICTED
NOT_APPLICABLE
```

`UNKNOWN` is not pass, fail, absent, false, or unavailable. `CONFLICTED`
preserves incompatible current evidence. `NOT_APPLICABLE` requires an explicit
scope reason and cannot be used to hide a missing required signal.

These statuses describe one signal only. They are not lifecycle states,
validation verdicts, authority decisions, work priorities, or Goal states.

### Finding classes

```text
DEGRADATION
FAILURE
EVIDENCE_GAP
EVIDENCE_CONFLICT
STALE_EVIDENCE
PRIVACY_OR_SECURITY
MANIFEST_GAP
```

A health Finding is a reviewable evidence-backed conclusion. It is not a
validation finding, an Idea, a Goal, an Incident, a Correction, or a persisted
recommendation.

### Domain categories

CODIE categories:

```text
TESTS
VALIDATORS
DATA_INTEGRITY
PROVENANCE
INGESTION
SERVICES
INVARIANTS
SECURITY_PRIVACY
DEPENDENCIES
PERFORMANCE
RELIABILITY
SOURCE_HEALTH
```

JIN categories:

```text
FACTUAL_CORRECTNESS
CITATION_COVERAGE
PRIVACY
CORRECTION_HANDLING
RETRIEVAL_QUALITY
CLARITY
USEFULNESS
```

THEORY_CORPUS categories:

```text
MANIFEST_COMPLETENESS
INGESTION_INTEGRITY
REPRESENTATION_COVERAGE
RETRIEVAL_QUALITY
ATTRIBUTION_QUALITY
CONTRADICTION_COVERAGE
GRAPH_HEALTH
DISCOVERED_GAPS
```

Category/domain mismatches fail closed. New categories require a later
versioned contract.

## Required Immutable Records

All records are frozen dataclasses with exact-field parsing, canonical
serialization, and fail-closed validation. No record may contain raw provider
payloads, private deck text, prompts, prompt logs, credentials, secrets,
tokens, cookies, sessions, or unbounded metadata.

### HealthSignalDefinition

Required fields:

```text
definition_id: str
definition_version: int
domain: str
category: str
assessment_class: str
title: str
description: str
pass_condition: str
degraded_condition: str
fail_condition: str
unknown_condition: str
allowed_evidence_classes: tuple[str, ...]
policy_ref_ids: tuple[str, ...]
schema_version: str
```

A definition explains how one signal is interpreted. Conditions are bounded
descriptions for review and do not execute code. `policy_ref_ids` must resolve
to caller-supplied immutable accepted policy records when present. A
definition cannot contain a weight, global contribution, priority, target
Goal, intervention, or automatic action.

### HealthSignalObservation

Required fields:

```text
signal_id: str
definition_id: str
definition_version: int
domain: str
category: str
subject_id: str
status: str
summary: str
observed_value: str | int | float | bool | None
measurement_unit: str | None
confidence: float
observed_at: str
fresh_until: str | None
evidence_ref_ids: tuple[str, ...]
conflict_ref_ids: tuple[str, ...]
limitation: str | None
not_applicable_reason: str | None
schema_version: str
```

Observations are supplied by the caller. Phase44I may validate and package
them but may not inspect the repository, run tests, poll providers, query a
database, call a model, read the wall clock, or manufacture measurements.

An observation must match its definition's domain, category, and version.
`PASS`, `DEGRADED`, and `FAIL` require supporting evidence. `CONFLICTED`
requires at least two resolvable conflict references. `UNKNOWN` requires a
limitation. `NOT_APPLICABLE` requires a reason and is forbidden for required
manifest definitions. Evidence and conflict references remain disjoint.

Confidence describes support for that observation only. It grants no
authority and cannot convert missing or conflicting evidence into a pass.

### HealthManifest

Required fields:

```text
manifest_id: str
revision: int
domain: str
subject_id: str
scope_label: str
definition_ids: tuple[str, ...]
required_definition_ids: tuple[str, ...]
optional_definition_ids: tuple[str, ...]
scope_manifest_ref_ids: tuple[str, ...]
supersedes_manifest_hash: str | None
created_at: str
schema_version: str
```

The required and optional sets are disjoint, contain no duplicates, and union
exactly to `definition_ids`. Every referenced definition belongs to the
manifest domain. Revision greater than one requires the immediately prior
semantic hash; revision one forbids it.

Every observation in an assessment must match the manifest `subject_id`.
`THEORY_CORPUS` requires at least one immutable declared corpus-manifest
reference. Completeness, coverage, gap, and retrieval claims are bounded to
that declared manifest. No assessment may claim corpus completeness beyond
the manifest evidence. Other domains may use scope-manifest references but
cannot treat them as authority or a source of raw evidence.

### HealthFinding

Required fields:

```text
finding_id: FindingIdentifier
domain: str
finding_class: str
signal_ids: tuple[str, ...]
statement: str
why_it_matters: str
evidence_ref_ids: tuple[str, ...]
conflict_ref_ids: tuple[str, ...]
confidence: float
disconfirmation_criteria: tuple[str, ...]
limitations: tuple[str, ...]
created_at: str
schema_version: str
```

A Finding must resolve to one or more non-`PASS`, non-`NOT_APPLICABLE`
signals in the same domain. Its evidence cannot exceed the evidence carried by
those signals. It must state what would weaken or overturn it.

Health Findings are immutable, in-memory outputs in Phase44I. They are not
inserted into the future durable Findings/Idea Ledger, converted into Goals,
ranked as work, scheduled, promoted, or persisted. Phase44K-M will separately
define any durable ledger admission and lineage rules.

### SubsystemHealthAssessmentReference

Required fields:

```text
assessment_id: str
revision: int
domain: str
semantic_hash: str
schema_version: str
```

The domain must match the referenced assessment. References do not summarize,
score, approve, or supersede an assessment.

### SubsystemHealthAssessment

Required fields:

```text
assessment_id: str
revision: int
domain: str
manifest: HealthManifest
as_of: str
definitions: tuple[HealthSignalDefinition, ...]
signals: tuple[HealthSignalObservation, ...]
findings: tuple[HealthFinding, ...]
evidence_snapshot: tuple[GoalEvidenceReference, ...]
required_signal_count: int
observed_required_signal_count: int
unknown_required_signal_count: int
conflicted_required_signal_count: int
supersedes_assessment: SubsystemHealthAssessmentReference | None
schema_version: str
```

The assessment contains exactly one domain. It exposes bounded counts for
manifest coverage and evidence gaps but contains no overall status, score,
percentage, grade, rank, recommendation, priority, Goal candidate, or action.

Revision greater than one requires the immediately prior assessment reference;
revision one forbids it. Revision checks are explicit caller-invoked
validation and do not perform storage or discovery.

## Allowed Pure Interfaces

Future Phase44I may expose only:

```text
validate_health_domain(...)
validate_assessment_class(...)
validate_signal_status(...)
validate_finding_class(...)
validate_health_signal_definition(...)
validate_health_manifest(...)
validate_subsystem_health_assessment(...)
validate_subsystem_health_assessment_revision(...)
build_subsystem_health_assessment(...)
health_signal_definition_to_dict(...) / from_dict(...)
health_signal_observation_to_dict(...) / from_dict(...)
health_manifest_to_dict(...) / from_dict(...)
health_finding_to_dict(...) / from_dict(...)
subsystem_health_assessment_reference_to_dict(...) / from_dict(...)
subsystem_health_assessment_to_dict(...) / from_dict(...)
*_semantic_hash(...)
```

The implementation may use existing Foundation v1 canonical JSON, hash,
evidence-reference, Finding-identifier, and accepted-policy validation helpers.
It may not modify existing modules to weaken their contracts.

## Assessment Algorithm Contract

`build_subsystem_health_assessment(...)` must be pure and deterministic:

1. Validate one manifest, its exact domain, and its complete definition set.
2. Validate caller-supplied `as_of` as UTC without reading the wall clock.
3. Validate every observation against its exact definition and domain.
4. Reject duplicate IDs, duplicate required observations, dangling references,
   cross-domain records, forbidden fields, non-finite numbers, and unsorted or
   semantically ambiguous inputs.
5. Resolve every evidence, conflict, policy, manifest, and prior-assessment
   reference against caller-supplied immutable snapshots.
6. Preserve current, stale, unknown, conflicted, and not-applicable dimensions
   without substituting one for another.
7. Require exactly one observation for every required definition. Missing or
   duplicate required observations fail closed; an explicit `UNKNOWN`
   observation emits an `EVIDENCE_GAP` or `MANIFEST_GAP` Finding.
8. Emit a `STALE_EVIDENCE` Finding when caller-supplied `as_of` exceeds
   `fresh_until`, without rewriting the caller's signal status.
9. Emit evidence-bounded Findings for `DEGRADED`, `FAIL`, and `CONFLICTED`
   observations; preserve all conflicting evidence.
10. Do not emit a problem Finding from `PASS` or `NOT_APPLICABLE` alone.
11. Derive generated Finding IDs from canonical domain, subject, definition,
    signal, Finding-class, and evidence semantics; use `as_of` as generated
    `created_at`; never use randomness or the wall clock.
12. Calculate only exact manifest counts. Do not average, weight, normalize,
    rank, compare, or aggregate signals into a health score or overall verdict.
13. Sort all definitions, observations, Findings, evidence references, and
    identifier sets canonically.
14. Return a byte-stable single-domain assessment.

Caller-supplied Findings may be accepted only if they satisfy the same
signal/evidence constraints. The builder must reject invented evidence,
cross-domain Finding inputs, and duplicate semantic Findings.

## Domain-Specific Evidence Rules

### CODIE

CODIE health is objective and may summarize only caller-supplied evidence for
tests, validators, data integrity, provenance, ingestion, services,
invariants, security/privacy, dependencies, performance, reliability, and
source health. Passing tests do not prove constitutional compliance, Build
acceptance, Goal success, source freshness, or operational reliability.

Provider freshness or failure must remain a source-health signal with visible
downstream impact. It cannot silently change evidence class, elevate a source,
or cause network refresh.

### JIN

JIN objective correctness, citation, and privacy evidence remains separate
from semi-objective correction/retrieval evidence and subjective
clarity/usefulness feedback. User feedback is controlling for that user's
communication preference and subjective usefulness only. It cannot overwrite
Rules, card truth, tournament results, provenance, legality, or any other
factual evidence.

Long-horizon Jin improvement domains are monitoring subjects, not permanent
mutating Goals. A JIN Finding may request human review but cannot alter Jin,
rewrite an answer, update memory, activate a Correction, or schedule work.

### THEORY_CORPUS

THEORY_CORPUS health is relative to an immutable declared corpus manifest. It
may describe source completeness, ingestion integrity, representation
coverage, retrieval quality, attribution quality, contradiction coverage,
graph health, and discovered gaps only within that scope.

Unreviewed Theory can identify an intake or review gap but cannot count as an
accepted claim, objective fact, Rules evidence, tournament evidence, policy,
or implementation authority. Theory-skill review gates remain mandatory.

## Canonical Serialization And Hashing

Future Phase44I must preserve Foundation v1 conventions:

```text
UTF-8
JSON object keys sorted
compact separators
Unicode preserved
non-finite numbers rejected
SHA-256 lowercase semantic hashes
semantically unordered identifier sets sorted before storage
same canonical input -> byte-identical output
```

Full assessment hashes include provenance and evidence references. If a
comparison hash is introduced, the exact comparison dictionary must be public,
bounded, tested, domain-preserving, and unable to hide evidence differences.

## Hard Evidence Boundary

Subsystem Health v1 must keep separate:

```text
fact from human decision
objective from semi-objective from subjective assessment
historical validity from current applicability
current evidence from stale evidence
unknown from absent, false, unavailable, and not applicable
supporting evidence from conflicting evidence
signal from Finding
Finding from Idea
Finding from Goal
health Finding from validator finding
source health from source authority
deck health from subsystem health
confidence from authority
manifest coverage from universal completeness
passing validation from Build acceptance and Goal success
```

Missing, stale, and conflicting evidence remains visible. The health foundation
must not manufacture consensus, fill gaps, infer causality, infer consent,
rewrite history, or present a candidate as universally correct.

## Local-First, Privacy, Cost, And Dependency Boundary

Future Phase44I remains:

```text
local-only
in-memory
deterministic
zero-cost
standard-library only
caller-input only
free of filesystem and database reads or writes
free of repository and worktree inspection
free of provider and network access
free of process, environment, and wall-clock access
free of model calls
free of telemetry and analytics emission
```

Only bounded references and summaries enter health records. Private deck text,
raw user context, raw provider payloads, secrets, credentials, prompts, model
transcripts, and session data fail closed at mapping boundaries.

## Theory, Rules, Corrections, And Hareruya Boundary

Theory and theory-skill review gates remain external and mandatory. Health may
reference already reviewed Theory or flag missing review; it cannot ingest,
review, promote, translate, rewrite, or treat unreviewed Theory as factual,
measured, rules, policy, authority, or regression truth.

Rules authority, legality, and Corrections remain external. Health cannot
mutate Rules, activate Corrections, resolve correction conflicts, or allow a
health status to override a legality or evidence ceiling.

Hareruya remains tournament-only provenance. A Hareruya reference may support
a tournament observation, event, deck instance, or bounded tournament-source
health signal. It cannot become general Codie/Jin/Theory truth, user context,
policy, authority, approval, Theory, Rules, Correction, or a write target.

Official Scryfall data remains card truth within its accepted version and
provenance boundary. Public Moxfield and pasted user deck inputs remain user-
initiated inputs and are not tournament evidence. Health performs no fetch.

## Stream Deck Boundary

Stream Deck is absent from Phase44I and remains supplemental-only in any later
separately accepted packet. Health may not add a Stream Deck adapter, command,
event handler, approval, confirmation, notification, monitoring, or mutation
surface.

A future read-only display may show an already-produced assessment only after
a separate contract. It cannot select evidence, acknowledge a Finding, create
a Goal, resolve a conflict, change authority, or replace the primary interface.

## Roadmap And Authority Boundary

Phase44I implements only Subsystem Health Foundation v1. It does not implement:

```text
Phase44J checkpoint work
Phase44K-M durable Findings + Idea Ledger runtime
Phase44N-P Change / Impact Engine
Phase44Q-S Experiment Engine
Phase44T-V Read-Only Decision Core
Phase44W-Y Goal Regression Corpus
Phase45 Independent Goal Validator or Shadow Mode
Phase46 Stage 1 work-order authority
Phase47 safe experiment authority
Phase48 Build Graph or CCPM-inspired execution
Phase49 mature operating-model automation
Stage 4 investigation or authority
```

Health cannot rank, select, activate, schedule, mutate, execute, retry, close,
promote, or reprioritize work. It cannot create a Goal or Goal Contract,
enforce one-active-mutating-Goal, grant capability, calculate authority,
resolve State Engine conflicts, trigger safe mode, or bypass human roadmap,
merge, release, or promotion authority.

The existing human-authored roadmap remains the canonical work order until
Stage 1 passes all gates and receives explicit human promotion.
Build Graph and CCPM-inspired execution remain conditional Phase48 work only.

## Future Phase44I Forbidden Work

Phase44I must not:

```text
add any global, overall, combined, universal, weighted, or percentage health score
combine CODIE, JIN, and THEORY_CORPUS into one assessment
produce or persist a Goal, Goal candidate, Goal Contract, Idea, work item, or recommendation
persist a Finding or implement the future Findings/Idea Ledger
read the repository, filesystem, database, provider, network, process, environment, or wall clock
run tests, validators, ingestion, retrieval, analytics, simulation, or model calls
fetch Scryfall, Moxfield, Hareruya, Theory, Rules, or community sources
change State Engine v1 or Foundation v1 behavior
change evidence classes, source authority, provenance, privacy, or confidence ceilings
use user preference to override fact
bypass Theory or theory-skill review
mutate Rules or activate Corrections
use Hareruya outside tournament provenance
add UI, CLI, API, service, worker, queue, scheduler, notification, or Stream Deck behavior
add schema, migration, repository, dependency, fixture, workflow, validator, or repair behavior
implement Build Graph, CCPM, agents, issue dispatch, or autonomous execution
bypass human roadmap, merge, release, approval, or promotion gates
```

## Authorized Phase44H Files

This contract packet may change only:

```text
docs/PHASE44H_GOAL_ENGINE_SUBSYSTEM_HEALTH_FOUNDATION_CONTRACT.md
docs/CHECKPOINT_PHASE44H_GOAL_ENGINE_SUBSYSTEM_HEALTH_FOUNDATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE44H_GOAL_ENGINE_SUBSYSTEM_HEALTH_FOUNDATION_CONTRACT_PROMPT.md
docs/GOAL_ENGINE_IMPLEMENTATION_PROGRAM_V1.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

The separate scope-transition commit is not part of this eight-document
packet. Phase44H must not alter `docs/CODIE_ACTIVE_VALIDATION_SCOPE.json`.

## Required Future Phase44I Tests

Future focused tests must prove:

```text
exact schema and enum validation
strict exact-field parsing and forbidden-field rejection
domain/category and assessment-class rules
three domains remain separate
cross-domain definitions, observations, Findings, and references fail closed
required/optional manifest sets are exact and disjoint
Theory Corpus coverage never exceeds its declared manifest
PASS/DEGRADED/FAIL evidence requirements
UNKNOWN limitation and CONFLICTED reference requirements
NOT_APPLICABLE cannot hide a required signal
duplicate and dangling IDs fail closed
stale evidence remains visible
missing required observations fail closed
explicit UNKNOWN required observations create gap Findings
non-pass observations create evidence-bounded Findings
PASS and NOT_APPLICABLE alone do not create problem Findings
Findings never contain Goals, priorities, interventions, or authority
user feedback controls only subjective Jin usefulness/preferences
subjective evidence cannot weaken factual evidence
no score, overall verdict, weighting, ranking, or cross-domain aggregation exists
revision chains require the exact prior semantic hash
canonical serialization and hashing are byte-stable
no I/O, network, database, provider, model, wall-clock, or persistence behavior
no forbidden imports, raw payload fields, private deck text, or secret fields
Foundation v1 and State Engine v1 regression suites remain unchanged and pass
```

## Required Phase44H Validation

```text
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -p "test_*.py"
authorized eight-document boundary scan
protected active-scope scan against the separate scope-transition commit
Markdown fence and trailing-whitespace scans
runtime/schema/provider/dependency/workflow/constitution diff scan
hard-evidence, domain-separation, local-first, Theory-review, Hareruya,
supplemental-only Stream Deck, and roadmap-authority scans
```

## Gate

Phase44I remains blocked until this exact Phase44H contract SHA receives
artifact-backed `PASS` or `PASS WITH REVIEW NOTES` and Phase44H is merged by
human authority. Phase44I must implement only this accepted contract. Phase44J
and every later packet remain sequentially blocked.
