# Phase 44K Goal Engine Findings + Idea Ledger Runtime Contract

Status: implementation contract only

## Validation Tuple

```text
phase_id: Phase44K
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase44L
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase44K defines the only implementation boundary permitted for Phase44L: a
pure, immutable, deterministic, caller-input Findings + Idea Ledger v1.

The governing distinction is permanent:

```text
Idea != Finding != Goal
```

The future ledger may preserve evidence-backed Findings, faithfully captured
Ideas, recurrence, explicit relations, conditional reconsideration triggers,
and append-only history. It may not silently merge Ideas, infer a collision,
promote an Idea or Finding into a Goal, select work, or grant authority.

This packet is documentation-only. It changes no production code, tests,
schema, repositories, dependencies, workflows, active scope, providers, UI,
CLI, Stream Deck integration, model behavior, or runtime authority.

## Governing Authority

The authority order remains:

```text
docs/CODIE_V2_CONSTITUTION.md
-> accepted constitutional ADRs and contracts
-> docs/GOAL_ENGINE_V1_SPEC.md
-> docs/GOAL_ENGINE_IMPLEMENTATION_PROGRAM_V1.md
-> this bounded Phase44K contract
```

Goal Engine v1 remains subordinate to the Codie V2 Constitution. Chat,
generated text, local notes, health status, a Finding, an Idea, recurrence,
relation confidence, and unreviewed Theory cannot supersede this authority
order.

## Accepted Baseline

Phase44K begins only because its required predecessor gates are satisfied:

```text
Phase44A Goal Engine ratification: accepted
Phase44B-C Foundation v1 contract and implementation: accepted
Phase44D Foundation v1 checkpoint/freeze: accepted
Phase44E-F State Engine v1 contract and implementation: accepted
Phase44G State Engine v1 checkpoint/freeze: accepted
Phase44H-I Subsystem Health Foundation v1 contract and implementation: accepted
Phase44J Subsystem Health Foundation v1 checkpoint/freeze: accepted through PR #92
Phase50A-C Local Working Iteration v0.1: accepted and frozen
```

Phase44J acceptance evidence:

```text
pull request: 92
validated SHA: 6511459632ccdcb7711e3b6d13d58dd8cb8449e5
workflow run ID: 33255846278
validation job ID: 99109283311
artifact: codie-pr-validation-6511459632ccdcb7711e3b6d13d58dd8cb8449e5
artifact ID: 9715775896
artifact digest: sha256:1ca2245c4b505f1ede7b249ba76b126d8c0e66bb7f2f245081b7ef87fb45d590
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: CLEAN_PASS
aggregate: CLEAN_PASS
findings: 0
errors: 0
skipped validators: 0
merge commit: fd255eb72b8a4c6ac56d633da499427f482fef21
post-merge main workflow run ID: 33257430750
post-merge main validation: PASS
```

The protected Phase44K active tuple was established separately in branch
ancestry by local scope-transition commit
`b2ac50bb76423c8c48bc914e2e66e00814255e83`. That one-file transition is not
part of this eight-document contract packet and must reach `main` before the
contract PR is published.

## Existing Architecture Reconciliation

Repository inspection establishes:

```text
codie/goal_engine/foundation.py owns IdeaIdentifier, FindingIdentifier, and GoalIdentifier
codie/goal_engine/foundation.py owns GoalEvidenceReference and immutable lineage helpers
codie/goal_engine/state_engine.py owns observational project-state reconciliation
codie/goal_engine/health.py produces immutable in-memory HealthFinding records
codie/goal_engine/idea_ledger.py does not exist
tests/test_goal_engine_idea_ledger.py does not exist
HealthFinding is not a durable ledger entry
validator findings are not Goal Engine Findings
Correction Ledger records are not Findings or Ideas
incidents, recommendations, Theory claims, and user feedback are not ledger entries by default
```

Findings + Idea Ledger v1 must remain an isolated Goal Engine layer. It may
reference accepted immutable records but cannot repurpose the Correction
Ledger, State Engine, provider health, deck health, validator output,
recommendation storage, chat history, or roadmap as its persistence or
authority surface.

## Future Phase44L Files

Phase44L may change only:

```text
codie/goal_engine/idea_ledger.py
codie/goal_engine/__init__.py
tests/test_goal_engine_idea_ledger.py
docs/PHASE44L_GOAL_ENGINE_FINDINGS_IDEA_LEDGER_IMPLEMENTATION_REPORT.md
```

No schema, migration, fixture, repository, provider, dependency, workflow,
validator, CLI, UI, API, service, worker, queue, scheduler, Stream Deck,
configuration, or constitutional file is authorized.

## Required Schema Versions

Future Phase44L must use exact v1 schema identifiers:

```text
codie.goal_engine.ledger_finding.v1
codie.goal_engine.idea_record.v1
codie.goal_engine.idea_occurrence.v1
codie.goal_engine.ledger_entity_reference.v1
codie.goal_engine.ledger_relation.v1
codie.goal_engine.reconsideration_trigger.v1
codie.goal_engine.reconsideration_request.v1
codie.goal_engine.ledger_history_event.v1
codie.goal_engine.ledger_snapshot_reference.v1
codie.goal_engine.findings_idea_ledger_snapshot.v1
```

Existing `FindingIdentifier`, `IdeaIdentifier`, `GoalIdentifier`,
`GoalEvidenceReference`, policy records, and canonical Foundation v1 helpers
must be reused. Phase44L must not fork those records or create a new evidence,
authority, Goal, or identifier class.

## Core Invariants

```text
Idea != Finding != Goal
an Idea preserves the submitter's original wording
a Finding requires visible support, limitations, and disconfirmation criteria
a Goal requires later Goal evaluation and authority outside this ledger
GOAL_CANDIDATE remains an Idea state, not a Goal
recurrence is evidence of recurrence only, not importance or authority
relations remain explicit records and never silently merge entities
duplicate means linked duplicate records, not deletion or replacement
new means no caller-supplied collision was recorded, not universal novelty
reconsideration produces a review request, not automatic reactivation
history is append-only and semantic revisions retain exact prior hashes
confidence never grants authority
recency never creates precedence
the ledger does not select, rank, schedule, activate, or execute work
```

## Canonical Vocabulary

### Idea states

The exact ratified Idea states are:

```text
UNTRIAGED
NOTE
CONDITIONAL
WATCHING
NEEDS_RESEARCH
INVESTIGATION_CANDIDATE
GOAL_CANDIDATE
POLICY_IDEA
ARCHIVED_CONDITIONAL
```

These states classify one Idea for review. They are not Goal lifecycle states,
work priority, readiness, approval, or authority. `GOAL_CANDIDATE` means only
that a later Goal evaluation may consider the Idea. `POLICY_IDEA` does not
change policy. `ARCHIVED_CONDITIONAL` requires at least one explicit
reconsideration trigger.

### Finding origins

The exact v1 Finding origins are:

```text
HEALTH_FINDING
RESEARCH_FINDING
OPERATIONAL_FINDING
HUMAN_REVIEW_FINDING
```

Origin describes provenance only. It does not grant fact, Rules, policy,
priority, or authority status. A validator finding, Correction, Incident,
Recommendation, Theory claim, user preference, Idea, or Goal cannot be relabeled
as a ledger Finding merely by changing this field.

### Relation types

The exact ratified relation types are:

```text
duplicate
extension
alternative
contradiction
dependency
related
```

`new` is the no-collision result on an Idea collision assessment; it is not a
binary edge. Every relation names two distinct typed entities and visible
basis references. Relations do not merge, supersede, resolve, rank, approve,
or promote either entity.

### Ledger entity kinds

```text
IDEA
FINDING
GOAL
FAILED_WORK
REWIND
CONDITIONAL_OPPORTUNITY
```

Only `IDEA` and `FINDING` are stored as ledger records in v1. Other entity
kinds are immutable caller-supplied references for collision and lineage
context. A relation to a Goal does not make an Idea a Goal.

### Trigger kinds

```text
EVIDENCE_CHANGE
DEPENDENCY_CHANGE
RECURRENCE_THRESHOLD
CONTEXT_CHANGE
POLICY_CHANGE
TIME_WINDOW
HUMAN_REQUEST
```

Trigger definitions are bounded declarative conditions. They execute no code,
read no clock, poll no source, and create no state transition. A caller must
supply the triggering observation and supporting evidence.

### History event kinds

```text
FINDING_ADMITTED
IDEA_CAPTURED
IDEA_REVISED
IDEA_CLASSIFIED
OCCURRENCE_RECORDED
RELATION_RECORDED
TRIGGER_DEFINED
RECONSIDERATION_REQUESTED
GOAL_LINK_RECORDED
ARCHIVED_CONDITIONAL
```

An event records what a caller supplied or an accepted pure operation returned.
It is not permission, execution, approval, or proof that a Goal outcome
occurred.

## Required Immutable Records

All records are frozen dataclasses with exact-field parsing, canonical
serialization, and fail-closed validation. Repeated fields are immutable
tuples. IDs, timestamps, references, decisions, policy references, and
authority references are caller supplied.

### LedgerFinding

Required fields:

```text
finding_id: FindingIdentifier
origin: str
statement: str
why_it_matters: str
source_record_ref_id: str
source_record_semantic_hash: str
evidence_ref_ids: tuple[str, ...]
conflict_ref_ids: tuple[str, ...]
confidence: float
disconfirmation_criteria: tuple[str, ...]
limitations: tuple[str, ...]
observed_at: str
recorded_at: str
sensitivity: str
owner_ref_id: str | None
schema_version: str
```

A ledger Finding preserves an accepted source record by reference and exact
semantic hash. It does not rewrite the source. Evidence cannot exceed the
source record's evidence boundary. `recorded_at` is ledger receipt time supplied
by the caller and does not replace `observed_at` or make stale evidence current.

Every Finding requires at least one evidence or conflict reference, at least
one disconfirmation criterion, and at least one limitation. Confidence is
bounded support only. `HUMAN_REVIEW_FINDING` must remain visibly human-supplied
and cannot make an objective claim without separate objective evidence.

### IdeaRecord

Required fields:

```text
idea_id: IdeaIdentifier
revision: int
original_wording: str
current_summary: str
state: str
origin_ref_ids: tuple[str, ...]
finding_ref_ids: tuple[str, ...]
relation_ids: tuple[str, ...]
occurrence_ids: tuple[str, ...]
trigger_ids: tuple[str, ...]
human_decision_ref_ids: tuple[str, ...]
policy_ref_ids: tuple[str, ...]
created_at: str
updated_at: str
sensitivity: str
owner_ref_id: str | None
supersedes_idea_hash: str | None
schema_version: str
```

`original_wording` is immutable across every revision and preserves the
bounded text submitted by the caller. `current_summary` may change only in a
new revision that retains the exact prior semantic hash. A summary never
replaces original wording or becomes a factual Finding.

State changes require a new revision and a corresponding history event.
Classification may reference human decisions or accepted policies, but the
record cannot infer either. `GOAL_CANDIDATE` requires no `GoalIdentifier` and
creates none. `ARCHIVED_CONDITIONAL` requires a trigger reference. A trigger
observation never edits an archived Idea in place.

### IdeaOccurrence

Required fields:

```text
occurrence_id: str
idea_id: IdeaIdentifier
occurred_at: str
context_summary: str
source_ref_ids: tuple[str, ...]
evidence_ref_ids: tuple[str, ...]
sensitivity: str
owner_ref_id: str | None
schema_version: str
```

An occurrence records that the same stable Idea was observed again in a
bounded context. It does not alter state, confidence, priority, necessity, or
authority. Duplicate occurrence IDs, missing source references, cross-owner
private references, and time before Idea creation fail closed.

### LedgerEntityReference

Required fields:

```text
entity_kind: str
entity_id: str
revision: int | None
semantic_hash: str
schema_version: str
```

References retain the exact identity and semantic hash of caller-supplied
ledger or external entities. They do not import raw records or claim current
applicability.

### LedgerRelation

Required fields:

```text
relation_id: str
source: LedgerEntityReference
target: LedgerEntityReference
relation_type: str
basis_ref_ids: tuple[str, ...]
confidence: float
limitations: tuple[str, ...]
created_at: str
created_by_ref_id: str
schema_version: str
```

Every relation is caller-supplied, directional, and visible. Source and target
must differ. `duplicate` retains both records. `dependency` does not schedule
or block work. `contradiction` does not decide which entity is correct.
Relations require explicit basis and limitations and cannot be inferred from
text similarity, recurrence, recency, confidence, or source name.

### ReconsiderationTrigger

Required fields:

```text
trigger_id: str
idea_id: IdeaIdentifier
trigger_kind: str
condition_summary: str
required_evidence_classes: tuple[str, ...]
recurrence_threshold: int | None
not_before: str | None
expires_at: str | None
created_at: str
created_by_ref_id: str
schema_version: str
```

Only `RECURRENCE_THRESHOLD` may use `recurrence_threshold`, which must be a
positive integer. Only `TIME_WINDOW` requires `not_before`. Caller-supplied
timestamps are UTC. Trigger conditions are non-executable review descriptions.

### ReconsiderationRequest

Required fields:

```text
request_id: str
idea_id: IdeaIdentifier
idea_revision: int
trigger_id: str
as_of: str
evidence_ref_ids: tuple[str, ...]
occurrence_ids: tuple[str, ...]
human_request_ref_ids: tuple[str, ...]
limitations: tuple[str, ...]
schema_version: str
```

A request means only that a fresh evaluation and Necessity Test may be needed.
It does not change Idea state, reactivate a prior Goal, create a new Goal,
restore work, grant authority, or assert that the trigger is universally true.

### LedgerHistoryEvent

Required fields:

```text
event_id: str
event_kind: str
entity: LedgerEntityReference
related_ref_ids: tuple[str, ...]
evidence_ref_ids: tuple[str, ...]
human_decision_ref_ids: tuple[str, ...]
policy_ref_ids: tuple[str, ...]
statement: str
created_at: str
prior_event_hash: str | None
schema_version: str
```

Fact, human-decision, and policy references remain disjoint. The first event
for one entity forbids `prior_event_hash`; each later event requires the exact
immediately prior event hash. Event time cannot precede the referenced entity
or its prior event. Event chains are append-only and contain no deletion or
history-rewrite operation.

### LedgerSnapshotReference

Required fields:

```text
snapshot_id: str
revision: int
semantic_hash: str
schema_version: str
```

### FindingsIdeaLedgerSnapshot

Required fields:

```text
snapshot_id: str
revision: int
ledger_scope_id: str
as_of: str
findings: tuple[LedgerFinding, ...]
ideas: tuple[IdeaRecord, ...]
occurrences: tuple[IdeaOccurrence, ...]
relations: tuple[LedgerRelation, ...]
triggers: tuple[ReconsiderationTrigger, ...]
reconsideration_requests: tuple[ReconsiderationRequest, ...]
history_events: tuple[LedgerHistoryEvent, ...]
evidence_snapshot: tuple[GoalEvidenceReference, ...]
external_entity_references: tuple[LedgerEntityReference, ...]
supersedes_snapshot: LedgerSnapshotReference | None
schema_version: str
```

The snapshot is an immutable, caller-persistable value object. It performs no
storage. Revision one forbids a predecessor; later revisions require the same
snapshot identity, the next exact revision, and the immediately prior semantic
hash. Every identifier and reference must resolve exactly once within the
appropriate caller-supplied snapshot.

## Sensitivity And Ownership

The exact v1 sensitivity values are:

```text
PUBLIC_REFERENCE
PROJECT_INTERNAL
USER_PRIVATE
DECK_PRIVATE
SECRET_REFERENCE
```

`USER_PRIVATE` and `DECK_PRIVATE` require an `owner_ref_id`. Cross-owner
relations, occurrences, or exports require an explicit caller-supplied share or
human-decision reference; Phase44L performs no sharing or export.

`SECRET_REFERENCE` may record only that protected material exists through a
bounded reference. Original wording, summaries, statements, contexts,
limitations, metadata, and mappings must not contain credentials, tokens,
cookies, session data, private keys, or other raw secrets.

## Allowed Pure Interfaces

Future Phase44L may expose only:

```text
validate_idea_state(...)
validate_finding_origin(...)
validate_relation_type(...)
validate_ledger_entity_kind(...)
validate_trigger_kind(...)
validate_history_event_kind(...)
validate_ledger_finding(...)
validate_idea_record(...)
validate_idea_revision(...)
validate_ledger_snapshot(...)
validate_ledger_snapshot_revision(...)
build_findings_idea_ledger_snapshot(...)
record_idea(...)
record_finding(...)
record_occurrence(...)
record_relation(...)
define_reconsideration_trigger(...)
build_reconsideration_request(...)
append_ledger_history_event(...)
*_to_dict(...) / *_from_dict(...)
*_semantic_hash(...)
```

Every builder returns a new immutable value and uses only caller inputs.
Interfaces may validate or deterministically package explicit records. They may
not search, infer similarity, decide collisions, read prior storage, monitor a
trigger, or perform a Necessity Test.

## Finding Admission Contract

`record_finding(...)` must:

1. validate one accepted source reference and exact semantic hash;
2. preserve the source statement, evidence ceiling, conflicts, limitations,
   and disconfirmation boundary;
3. reject a Finding that lacks visible support or invents evidence;
4. keep historical observation time separate from ledger receipt time;
5. reject a validator finding, Correction, Incident, Recommendation, Idea,
   Goal, Theory claim, or user preference relabeled as a ledger Finding;
6. retain source provenance and sensitivity;
7. append a `FINDING_ADMITTED` history event; and
8. return a new snapshot without ranking, scheduling, persistence, or Goal
   production.

A Phase44I `HealthFinding` may be admitted only through its exact source
reference and semantic hash. Admission does not alter the health assessment or
claim that the Finding remains current.

## Faithful Idea Capture Contract

`record_idea(...)` must:

1. accept a caller-supplied stable `IdeaIdentifier` and bounded original text;
2. preserve original wording byte-for-byte after Unicode normalization rules
   are applied at initial capture;
3. begin at revision one and state `UNTRIAGED` unless an explicit human or
   accepted-policy classification reference is supplied;
4. preserve origin, sensitivity, ownership, and caller timestamp;
5. reject duplicate Idea IDs and hidden raw-content mappings;
6. append an `IDEA_CAPTURED` history event; and
7. return a new snapshot without evaluating necessity, novelty, impact,
   actionability, priority, or Goal candidacy.

Later revisions retain the same `IdeaIdentifier`, original wording, creation
time, sensitivity ceiling, and exact prior hash. Editorial summary change,
state classification, Finding linkage, relation linkage, and trigger linkage
remain distinct visible revision reasons.

## Collision And Relation Contract

Collision review compares an Idea only against caller-supplied immutable
references to existing Ideas, Findings, Goals, failed work, rewinds, and
conditional opportunities. Phase44L performs no text search, embedding,
similarity score, model call, repository scan, or automatic classification.

The caller supplies either:

```text
new: no supported collision relation in the supplied comparison set
one or more explicit LedgerRelation records with basis and limitations
```

`new` is local to the supplied comparison set and cannot claim universal
novelty. Relations are never silently added. `duplicate` retains both records,
both original wordings, both histories, and the explicit relation. No relation
deletes, overwrites, aliases, merges, or redirects identity.

## Recurrence Contract

Each recurrence is a separate `IdeaOccurrence`. Recurrence counts only exact
validated occurrences attached to one Idea. It cannot:

```text
raise confidence automatically
change Idea state
create a relation
prove necessity
prove impact
create or reactivate a Goal
change work priority
grant authority
override disconfirming evidence
```

A `RECURRENCE_THRESHOLD` trigger may be satisfied only from caller-supplied
occurrence records and caller-supplied `as_of`. Meeting the threshold creates a
`ReconsiderationRequest` only.

## Conditional Reconsideration Contract

`ARCHIVED_CONDITIONAL` requires a specific trigger. When a caller supplies
evidence that a trigger condition may be met, Phase44L may build a deterministic
reconsideration request. It must preserve the archived Idea revision, trigger,
evidence, occurrences, limitations, and request time.

The request routes to a future fresh evaluation and Necessity Test. It does not
automatically change the Idea to `UNTRIAGED`, `GOAL_CANDIDATE`, or any other
state. It does not reactivate a prior Goal or reuse an old Goal Contract.

## History And Lineage Contract

The ratified conceptual lineage remains:

```text
IDEA
-> RESEARCH
-> FINDING
-> GOAL
-> EXPERIMENT
-> IMPLEMENTATION
-> OBSERVATION
-> OUTCOME
```

Phase44L implements only the Idea and Finding ledger portion plus references to
existing external entities. A history link records lineage; it does not claim
that a later stage is approved or complete. Every semantic change is a new
record revision plus a hash-linked history event. Superseded revisions and
contradicted records remain historical evidence and are never deleted or
rewritten.

## Snapshot Construction Algorithm

`build_findings_idea_ledger_snapshot(...)` must be pure and deterministic:

1. Validate caller-supplied UTC `as_of` without reading the wall clock.
2. Validate all records, exact schemas, vocabularies, sensitivity, and owners.
3. Reject duplicate IDs, dangling references, cross-owner private leakage,
   broken revision chains, malformed hashes, mutable fields, and unknown keys.
4. Resolve evidence, Finding, Idea, occurrence, relation, trigger, request,
   history, policy, human-decision, and external-entity references exactly.
5. Preserve Finding evidence and source-record ceilings.
6. Preserve Idea original wording and every semantic revision.
7. Preserve every explicit occurrence and relation without inference.
8. Require every archived-conditional Idea to reference a valid trigger.
9. Require every reconsideration request to reference a valid archived Idea
   revision and trigger without changing either.
10. Validate append-only event chains and exact prior hashes.
11. Sort semantically unordered collections canonically.
12. Return a byte-stable snapshot with no score, ranking, recommendation,
    work order, Goal, persistence, or authority output.

## Canonical Serialization And Hashing

Future Phase44L must preserve Foundation v1 conventions:

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

Original wording remains part of Idea semantic hashes. Full ledger hashes
include provenance, evidence, ownership, sensitivity, relations, occurrences,
triggers, requests, and history. No comparison hash may hide those differences.

## Hard Evidence Boundary

Findings + Idea Ledger v1 must keep separate:

```text
fact from human decision, policy, and authority
objective evidence from subjective preference
historical validity from current applicability
source observation time from ledger receipt time
supporting evidence from conflicting evidence
Finding from validator finding, Correction, Incident, and Recommendation
Finding from Idea
Idea from Goal and Goal Contract
GOAL_CANDIDATE from Goal
recurrence from necessity, impact, priority, and authority
relation confidence from truth or permission
duplicate relation from identity merge
reconsideration request from reactivation
lineage reference from lifecycle completion
passing validation from Build acceptance and Goal success
```

Missing, stale, conflicting, and disconfirming evidence remains visible. The
ledger must not manufacture consensus, fill gaps, infer causality, infer
consent, rewrite history, or present a candidate as universally correct.

## Local-First, Privacy, Cost, And Persistence Boundary

Future Phase44L remains:

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

The v1 snapshot is caller-persistable but Phase44L performs no persistence.
SQLite, files, migrations, repository ownership, indexes, transactions,
retention, deletion, redaction storage mechanics, multi-user authentication,
sync, backup, export, and cloud transmission require later separately accepted
contracts.

## Theory, Rules, Corrections, Sources, And User Input

Theory and theory-skill review gates remain external and mandatory. A Theory
gap or reviewed claim may be referenced, but Phase44L cannot ingest, review,
promote, translate, or treat unreviewed Theory as fact, Rules, tournament
evidence, policy, authority, or regression truth.

Rules authority, legality, and Corrections remain external. A `POLICY_IDEA`
cannot mutate policy. A Finding or Idea cannot change Rules, activate a
Correction, resolve a Correction conflict, or override an evidence ceiling.

Official Scryfall remains card truth within its accepted version and
provenance boundary. Public Moxfield and pasted deck inputs remain explicit
user-initiated non-tournament inputs. Hareruya remains tournament-only
provenance. The ledger performs no fetch and cannot use source recurrence as
authority.

User wording is controlling for faithfully recording that user's Idea and
communication preference. It is not controlling for card truth, Rules,
tournament results, population evidence, another user, or project authority.

## Stream Deck Boundary

Stream Deck is absent from Phase44L and remains supplemental-only in any later
separately accepted packet. The ledger may not add a Stream Deck adapter,
capture command, classification command, trigger acknowledgement, approval,
notification, monitoring, or mutation surface.

A future supplemental read-only display may show an already-produced bounded
ledger summary only after a separate contract. It cannot capture original
wording, merge Ideas, classify state, acknowledge a trigger, create a Goal, or
replace the primary interface.

## Roadmap And Authority Boundary

Phase44L implements only the pure in-memory Findings + Idea Ledger v1. It does
not implement:

```text
Phase44M checkpoint work
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

The ledger cannot evaluate Necessity, choose an intervention, rank or select
work, create or revise a Goal Contract, enforce one-active-mutating-Goal, grant
capability, calculate authority, resolve State Engine conflicts, trigger safe
mode, or bypass human roadmap, merge, release, approval, or promotion authority.

The existing human-authored roadmap remains the canonical work order until
Stage 1 passes all gates and receives explicit human promotion. Build Graph and
CCPM-inspired execution remain conditional Phase48 work only.

## Future Phase44L Forbidden Work

Phase44L must not:

```text
conflate or convert Idea, Finding, and Goal identities
turn GOAL_CANDIDATE into a Goal or Goal Contract
silently merge, delete, overwrite, alias, or redirect Ideas
infer relations, novelty, duplication, recurrence, or trigger satisfaction
rank, prioritize, schedule, activate, execute, retry, close, or promote work
persist a ledger or add schema, migrations, repositories, files, or database I/O
read the filesystem, repository, provider, network, environment, process, or clock
run models, embeddings, similarity search, retrieval, analytics, or telemetry
change Foundation v1, State Engine v1, or Health Foundation v1 behavior
change evidence classes, source authority, provenance, privacy, or confidence ceilings
use user preference or recurrence to override fact
bypass Theory or theory-skill review
mutate Rules, policies, or Corrections
use Hareruya outside tournament provenance
fetch Scryfall, Moxfield, Hareruya, Theory, Rules, or community sources
add UI, CLI, API, service, worker, queue, scheduler, notification, or Stream Deck behavior
add dependencies, fixtures, workflows, validators, repair, agents, or orchestration
implement impact, experiment, decision, regression, validator, shadow, or Build Graph work
bypass human roadmap, merge, release, approval, or promotion gates
```

## Authorized Phase44K Files

This contract packet may change only:

```text
docs/PHASE44K_GOAL_ENGINE_FINDINGS_IDEA_LEDGER_RUNTIME_CONTRACT.md
docs/CHECKPOINT_PHASE44K_GOAL_ENGINE_FINDINGS_IDEA_LEDGER_RUNTIME_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE44K_GOAL_ENGINE_FINDINGS_IDEA_LEDGER_RUNTIME_CONTRACT_PROMPT.md
docs/GOAL_ENGINE_IMPLEMENTATION_PROGRAM_V1.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

The separate scope-transition commit is not part of this eight-document packet.
Phase44K must not alter `docs/CODIE_ACTIVE_VALIDATION_SCOPE.json`.

The implementation-program edit is status-only. It does not change the
accepted Phase44-49 sequence, capability roadmap, evidence rules, authority
gates, Stage 4 disposition, or conditional Phase48 CCPM placement.

## Required Future Phase44L Tests

Future focused tests must prove:

```text
exact schema and vocabulary validation
strict exact-field parsing and forbidden-field rejection
IdeaIdentifier, FindingIdentifier, and GoalIdentifier remain distinct
Idea original wording is immutable across revisions
all Idea states remain classification only
GOAL_CANDIDATE creates no Goal or authority
Finding admission preserves source hash and evidence ceiling
validator findings, Corrections, Incidents, and Recommendations cannot be relabeled
duplicate IDs, dangling references, broken hashes, and mutable fields fail closed
relations remain explicit, directional, evidence-bounded, and non-merging
new is local to the supplied comparison set
recurrence records do not change state, priority, confidence, or authority
ARCHIVED_CONDITIONAL requires a trigger
trigger evidence creates only a reconsideration request
reconsideration does not reactivate a Goal or mutate Idea state
history chains require exact prior hashes and preserve every revision
fact, human-decision, policy, and authority references remain disjoint
private ownership and sensitivity boundaries fail closed
secret or raw-content mappings fail closed
canonical serialization and hashing are byte stable
no score, rank, priority, action, work order, Goal, or Goal Contract output exists
no I/O, persistence, network, provider, model, clock, or environment behavior
no later-phase imports, methods, or authority surfaces exist
Foundation, State Engine, and Health Foundation regressions remain unchanged and pass
```

## Required Phase44K Validation

```text
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -p "test_*.py"
authorized eight-document boundary scan
protected active-scope scan against the separate scope-transition commit
Markdown fence and trailing-whitespace scans
runtime/test/schema/provider/dependency/workflow/constitution diff scan
Idea/Finding/Goal separation, faithful wording, recurrence, relation,
reconsideration, append-only history, local-first, privacy, Theory-review,
Hareruya, supplemental-only Stream Deck, and roadmap-authority scans
```

## Gate

Phase44L remains blocked until this exact Phase44K contract SHA receives
artifact-backed `PASS` or `PASS WITH REVIEW NOTES` and Phase44K is merged by
human authority. Phase44L must implement only this accepted contract. Phase44M
and every later packet remain sequentially blocked.
