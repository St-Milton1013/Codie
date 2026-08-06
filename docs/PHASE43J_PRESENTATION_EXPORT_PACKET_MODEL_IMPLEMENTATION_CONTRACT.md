# Phase 43J Presentation/Export Packet Model Implementation Contract

```text
phase_id: Phase43J
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase43K
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase 43J defines the next implementation boundary for pure, in-memory
presentation/export packet models. It authorizes a future Phase 43K
implementation contract target only; it does not implement code in this packet.

The implementation may create deterministic packet classes, validation helpers,
serialization helpers, and tests for presentation/export metadata that is already
accepted by upstream phases. It must not render UI, write files, call providers,
publish externally, or mutate any evidence source.

## Future implementation files

Phase 43K may create:

```text
codie/presentation_export/__init__.py
codie/presentation_export/packets.py
tests/test_presentation_export_packets.py
docs/PHASE43K_PRESENTATION_EXPORT_PACKET_MODEL_IMPLEMENTATION_REPORT.md
```

## Future public interface

Phase 43K may define:

```text
PresentationExportPacketError
PresentationContextRef
PresentationEvidenceRef
PresentationPrivacyState
PresentationAccessibilityState
PresentationStatusMessage
PresentationExportIntent
PresentationPacket
PresentationExportPacketOptions
build_presentation_context_ref(...)
build_presentation_evidence_ref(...)
build_presentation_privacy_state(...)
build_presentation_accessibility_state(...)
build_presentation_status_message(...)
build_presentation_export_intent(...)
build_presentation_packet(...)
presentation_context_ref_to_dict(...)
presentation_evidence_ref_to_dict(...)
presentation_privacy_state_to_dict(...)
presentation_accessibility_state_to_dict(...)
presentation_status_message_to_dict(...)
presentation_export_intent_to_dict(...)
presentation_packet_to_dict(...)
validate_presentation_packet(...)
```

Names may be adjusted during implementation only if the same boundaries remain
explicit and tests prove the same behavior.

## Data model boundaries

The packet layer may represent:

- stable presentation context identity;
- source/evidence references already accepted by upstream packets;
- content-class labels for measured evidence, reviewed Theory, Rules authority,
  Corrections, user context, simulation, recommendation, example, and unknown;
- privacy states for public, local-only, redacted, omitted, blocked, unavailable,
  and secret-blocked content;
- accessibility states for keyboard, screen-reader, focus, reduced-motion,
  non-color warning, and deterministic status-message equivalents;
- export intent metadata that remains inert until passed to a separately
  accepted renderer and safe writer;
- stale/current status, conflict status, legality status, and unsupported states.

The packet layer must not contain raw private deck text, prompts, traces,
chain-of-thought, secrets, tokens, credentials, provider cookies, session data,
or unreviewed Theory excerpts.

## Required validation behavior

The future implementation must be deterministic, pure, serializable, and
fixture-testable. It must reject:

- missing context identity;
- missing evidence/provenance identity where a displayed claim depends on it;
- content-class ambiguity;
- confidence/source-agreement collapse;
- local-only material marked exportable;
- secret/token/credential fields anywhere in recursive input;
- unreviewed Theory marked as reviewed;
- Hareruya references outside tournament/event/deck provenance;
- Stream Deck confirmation, consent, write, or retry authority;
- renderer, writer, path, overwrite, receipt, provider-write, sync, publish, or
  route/API authority smuggled into export metadata.

## Accessibility contract

Every blocking, warning, omitted, redacted, stale, conflict, legality, unsupported,
and success state must have a text status suitable for assistive technology.
Color, hover, animation, layout position, or icon-only state cannot be the only
carrier of meaning.

The packet model must preserve focus-safe and keyboard-reachable state
descriptions but does not implement focus management, DOM behavior, components,
or UI layouts.

## Privacy and local-first contract

All packet construction is local-first and offline-testable. The packet model may
describe an export intent, but exportability is false by default for private
decks, user notes, conversations, corrections, experiments, Theory excerpts,
local-meta material, prompts, traces, secrets, tokens, and credentials.

Redaction and omission must be explicit in serialized output. A redacted or
omitted value cannot be replaced with fabricated evidence or a weaker unlabeled
summary.

## Theory, Rules, Corrections, Hareruya, and providers

Reviewed Theory retains author, work, immutable version, citation, rights class,
transferability, contradiction, and review state. Theory cannot become measured
evidence, hidden authority, or export permission.

Rules authority retains version, assumptions, legality state, and unsupported
state. Corrections retain scope, authority ceiling, review state, and conflict
state. Neither can be silently overridden by packet construction.

Hareruya remains tournament-only evidence provenance. It cannot become Theory,
rules, correction, curriculum, user-context, export authority, write target, or
provider mutation target.

Provider write-back remains prohibited. Packets may reference existing provider
provenance identities but cannot fetch, mutate, upload, sync, publish, or call a
provider.

## Stream Deck boundary

Stream Deck remains optional and supplemental-only. Packet models may describe a
future navigation label or read-only status label, but cannot represent Stream
Deck confirmation, consent, write, retry, evidence selection, privacy override,
legality override, or validation bypass.

## Do not do in Phase 43K

```text
do not add schema
do not add renderer implementation
do not add UI components
do not add routes or APIs
do not add filesystem writes
do not implement the safe file writer
do not create directories or output files
do not add persistence
do not read databases
do not read providers
do not call providers
do not write back to providers
do not publish, sync, upload, or share externally
do not call LLM/model APIs
do not generate recommendations
do not run simulator logic
do not ingest or promote Theory
do not mutate Rules authority
do not activate Corrections
do not implement Stream Deck adapters
do not add workflow automation
do not add dependencies
do not edit active validation scope
```

## Acceptance requirements

Phase 43K must include tests proving:

1. deterministic serialization;
2. recursive secret/token/credential rejection;
3. private/local-only export blocking;
4. explicit redacted/omitted/blocked states;
5. content-class separation;
6. confidence and source-agreement separation;
7. reviewed/unreviewed Theory separation;
8. Rules, Correction, legality, and unsupported-state preservation;
9. Hareruya tournament-only enforcement;
10. Stream Deck supplemental-only enforcement;
11. no renderer, writer, path, provider, publish, sync, or API authority;
12. accessibility text-state coverage.

## Not authorized

This packet does not authorize implementation code, schema changes, UI,
renderers, routes, APIs, filesystem writes, safe-writer behavior, persistence,
provider access, provider write-back, publication, model calls, recommendation
generation, simulation, Stream Deck adapters, dependencies, workflow automation,
or active-scope edits.

