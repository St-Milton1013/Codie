# Phase 42E - Minimal User Correction Ledger Core Contract

Status: contract only; implementation not authorized

## Validation Tuple

```text
phase_id: Phase42E
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase42F
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 42F is reserved for the Theory Source Registry, Rights, Immutable Source
Version, and Citation Contract. It remains blocked until Phase 42E outside
validation returns PASS or PASS WITH REVIEW NOTES.

## Purpose

Phase 42E defines the minimal governed correction overlay required by Codie V2.

The ledger answers:

```text
what prior behavior or claim needs correction
what bounded correction is proposed
what evidence supports it
who or what has authority for it
where and when it applies
which subsystem may consume it
whether it is active, conflicting, stale, or blocked
which correction bundle affected an operation
```

The ledger is not another truth database. It references authority and evidence
without rewriting them.

## Authority

This contract is governed in descending order by:

1. `docs/CODIE_V2_CONSTITUTION.md`;
2. `docs/ROADMAP_PATCH_V2_INTELLIGENCE_PROGRAM_INTAKE.md`;
3. the accepted Phase 42A cross-specification boundary;
4. the accepted Phase 42B fixed regression-corpus contract;
5. the accepted Phase 42C Rules authority contract;
6. the accepted Phase 42D model-profile and privacy contract;
7. accepted canonical, measured-evidence, simulator, snapshot, and
   recommendation contracts;
8. `docs/design_inputs/v2_intelligence_program/CODIE_V2_USER_CORRECTION_LEDGER_PROPOSAL.md`
   as preserved design input only.

The proposal does not authorize its large schema or service design.

## Core Invariants

```text
official authority and canonical truth remain outside the ledger
measured evidence is never rewritten by a correction
persisted recommendations are never written by the ledger
corrections apply at the narrowest valid scope
semantic history is append-only
only active and valid corrections may affect behavior
equal-rank contradiction stays visible
newest does not automatically win
repetition does not promote authority
Jin and models may propose but not activate corrections
every application is reproducible from a versioned bundle
private corrections remain local by default
```

## Correction Overlay

The governed resolution relationship is:

```text
official authority and canonical truth
+ measured evidence
+ applicable correction overlay
+ current user or deck context
= bounded behavior for one operation
```

The correction overlay may:

```text
annotate or suppress a known reasoning failure
apply a user preference
apply a deck-snapshot or deck-lineage principle
filter a known-invalid trace or parser interpretation after accepted review
route a review item
warn about an unresolved defect
downgrade confidence because a known limitation remains
```

It may not:

```text
change official rules, Oracle text, rulings, or legality
change Scryfall or Commander Spellbook canonical records
change tournament observations
change measured frequencies, rates, or confidence
turn a user preference into a population fact
create or revise a persisted recommendation
turn a theory claim into authority
```

## Minimal Correction Record

Every correction packet must preserve:

```text
correction_id
stable_key
revision
category
title
original_claim
corrected_claim
supporting_reason
reusable_rule, when any
authority_level
lifecycle_state
scope_type
scope_selector
subject_type
subject_id, when any
affected_subsystems
application_modes
exceptions
supporting_evidence_refs
contradicting_evidence_refs
valid_from and valid_until
effective_from and effective_until
supersedes_correction_id, when any
revalidation_triggers
sensitivity
created_at
created_by
record_version
metadata
```

Metadata is schema-validated, JSON-compatible, and prohibited from carrying
raw private conversations, secrets, executable content, or hidden scope.

## Categories

The minimal closed category set is:

```text
factual_correction
rules_correction
source_policy_correction
reasoning_failure
missing_capability
simulator_model_correction
deck_specific_principle
ui_output_preference
acceptable_low_confidence_result
terminology_correction
data_parsing_correction
```

Finer distinctions use controlled tags and affected-subsystem fields. A later
implementation cannot add categories casually.

## Authority Levels

Official authority is an external barrier, not an editable correction level.

| Level | Meaning | Maximum effect |
|---|---|---|
| `A0` | candidate or model-generated proposal | review material only |
| `A1` | user preference or terminology | the same user and presentation scope |
| `A2` | user-approved contextual correction | bounded user, deck, or experiment scope |
| `A3` | project-verified operational correction | accepted shared subsystem behavior |
| `A4` | authority-backed operational correction | behavior supported by cited official authority |

Rules:

```text
A0 never changes behavior
A1 never changes canonical identity or another user
A2 never enters global evidence or shared truth
A3 requires reproducible fixtures or equivalent accepted evidence
A4 requires verified authority references
official authority can block every level
```

An `A2` correction may be more specific than an `A3` general reasoning rule
within one deck, but it cannot violate official authority or rewrite evidence.

## Lifecycle

The ratified lifecycle states are:

```text
proposed
verified
active
superseded
rejected
revalidation_required
```

State meaning:

| State | May affect behavior | Meaning |
|---|---:|---|
| `proposed` | no | captured candidate awaiting review |
| `verified` | no | evidence and scope verified but not activated |
| `active` | yes | eligible for deterministic resolution |
| `superseded` | no | replaced by an explicit correction relation |
| `rejected` | no | did not meet authority, evidence, or scope requirements |
| `revalidation_required` | no by default | a dependency changed or correctness is uncertain |

Allowed transitions:

```text
proposed -> verified
proposed -> rejected
verified -> active
verified -> rejected
active -> superseded
active -> revalidation_required
revalidation_required -> verified
revalidation_required -> active after accepted review
revalidation_required -> superseded
revalidation_required -> rejected
```

An `A1` private preference may move from `proposed` to `active` only through a
future explicitly authorized convenience rule. Phase 42E does not implement
that transition.

No record is deleted or overwritten to simulate a state transition.

## Scope Types

Each correction has exactly one primary scope:

```text
system_global
subsystem_global
provider
format_and_date
card_identity
interaction_signature
commander_signature
archetype
deck_lineage
deck_snapshot
user_profile
experiment
session
```

Each scope has required selectors.

Examples:

```text
deck_snapshot requires immutable snapshot ID and deck hash
deck_lineage requires lineage ID
user_profile requires user or tenant subject
provider requires provider ID and may include provider version
format_and_date requires format plus evaluation interval
card_identity requires canonical oracle or card identity
interaction_signature requires a versioned interaction identity
```

Missing, contradictory, wildcard, or ambiguous selectors fail closed.

## Narrowest-Scope Resolution

Corrections apply no more broadly than their support.

```text
one snapshot is not a deck lineage
one deck lineage is not a commander population
one user is not every user
one provider field defect is not every provider
one interaction is not every card with a shared tag
one simulator version is not every simulator version
one accepted low-confidence answer does not alter global confidence
```

Scope expansion is a semantic change requiring:

```text
a new correction or supersession relation
expanded supporting evidence
explicit review
regression coverage
new effective time
```

Repeated statements do not expand scope.

## Temporal Identity

Correction packets preserve:

```text
valid_from and valid_until
effective_from and effective_until
recorded_at
activated_at, when active
superseded_at, when superseded
```

Valid time describes when the correction is true in the domain. System time
describes when Codie knew and recorded it. Effective time controls when an
accepted operation may apply it.

Historical replay must name both domain time and knowledge time where they
differ.

## Revisions And Supersession

Non-semantic editorial fixes may create a new revision of one correction.

Changes to claim, rule, scope, authority, exception, application mode, or
effective interval require a new correction linked by an explicit relation:

```text
full_replacement
partial_replacement
scope_narrowing
scope_expansion
exception_added
refinement
revocation
duplicate_of
```

Supersession records preserve:

```text
source and target correction IDs
relation type
affected scopes
effective time
reason
historical receipt treatment
```

Supersession cycles are invalid.

The latest correction does not automatically win.

## Evidence Requirements

Evidence references remain pointers to independently governed packets.

Minimum support:

| Correction | Required support |
|---|---|
| rules, Oracle, or legality | verified Phase 42C authority references |
| shared simulator behavior | reproducible trace plus expected behavior and regression case |
| shared parser behavior | raw fixture plus current and expected parsed outputs |
| source policy | source-role analysis plus governance approval |
| reasoning failure | original answer or decision packet plus bounded corrected rule |
| deck principle | user statement plus immutable deck scope |
| UI or terminology preference | user statement within the same user scope |
| missing capability | explicit unsupported case |
| acceptable low-confidence result | original result plus user acceptance |

A user statement is sufficient for that user's preference. It is not
sufficient for changing official rules, shared parser behavior, or measured
evidence.

Supporting and contradicting evidence remain visible.

## Authority Barrier

Resolution begins by establishing official and canonical constraints.

If a candidate conflicts with current official authority or canonical truth:

```text
it does not activate
it becomes an authority-verification request, canonical-data incident,
unresolved dispute, or rejected correction
the user report and resolution history remain visible
```

The ledger cannot use a correction to work around an authority package being
stale, missing, or unresolved.

Authority-sensitive corrections require governance review before shared
activation.

## Exceptions

Exceptions are structured, versioned predicates:

```text
exception_id
parent_correction_id
predicate_type
predicate
effect
reason
exception_version
```

Allowed effects:

```text
bypass
modify
downgrade
require_review
```

An exception may narrow a correction. It cannot grant more authority or wider
scope than its parent.

Malformed or ambiguous safety-sensitive exceptions fail closed.

## Revalidation

Corrections name dependency keys and revalidation triggers.

Required trigger families:

```text
Oracle text or official ruling change
Comprehensive Rules or legality update
simulator engine or card-definition version change
parser or provider schema version change
ontology version change
Commander Spellbook snapshot change
immutable deck hash or material lineage change
commander signature change
Theory source attribution or rights change
constitution or source-policy change
contradictory new evidence
user withdrawal
effective-period expiration
privacy classification change
```

Safety-sensitive affected records move to `revalidation_required` and stop
enforcing behavior until accepted review.

A snapshot correction naturally stops matching a new snapshot. It is not
silently promoted to lineage scope.

## Conflict Resolution

The deterministic resolution order is:

```text
1. establish official and canonical authority barriers
2. match subject, subsystem, user, scope, and time
3. exclude non-active, expired, and incompatible records
4. exclude revalidation-required records
5. evaluate structured exceptions
6. apply explicit supersession
7. compare authority level
8. compare scope specificity
9. compare effective time and revision only where earlier rules do not decide
10. expose incompatible equal-rank records as a conflict
```

Equal-rank incompatible corrections are never averaged and never resolved by
creation date alone.

Shared enforcement pauses where an unresolved safety-sensitive conflict
exists. The conflict remains visible to downstream consumers.

## Resolution Packet

The minimal resolution result preserves:

```text
correction_bundle_id
bundle_hash
resolution_policy_version
generated_at
requested domain time
requested knowledge time
authority barrier refs
applied corrections and revisions
shadowed corrections and reasons
blocked corrections and reasons
revalidation-required corrections and triggers
conflicts and required actions
scope-match explanations
```

Bundle serialization and hashing are deterministic. Every affected operation
records the exact bundle ID, hash, and resolution-policy version.

## Application Modes

Allowed modes:

```text
enforce
block
filter
annotate
warn
prefer
route
suppress
downgrade_confidence
create_review_item
```

Mode authority is bounded:

```text
A1 and A2 cannot enforce shared subsystem behavior
acceptable_low_confidence_result cannot raise confidence
annotate does not rewrite its referenced evidence
route does not broaden rights or provider access
prefer does not alter canonical identity
filter and block require authority appropriate to the subsystem
```

## Application Receipts

Every operation that applies corrections preserves a receipt:

```text
receipt_id
operation_type
operation_id
correction_bundle_id
bundle_hash
resolution_policy_version
applied correction IDs and revisions
blocked and conflicting correction IDs
result_digest
applied_at
```

Receipts do not duplicate private correction content unnecessarily.

## Subsystem Boundaries

### Jin

Jin may later retrieve a resolution packet and may submit an `A0` candidate.
It may not activate, broaden, supersede, or globally promote a correction.

### Rules

Rules authority blocks unsupported corrections. The ledger never becomes a
second legality source.

### Simulator

Only accepted `A3` or `A4` corrections may affect shared simulator validation.
Deck-scoped corrections may change a test target or interpretation, not the
shared legal-action engine.

### Parsers

Shared parser corrections require provider-scoped fixtures. They may not guess
unresolved card identity.

### Decision Intelligence

Decision Intelligence may consume bounded correction context. The ledger does
not write persisted recommendations or increase measured confidence.

### Theory Corpus

Attribution and terminology corrections remain linked correction records.
They do not become theorist claim nodes.

### User Interface

User preferences remain isolated by user. Presentation preference does not
alter analytics, source eligibility, or another user's interface.

## Privacy

The ledger is private and local by default.

Sensitivity classes:

```text
public_reference
project_internal
user_private
deck_private
secret_reference
```

`secret_reference` may record that protected material exists. It may never
store the secret itself.

Correction packets are excluded from cloud transmission unless the accepted
Phase 42D profile, exact data classes, rights state, redaction policy, purpose,
and consent all allow the minimized packet.

Raw conversation history is not required correction content.

Exports default to non-private identifiers, state, bounded rule, scope
summary, and permitted references. Private evidence and original text require
explicit authorization and redaction.

Deletion of private content preserves a non-reconstructive audit tombstone,
not the deleted content.

## Multi-User Isolation

The minimal contract requires a tenant or user boundary for private records.

```text
one user's correction cannot resolve for another user by default
user-profile preferences never conflict across users
deck-private selectors require ownership or explicit share authorization
global promotion requires project review and a new scope
audit access follows the same tenant boundary
```

Phase 42E does not decide authentication or persistence implementation.

## Required Regression Cases

A future implementation contract must cover:

```text
Paradise Mantle invalid and valid trace distinction
Springleaf Drum and Valley Floodcaller invalid loop reasoning
target-turn runs remain separate experiments
WrongSi snapshot correction does not apply to another snapshot
Rograkh/Ishai lineage principle does not become commander-wide
sideboard-only copies do not alter mainboard frequency
equal-rank incompatible corrections return conflict
two users can hold opposite UI preferences without conflict
low-confidence acceptance closes review without raising confidence
user Oracle claim cannot override official authority
Jin-created candidate remains A0 and non-active
newer low-authority correction does not beat older authority-backed correction
revalidation-required safety record stops applying
supersession cycles fail
malformed exception cannot bypass a safety gate
historical replay returns the time-valid bundle
private correction content stays out of default export and cloud packet
no correction write reaches canonical, measured, or recommendation storage
```

## Resolved Decisions

Phase 42E resolves:

```text
the minimal closed category set
the A0-A4 ledger authority levels
official authority as an external hard barrier
the six ratified lifecycle states
the minimal primary-scope set
append-only semantic history
explicit supersession instead of latest-wins
deterministic narrowest-scope resolution
equal-rank conflicts as visible unresolved output
safety-sensitive revalidation records as non-enforcing
versioned deterministic correction bundles
application receipts
private-local default and user isolation
Jin candidate creation without activation
```

## Deferred Decisions

Later accepted contracts must define:

```text
SQLite schema and migrations
repository ownership and indexes
command authorization
activation-review roles
revalidation fan-out implementation
retention and redaction storage mechanics
consumer adapters
UI review and conflict workflows
export writers
cloud transmission implementation
multi-user authentication
```

The absence of those implementations does not weaken the boundaries above.

## Future Implementation Boundary

A later implementation contract may authorize pure in-memory packet models
and validators before persistence:

```text
CorrectionRecord
CorrectionScope
CorrectionEvidenceRef
CorrectionException
CorrectionRelation
CorrectionConflict
CorrectionResolutionRequest
CorrectionResolutionPacket
CorrectionApplicationReceipt
```

Schema, repositories, migrations, command services, consumers, and UI require
separately named accepted contracts.

## Phase 42F Boundary

Phase 42F may define only the Theory Source Registry, Rights, Immutable Source
Version, and Citation Contract.

It must keep theory contextual, attributed, rights-aware, and separate from
official authority, measured evidence, corrections, and recommendations.

Phase 42F must not implement source acquisition, transcription, embeddings,
graph storage, retrieval, models, UI, exports, or live network calls.

## Forbidden Phase 42E Work

Phase 42E must not add:

```text
production correction code
implementation tests or fixtures
schema, migrations, or repositories
write services or activation workflows
consumer integration
Jin or model calls
Rules implementation
Theory Corpus implementation
Decision Intelligence or recommendation output
simulator or parser mutation
provider or live network behavior
cloud transmission
UI or CLI behavior
file writing
dependency changes
workflow or validator changes
active-scope changes in the PR
constitution changes
```

## Acceptance Gate

Phase 42E passes only when outside validation confirms that it:

1. remains contract-only;
2. records Phase 42D artifact-backed acceptance;
3. preserves official and canonical authority ceilings;
4. prevents measured-evidence and recommendation mutation;
5. defines immutable, versioned correction records;
6. applies corrections at the narrowest valid scope;
7. uses only the six ratified lifecycle states;
8. prevents repetition, recency, or model authorship from promoting authority;
9. returns equal-rank conflicts visibly;
10. makes safety-sensitive revalidation records non-enforcing;
11. produces deterministic correction bundles and receipts;
12. preserves privacy and user isolation; and
13. keeps Phase 42F blocked.

Phase 42F may begin only after Phase 42E outside validation returns PASS or
PASS WITH REVIEW NOTES.
