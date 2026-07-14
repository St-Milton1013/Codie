# Codie Local Validation Automation Contract

Status: Packet 1 contract before implementation

## Problem Solved

Codie needs a zero-cost, local-first validation gate that can be started from
GitHub Actions without using GitHub-hosted runners, paid APIs, API keys, or
cloud LLM services. The gate must validate the current Phase 35A outside
validation target, reject stale reports, preserve finding history, and produce
both machine-readable and human-readable output.

## Files Created And Modified

Created:

```text
.github/workflows/codie-local-validation.yml
codie/validation/local_gate.py
schemas/codie_validator_report_v1.schema.json
scripts/codie_validation_gate.py
tests/test_validation_local_gate.py
docs/CODIE_LOCAL_VALIDATION_AUTOMATION_CONTRACT.md
```

Modified:

```text
codie/validation/__init__.py
```

## Commands And Public Entry Points

Workflow:

```text
Codie Local Validation Gate
```

Manual dispatch inputs:

```text
phase_id
phase_part
gate_scope
pull_request_number
target_sha
```

Local command:

```powershell
& "C:\Users\Main\.venvs\codie-py312\Scripts\python.exe" scripts/codie_validation_gate.py --phase-id Phase35A --phase-part outside-validation --gate-scope INTERMEDIATE_PACKET --target-sha <sha>
```

Public Python entry points:

```text
codie.validation.local_gate.ValidationGateOptions
codie.validation.local_gate.run_validation_gate(...)
codie.validation.local_gate.aggregate_validator_reports(...)
codie.validation.local_gate.validate_report_payload(...)
codie.validation.local_gate.render_markdown_summary(...)
```

## Dependencies

No new third-party Python dependencies.

Runtime tools:

```text
git
python scripts/check_schema.py
python -m unittest discover -s tests -v
ollama
qwen2.5-coder:7b
llama3.1:latest
```

The GitHub workflow uses the existing local Python 3.12 interpreter:

```text
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe
```

## Schema Impact

No product schema impact. This packet does not modify Codie SQLite schema files,
repositories, migrations, provider records, canonical records, analytics tables,
or product data contracts.

It adds only a validation-report JSON Schema under `schemas/`.

## Tests

Packet 1 tests cover:

```text
valid clean reports
malformed JSON
schema violations
stale SHA
wrong phase
duplicate findings
contradictory findings
intermediate severity policy
final clean-pass policy
validator failure
Ollama unavailable
cost-policy violation
```

Full validation commands:

```powershell
git diff --check
& "C:\Users\Main\.venvs\codie-py312\Scripts\python.exe" scripts/check_schema.py
& "C:\Users\Main\.venvs\codie-py312\Scripts\python.exe" -m unittest discover -s tests -v
```

## Failure Modes

The gate reports:

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

Validator reports use:

```text
CLEAN_PASS
FAIL
ERROR
```

Finding severities use:

```text
BLOCKER
CRITICAL
HIGH
MEDIUM
LOW
INFORMATIONAL
```

## Security Boundaries

Validators are read-only.

Repository and PR text are untrusted input. Finding text is never interpolated
into shell commands.

The workflow refuses fork pull requests and runs only on a self-hosted Windows
runner with local validation labels.

The workflow does not use `OPENAI_API_KEY`, paid APIs, or GitHub-hosted runners.

The gate verifies repository, branch, phase, and SHA before producing a clean
result.

## Prohibited Scope

This packet must not:

```text
modify docs/CODIE_V1_CONSTITUTION.md
implement Phase 35B
advance Phase 35C
call paid APIs
use OPENAI_API_KEY
weaken validator policy
modify product schema
write product data
merge pull requests
run on GitHub-hosted runners
```
