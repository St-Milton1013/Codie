# Outside Validation - Phase 40I Relationship Intelligence Population Resolution Implementation Contract

Validate the exact PR head from a clean checkout.

## Review Files

```text
docs/PHASE40I_RELATIONSHIP_INTELLIGENCE_POPULATION_RESOLUTION_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE40I_RELATIONSHIP_INTELLIGENCE_POPULATION_RESOLUTION_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE40I_RELATIONSHIP_INTELLIGENCE_POPULATION_RESOLUTION_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE40H_RELATIONSHIP_INTELLIGENCE_POPULATION_RESOLUTION_CONTRACT.md
docs/PHASE40G_RELATIONSHIP_INTELLIGENCE_METRIC_CALCULATION_IMPLEMENTATION_REPORT.md
codie/analytics/relationship_metrics.py
docs/CODIE_V2_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Confirm Phase 40I:

```text
is implementation-contract-only
limits Phase 40J to one analytics module, one focused test file, and exports
defines immutable endpoint, deck-presence, spec, exclusion, manifest, and resolution packets
requires deterministic semantic manifest identity and input-order independence
requires stable explicit canonical-snapshot deduplication
excludes inactive, private, unapproved, and unresolved records visibly
counts endpoint presence once per usable deck
keeps sideboard and auxiliary identities opt-in
defines card, tag, package, commander, and exact partner-pair matching
requires already-built tag and package inputs
rejects direct card-to-tag measurement without an anti-tautology rule
emits the existing validated RelationshipCountPacket
preserves count, coverage, sample, provenance, caveat, and timestamp visibility
uses caller time and no wall clock
remains measured-evidence-only
does not authorize schema, repositories, providers, persistence, metrics,
recommendations, Jin, Tournament Exposure, simulator, UI, LLM, network,
file-writing, workflow, dependency, active-scope, or constitutional changes
records an explicit Phase40I to Phase40J validation tuple
```

Run:

```text
git diff --check
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe scripts/check_schema.py
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest discover -s tests -v
```

Allowed verdicts:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Phase 40J remains blocked until PASS or PASS WITH REVIEW NOTES.
