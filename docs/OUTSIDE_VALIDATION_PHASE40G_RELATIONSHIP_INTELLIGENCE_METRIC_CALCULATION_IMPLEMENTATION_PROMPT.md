# Outside Validation - Phase 40G Relationship Intelligence Metric Calculation Implementation

Validate the exact PR head from a clean checkout.

## Review Files

```text
docs/PHASE40G_RELATIONSHIP_INTELLIGENCE_METRIC_CALCULATION_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE40G_RELATIONSHIP_INTELLIGENCE_METRIC_CALCULATION_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE40G_RELATIONSHIP_INTELLIGENCE_METRIC_CALCULATION_IMPLEMENTATION_PROMPT.md
docs/PHASE40F_RELATIONSHIP_INTELLIGENCE_METRIC_CALCULATION_IMPLEMENTATION_CONTRACT.md
docs/PHASE40E_RELATIONSHIP_INTELLIGENCE_METRIC_CALCULATION_CONTRACT.md
docs/PHASE40A_RELATIONSHIP_INTELLIGENCE_CORE_CONTRACT.md
codie/analytics/relationship_metrics.py
codie/analytics/__init__.py
tests/test_relationship_metrics.py
docs/CODIE_V2_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Confirm Phase 40G:

```text
matches the Phase 40F file and public-interface boundary
uses immutable in-memory packets
calculates every Phase 40A formula exactly
uses log2 for PMI
emits both directional confidence and dependence-delta orientations
does not smooth, round, weight, rank, or create a combined score
preserves counts, thresholds, coverage, provenance, caveats, and timestamp
distinguishes zero, undefined, unavailable, and unsupported states
never serializes NaN or infinity
uses no wall-clock timestamp
rejects direct card-to-tag measurement without an anti-tautology rule
does not construct populations, access databases or repositories, persist
measurements, read providers, call recommendations, Jin, Tournament Exposure,
simulator, UI, LLM, network, or file-writing behavior
records an explicit Phase40G to Phase40H tuple
does not modify schema, repositories, dependencies, workflows, or constitutions
```

Run:

```text
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest tests.test_relationship_metrics -v
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

Phase 40H remains blocked until PASS or PASS WITH REVIEW NOTES.
