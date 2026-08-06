# Phase 43I Presentation/Export Implementation Planning

```text
phase_id: Phase43I
phase_part: planning
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase43J
next_phase_part: implementation-contract
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase 43I plans the first implementation-contract slice after the accepted
Phase 43A through Phase 43H presentation/export governance chain. It does not
implement runtime behavior.

The next implementation contract should start with a narrow, local, deterministic
presentation/export packet model boundary before any UI, renderer, safe writer,
provider integration, Stream Deck adapter, or workflow automation is authorized.

## Recommended Phase 43J target

Phase 43J should define an implementation contract for in-memory presentation
and export request packet models only.

The target may define future pure packet builders for:

- shared presentation context identity;
- evidence/provenance display references;
- privacy/redaction display states;
- accessibility status and error states;
- export intent metadata that can later be handed to a separate safe writer.

## Required exclusions

Phase 43J must not authorize:

```text
filesystem writes
safe file writer implementation
renderer implementation
UI components
routes or APIs
database reads or writes
provider reads or provider write-back
Moxfield/Archidekt/Hareruya/Cockatrice mutation
external publication, sync, cloud delivery, or sharing
LLM/model calls
recommendation generation
simulation execution
Theory ingestion or promotion
Rules authority mutation
Correction activation
Stream Deck adapter implementation
workflow automation
dependency additions
active-scope edits
```

## Planning guardrails

Future packet models must keep these concepts visibly separate:

- measured evidence, reviewed Theory, Rules authority, Corrections, user
  preferences, examples, simulations, and recommendations;
- confidence and source agreement;
- current and stale snapshots;
- blocked, omitted, redacted, unavailable, and successful states;
- render planning and file writing;
- user confirmation and supplemental navigation.

All planned models must be local-first, deterministic, serializable, and
testable without network access, external applications, live providers, a UI
runtime, or model APIs.

## Accessibility and privacy planning requirements

Phase 43J must require packet fields or error states sufficient to test:

- keyboard and screen-reader equivalent status;
- non-color-only warnings and errors;
- focus-safe blocking states;
- reduced-motion compatibility;
- redaction labels visible to assistive technology;
- explicit privacy-blocked states;
- secret/token/credential exclusion;
- no hidden export of private decks, notes, conversations, experiments,
  corrections, prompts, traces, or Theory excerpts.

## Adversarial planning requirements

Phase 43J must include adversarial test obligations for:

- unreviewed Theory presented as authority;
- Hareruya reused outside tournament provenance;
- Stream Deck confirmation or consent;
- provider write-back requests;
- path/write authority smuggled into render/export metadata;
- stale snapshots presented as current;
- missing evidence upgraded into a stronger substitute;
- collision/overwrite or receipt semantics claimed before the safe writer exists.

## Validation tuple

```text
phase_id: Phase43I
phase_part: planning
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase43J
next_phase_part: implementation-contract
next_gate_scope: INTERMEDIATE_PACKET
```

