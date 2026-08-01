# Phase 42J Experiment and Permitted User-Context Write Contract

## Validation tuple

```text
phase_id: Phase42J
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase42K
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 42K is reserved for the Judge-Training and Curriculum Contract and remains
blocked until Phase 42J outside validation returns `PASS` or
`PASS WITH REVIEW NOTES`.

## Status and authority

```text
document_type: contract-only packet
implementation_authorized: no
schema_authorized: no
persistence_authorized: no
model_or_network_execution_authorized: no
active_scope: Phase42J
active_scope_base: bba6c96518332693d6d2a121dc87f15a91ff646b
```

This contract defines which Jin outputs may later become explicitly confirmed
user-context records. It does not implement or execute those writes.

## Constitutional boundary

Jin may never write canonical tournament evidence, source records, measured
metrics, confidence tables, legality truth, commander staples, package
statistics, or persisted recommendations.

The only record families Phase 42J may define are:

```text
EXPERIMENT_CANDIDATE
THEORY_NOTE
USER_TESTING_NOTE
CORRECTION_CANDIDATE
DECK_SPECIFIC_HYPOTHESIS
STRUCTURED_CONVERSATION_SUMMARY
```

Every such record remains user context, theory, or a candidate. Creation does
not promote it into evidence, rules authority, an active correction, or a
recommendation.

## Required source boundary

A permitted write request may originate only from a finalized Phase 42I answer
packet or an explicit user-authored request. Raw writer drafts, auditor text,
retrieval packets, community items, theory candidates, and Stream Deck actions
cannot independently create a write request.

The input envelope must contain:

```text
request_id
record_family
proposed_payload
source_answer_packet_id or explicit_user_input_ref
user_scope
deck_scope when applicable
session_scope when applicable
provenance_refs
evidence_class_labels
theory_claim_refs
correction_refs
privacy_classification
retention_choice
requested_at
```

Missing source identity, ownership scope, privacy classification, or retention
choice fails closed.

## Two-step confirmation gate

No model, finalizer, integration, or background process may directly persist a
permitted record. The required lifecycle is:

```text
DRAFTED
  -> PRESENTED_FOR_CONFIRMATION
  -> CONFIRMED | EDITED_AND_CONFIRMED | CANCELLED | EXPIRED
  -> WRITE_PLANNED
```

Only an explicit user action may produce `CONFIRMED` or
`EDITED_AND_CONFIRMED`. Silence, navigation, session close, timeout, a generic
approval from another workflow, or a Stream Deck shortcut is not confirmation.

The confirmation view must show the exact payload, destination family, scope,
provenance, privacy class, retention choice, and effects of cancellation.

## Ownership and isolation

Records must use the narrowest valid ownership scope:

```text
user
user + deck snapshot
user + conversation
user + experiment
```

A deck-specific hypothesis cannot silently become a user-global belief. A
conversation summary cannot become tournament population evidence. A theory
note cannot alter the shared Theory Corpus. Multi-user or shared-machine data
must remain isolated by explicit owner identity.

## Record-family rules

### Experiment candidate

An experiment candidate states a testable question, controlled inputs,
expected observations, stop conditions, and limits. It must distinguish a
hypothesis from a recommendation and must not claim that an unrun experiment
supports a conclusion.

### Theory note

A theory note is user-authored context. Any referenced framework must retain
author, work, immutable version, citation, rights class, transferability state,
and review status. Unreviewed theory remains labeled and cannot be promoted by
the write.

### User testing note

A testing note records what the user reports or observes. It is not a simulator
result, tournament observation, or measured metric unless a separately
governed subsystem independently validates it.

### Correction candidate

A correction candidate is a proposal only. It cannot activate a correction,
change authority, mutate source truth, or trigger revalidation. Phase 42E
scope, authority ceiling, review, and conflict rules remain controlling.

### Deck-specific hypothesis

A hypothesis must identify the exact deck snapshot and assumptions. It cannot
generalize to other decks, commanders, metagames, or populations without new
evidence and review.

### Structured conversation summary

A summary may retain user decisions, open questions, cited evidence references,
confirmed preferences, and expressly retained hypotheses. It must not retain
raw hidden prompts, chain-of-thought, auditor drafts, undisclosed private
material, or an inference presented as a user statement.

## Evidence and theory gates

- Canonical and measured evidence remain read-only references.
- Community material remains community context.
- Theory remains attributed context and must pass the accepted theory-source
  and reviewed-claim gates before it is presented as reviewed theory.
- Hareruya references are permitted only for canonicalized tournament, event,
  or deck observations. Hareruya is not a theory or community source.
- Unknown, unsupported, stale, contradictory, and unavailable states remain
  visible in the proposed record.

## Local-first and privacy rules

- The entire confirmation and write-planning path must have a local-only mode.
- Cloud processing is deny-by-default and never required.
- Private payloads cannot be transmitted without separate, explicit,
  destination-specific consent after redaction preview.
- Consent to answer a question is not consent to persist its content.
- Consent to persist one record is not consent for future records.
- Cancellation and deletion must be available through the eventual owning
  subsystem without silently deleting immutable evidence or audit records.

## Retention and deletion contract

Every proposed record requires an explicit retention choice:

```text
SESSION_ONLY
UNTIL_DATE
UNTIL_USER_DELETES
PROJECT_LOCAL
```

No indefinite default is permitted. Expired drafts are not writes. Eventual
deletion must remove the user-context payload and leave only the minimum
non-sensitive tombstone needed to prevent accidental resurrection, where a
later implementation contract demonstrates that a tombstone is required.

## Supplemental integration boundary

Stream Deck may later open the confirmation view or navigate to an existing
experiment. It may not confirm, edit-and-confirm, activate a correction,
transmit private content, or bypass retention and deletion choices.

## Deterministic write-plan result

Phase 42J defines a future deterministic planner result:

```text
WRITE_PLAN_READY
BLOCKED_MISSING_CONFIRMATION
BLOCKED_SCOPE
BLOCKED_PRIVACY
BLOCKED_RIGHTS
BLOCKED_AUTHORITY
CANCELLED
EXPIRED
```

The planner may validate and serialize a plan. It may not perform persistence.

## Audit requirements

A future implementation must retain replayable evidence of:

```text
proposal identity and hash
source answer or explicit user input
payload shown to the user
user edits
confirmation event
owner and destination scope
privacy and retention choices
policy and schema versions
write-plan result
created and expiry timestamps
```

The audit record must not contain hidden reasoning or unnecessary private text.

## Failure behavior

Ambiguity fails closed. Partial writes are prohibited. A failed, cancelled, or
expired plan must not create destination data. Retry requires a fresh display
of the exact payload whenever the payload, destination, scope, privacy class,
retention choice, or governing policy changes.

## Acceptance cases

Outside validation must confirm at minimum:

1. Only the six permitted record families are defined.
2. All writes require explicit, payload-specific user confirmation.
3. Canonical, measured, legality, confidence, source, and recommendation data
   remain immutable.
4. Correction candidates cannot activate corrections.
5. Theory notes retain rights, attribution, version, citation, and review state.
6. Hareruya remains tournament-only.
7. Local-only operation remains complete and cloud remains optional.
8. Stream Deck cannot confirm or bypass safety gates.
9. Retention is explicit and deletion behavior is bounded.
10. The packet contains no implementation, persistence, model calls, schemas,
    dependencies, workflows, or constitution changes.

## Explicit non-authorization

This phase does not authorize production code, tests for new behavior, schema,
migrations, repositories, file writers, database writes, model calls, prompt
execution, answer generation, correction activation, experiment execution,
simulation, provider access, UI, CLI, API, exports, Stream Deck implementation,
dependencies, workflows, or constitutional changes.
