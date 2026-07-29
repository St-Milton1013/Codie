# Outside Validation - Phase 40J Relationship Intelligence Population Resolution Implementation

Validate the exact PR head from a clean checkout.

## Review Files

```text
docs/PHASE40J_RELATIONSHIP_INTELLIGENCE_POPULATION_RESOLUTION_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE40J_RELATIONSHIP_INTELLIGENCE_POPULATION_RESOLUTION_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE40J_RELATIONSHIP_INTELLIGENCE_POPULATION_RESOLUTION_IMPLEMENTATION_PROMPT.md
docs/PHASE40I_RELATIONSHIP_INTELLIGENCE_POPULATION_RESOLUTION_IMPLEMENTATION_CONTRACT.md
docs/PHASE40H_RELATIONSHIP_INTELLIGENCE_POPULATION_RESOLUTION_CONTRACT.md
codie/analytics/relationship_population.py
codie/analytics/relationship_metrics.py
codie/analytics/__init__.py
tests/test_relationship_population.py
tests/test_relationship_metrics.py
docs/CODIE_V2_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Confirm Phase 40J:

```text
implements only the accepted pure population resolver
uses immutable JSON-compatible packets without caller mutation
derives stable semantic hashes without input order, current time, or randomness
uses stable canonical-snapshot deduplication and visible duplicate exclusions
excludes resolved, ignored-by-policy, private, and unapproved observations
allows private observations only when explicitly approved
counts endpoint presence once per usable deck
keeps sideboard and auxiliary card identities opt-in
matches card, tag, package, commander, and exact partner-pair endpoints
normalizes exact partner-pair order
uses already-built tag and package IDs
rejects unsupported endpoints and direct card-to-tag measurement
emits the existing validated RelationshipCountPacket
preserves population, exclusion, coverage, sample, provenance, caveat, and caller-time fields
keeps low-sample and low-coverage labels visible without changing counts
rejects unresolved identities and private metadata
remains measured-evidence-only
does not calculate relationship metrics
does not access schema, repositories, providers, raw source tables, persistence,
recommendations, Jin, Tournament Exposure, simulator, UI, LLM, network,
wall-clock, or file-writing behavior
records an explicit Phase40J to Phase40K validation tuple
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

Phase 40K remains blocked until PASS or PASS WITH REVIEW NOTES.
