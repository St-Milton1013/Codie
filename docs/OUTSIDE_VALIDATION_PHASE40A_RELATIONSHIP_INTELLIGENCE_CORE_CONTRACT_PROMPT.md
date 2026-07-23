# Outside Validation Prompt - Phase 40A Relationship Intelligence Core Contract

Validate Phase 40A as a contract-only packet.

Return one of:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Only PASS or PASS WITH REVIEW NOTES may unblock Phase 40B.

## Required Review Files

```text
docs/PHASE40A_RELATIONSHIP_INTELLIGENCE_CORE_CONTRACT.md
docs/CHECKPOINT_PHASE40A_RELATIONSHIP_INTELLIGENCE_CORE_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE40A_RELATIONSHIP_INTELLIGENCE_CORE_CONTRACT_PROMPT.md
docs/CODIE_V2_CONSTITUTION.md
docs/ROADMAP_PATCH_V2_INTELLIGENCE_PROGRAM_INTAKE.md
docs/design_inputs/v2_intelligence_program/README.md
docs/design_inputs/v2_intelligence_program/CODIE_V2_RELATIONSHIP_INTELLIGENCE_PROPOSAL.md
docs/PHASE39D_COCKATRICE_INTEROPERABILITY_CHECKPOINT_CONTRACT.md
docs/CHECKPOINT_PHASE39D_COCKATRICE_INTEROPERABILITY_CHECKPOINT_REPORT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

## Required Checks

Confirm:

```text
Phase 40A is contract-only
Phase 39D is recorded as artifact-backed PASS
Phase 39D run ID, target SHA, artifact, and validator results match
Phase 40A declares phase_id, phase_part, and gate_scope
Phase 40A declares next_phase_id, next_phase_part, and next_gate_scope
Phase 40B remains blocked
active validation scope was not modified by the PR
Constitution V2 Section 17 is the governing authority
the design proposal remains non-authoritative
```

Confirm the contract preserves:

```text
Relationship Intelligence as Class 2 measured evidence
typed relationship and evidence-class separation
canonical population manifests
present, absent, and unknown endpoint states
N, nA, nB, and nAB
observed and expected co-occurrence
support
directional confidence A->B and B->A
dependence delta A->B as P(B|A) - P(B)
dependence delta B->A as P(A|B) - P(A)
lift
leverage
population Jaccard
PMI as log2(lift)
visible undefined reasons
no additive smoothing
population filters and deduplication policy
coverage and low-sample caveats
source lineage and metric versions
deterministic reproducibility
```

Confirm the contract distinguishes:

```text
measured co-occurrence
Tagger ontology membership
Spellbook combo membership
rules interactions
curated package membership
theory attribution
```

Confirm it does not authorize:

```text
production code
implementation tests or fixtures
schema or migrations
repositories or SQL
provider or raw source reads
metric calculation
population resolution
Evidence Fusion integration
Decision Intelligence output
Tournament Exposure
Jin or Theory Corpus behavior
UI, CLI, or file writing
LLM or live network calls
dependencies
validator or workflow changes
active validation scope changes
constitution changes
```

Reject if the contract:

```text
uses the proposal's conditional-comparison delta as dependence_delta
uses natural-log PMI
collapses metrics into an opaque score
allows causal or strategic claims
allows recommendations
treats unknown as absent
silently smooths zero joint counts
allows user decks into global evidence populations
confuses measured and structural relationships
allows Phase 40B implementation before Phase 40A acceptance
```

## Required Commands

```text
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -v
```

## Final Gate

```text
Phase 40A must merge before its protected active-scope transition.
Phase 40A must receive artifact-backed phase-ledger PASS or PASS WITH REVIEW NOTES.
Phase 40B remains blocked until then.
```
