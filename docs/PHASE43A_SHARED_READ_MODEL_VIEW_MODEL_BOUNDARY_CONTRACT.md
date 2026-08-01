# Phase 43A Shared Read-Model and View-Model Boundary Contract

## Validation tuple

```text
phase_id: Phase43A
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase43B
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 43B is reserved for the Desktop Deck and Analysis Workspace Contract and
remains blocked until Phase 43A outside validation passes.

## Status

```text
document_type: contract-only packet
implementation_authorized: no
schema_authorized: no
UI_authorized: no
API_authorized: no
persistence_authorized: no
active_scope_base: 8a1d2457f458823cb49530b51ed546983c5dc20f
```

## Purpose

Define one projection boundary that presentation surfaces can share without
duplicating domain logic or weakening evidence, privacy, and authority rules.

Read models and view models are immutable projections. They do not become a
new domain layer, evidence source, recommendation engine, or persistence path.

## Allowed inputs

```text
canonical read records
measured evidence packets
Unified Evidence packets
Decision Intelligence outputs
finalized Jin answer packets
accepted source-conflict packets
deck snapshots and simulation reports
reviewed Theory claim packets
permitted user-context records
lesson and curriculum packets
validation and source-health states
```

Each input must retain stable identity, version, provenance, class, scope,
confidence or uncertainty where applicable, and privacy classification.

## Forbidden calculations and writes

The projection boundary may not:

- ingest providers or canonicalize records;
- calculate metrics, simulations, confidence, or recommendations;
- resolve rules, legality, corrections, theory conflicts, or contradictions;
- call models or retrieval tools;
- activate corrections or experiments;
- mutate source records, deck snapshots, progress, or user context;
- persist recommendations or presentation-derived conclusions;
- transmit private data or invoke integrations.

## Shared projection envelope

Every future shared read model must include:

```text
view_model_id
view_model_type
schema_version
source_packet_refs
source_versions
generated_at
content_sections
content_class_labels
citation_refs
confidence_and_uncertainty
conflict_and_caveat_refs
unsupported_and_unavailable_states
privacy_classification
allowed_actions
blocked_actions
staleness_state
replay_identity
```

`generated_at` reports projection time, not evidence observation time.

## Content-class preservation

Presentation must preserve visible separation among:

```text
AUTHORITY
CANONICAL_OBSERVATION
MEASURED_EVIDENCE
CONCLUSION
REVIEWED_THEORY
EXAMPLE_OR_HYPOTHETICAL
COMMUNITY_CONTEXT
USER_CONTEXT
MODEL_EXPLANATION
```

Styling or summarization cannot promote a lower class. Missing and unknown
states cannot be rendered as zero, false, safe, legal, or not recommended.

## Actions

An `allowed_action` is navigation or a request to an already accepted owning
subsystem. It is not permission for the view model to execute the action.

Actions that change state must carry the destination owner, required
confirmation, privacy requirements, and governing contract. A presentation
surface cannot synthesize a write or reuse confirmation from another action.

## Privacy and redaction

- Private content is excluded unless the requesting local user and surface are
  authorized for that exact scope.
- Redaction occurs before projection across a boundary, not only at rendering.
- A share/export view model must default to excluding private decks, notes,
  progress, conversations, experiments, and theory excerpts.
- Cloud processing and remote presentation remain optional and deny-by-default.
- Equivalent local presentation must remain available.

## Theory, rules, and correction presentation

Theory projections retain author, work, immutable version, citation, rights
class, transferability, contradiction, and review state. Rules projections
retain authority version and unsupported states. Correction projections retain
scope, authority ceiling, review state, and conflicts.

Presentation may not flatten these into a generic `fact` field.

## Tournament-source presentation

Hareruya may appear only as provenance for canonicalized tournament, event, or
deck observations. A view model cannot present Hareruya as theory, curriculum,
community sentiment, or recommendation authority. WAF/live-access state may be
shown as source health but is not a critical-path dependency.

## Stream Deck boundary

Stream Deck may later consume a minimal navigation/action projection. It may
not receive hidden private content, confirm writes, answer assessments, change
scores, or bypass the owning surface. The standalone Game Tracker remains out
of scope.

## Determinism and staleness

Equivalent accepted inputs, versions, permissions, locale, and profile must
produce an equivalent deterministic projection. Ordering and serialization
must be stable.

Staleness must identify the stale source packet and reason. A projection may
not silently refresh providers, models, evidence, or user context.

## Accessibility and localization

Content class, confidence, conflicts, and blocked states cannot rely on color
alone. Labels must remain machine-readable and screen-reader accessible.
Localization may translate presentation text but cannot alter citations,
authority, card identity, evidence class, or claim scope.

## Acceptance requirements

Outside validation must confirm:

1. Read/view models are immutable projections only.
2. No evidence, metric, confidence, rule, correction, recommendation, model,
   retrieval, or persistence behavior is authorized.
3. Content classes and unknown states remain visible.
4. Private content is local-first and excluded by default across boundaries.
5. Theory, rules, corrections, and source provenance retain their gates.
6. Hareruya remains tournament-only.
7. Stream Deck remains supplemental-only.
8. No production code, tests for new behavior, schema, UI, API, dependency,
   workflow, or constitution change is present.
9. Phase 43B remains blocked.

## Explicit non-authorization

This phase does not authorize implementation, schemas, repositories,
persistence, provider access, analytics, simulations, models, prompts,
recommendations, UI, CLI, API, exports, integrations, dependencies, workflows,
or constitutional changes.
