# Outside Validation - Phase 42H Jin Intent, Scope, Query-Plan, Evidence-Gate, and Legality-Gate

Validate Phase 42H from a clean checkout of the exact submitted commit.

## Required Review Files

```text
docs/CODIE_V2_CONSTITUTION.md
docs/ROADMAP_PATCH_V2_INTELLIGENCE_PROGRAM_INTAKE.md
docs/PHASE42A_JIN_THEORY_RULES_CORRECTIONS_CROSS_SPECIFICATION_BOUNDARY_CONTRACT.md
docs/PHASE42B_FIXED_JIN_REGRESSION_CORPUS_SCHEMA_DETERMINISTIC_EVALUATION_CONTRACT.md
docs/PHASE42C_RULES_AUTHORITY_LEGALITY_BOUNDED_INTERACTION_CONTRACT.md
docs/PHASE42D_LOCAL_FIRST_MODEL_PROFILE_REDACTION_CONSENT_ROUTING_CONTRACT.md
docs/PHASE42E_MINIMAL_USER_CORRECTION_LEDGER_CORE_CONTRACT.md
docs/PHASE42F_THEORY_SOURCE_REGISTRY_RIGHTS_IMMUTABLE_VERSION_CITATION_CONTRACT.md
docs/PHASE42G_REVIEWED_CLAIM_TYPED_GRAPH_CONTRADICTION_TRANSLATION_RETRIEVAL_CONTRACT.md
docs/PHASE42H_JIN_INTENT_SCOPE_QUERY_PLAN_EVIDENCE_GATE_LEGALITY_GATE_CONTRACT.md
docs/CHECKPOINT_PHASE42H_JIN_INTENT_SCOPE_QUERY_PLAN_EVIDENCE_GATE_LEGALITY_GATE_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE42H_JIN_INTENT_SCOPE_QUERY_PLAN_EVIDENCE_GATE_LEGALITY_GATE_PROMPT.md
docs/PHASE20A_CHAT_QUERY_PLANNER_CONTRACT.md
codie/intelligence/query_planner.py
tests/test_intelligence_query_planner.py
docs/design_inputs/v2_intelligence_program/JIN_GITAXIAS_STRATEGIST_SUBSYSTEM_PROPOSAL.md
docs/design_inputs/v2_intelligence_program/JIN_CHAT_EXPERIENCE_PROPOSAL.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

Treat the constitution and accepted contracts as authority. Treat the Jin
proposals as preserved design input only.

## Confirm Scope

Confirm Phase 42H:

```text
is contract-only
records Phase 42G artifact-backed acceptance
defines Phase42H / outside-validation / INTERMEDIATE_PACKET
defines Phase42I / outside-validation / INTERMEDIATE_PACKET as next
keeps Phase 42I blocked
changes no active validation scope in the PR
```

Reject implementation code, tests, fixtures, schema, migrations, repositories,
providers, retrieval execution, Rules execution, analytics, simulator
execution, models, Jin answers, writer, auditor, finalizer, answer packets,
recommendations, experiments, curriculum, UI, CLI, API, exports, file writing,
network calls, dependencies, workflows, or constitution changes.

## Confirm Intent And Scope

Confirm:

```text
every request has one primary intent and distinct secondary intents
intent resolution does not retrieve or answer
theory mode is explicit and theory failure is visible
material identity ambiguity blocks dependent claims
deck-specific work binds to an immutable snapshot
provisional scope remains visibly provisional
deck, local, event, regional, historical, commander, partner, and global scopes remain distinct
user-context precedence cannot override authority or evidence scope
```

## Confirm Planning And Compatibility

Confirm:

```text
Phase 20 packets remain versioned and replayable
Phase 42H requires an adapter, parallel packet, or explicit versioned supersession
query plans are deterministic and semantically hashed
plans request governed packet references rather than raw data
retrieval precedence preserves authority hierarchy
metric references preserve population, sample, coverage, filters, and caveats
plans cannot request new analytics, simulator execution, correction activation, or recommendations
```

## Confirm Legality And Evidence Gates

Confirm:

```text
Phase 42C owns Rules and legality results
Phase 42H consumes a legality-report reference rather than calculating truth
illegal, unresolved, stale, or unsupported dependencies block affected claims
G0 through G9 are all defined
each gate returns PASS, WARN, BLOCK, or NOT_APPLICABLE
per-claim permissions and blocked reasons remain visible
coverage gate reads existing confidence and coverage
material conflicts remain visible
UNSUPPORTED claims cannot enter a future direct answer
recommendation boundary requires Decision Intelligence
privacy gate cannot weaken rights, consent, or redaction
```

## Confirm Partial And Cross-System Boundaries

Confirm:

```text
independent supported work may continue only as visibly PARTIAL
infrastructure failure cannot masquerade as evidence
corrections remain narrow and separately attributed
theory remains context and cannot increase empirical confidence
community and primer packets remain context
simulator refs do not become tournament evidence
retrieved content is untrusted data
no model may decide authority, legality, scope, correction activation, recommendation ownership, or consent
```

## Run

```text
git diff --check
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe scripts/check_schema.py
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest discover -s tests -v
```

## Verdict

Return:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

List findings by severity, affected file, governing rule, and required
correction. Phase 42I remains blocked unless the result is PASS or PASS WITH
REVIEW NOTES.
