# Phase 43D Jin Conversation and Evidence Inspection Contract

## Validation tuple

```text
phase_id: Phase43D
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase43E
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 43E is reserved for the Staged Experiment and Correction Workflow Contract and remains blocked until Phase 43D outside validation passes.

## Status and authority

```text
document_type: contract-only packet
implementation_authorized: no
schema_authorized: no
UI_authorized: no
API_authorized: no
model_execution_authorized: no
persistence_authorized: no
active_scope_base: 8ad6810b8c4a3953f139ba81d9f9dd2b4be40d9b
```

This packet defines how already-finalized Jin answer packets and their evidence links may be presented and inspected. It does not authorize prompting, retrieval, model execution, answer generation, conversation persistence, or writes.

## Placement and non-obstruction

Jin is a separate discussion region in the Analysis Workspace. It may be docked or opened as an accessible drawer, but it must not cover the active Decision Evidence Panel or remove substantive evidence. Narrow layouts may collapse Jin while retaining explicit reopen and binding status.

## Thread binding and staleness

Every substantive thread is bound to stable identities:

```text
deck_snapshot_id
analysis_run_id
optional_decision_id
analysis_profile_id
weight_profile_id
theory_retrieval_version
query_plan_id
answer_packet_id
```

A snapshot, run, profile, corpus, policy, or evidence-version change makes the prior thread historical or stale. The interface may preserve inspection of the old thread but cannot silently treat it as current, rebind it, or transplant conclusions to a new deck state.

## Final answer presentation

A Jin answer card presents only the accepted Phase 42I final answer packet and retains:

- direct answer and bounded claim type;
- evidence level and content-class labels;
- speculation label and confidence ceiling;
- legality result and assumptions;
- contradictions, unresolved questions, and abstention reasons;
- snapshot, analysis run, query plan, policy, model-profile, corpus, and packet versions;
- links to exact evidence, simulation, rules, correction, reviewed Theory, and decision records.

Draft writer output, auditor notes, hidden chain-of-thought, internal prompts, and discarded candidates are not user-facing evidence.

## Evidence inspection

Selecting an evidence link navigates to the exact immutable Phase 43A projection or Phase 43C panel section identified by the answer packet. Inspection preserves source identity, observation time, version, content class, confidence, coverage, conflicts, caveats, rights state, redaction state, and replay identity.

The conversation surface cannot fabricate a missing target, summarize a link as stronger than its source, merge incompatible evidence versions, or convert an inference, Theory claim, community item, correction, or user preference into measured evidence.

## Conversation boundaries

The surface may display user questions, finalized answers, follow-up affordances, citations, and navigation. It may not:

- alter evidence weights or recommendation confidence;
- resolve conflicts, rules, legality, or corrections;
- stage or apply a deck edit without a separately governed explicit action;
- create or persist a recommendation, experiment, correction, Theory claim, or user context;
- canonicalize data, run analytics or simulations, fetch sources, or rerun Jin;
- imply that conversational fluency is authority.

A future follow-up request must enter the accepted Phase 42H planning and Phase 42I finalization gates as a new governed request. UI continuity cannot bypass those gates.

## Theory, Rules, Corrections, and Hareruya

Reviewed Theory remains a separate explanatory lens with author, work, immutable version, citation, rights class, transferability, contradiction, and review state. Disagreements remain visible. Theory cannot occupy the primary evidence or recommendation header and receives no hidden author bonus.

Rules and legality retain their accepted authority versions and unsupported states. Corrections retain scope, authority ceiling, review state, and conflicts. Conversation cannot activate or broaden either.

Hareruya may appear only through evidence links to canonicalized tournament, event, or deck observations. It cannot become a Theory, rules, correction, curriculum, user-context, or conversational-authority source.

## Local-first privacy and routing disclosure

- The required Jin inspection experience remains available on the local path.
- Private questions, decks, notes, corrections, experiments, and Theory excerpts remain local by default.
- Any separately approved remote route requires informed consent, pre-route redaction, route/model disclosure, and retained local fallback.
- The visible answer identifies whether it was produced locally or through an approved remote exception and which redactions applied.
- Cross-user or cross-profile thread leakage is prohibited.

## Proposed actions and writes

Jin may display a proposal already present in an accepted answer packet, including an experiment proposal, correction candidate, deck-specific hypothesis, structured comparison, or Theory note. Display is not activation. Any write must enter the separately accepted Phase 42J confirmation and authority path; Phase 43E will define presentation of that staged workflow.

## Stream Deck boundary

Stream Deck remains optional and supplemental-only. A future adapter may navigate to Jin, repeat a finalized answer, or open an existing evidence link. It cannot submit prompts, select answers, confirm writes, mark evidence reviewed, resolve conflicts, bypass consent or legality gates, or perform live-game tracking.

## Accessibility and deterministic behavior

- Questions and answers use semantic headings and ordered conversation structure.
- Evidence links have meaningful accessible names and move focus to the referenced heading.
- Opening/closing Jin restores logical focus and background updates do not steal it.
- Content class, confidence, contradiction, legality, staleness, and privacy state do not rely on color alone.
- The same finalized packet and projection set produce the same visible answer, ordering, binding labels, and link targets.
- Missing, stale, redacted, blocked, unavailable, superseded, and error states are explicit.

## Acceptance criteria

1. Conversation presentation consumes finalized answer packets only.
2. Threads retain exact snapshot, run, decision, profile, corpus, plan, and packet identity.
3. Stale threads remain historical and are never silently rebound.
4. Evidence links resolve to exact immutable projections with preserved classes and provenance.
5. Drafts, prompts, chain-of-thought, and discarded candidates are not exposed as evidence.
6. Conversation performs no retrieval, model execution, calculation, resolution, or write.
7. New follow-ups must re-enter Phase 42H/42I gates.
8. Local-first privacy, consent, routing disclosure, and redaction remain mandatory.
9. Reviewed Theory, Rules, and Correction gates remain intact.
10. Hareruya remains tournament-only.
11. Stream Deck remains supplemental-only.
12. Phase 43E remains blocked.

## Explicit exclusions

No code, schema, packet class, component, renderer, route, API, persistence, prompt, retrieval, model call, answer generation, calculation, simulation, recommendation, experiment/correction write, export, mobile surface, Stream Deck adapter, dependency, workflow, or active-scope edit is authorized.
