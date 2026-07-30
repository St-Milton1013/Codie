# Outside Validation - Phase 42F Theory Source Registry, Rights, Immutable Version, and Citation

Validate Phase 42F from a clean checkout of the exact submitted commit.

## Required Review Files

```text
docs/CODIE_V2_CONSTITUTION.md
docs/ROADMAP_PATCH_V2_INTELLIGENCE_PROGRAM_INTAKE.md
docs/PHASE42A_JIN_THEORY_RULES_CORRECTIONS_CROSS_SPECIFICATION_BOUNDARY_CONTRACT.md
docs/PHASE42D_LOCAL_FIRST_MODEL_PROFILE_REDACTION_CONSENT_ROUTING_CONTRACT.md
docs/PHASE42E_MINIMAL_USER_CORRECTION_LEDGER_CORE_CONTRACT.md
docs/PHASE42F_THEORY_SOURCE_REGISTRY_RIGHTS_IMMUTABLE_VERSION_CITATION_CONTRACT.md
docs/CHECKPOINT_PHASE42F_THEORY_SOURCE_REGISTRY_RIGHTS_IMMUTABLE_VERSION_CITATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE42F_THEORY_SOURCE_REGISTRY_RIGHTS_IMMUTABLE_VERSION_CITATION_PROMPT.md
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

Confirm Phase 42F:

```text
is contract-only
records Phase 42E artifact-backed acceptance
defines Phase42F / outside-validation / INTERMEDIATE_PACKET
defines Phase42G / outside-validation / INTERMEDIATE_PACKET as next
keeps Phase 42G blocked
changes no active validation scope in the PR
```

Reject implementation code, tests, fixtures, schema, migrations, repositories,
source acquisition, scraping, transcription, embeddings, claims, graph work,
retrieval, models, Jin, curriculum, providers, UI, CLI, exports, file writing,
network calls, dependencies, workflows, or constitution changes.

## Confirm Source And Rights Rules

Confirm:

```text
theory remains context rather than authority or measured evidence
authors remain provenance subjects rather than truth scores
source type and source role remain separate
work, edition, asset, version, segment, and anchor identity remain distinct
uncertain people and works remain separate
storage, processing, indexing, quotation, export, cloud, and retention rights are independent
unknown rights are metadata-only and fail closed
user possession is not redistribution permission
private licensed content remains local by default
community and discovery items remain candidates by default
```

## Confirm Version And Citation Rules

Confirm:

```text
source versions are immutable and content-hashed
revisions create new versions rather than silent mutation
transcript provenance and speaker identity remain visible
every future approved claim requires an exact anchor
media anchors use timestamps and speakers
forum anchors use post or comment paths
paraphrases retain the underlying anchor
quotation state obeys the rights profile
small excerpts cannot reconstruct restricted works
takedown blocks new use without erasing historical identity
```

## Confirm Boundaries

Confirm Rules material stays under Phase 42C authority, Phase 42D controls all
model/cloud transmission, Phase 42E corrections do not become theory claims,
and no Theory record becomes a recommendation.

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
correction. Phase 42G remains blocked unless the result is PASS or PASS WITH
REVIEW NOTES.
