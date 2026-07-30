# Phase 42D - Local-First Model Profile, Redaction, Consent, and Routing Contract

Status: contract only; implementation not authorized

## Validation Tuple

```text
phase_id: Phase42D
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase42E
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 42E is reserved for the Minimal User Correction Ledger Core Contract.
It remains blocked until Phase 42D outside validation returns PASS or PASS
WITH REVIEW NOTES.

## Purpose

Phase 42D defines the model-execution trust boundary for Codie V2. It governs:

```text
model profile identity and versioning
local-first and deterministic execution
data classification
cloud deny-by-default behavior
consent scope and invalidation
pre-egress redaction and minimization
model capability declarations
eligible-target routing
fallback behavior
provider admission requirements
model-run audit metadata
output distrust and downstream validation
```

This phase creates no model adapter, provider integration, consent engine,
redaction engine, router, audit repository, prompt, UI, schema, migration, or
runtime behavior.

## Authority

This contract is governed in descending order by:

1. `docs/CODIE_V2_CONSTITUTION.md`;
2. `docs/ROADMAP_PATCH_V2_INTELLIGENCE_PROGRAM_INTAKE.md`;
3. the accepted Phase 42A cross-specification boundary;
4. the accepted Phase 42B fixed regression-corpus contract;
5. the accepted Phase 42C Rules authority contract;
6. accepted earlier privacy, immutable-snapshot, evidence, and recommendation
   contracts;
7. `docs/design_inputs/v2_intelligence_program/CODIE_V2_MODEL_PROFILE_PROPOSAL.md`
   as preserved design input only.

The design proposal cannot override the ratified constitution or authorize
implementation.

## Governing Invariants

```text
Codie remains useful without cloud access.
No paid model is required for a core workflow.
Cloud execution is disabled by default.
Provider configuration is not consent.
Consent is specific, visible, revocable, and fail-closed.
Redaction and minimization complete before any external invocation.
Models receive only finalized transmission packets.
Local failure never silently broadens execution to cloud.
Models cannot mutate protected or canonical records.
Model output remains untrusted external content.
Every substantive model run is versioned and auditable.
Tests require neither live network access nor paid credentials.
```

## Trust Boundary

The future execution sequence is:

```text
governed request packet
-> task and risk classification
-> data-class inventory
-> accepted model-profile resolution
-> target eligibility evaluation
-> consent evaluation
-> rights filtering
-> purpose minimization
-> deterministic redaction
-> secret and path scanning
-> exact transmission preview
-> approved local or optional cloud adapter
-> untrusted response packet
-> schema validation
-> authority, legality, evidence, and contradiction gates
-> governed downstream answer packet
```

No stage may be skipped because a model or provider requests more context.

## Responsibility Separation

| Component | Owns | Must not |
|---|---|---|
| request classifier | task, risk, and data-class inventory | select a provider |
| profile resolver | accepted profile and version | invent consent |
| consent evaluator | permission for the exact transmission | redact content |
| rights filter | source-rights eligibility | broaden source use |
| redactor | deterministic transformation and minimization | call a model |
| router | selection among eligible targets | make an ineligible target eligible |
| adapter | one bounded invocation | read arbitrary local state |
| output validator | schema and safety checks | repair evidence or authority |
| audit owner | approved metadata and permitted content logs | store forbidden content |

An implementation may combine pure helpers in one module, but it must preserve
these logical boundaries and test them independently.

## Data Classification

Every object considered for a model request must carry one or more explicit
data classes.

| Code | Class | Local default | Cloud default |
|---|---|---:|---:|
| `D0` | public authority | allow | eligible |
| `D1` | public observational evidence | allow | eligible |
| `D2` | public measured or derived evidence | allow | eligible |
| `D3` | public rights-cleared theory context | allow | eligible after rights filtering |
| `D4` | restricted or licensed theory material | allow locally | deny |
| `D5` | private deck or snapshot data | allow locally | deny |
| `D6` | private user context and local-meta notes | allow locally | deny |
| `D7` | correction records and audit history | allow locally | deny |
| `D8` | private simulations and full traces | allow locally | deny |
| `D9` | operational metadata | allow locally | omit unless provider operation requires it |
| `D10` | secrets and credentials | deny to all models | absolute deny |
| `D11` | personal identifiers and identifying local paths | minimize locally | deny |
| `D12` | provider or model response content | untrusted | not an outbound source class |

The strictest applicable class controls. Multiple labels are preserved.

Redaction does not automatically declassify an object. A transformed object
receives a less restrictive class only through a deterministic, versioned,
reviewed transformation that produces a genuinely non-identifying derivative.

Examples:

```text
removing a private deck name does not make the cardlist public
pseudonymizing a pilot does not make private matchup notes public
role counts derived from a private deck remain private unless the accepted
derivation policy proves they are safe for the declared purpose
```

## Required Logical Profiles

Profiles are versioned policy packets, not provider marketing labels.

### `local_strict`

```text
default: yes
execution: local only
cloud allowed: no
private local classes: allowed by task scope
raw prompt logging: no
default logging: metadata only
fallback: local then deterministic
```

This profile must never discover or invoke a cloud target.

### `local_balanced`

```text
default: no
execution: local only
cloud allowed: no
routing: accepted local targets only
fallback: accepted local target then deterministic
```

Local escalation may not broaden task scope or data access.

### `offline_deterministic`

```text
model runtime required: no
network required: no
generative prose: unavailable when no accepted deterministic template exists
available: evidence retrieval, citations, legality status, structured reports,
correction application, and explicit unsupported or queued states
```

This profile is a required fallback, not a claim that deterministic templates
can replace all generative work.

### `cloud_public_only`

```text
default: disabled
allowed source classes: D0, D1, D2, rights-cleared D3
private classes: denied
provider admission: required
explicit profile selection: required
```

This profile cannot silently substitute a public deck for a private request.
It must exclude the private portion or block with a visible reason.

### `cloud_redacted_snapshot`

```text
default: disabled
private deck transmission: only a minimized derivative of one immutable snapshot
consent: one request or one named snapshot
exact preview: required
provider admission: required
```

Permitted detail levels must be explicit:

```text
none
commander_only
selected_cards
functional_summary
normalized_cardlist
snapshot_context
```

`full_private_context` is not admitted in the first implementation contract.
Any future admission requires a separate privacy review and accepted contract.

### `hybrid_local_primary`

```text
default: disabled
primary drafting: local
optional cloud role: objections or bounded review only
cloud input: separately minimized and consented
final authority: deterministic gates, never the cloud reviewer
```

The cloud reviewer does not receive the full local workspace by implication.

## Provider Admission

Phase 42D admits no cloud provider and no live endpoint.

A future provider-specific contract must declare:

```text
provider_id
allowed endpoint origins
model identity and mutable-alias behavior
data-use and training policy
retention policy and verification state
request and response logging behavior
region or processing-location disclosure when available
credential source
timeout and retry policy
cost limits
supported data classes
policy snapshot identity and effective time
```

Unknown or unverifiable retention is displayed as unknown. It is never
described as private, zero-retention, or safe.

Material provider-policy changes invalidate prior provider admission and
affected consent.

## Consent Contract

Consent is evaluated across every dimension:

```text
consent_id
provider_id
model or accepted model pattern
data classes
purpose
immutable deck snapshot or bounded project scope
duration
retention expectation
logging mode
redaction policy version
created_at
expires_at
revoked_at
```

An absent or ambiguous dimension makes consent invalid.

Allowed consent states:

```text
deny
ask_each_request
allow_once
allow_session
allow_snapshot
```

`allow_profile` and `allow_until_revoked` are not admitted for private data in
the first implementation contract. Public-only profile selection is not
private-data consent.

Consent must be requested again when:

```text
provider changes
model identity leaves the consented pattern
provider policy changes materially
new data classes are added
purpose changes
snapshot-scoped data uses another snapshot
redaction becomes less restrictive
detail level increases
logging becomes more permissive
consent expires or is revoked
```

Login, API-key configuration, provider enablement, prior use, or consent for a
different deck does not imply consent.

## Redaction And Minimization

The required order is:

```text
classify
-> exclude forbidden objects
-> minimize to the declared purpose
-> redact forbidden fields
-> pseudonymize locally
-> apply theory-rights filtering
-> scan secrets and identifiers
-> enforce size and structure limits
-> render exact preview
-> hash finalized transmission packet
-> invoke the accepted adapter
```

Mandatory external exclusions include:

```text
credentials and authorization headers
environment values and repository secrets
local absolute paths
private account handles and emails unless independently necessary and consented
unrelated deck snapshots and zones
unrelated user notes or correction history
full private simulation traces unless separately admitted
restricted or licensed theory text
hidden system or repair prompts
pseudonym mappings
```

The exact bytes or canonical structured representation represented by the
preview hash must be the payload sent to the adapter. The adapter may add only
declared transport framing and provider-required non-content metadata.

A redaction, rights, secret, consent, or preview-validation failure blocks
transmission. There is no best-effort send.

## Snapshot And Zone Isolation

Every packet containing `D5` records:

```text
deck_snapshot_id
deck_hash
disclosure_level
included zones
excluded zones
commander inclusion
source URL inclusion
deck-note inclusion
local-meta inclusion
consent_id
```

Zones remain distinct. A model preference cannot flatten commanders,
mainboard, sideboard, companion, or auxiliary objects.

Output remains bound to the transmitted snapshot. A later deck mutation
creates a stale-snapshot warning; it does not reinterpret old output.

## Capability And Risk Contract

Each target declares versioned, validated capabilities:

```text
structured-output support
context limit
tool access, normally none
language support
task families
rules reasoning validation state
strategic synthesis validation state
local or external execution
model identity, digest, quantization, and runtime where available
reproducibility level
```

Capability declarations are configuration plus validation evidence. Marketing
claims do not make a capability accepted.

Task risk:

| Risk | Example | Minimum handling |
|---|---|---|
| `R0` | formatting | accepted eligible target |
| `R1` | public summary | normal output validation |
| `R2` | deck-specific strategy | evidence and correction gates |
| `R3` | combo, tutor pile, or rules interaction | Rules validation and audit or refusal |
| `R4` | protected mutation request | refuse write path |
| `R5` | forbidden transmission | block before invocation |

## Routing Contract

Eligibility is determined before scoring.

```text
profile permits target
AND data classes are permitted
AND consent is valid
AND source rights permit transmission
AND provider policy is compatible
AND cost policy permits the target
AND runtime is available
AND declared capability supports the task
```

If any condition is false, the target is ineligible and cannot be rescued by
a high score.

The router may rank eligible targets using only versioned factors such as:

```text
capability fit
validated reliability
structured-output fit
context fit
latency policy
reproducibility fit
local hardware limits
```

Cost may be a hard ceiling. Paid status is never a positive quality signal.

The first implementation contract must use deterministic tie-breaking and
record the eligible set, exclusions, selected target, and fallback chain.

## Fallback Contract

Local-only profiles may fall back only to another accepted local target or to
`offline_deterministic`.

```text
local failure does not ask for cloud consent automatically
local failure does not queue private content for later external transmission
retry does not broaden data classes, detail level, or purpose
timeout does not retain partial streams unless the logging policy permits it
malformed output does not authorize fabricated fields or citations
```

A cloud target may appear only in a cloud-capable profile's explicit fallback
chain and only after all eligibility and consent gates pass for that attempt.

Network failure returns a visible unavailable or local-fallback state. It does
not weaken privacy controls.

## Output Distrust

All model and provider responses are untrusted.

Before downstream use, a response must pass:

```text
size and encoding limits
structured schema validation where required
blocked-key and executable-content checks
citation existence checks
Rules authority and legality gates for applicable claims
evidence-reference validation
contradiction disclosure
unsupported-claim handling
prompt-injection and tool-request rejection
```

Models cannot:

```text
write canonical, measured, legality, correction, or recommendation records
execute code or tools unless a later contract admits one bounded tool
alter their own profile, consent, redaction, or cost policy
fabricate missing evidence or citations
turn conversation into a persisted recommendation
```

## Audit And Reproducibility

Default logging mode is `metadata_only`.

Allowed logical modes:

```text
none
metadata_only
redacted_content
full_local_content
debug_temporary
```

Cloud transmission never implies permission to retain full local input.

Mandatory run metadata:

```text
run_id
request_id
created_at and completed_at
profile_id and profile_version
execution_target
provider_id
model_id and concrete version
model digest and quantization when local
runtime version
prompt-policy version
router version
redaction-policy version
consent IDs
data classes present and transmitted
deck snapshot ID and hash when applicable
evidence packet ID
Rules authority package ID
Theory Corpus version
Correction Ledger version
cloud_request_sent
fallback_used
eligible and rejected target summaries
transmission preview hash when external
result and validation status
reproducibility level
```

Metadata-only logs contain no raw prompt, response, secret, private deck name,
licensed theory text, authorization header, or environment value.

Provider-declared retention and Codie local retention remain separate fields.

## Required Failure States

```text
PROFILE_NOT_FOUND
PROFILE_NOT_ACCEPTED
NO_ELIGIBLE_TARGET
LOCAL_RUNTIME_UNAVAILABLE
MODEL_FILE_UNAVAILABLE
CLOUD_DISABLED
CONSENT_REQUIRED
CONSENT_INVALID
PROVIDER_POLICY_MISMATCH
DATA_CLASS_FORBIDDEN
RIGHTS_BLOCKED
REDACTION_FAILED
SECRET_DETECTED
PREVIEW_MISMATCH
COST_LIMIT_BLOCKED
NETWORK_UNAVAILABLE
MODEL_TIMEOUT
INVALID_MODEL_OUTPUT
STALE_MODEL_IDENTITY
STALE_SNAPSHOT
UNSUPPORTED_TASK
```

Failure states are visible and auditable. They do not contain the blocked
secret or private payload.

## Regression Requirements

A later implementation contract must include fixture-first tests for:

```text
local_strict never invokes cloud
local failure falls back locally or deterministically
no installed model preserves deterministic evidence surfaces
public-only cloud profile rejects private deck data
snapshot consent does not authorize another snapshot
provider change invalidates consent
purpose change invalidates consent
less restrictive redaction invalidates consent
secret detection blocks transmission and logs no secret
absolute local path is removed before preview
pseudonyms are stable within a request and mappings remain local
removing a deck name does not declassify a private cardlist
restricted theory never enters a cloud packet or cloud log
metadata-only logs contain no content
preview hash identifies the actual transmitted content
retry does not add data classes
local-only profile cannot name a cloud fallback
paid target is ineligible at zero cost limit
provider alias is not recorded as exactly reproducible
model response cannot alter profile, consent, or protected records
prompt injection cannot enable cloud, tools, or wider scope
cross-deck request state remains isolated
R3 output is validated or refused
```

Phase 42B regression families remain the future release gate. Phase 42D does
not create those fixtures or execute models.

## Resolved Decisions

Phase 42D resolves:

```text
local_strict is the default logical profile
offline_deterministic is a required fallback
cloud is disabled and deny-by-default
no cloud provider is admitted by this phase
private cloud consent is request- or snapshot-scoped initially
full_private_context is not admitted initially
metadata_only is the default logging mode
redaction happens before adapter invocation
preview identity must match transmitted content
local failure cannot silently become cloud execution
target eligibility precedes scoring
paid targets are blocked by zero-cost policy
model output cannot mutate protected records
```

## Deferred Decisions

Later accepted implementation or provider contracts must decide:

```text
exact local inference runtimes
minimum hardware profiles
default model files and quantization tiers
provider-specific cloud admission
at-rest encryption for private logs and consent records
provider retention verification adapters
maximum excerpt sizes by rights class
local privacy gateway support
model benchmarking thresholds
whether R3 always requires a separate local auditor
whether any cloud request body may be retained
```

Restrictive defaults apply until those decisions are accepted.

## Future Implementation Boundary

A later implementation contract may authorize pure packet models and
validators for:

```text
ModelDataClass
ModelProfile
ModelCapabilityDeclaration
ModelConsentRecord
ModelTransmissionManifest
ModelRedactionFinding
ModelRouteCandidate
ModelRoutingDecision
ModelRunAuditRecord
```

It may not authorize live model invocation, provider SDKs, network calls,
secrets, repositories, schema, UI, or file writing unless those surfaces are
named explicitly in a later accepted contract.

## Phase 42E Boundary

Phase 42E may define only the Minimal User Correction Ledger Core Contract.
It must preserve Rules authority ceilings, narrowest-scope application,
immutable history, and separation from canonical truth.

Phase 42E must not implement correction storage, repositories, application
logic, model calls, Jin integration, UI, or exports.

## Forbidden Phase 42D Work

Phase 42D must not add:

```text
production model or routing code
implementation tests or fixtures
provider adapters or SDKs
live network calls
secrets or credentials
prompt templates
schema, migrations, or repositories
consent or audit persistence
redaction runtime
Jin answer generation
Rules implementation
Correction Ledger implementation
Theory Corpus implementation
Decision Intelligence or recommendation output
simulator execution
UI or CLI behavior
file writing
dependency changes
workflow or validator changes
constitution changes
```

## Acceptance Gate

Phase 42D passes only when outside validation confirms that this packet:

1. preserves the Phase 42A trust boundaries;
2. remains contract-only;
3. makes local operation first-class;
4. makes cloud deny-by-default and optional;
5. defines explicit data classes and strictest-class handling;
6. requires specific consent and deterministic pre-egress redaction;
7. forbids silent local-to-cloud fallback;
8. separates eligibility from routing score;
9. preserves output distrust and protected-record write bans;
10. records replayable model, profile, consent, redaction, and route identity;
11. defers exact runtimes and providers without weakening defaults; and
12. keeps Phase 42E blocked.

Phase 42E may begin only after Phase 42D outside validation returns PASS or
PASS WITH REVIEW NOTES.
