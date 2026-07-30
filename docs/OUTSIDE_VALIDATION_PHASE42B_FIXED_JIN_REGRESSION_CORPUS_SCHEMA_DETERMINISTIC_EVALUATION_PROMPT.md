# Outside Validation - Phase 42B Fixed Jin Regression Corpus Schema and Deterministic Evaluation

Validate the exact PR head from a clean checkout.

## Review Files

```text
docs/PHASE42B_FIXED_JIN_REGRESSION_CORPUS_SCHEMA_DETERMINISTIC_EVALUATION_CONTRACT.md
docs/CHECKPOINT_PHASE42B_FIXED_JIN_REGRESSION_CORPUS_SCHEMA_DETERMINISTIC_EVALUATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE42B_FIXED_JIN_REGRESSION_CORPUS_SCHEMA_DETERMINISTIC_EVALUATION_PROMPT.md
docs/PHASE42A_JIN_THEORY_RULES_CORRECTIONS_CROSS_SPECIFICATION_BOUNDARY_CONTRACT.md
docs/CHECKPOINT_PHASE42A_JIN_THEORY_RULES_CORRECTIONS_CROSS_SPECIFICATION_BOUNDARY_REPORT.md
docs/CODIE_V2_CONSTITUTION.md
docs/ROADMAP_PATCH_V2_INTELLIGENCE_PROGRAM_INTAKE.md
docs/design_inputs/v2_intelligence_program/README.md
docs/design_inputs/v2_intelligence_program/CODIE_V2_FIXED_JIN_REGRESSION_CORPUS_PROPOSAL.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Confirm Phase 42B:

```text
is contract-only
records exact artifact-backed Phase 42A acceptance
defines immutable, versioned corpus releases
requires at least 104 v1 cases across thirteen required families
requires positive, negative, adversarial, scope-mutation, and
provenance/authority-mutation coverage in every family
defines deterministic manifest, case, fixture, assertion, result, and artifact fields
evaluates structured semantics rather than exact prose
allows no hidden state or undeclared fixtures
requires immutable fixture hashes and repository-contained relative paths
uses deterministic operators rather than LLM judging for release verdicts
preserves every repetition and assertion result
defines visible PASS, FAIL, unsupported, incomplete, and evaluator-error states
keeps fabricated citations, illegal output, authority misuse, unsupported
claims, class promotion, hidden contradictions, scope contamination, privacy
leaks, network attempts, overconfidence, false combo certification, false
tutor-pile certification, and protected mutation as hard failures
keeps model-backed Jin blocked until the corpus/evaluator implementation is
separately contracted, implemented, and accepted
treats artifacts as release evidence rather than production evidence
does not implement corpus files, fixtures, schemas, evaluator code, models,
prompts, Jin, Rules, corrections, Theory, UI, dependencies, workflows, active
scope, or constitution changes
records an explicit Phase42B to Phase42C validation tuple
keeps Phase 42C contract-only and blocked until Phase 42B acceptance
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

Phase 42C remains blocked until PASS or PASS WITH REVIEW NOTES.
