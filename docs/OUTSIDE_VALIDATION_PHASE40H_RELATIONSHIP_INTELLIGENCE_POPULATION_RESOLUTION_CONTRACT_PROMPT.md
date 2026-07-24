# Outside Validation - Phase 40H Relationship Intelligence Population Resolution Contract

Validate the exact PR head from a clean checkout.

## Review Files

```text
docs/PHASE40H_RELATIONSHIP_INTELLIGENCE_POPULATION_RESOLUTION_CONTRACT.md
docs/CHECKPOINT_PHASE40H_RELATIONSHIP_INTELLIGENCE_POPULATION_RESOLUTION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE40H_RELATIONSHIP_INTELLIGENCE_POPULATION_RESOLUTION_CONTRACT_PROMPT.md
docs/PHASE40G_RELATIONSHIP_INTELLIGENCE_METRIC_CALCULATION_IMPLEMENTATION_REPORT.md
docs/PHASE40F_RELATIONSHIP_INTELLIGENCE_METRIC_CALCULATION_IMPLEMENTATION_CONTRACT.md
docs/PHASE40E_RELATIONSHIP_INTELLIGENCE_METRIC_CALCULATION_CONTRACT.md
docs/PHASE40A_RELATIONSHIP_INTELLIGENCE_CORE_CONTRACT.md
codie/analytics/relationship_metrics.py
docs/CODIE_V2_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Confirm Phase 40H:

```text
is contract-only
defines deterministic canonical population membership and manifest identity
requires explicit stable deduplication and visible duplicate counts
preserves every exclusion reason
excludes inactive records by default
counts endpoint presence once per usable deck
keeps sideboard and auxiliary objects out by default
preserves sample size, coverage, provenance, caveats, and caller timestamp
keeps zero, unavailable, unsupported, excluded, and deduplicated states distinct
excludes private user decks from global evidence without approved-observation status
uses already-built canonical tag assignments and never calls Tagger
rejects direct card-to-tag measurement without an accepted anti-tautology rule
emits the existing RelationshipCountPacket shape without calculating metrics
remains measured-evidence-only
does not implement code, tests, fixtures, schema, repositories, providers,
metrics, recommendations, Jin, Tournament Exposure, simulator behavior, UI,
LLM, network, file-writing, workflow, dependency, active-scope, or
constitutional changes
records an explicit Phase40H to Phase40I validation tuple
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

Phase 40I remains blocked until PASS or PASS WITH REVIEW NOTES.
