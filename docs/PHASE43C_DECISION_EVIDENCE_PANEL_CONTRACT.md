# Phase 43C Decision Evidence Panel Contract

## Validation tuple

```text
phase_id: Phase43C
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase43D
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 43D is reserved for the Jin Conversation and Evidence Inspection Contract and remains blocked until Phase 43C outside validation passes.

## Status and authority

```text
document_type: contract-only packet
implementation_authorized: no
schema_authorized: no
UI_authorized: no
API_authorized: no
persistence_authorized: no
active_scope_base: cc73ca5ced61d14d078b0219d43f859c6c2f1a7c
```

The Decision Evidence Panel is one expandable explanation surface for one already-produced decision packet at a time. It presents conclusions and their support without calculating, rewriting, combining, or authorizing them.

## Required visible summary

The default panel retains decision, subject, deck snapshot, analysis run, analysis/weight profiles and versions, observed concern, bounded conclusion, candidate action, expected impact, primary tradeoff, confidence and ceiling, source agreement, legality, material conflicts, caveats, staleness, and status.

The panel cannot hide a material conflict, legality block, privacy block, unsupported state, or confidence ceiling behind an optional drawer.

## Expandable explanation sections

The panel may expose immutable Phase 43A projections for replacement logic; evidence contributions with raw observation, method, selected weight, direction, sample size, coverage, confidence, and provenance; simulation references and limits; conflicts; caveats; replay identity; reproducibility; and links to separately governed Jin or experiment workflows.

The panel does not combine unrelated findings into a synthetic score. It does not calculate weights, normalize evidence, run simulations, resolve conflicts, determine legality, produce recommendations, or generate Jin answers.

## Confidence, agreement, and legality

Confidence describes reliability under the declared model. Source agreement describes concurrence among eligible sources. Neither substitutes for the other. Numeric confidence remains hidden unless calibrated, documented, and interpretable. Class 0 authority is not counted as one vote among community or Theory sources.

Legality states are `VALIDATED`, `VALIDATED_WITH_ASSUMPTIONS`, `UNRESOLVED`, `INVALID`, or `NOT_APPLICABLE`. Invalid or unresolved decisions cannot expose an action their governing contract forbids. The panel may navigate to a separately approved confirmation surface; it cannot confirm or execute an action.

## Replacement and contribution integrity

Replacement comparison retains current/candidate identity, preserved, gained, lost, changed, and unknown dimensions, package/combo/tag effects, mana and cost effects, matchup effects, and simulator coverage. Matching one label is not sufficient evidence of functional equivalence.

Each contribution retains its content class. Tournament observations, regional evidence, functional measurements, simulations, reviewed Theory, user context, and authority records remain visibly distinct. Selected weights are accepted profile inputs, not chosen by the panel.

## Theory, Rules, Corrections, and Hareruya

Reviewed Theory is a labeled explanatory contribution with author, work, immutable version, citation, rights class, transferability, contradiction, and review state. It never becomes measured evidence or hidden authority. Rules and legality retain authority version, assumptions, and unsupported states. Corrections retain scope, authority ceiling, review state, and conflicts.

Hareruya may appear only as provenance for canonicalized tournament, event, or deck observations. It cannot supply Theory, rules, curriculum, corrections, user context, or recommendation authority.

## Local-first privacy boundary

- The complete panel remains available on the local path.
- Private decks, notes, corrections, experiments, conversations, and Theory excerpts remain local by default.
- Redaction occurs before a separately approved boundary crossing.
- Privacy-blocked content is labeled and omitted, not replaced with fabricated or weaker evidence.
- Export, sharing, telemetry, synchronization, and remote rendering remain outside this packet.

## Jin, experiments, and Stream Deck

Jin links carry explicit decision, snapshot, run, evidence, and Theory identities but do not authorize conversation execution. Experiment links may open a separately governed confirmation workflow; the panel cannot create or commit it.

Stream Deck remains optional and supplemental-only. It may later request navigation to an existing decision or action surface. It cannot choose evidence, alter weights, answer Jin prompts, confirm writes, dismiss conflicts, bypass legality/privacy gates, or perform live-game tracking.

## Accessibility, ordering, and failure behavior

- One decision heading anchors focus and semantic structure.
- Sections and controls are keyboard operable with correct expanded state.
- Severity, confidence, agreement, content class, conflict, caveat, and legality do not rely on color alone.
- Ordering is deterministic for the same immutable packet.
- Loading, empty, stale, partial, unsupported, superseded, historical, privacy-blocked, and error states are explicit.
- Optional subsystem failure does not erase available evidence.

## Acceptance criteria

1. One immutable decision packet is presented at a time.
2. Identity, snapshot, run, profile, version, and status stay visible.
3. Confidence, agreement, legality, conflict, and caveat remain distinct.
4. Contributions preserve observation, method, weight, uncertainty, class, and provenance.
5. Material conflicts and blocking states cannot be hidden.
6. The panel performs no domain calculation, conflict resolution, or write.
7. Local-first privacy and pre-boundary redaction remain mandatory.
8. Reviewed Theory, Rules, and Correction gates remain intact.
9. Hareruya remains tournament-only.
10. Stream Deck remains supplemental-only.
11. Accessibility and deterministic failure states are required.
12. Phase 43D remains blocked.

## Explicit exclusions

No code, schema, packet class, component, renderer, route, API, persistence, calculation, normalization, simulation, recommendation, Jin execution, experiment write, export, mobile surface, Stream Deck adapter, dependency, workflow, or active-scope edit is authorized.
