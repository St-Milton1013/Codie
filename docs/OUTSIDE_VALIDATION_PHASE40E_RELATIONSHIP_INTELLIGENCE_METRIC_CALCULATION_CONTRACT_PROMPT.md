# Outside Validation - Phase 40E Relationship Intelligence Metric Calculation Contract

Validate the exact PR head from a clean checkout.

Confirm:

```text
Phase 40D acceptance evidence is exact
Phase40E and Phase40F tuples are explicit
Phase 40E is documentation-only
all formulas exactly match Phase 40A
PMI uses log2
dependence delta uses conditional probability minus marginal probability
metrics remain separate
directional values emit both orientations
undefined values preserve null plus reason
zero, unavailable, unknown, and unsupported remain distinct
thresholds and coverage remain visible
the calculator consumes already-counted packets
no repository/provider/source reads or persistence are authorized
no recommendations, causal claims, Jin, Tournament Exposure, simulator, UI,
LLM, file writing, network, dependency, workflow, active-scope, or
constitution changes are authorized
```

Run:

```text
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -v
```

Return PASS, PASS WITH REVIEW NOTES, PASS WITH REQUIRED FIXES, or FAIL.
Phase 40F remains blocked until PASS or PASS WITH REVIEW NOTES.

