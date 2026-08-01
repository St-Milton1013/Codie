# Phase 42I - Jin Writer, Auditor, Deterministic Finalizer, and Answer-Packet Contract

Status: contract only; implementation not authorized

## Validation Tuple

```text
phase_id: Phase42I
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase42J
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 42J is reserved for the Experiment and Permitted User-Context Write
Contract. It remains blocked until Phase 42I outside validation returns PASS or
PASS WITH REVIEW NOTES.

## Purpose

Phase 42I defines how an approved Phase 42H gate report may become a governed
Jin answer packet without granting a writer or auditor authority over data,
evidence, legality, confidence, or recommendations.

This contract governs:

```text
capability-free writer input
structured writer drafts
per-claim ledgers
deterministic contradiction scanning
risk-based adversarial audit
deterministic finalization
final answer packet fields and statuses
raw-draft containment
```

It does not invoke a model, generate live prose, retrieve data, persist
answers, write files, generate recommendations, create experiments, or modify
user context.

## Authority

This contract is governed by:

1. `docs/CODIE_V2_CONSTITUTION.md`;
2. `docs/ROADMAP_PATCH_V2_INTELLIGENCE_PROGRAM_INTAKE.md`;
3. the accepted Phase 42A cross-specification boundary;
4. the accepted Phase 42B fixed regression-corpus contract;
5. the accepted Phase 42C Rules authority contract;
6. the accepted Phase 42D model-profile, redaction, consent, and routing
   contract;
7. the accepted Phase 42E Correction Ledger core contract;
8. the accepted Phase 42F Theory source and citation contract;
9. the accepted Phase 42G reviewed Theory graph and retrieval contract;
10. the accepted Phase 42H intent, scope, planning, and gate contract;
11. the accepted Phase 21 answer-builder and Phase 22 writer/auditor packet
    surfaces;
12. `docs/design_inputs/v2_intelligence_program/JIN_GITAXIAS_STRATEGIST_SUBSYSTEM_PROPOSAL.md`
    and `docs/design_inputs/v2_intelligence_program/JIN_CHAT_EXPERIENCE_PROPOSAL.md`
    as preserved design input only.

## Governing Invariants

```text
The writer receives only an approved, sanitized, bounded input packet.
The writer cannot retrieve, calculate, persist, call tools, or alter scope.
Every substantive draft claim has a claim-ledger record.
The writer cannot assign confidence or recommendation authority.
The contradiction scanner always runs after drafting.
High-risk answers cannot bypass required audit.
The auditor cannot retrieve, persist, finalize, or add unsupported claims.
Only the deterministic finalizer decides which claims survive.
Blocked claims, illegal suggestions, and mandatory caveats remain visible.
No raw writer draft is ever returned as a final answer.
Failure returns a structured failure packet.
Decision Intelligence remains the only persisted recommendation owner.
```

## Existing Phase 21 And Phase 22 Compatibility

The accepted surfaces remain valid:

```text
Phase 21 ChatAnswer and structured answer-builder packets
Phase 22 LLMWriterInput
Phase 22 LLMWriterDraft
Phase 22 LLMAuditFinding
Phase 22 LLMAuditResult
```

Phase 42I does not silently mutate their schemas or semantics.

A future implementation must use:

```text
versioned adapters into the Phase 42I packet family
parallel Phase 42I packets with explicit predecessor refs
or explicit versioned supersession after compatibility validation
```

Historical Phase 21 and Phase 22 packets remain replayable under their
recorded versions.

## Trust Boundary

```text
accepted Phase 42H evidence-gate report
and bounded approved answer bundle
-> writer input
-> structured writer draft and claim ledger
-> deterministic contradiction report
-> optional or mandatory adversarial audit
-> deterministic finalizer
-> final Jin answer packet
```

Only the final packet may cross the answer boundary. Drafts, model messages,
auditor prompts, chain-of-thought, and internal revisions remain internal.

## Approved Answer Bundle

The writer input is assembled only from already-built references:

```text
request ID
resolved intent
bound scope
query plan
evidence-gate report
claim-permission ledger
sanitized retrieval-bundle refs
Theory retrieval-packet refs
applicable correction refs
legality-report ref
mandatory conflict refs
confidence-ceiling refs
privacy and model-route decision
required output sections
```

The bundle cannot contain:

```text
repository objects
database credentials
raw provider payloads
private source bodies
raw imported deck text
raw simulator traces
unbounded filesystem content
unredacted cloud-ineligible content
write-capable tools
```

## Writer Input Packet

```text
writer_input_id
writer_input_version
request_id
plan_id
plan_hash
resolved_intent_id
bound_scope_id
evidence_gate_report_id
allowed_claim_ids
allowed_claim_classes
blocked_claim_ids
required_labels
mandatory_caveat_ids
required_conflict_ids
confidence_ceiling_refs
legality_report_ref
sanitized_evidence_refs
theory_packet_refs
correction_refs
unsupported_dependency_refs
expected_output_sections
answer_style_profile
privacy_class
model_route_ref
generated_at
metadata
```

The writer input is immutable, bounded, deterministically serialized, and
hash-addressed.

## Writer Permissions

The future writer may:

```text
produce direct-answer prose from allowed claims
produce structured comparisons
produce a claim ledger
state visible assumptions
preserve uncertainty
describe a permitted future experiment candidate
```

The writer may not:

```text
retrieve additional data
query providers or repositories
calculate analytics or confidence
run simulations
alter request intent or bound scope
change legality status
resolve a source or Theory disagreement
activate or rewrite a correction
add a new Decision Intelligence result
assign recommendation confidence
persist output
call tools directly
```

## Structured Writer Draft

```text
draft_id
draft_version
writer_input_id
request_id
plan_id
direct_answer_draft
structured_section_drafts
claim_records
citation_ids
caveat_ids
conflict_ids
unsupported_item_ids
suggested_experiment_drafts
assumptions
writer_identity
model_profile_ref
prompt_policy_version
generated_at
metadata
```

The draft is never user-visible merely because generation completed.

## Claim Ledger

Every substantive claim has:

```text
claim_id
claim_version
draft_section_id
proposed_text
claim_class
subject_refs
scope
supporting_refs
contradicting_refs
legality_dependency_ids
unsupported_dependency_ids
theory_refs
correction_refs
confidence_ceiling_ref
causation_language_status
recommendation_status
required_labels
mandatory_caveat_ids
writer_disposition
```

Claims without ledger entries cannot appear in substantive final sections.
Minor connective language may remain outside the ledger only when it makes no
factual, strategic, Rules, legality, empirical, or recommendation assertion.

Writer dispositions:

```text
PROPOSED
PROPOSED_WITH_CAVEAT
OMITTED_BY_WRITER
BLOCKED_BY_INPUT
```

## Citation Rules

Every material factual or attributed claim must resolve to the supporting
reference declared in the writer input.

```text
authority facts cite authority refs
measured claims cite scoped evidence refs
Decision Intelligence explanations cite decision IDs
Theory claims cite reviewed claim and exact Phase 42F anchors
primer or community context remains labeled and attributed
user context remains scoped
inference is labeled as inference
```

The writer may not invent, change, merge, or relabel citations.

## Draft Contradiction Scanner

The deterministic scanner always runs after drafting and before any audit or
finalization.

It checks:

```text
Oracle or Rules conflict
legality-report conflict
metric-value mismatch
population mismatch
date mismatch
region mismatch
commander or partner mismatch
stale snapshot usage
Correction Ledger conflict
omitted material Theory disagreement
claim stronger than evidence
correlation converted into causation
hypothesis converted into recommendation
unsupported item treated as modeled
simulator result generalized beyond conditions
community opinion presented as tournament evidence
privacy or rights violation
missing required citation, caveat, label, or conflict
```

A contradiction scanner proposes deterministic findings. It does not retrieve
new data, invoke a model, rewrite evidence, or persist output.

## Contradiction Finding

```text
finding_id
finding_version
finding_type
severity
claim_ids
section_ids
governing_ref_ids
conflicting_ref_ids
message
required_action
generated_at
```

Severity:

```text
CRITICAL
MAJOR
DISCLOSURE_REQUIRED
MINOR
INFORMATIONAL
```

Required actions:

| Severity | Action |
|---|---|
| `CRITICAL` | block packet or remove affected claim |
| `MAJOR` | require revision and adversarial audit |
| `DISCLOSURE_REQUIRED` | retain only with visible contradiction |
| `MINOR` | deterministic wording or label correction when unambiguous |
| `INFORMATIONAL` | retain in audit metadata |

The finalizer must not use an automated wording correction when multiple
material interpretations are possible.

## Authority Precedence During Scan

```text
1. official authority
2. Scryfall within its approved authority
3. canonical observations
4. reproducible measured evidence
5. existing Decision Intelligence result
6. attributed primer or Theory material
7. community context
8. model inference
```

Source quantity never overrides authority class.

## Audit Policy

Audit modes:

```text
REQUIRED
OPTIONAL
DETERMINISTIC_ONLY
UNAVAILABLE_BLOCKING
```

Audit is required for:

```text
novel combo or loop claims
tutor-pile certification
high-impact card comparisons
multi-object or continuous-effect Rules interactions
contentious strategic conclusions
mixed-evidence claims
unresolved material source conflicts
cloud-writer output
explanation of a persisted recommendation
high speculation
changes affecting more than the configured deck-slot threshold
MAJOR contradiction findings
```

Routine factual retrieval may use `DETERMINISTIC_ONLY` when all deterministic
checks pass. The contradiction scanner and finalizer are never bypassed.

If a required auditor is unavailable, the affected substantive packet is
blocked or reduced to an independently supported deterministic partial packet.

## Auditor Input

```text
audit_input_id
audit_input_version
draft_id
claim_ledger_ref
supporting_refs
contradicting_refs
legality_report_ref
correction_refs
evidence_gate_report_ref
contradiction_report_ref
risk_policy_ref
privacy_class
model_route_ref
generated_at
```

The auditor receives no retrieval or write capability.

## Auditor Permissions

The future auditor may:

```text
flag unsupported claims
flag missing citations, caveats, labels, or contradictions
flag scope drift
flag legality defects
flag causation overclaims
flag recommendation-boundary violations
flag privacy or rights violations
propose bounded revisions against existing refs
```

The auditor may not:

```text
retrieve arbitrary sources
add unreferenced factual or strategic claims
change evidence
change confidence
change legality
change scope
resolve Theory disagreements by preference
persist records
finalize the answer
```

## Audit Finding And Report

Finding fields:

```text
audit_finding_id
finding_type
severity
claim_ids
section_ids
source_ref_ids
message
proposed_action
```

Audit report fields:

```text
audit_report_id
audit_report_version
audit_input_id
draft_id
auditor_identity
model_profile_ref
prompt_policy_version
verdict
findings
accepted_claim_ids
rejected_claim_ids
revision_required_claim_ids
generated_at
```

Verdicts:

```text
ACCEPTED
REJECTED
REVISION_REQUIRED
HUMAN_REVIEW_REQUIRED
AUDITOR_UNAVAILABLE
```

An auditor finding is advice to the deterministic finalizer. It cannot mutate
the draft or become a claim.

## Audit Failure Behavior

```text
required auditor failure is never reported as accepted
timeout is distinct from rejection
malformed output is distinct from a substantive finding
cloud failure may use an authorized local fallback
no fallback may weaken privacy or rights policy
raw auditor output never becomes user-visible answer content
```

## Deterministic Finalizer

The finalizer receives only:

```text
writer input
structured draft
claim ledger
Phase 42H gate report
contradiction report
audit report or deterministic-only audit decision
packet policy
```

The finalizer determines:

```text
which claims survive
which claims are removed
which labels appear
which caveats and contradictions are mandatory
which citations remain attached
whether status is complete, partial, blocked, or failed
whether a permitted experiment draft may be attached
```

The finalizer must not:

```text
retrieve data
invoke a model
invent a replacement claim
raise confidence
weaken scope
change legality
resolve a disagreement without an accepted resolution
create a recommendation
persist output
```

## Finalization Actions

Per-claim actions:

```text
KEEP
KEEP_WITH_LABEL
KEEP_WITH_CAVEAT
KEEP_WITH_CONTRADICTION
REMOVE_UNSUPPORTED
REMOVE_ILLEGAL
REMOVE_SCOPE_MISMATCH
REMOVE_PRIVACY_BLOCKED
REMOVE_AUDIT_REJECTED
BLOCK_PACKET
REQUIRE_HUMAN_REVIEW
```

Every removed claim remains accounted for by ID and reason without exposing
disallowed source text.

## Final Answer Packet

```text
packet_id
packet_version
request_id
status
generated_at
resolved_intent_ref
bound_scope_ref
plan_id
plan_hash
direct_answer
structured_analysis
final_claim_ledger
evidence_level
speculation_level
source_coverage
material_source_refs
theory_perspectives
contradictory_evidence_refs
legality_status
legality_report_ref
unsupported_items
unsupported_claim_ids_removed
illegal_claim_ids_removed
confidence_ceiling_refs
decision_intelligence_ref
recommendation_status
correction_refs_applied
deck_snapshot_id
deck_hash
analysis_profile_ref
model_profile_ref
writer_identity
auditor_identity
audit_status
suggested_experiment_drafts
assumptions
caveats
privacy_disclosure
retrieval_provenance
evidence_gate_report_ref
contradiction_report_ref
audit_report_ref
analysis_manifest_ref
```

The UI may collapse evidence fields, but packet serialization keeps them
visible.

## Packet Status

```text
COMPLETE
PARTIAL
BLOCKED
FAILED
```

Rules:

```text
COMPLETE requires every material claim to survive all required checks
PARTIAL lists every omitted dependency and removed claim
BLOCKED contains no unapproved substantive answer
FAILED contains structured infrastructure failure, never raw draft prose
```

## Evidence Level

```text
AUTHORITY_VERIFIED
MEASURED
MIXED_EVIDENCE
CONTEXTUAL
THEORY_LED
INFERENCE_LED
INSUFFICIENT
```

This packet label summarizes the strongest support actually used. It does not
replace claim-level classification.

## Speculation Level

```text
NONE
LOW
MODERATE
HIGH
```

High speculation cannot be presented with high recommendation confidence and
cannot support a persisted recommendation.

## Recommendation Status

```text
NONE
EXPLAINS_EXISTING_DECISION_INTELLIGENCE
HYPOTHESIS_ONLY
TEST_CANDIDATE_ONLY
```

No Jin-created answer packet may claim `PERSISTED_RECOMMENDATION`.

## Direct-Answer Discipline

The future direct answer should:

```text
answer the user's actual question
state the principal evidence
state the principal limitation or contradiction
distinguish recommendation, hypothesis, experiment, and speculation
avoid hiding the answer behind provenance machinery
```

This is a presentation contract, not authority to omit required provenance
from the packet.

## Privacy And Model Routing

Phase 42D controls every writer and auditor route.

```text
local execution remains the default viable path
cloud use requires explicit profile consent
rights-blocked or local-only theory content cannot enter cloud packets
redaction occurs before model invocation
writer and auditor receive the minimum bounded packet
model prompts and raw responses are not final answer content
```

Phase 42I does not authorize live model invocation.

## Prompt-Injection Boundary

User and retrieved content remain untrusted data.

No instruction inside evidence, theory, primer, community, correction, deck,
or audit content may:

```text
change authority precedence
change scope
change gate or finalizer policy
add retrieval
grant write capability
alter model route
remove required citations or caveats
change recommendation ownership
override privacy or rights
```

## Rules And Legality Boundary

The finalizer consumes the Phase 42C legality report through Phase 42H.

It may remove or block affected claims. It cannot rewrite Rules truth or turn
an unresolved interaction into a legal line.

## Theory Boundary

Theory perspectives remain attributed and independent.

```text
material disagreements remain visible
format translations retain limitations
writer cannot imitate a theorist's voice
writer cannot attribute a new opinion to an author
Theory does not become measured evidence
Theory does not authorize a recommendation
```

## Correction Boundary

Corrections remain Phase 42E records.

The answer packet lists applied correction refs and scope. The writer,
auditor, and finalizer cannot create, activate, edit, or globalize a
correction.

## Simulator Boundary

Simulator references retain:

```text
simulation version
seed
target condition
unsupported behavior
opponent-dependency caveats
evidence-only classification
```

The writer cannot describe unsupported cards as modeled or a conditional line
as guaranteed.

## Failure Guarantees

```text
unsupported claim is never returned as fact
illegal suggestion is never returned as legal
unresolved card is never silently mapped
source conflict is never silently discarded
model draft never bypasses finalizer
auditor failure is never labeled successful
finalizer failure returns structured failure
privacy failure blocks the affected route
protected mutation attempt fails closed
no failure path exposes raw writer or auditor content
```

## Required Validation States

```text
WRITER_INPUT_INVALID
WRITER_SCOPE_DRIFT
WRITER_RETRIEVAL_ATTEMPT
WRITER_UNCITED_CLAIM
WRITER_CONFIDENCE_MUTATION
WRITER_RECOMMENDATION_VIOLATION
CLAIM_LEDGER_MISSING
CLAIM_LEDGER_ORPHAN
CONTRADICTION_SCAN_FAILED
CONTRADICTION_CRITICAL
AUDIT_REQUIRED
AUDITOR_UNAVAILABLE
AUDITOR_OUTPUT_INVALID
AUDITOR_UNSUPPORTED_ADDITION
FINALIZER_INPUT_INVALID
FINALIZER_NONDETERMINISTIC
FINALIZER_FAILED
RAW_DRAFT_ESCAPE_BLOCKED
PRIVACY_ROUTE_BLOCKED
HUMAN_REVIEW_REQUIRED
```

## Required Regression Cases

A future implementation contract must cover:

```text
writer input contains only approved bounded fields
writer cannot retrieve, calculate, persist, or call tools
every substantive draft claim has a ledger record
orphan substantive prose is rejected
citations resolve to writer input refs
writer cannot raise confidence
writer cannot assign recommendation authority
contradiction scanner always runs
Rules conflict is critical
population and date scope drift is detected
causation overclaim is detected
Theory disagreement omission is detected
unsupported simulator behavior is detected
high-risk answer requires audit
routine factual answer may use deterministic-only path
auditor cannot add unsupported claim
auditor cannot retrieve, persist, alter confidence, or finalize
required auditor unavailability blocks affected output
finalizer removes blocked and illegal claims
finalizer preserves mandatory caveats and contradictions
removed claim IDs and reasons remain visible
same inputs produce same final packet
COMPLETE, PARTIAL, BLOCKED, and FAILED remain distinct
raw writer draft cannot escape after scanner, auditor, or finalizer failure
existing Decision Intelligence may be explained but not changed
private or rights-blocked content cannot enter a model packet
prompt injection cannot alter writer, audit, or finalizer policy
Phase 21 and Phase 22 packet compatibility remains versioned
```

## Resolved Decisions

Phase 42I resolves:

```text
writer input and permissions
structured draft and claim-ledger requirements
deterministic contradiction categories and severity
mandatory and optional audit policy
auditor input, permissions, findings, and failure behavior
deterministic finalizer inputs and actions
final answer packet fields and statuses
evidence, speculation, and recommendation labels
raw-draft containment
Phase 21 and Phase 22 compatibility boundary
```

## Deferred Decisions

Later accepted contracts must decide:

```text
implementation packet models and validators
writer prompt and model execution
auditor prompt and model execution
contradiction scanner implementation
finalizer implementation
answer persistence and history
experiments
permitted user-context writes
conversation summaries
correction candidate submission
curriculum
API, UI, export, and Knowledge Vault projection
schema, migrations, and repositories
```

## Future Implementation Boundary

Later implementation contracts may authorize pure packet models, validators,
and deterministic finalizer logic in small slices before any live model route.

No implementation filename, model, prompt, persistence layer, or runtime
service is authorized by Phase 42I.

## Phase 42J Boundary

Phase 42J may define only experiments, theory notes, user testing notes,
correction candidates, deck-specific hypotheses, and structured conversation
summaries as explicitly permitted user-context writes.

It must not implement writes, persistence, recommendation generation,
canonical mutation, UI, exports, or network behavior unless separately
authorized.

## Forbidden Phase 42I Work

Phase 42I must not add:

```text
production Jin, writer, auditor, scanner, or finalizer code
implementation tests or fixtures
schema, migrations, repositories, or persistence
provider, source-table, or live retrieval access
analytics or simulator calculation
live model or network calls
prompt implementation
answer generation
answer persistence
Theory graph or Correction Ledger mutation
Decision Intelligence or recommendation generation
experiments or user-context writes
curriculum
UI, CLI, API, export, or file-writing behavior
dependency changes
workflow or validator changes
active-scope changes in the PR
constitution changes
```

## Acceptance Gate

Phase 42I passes only when outside validation confirms that it:

1. remains contract-only;
2. records Phase 42H artifact-backed acceptance;
3. preserves Phase 21 and Phase 22 through versioned compatibility;
4. gives the writer no retrieval, calculation, persistence, or tool
   capability;
5. requires a ledger for every substantive claim;
6. requires deterministic contradiction scanning;
7. requires audit for high-risk answers;
8. prevents the auditor from adding unsupported claims or finalizing;
9. makes the deterministic finalizer the only claim-survival authority;
10. preserves citations, caveats, conflicts, legality, scope, and removed
    claims;
11. keeps recommendation ownership with Decision Intelligence;
12. prevents raw draft escape on every failure path;
13. preserves privacy, rights, Theory, correction, simulator, and Rules
    boundaries; and
14. keeps Phase 42J blocked.

Phase 42J may begin only after Phase 42I outside validation returns PASS or
PASS WITH REVIEW NOTES.
