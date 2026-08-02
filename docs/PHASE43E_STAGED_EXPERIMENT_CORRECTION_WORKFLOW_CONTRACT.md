# Phase 43E Staged Experiment and Correction Workflow Contract

## Validation tuple

```text
phase_id: Phase43E
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase43F
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 43F is reserved for the Knowledge Vault Planner and Renderer Contract and remains blocked until Phase 43E outside validation passes.

## Status and authority

```text
document_type: contract-only packet
implementation_authorized: no
schema_authorized: no
UI_authorized: no
API_authorized: no
persistence_authorized: no
active_scope_base: c6279c178ed79201522bba578e1fdb19f6f3ef55
```

This packet defines presentation and confirmation boundaries for already-produced experiment proposals and correction candidates. It consumes accepted Phase 42J write-intent packets and never turns display, navigation, Jin output, or a shortcut into authorization.

## Separate workflow classes

Experiment and correction workflows remain distinct:

- an experiment creates an isolated candidate state and comparison request;
- a correction proposes scoped user-supplied context under the Phase 42E authority ceiling;
- neither mutates canonical evidence, measured analytics, accepted recommendations, source records, Rules authority, or reviewed Theory.

A proposal cannot change class after confirmation. Combined experiment/correction writes are rejected and must be split into independently reviewed intents.

## Required staging summary

Before confirmation, the workflow presents:

- intent ID, type, status, creator/source, and creation time;
- active deck, immutable baseline snapshot, analysis run, decision, profile, and answer-packet identities;
- proposed candidate change or correction statement;
- exact target scope and authority ceiling;
- evidence, Rules, Correction, and reviewed-Theory references;
- expected effect, tradeoffs, risks, conflicts, caveats, and blocked reasons;
- privacy class, route, redactions, destination, and retention policy;
- idempotency key, expiry, and confirmation requirements.

Unknown, stale, mismatched, privacy-blocked, authority-blocked, or legality-blocked state disables confirmation.

## Experiment staging

An experiment workflow may request:

1. preservation of the immutable original snapshot;
2. creation of an isolated candidate snapshot from declared changes;
3. validation of card identities, zones, locks, legality, and scope;
4. rerun of only separately approved affected analyses;
5. baseline/candidate comparison under identical declared profiles and versions;
6. an immutable experiment receipt and result reference.

Staging does not edit the original deck, accepted snapshot, provider deck, recommendation, or evidence. No push to Moxfield, Archidekt, Hareruya, Cockatrice, or another provider is permitted. A candidate result remains an experiment and cannot silently become the active deck or recommendation.

## Correction staging

A correction workflow retains the Phase 42E target, scope, authority level, evidence references, conflicts, review state, privacy class, and user/profile ownership. It cannot override Oracle, Comprehensive Rules, canonical identity, higher-authority accepted corrections, or another user's scope.

Display or user repetition does not promote authority. Model/Jin authorship confers no authority. A correction candidate remains inactive until the accepted review and activation path returns a receipt. Rejection, supersession, expiry, and conflict remain visible.

## Confirmation ceremony

Confirmation requires an explicit user action on a current, fully rendered review surface. It must be bound to the exact intent version, target identities, proposed payload hash, destination, authority ceiling, and idempotency key.

The following are not confirmation:

- opening the workflow, navigating to it, or selecting it;
- Jin wording, model output, recommendation confidence, or prior approval;
- keyboard focus, hover, timeout, background refresh, or application restart;
- Stream Deck, Discord, notification, API prefetch, or another workflow's action;
- a confirmation token created before a material change.

Any material payload, snapshot, run, profile, authority, conflict, privacy, route, or destination change invalidates prior confirmation and requires a new review.

## Idempotency, concurrency, and receipts

One idempotency key represents one immutable write intent. Retrying the same accepted intent may return the original receipt but cannot duplicate a snapshot, experiment, correction, or user-context record. Reusing a key with different content is rejected.

Optimistic concurrency checks the baseline and target versions at commit time. Concurrent changes produce a visible conflict and no partial write. Receipts identify intent, payload hash, actor, target, before/after versions, committed records, timestamp, and result. Failure receipts do not claim success.

## Cancellation and recovery

Cancellation before commit leaves no activated record and preserves the original snapshot. A mid-operation failure is atomic: either all authorized records commit or none do. Recovery may inspect status and retry the same immutable intent; it cannot invent a replacement intent or broaden scope.

## Local-first privacy boundary

- Staging, review, confirmation, and receipts remain available locally.
- Private deck changes, corrections, experiments, notes, and Jin-derived proposals remain local by default.
- Any separately approved boundary crossing requires informed consent, pre-route redaction, destination/retention disclosure, and local fallback.
- Default export and telemetry exclude private staged and correction content.
- Cross-user or cross-profile activation is prohibited.

## Theory, Rules, Corrections, and Hareruya

Reviewed Theory may explain a proposal but retains author, work, immutable version, citation, rights, transferability, contradiction, and review state. It cannot authorize or activate a write. Rules and legality gates can block a proposal and cannot be overridden by user confirmation.

Hareruya remains tournament-only evidence provenance. It cannot receive writes or become a correction, Theory, curriculum, user-context, experiment destination, or authority source.

## Stream Deck boundary

Stream Deck remains optional and supplemental-only. A future adapter may navigate to an existing staged review or show status. It cannot create, modify, confirm, cancel, retry, or commit an intent; supply an idempotency key; dismiss conflicts; or bypass consent, privacy, authority, and legality gates.

## Accessibility and deterministic behavior

- Review summaries and errors use semantic headings and keyboard-operable controls.
- Focus moves to blocking errors and returns predictably after dialogs.
- Change type, authority, privacy, conflict, confirmation, and outcome do not rely on color alone.
- The same immutable intent and state produce the same review summary and confirmation availability.
- Pending, expired, stale, conflicted, blocked, confirmed, committed, failed, canceled, superseded, and duplicate states are explicit.

## Acceptance criteria

1. Experiments and corrections remain distinct write-intent classes.
2. The immutable original snapshot is preserved.
3. Candidate snapshots and reruns are isolated and explicitly identified.
4. Correction scope and authority ceilings remain enforced.
5. Confirmation binds exact current content and is invalidated by material changes.
6. Idempotency and optimistic concurrency prevent duplicate or partial writes.
7. Receipts are immutable and accurately report outcome.
8. Provider write-back is prohibited.
9. Local-first privacy and pre-boundary redaction remain mandatory.
10. Reviewed Theory and Rules gates remain intact.
11. Hareruya remains tournament-only.
12. Stream Deck remains supplemental-only and cannot confirm.
13. Phase 43F remains blocked.

## Explicit exclusions

No code, schema, packet class, component, renderer, route, API, repository, write service, candidate-snapshot implementation, analysis rerun, correction activation, provider write-back, export, model call, mobile surface, Stream Deck adapter, dependency, workflow automation, or active-scope edit is authorized.
