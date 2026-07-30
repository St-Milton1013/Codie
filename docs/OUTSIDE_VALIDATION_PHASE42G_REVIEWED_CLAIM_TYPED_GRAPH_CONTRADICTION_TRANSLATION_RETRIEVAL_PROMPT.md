# Outside Validation - Phase 42G Reviewed Claim, Typed Graph, Contradiction, Translation, and Retrieval

Validate Phase 42G from a clean checkout of the exact submitted commit.

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
docs/CHECKPOINT_PHASE42G_REVIEWED_CLAIM_TYPED_GRAPH_CONTRADICTION_TRANSLATION_RETRIEVAL_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE42G_REVIEWED_CLAIM_TYPED_GRAPH_CONTRADICTION_TRANSLATION_RETRIEVAL_PROMPT.md
docs/design_inputs/v2_intelligence_program/CODIE_V2_THEORY_CORPUS_ATTRIBUTED_KNOWLEDGE_GRAPH_PROPOSAL.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

Treat the constitution and accepted contracts as authority. Treat the Theory
Corpus proposal as preserved design input only.

## Confirm Scope

Confirm Phase 42G:

```text
is contract-only
records Phase 42F artifact-backed acceptance
defines Phase42G / outside-validation / INTERMEDIATE_PACKET
defines Phase42H / outside-validation / INTERMEDIATE_PACKET as next
keeps Phase 42H blocked
changes no active validation scope in the PR
```

Reject implementation code, tests, fixtures, schema, migrations, repositories,
graph databases, source acquisition, extraction, embeddings, contradiction
scanning, translation engines, retrieval ranking, models, Jin, curriculum,
providers, UI, CLI, API, exports, file writing, network calls, dependencies,
workflows, or constitution changes.

## Confirm Claim And Graph Rules

Confirm:

```text
approved claims require accepted source versions and exact anchors
claims are atomic and preserve source modality
claim labels remain distinct
discovery material cannot support DIRECT_THEORY
Jin inference cannot become attributed source theory
definitions remain source-specific
normalized concepts do not blend definitions
substantive edges are typed, sourced, scoped, reviewed, and versioned
untyped substantive RELATED_TO edges are prohibited
attribution roles remain distinct
earliest local source does not automatically establish originator
```

## Confirm Translation And Contradiction Rules

Confirm:

```text
approval does not imply target-format transferability
historical or cross-format theory requires reviewed translation for full automatic routing
translations preserve changed assumptions and limitations
Rules conflicts block affected applications
disagreements remain typed and visible
author count, fame, popularity, and prestige cannot resolve disagreement
primary source outranks synthesis for attribution, not strategic correctness
empirical support remains scoped to population, time, metric, sample, and coverage
theory remains distinct from measured evidence
```

## Confirm Release And Retrieval Rules

Confirm:

```text
graph releases are immutable, versioned, and deterministic
claim corrections create new versions rather than silent mutation
retrieval uses only eligible reviewed graph members
rights, privacy, format, scope, and limitation gates apply before assembly
known material contradictions remain visible
duplicate restatements preserve attribution chains
ordering cannot use fame or popularity
retrieval packets preserve inclusions, exclusions, sources, limitations, and disagreements
retrieval packets are ephemeral and cannot mutate graph or evidence state
insufficient coverage produces explicit abstention
retrieval does not generate recommendations
```

## Confirm Cross-System Boundaries

Confirm Phase 42C remains Rules authority, Phase 42D controls all model and
cloud routes, Phase 42E corrections remain separately attributed, Phase 42F
controls source and rights eligibility, and Decision Intelligence remains the
only recommendation-producing layer.

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
correction. Phase 42H remains blocked unless the result is PASS or PASS WITH
REVIEW NOTES.
