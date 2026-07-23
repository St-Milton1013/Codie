# Outside Validation - Phase 40D Relationship Intelligence Persistence

Validate the exact PR head and inspect the Phase 40A through 40D contracts,
reports, implementation files, tests, schema specification, and four active
governance ledgers.

Confirm:

```text
exactly five relationship persistence tables are added
AnalyticsRepository is the only repository owner
manifest and measurement identities are immutable
parent-child insertion is transactional
raw counts and undefined reasons remain visible
only approved metric names can be persisted
private user content cannot enter global population JSON
stable retrieval ordering is tested
schema bootstrap and SCHEMA_SPEC agree
no metric calculation, population construction, provider/source reads,
recommendations, Jin, Tournament Exposure, simulator, UI, LLM, network, or
file-writing behavior is introduced
Phase 40E remains blocked
```

Run:

```text
git diff --check
python scripts/check_schema.py
python -m unittest tests.test_repositories tests.test_schema -v
python -m unittest discover -s tests -v
```

Return PASS, PASS WITH REVIEW NOTES, PASS WITH REQUIRED FIXES, or FAIL.

