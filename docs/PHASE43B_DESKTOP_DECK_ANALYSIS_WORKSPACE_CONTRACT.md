# Phase 43B Desktop Deck and Analysis Workspace Contract

## Validation tuple

```text
phase_id: Phase43B
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase43C
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 43C is reserved for the Decision Evidence Panel Contract and remains
blocked until Phase 43B outside validation passes.

## Status and authority

```text
document_type: contract-only packet
implementation_authorized: no
schema_authorized: no
UI_authorized: no
API_authorized: no
persistence_authorized: no
active_scope_base: 1d9b9132d4bf0ba50559bd55123f54c97f59ca09
```

This contract narrows the approved two-workspace information architecture. It
does not authorize a desktop shell, renderer, component tree, route, event bus,
state store, import flow, analysis launcher, Jin UI, export path, or mutation.

## Required information architecture

Codie has two primary desktop workspaces:

- **Deck Workspace**: controlled deck identity, immutable snapshot context,
  local staged changes, role/package inspection, warnings, comparisons, and
  analysis controls.
- **Analysis Workspace**: attention-ranked findings, analysis identity and
  status, conflict/caveat access, experiment and report navigation, and
  reserved regions for the Decision Evidence Panel and Jin discussion.

“Two-screen” is an information-architecture contract, not a hardware
dependency. Dual-display presentation may place one workspace on each display.
Single-display presentation must provide an equivalent top-level Deck/Analysis
switcher without losing evidence, state, or accessibility.

## Shared context boundary

The workspaces may synchronize only stable identities and presentation
selection state, including:

```text
active_deck_id
active_deck_snapshot_id
active_analysis_run_id
active_decision_id
active_card_id
active_experiment_id
active_jin_thread_id
analysis_profile_id
weight_profile_id
comparison_snapshot_id
```

They consume only Phase 43A-compliant immutable projections. They may not share
mutable evidence, calculations, recommendation objects, theory claims, rules
records, corrections, or private user content through ad hoc UI state.

Cross-workspace notifications are typed identity/selection messages. They
cannot carry domain authority, mutate evidence, trigger an unconfirmed write,
or silently change the active snapshot, profile, or analysis run.

## Deck Workspace responsibilities

The Deck Workspace may present:

- selected deck and canonical commander/card identities;
- immutable snapshot ID, hash, source status, and observation time;
- mainboard/zone separation, locked/ignored state, role/package labels;
- unresolved, unsupported, stale, or changed-source warnings;
- local staged changes and snapshot comparisons;
- controls that request separately authorized import, refresh, comparison, or
  analysis operations.

Every requested operation remains owned by its governing service and contract.
The workspace does not canonicalize cards, create snapshots, calculate roles,
refresh providers, run analyses, or commit staged changes itself. It is not a
replacement for a hosted deck-building/social platform.

## Analysis Workspace responsibilities

The Analysis Workspace may present:

- active deck snapshot, analysis run, profile, version, status, and staleness;
- attention-ranked findings without recalculating their rank;
- deck-health, replacement, simulation, comparison, conflict, caveat,
  experiment, report, export, and provenance navigation;
- a reserved central Decision Evidence Panel region;
- a separate Jin discussion region bound to explicit evidence and snapshot
  identities.

Phase 43B defines regions and navigation only. It does not define or implement
Decision Evidence Panel contents, recommendation presentation logic, Jin
conversation behavior, experiment writes, exports, or provenance rendering.

## Identity, provenance, and hard-evidence rules

The active snapshot ID must remain visible wherever a deck conclusion, analysis
run, comparison, experiment, report, or Jin thread is selected. Analysis profile,
weight profile, source/version identity, confidence, conflicts, caveats, and
staleness cannot be replaced with unlabeled UI state.

Changing deck, snapshot, run, profile, or comparison selection invalidates or
visibly marks incompatible projections. Cached results must show their original
snapshot, version, and observation time. A workspace may not imply that a stale,
partial, unsupported, inferred, theory-based, or user-supplied item is measured
canonical evidence.

## Local-first privacy boundary

- Both workspaces must remain fully usable on the required local path.
- Private decks, notes, staged changes, corrections, experiments, conversations,
  and theory excerpts remain local by default.
- Redaction occurs before any separately approved boundary crossing.
- Cloud, telemetry, sharing, synchronization, and remote rendering are opt-in
  only and remain outside this packet.
- Cross-workspace state must not leak content between users or profiles.

## Theory, rules, corrections, and Hareruya

Theory is a separately labeled explanation lens. It retains author, work,
immutable source version, citation, rights class, transferability, contradiction,
and review state; it cannot occupy an evidence or recommendation authority slot.
Rules and legality retain authority version and unsupported states. Corrections
retain scope, authority ceiling, review state, and conflicts.

Hareruya may appear only as provenance for canonicalized tournament, event, or
deck observations. It is not a theory, curriculum, recommendation, correction,
rules, or user-context source.

## Stream Deck boundary

Stream Deck remains optional and supplemental-only. A future adapter may request
navigation to a workspace or existing approved action surface. It cannot confirm
writes, bypass consent or validation, become required for desktop use, host live
game tracking, or become an independent evidence/action authority.

## Accessibility and responsive behavior

- All workspace selection and navigation must be keyboard operable.
- Focus changes are explicit, reversible, and do not steal focus on background
  cross-workspace updates.
- Severity, confidence, content class, conflict, caveat, staleness, and blocked
  state do not rely on color alone.
- Narrow desktop layouts may collapse Jin and the attention queue, but the
  central decision region and substantive evidence remain available.
- Single-display fallback is functionally equivalent to dual-display mode.
- User-visible labels support localization without changing stable identifiers.

Mobile delivery remains deferred and outside this packet. A future read-only
mobile surface requires a separate endpoint and read model, not hidden mutation
controls.

## Determinism and failure behavior

Given the same immutable projections and selection state, workspace identity,
ordering, visible status, and navigation targets are deterministic. Loading,
empty, stale, unsupported, privacy-blocked, authorization-blocked, and error
states must be explicit. Failure in Jin, simulation, provider refresh, export,
or another optional subsystem must not erase already available evidence.

## Acceptance criteria

1. Deck and Analysis responsibilities are separate and bounded.
2. Dual-display and single-display modes are equivalent information architecture.
3. Shared state is identity/selection only and consumes Phase 43A projections.
4. Snapshot, run, profile, provenance, uncertainty, and staleness stay visible.
5. Hard-evidence classes and authority boundaries cannot be relabeled by UI state.
6. Local-first privacy and pre-boundary redaction remain mandatory.
7. Reviewed Theory, Rules, and Correction gates remain intact.
8. Hareruya remains tournament-only.
9. Stream Deck remains supplemental-only and cannot confirm or bypass gates.
10. Accessibility and deterministic failure states are required.
11. No implementation surface is authorized.
12. Phase 43C remains blocked.

## Explicit exclusions

No code, schema, database, repository, component, layout implementation, API,
route, event bus, application store, provider access, calculation, simulation,
recommendation, Jin execution, experiment write, export, mobile delivery,
Stream Deck adapter, dependency, workflow, or active-scope edit is authorized.
