# Validator Report Format Guide

Schema:

```text
schemas/codie_validator_report_v1.schema.json
```

Validator result values:

```text
CLEAN_PASS
FAIL
ERROR
```

Finding severity values:

```text
BLOCKER
CRITICAL
HIGH
MEDIUM
LOW
INFORMATIONAL
```

Aggregator result values:

```text
CLEAN_PASS
REPAIR_REQUIRED
HUMAN_REVIEW_REQUIRED
VALIDATOR_ERROR
STALE_RESULTS
CONSTITUTION_CONFLICT
CODEX_USAGE_LIMIT
COST_POLICY_VIOLATION
```

User-facing reports include phase, phase part, PR number when supplied, commit
SHA, validation cycle, repair attempt, validator, severity, finding, affected
files, governing rule, required correction, repair performed, resolution status,
errors encountered during this phase, remaining open errors, and final result.
