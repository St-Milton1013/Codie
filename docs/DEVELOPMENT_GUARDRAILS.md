# Development Guardrails

Status: active developer workflow guidance

This document records local development tools added to reduce drift as Codie grows.

## Task Runner

Use the PowerShell task runner from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\dev.ps1 validate
```

`validate` runs:

```text
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests
```

Other tasks:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\dev.ps1 schema
powershell -ExecutionPolicy Bypass -File scripts\dev.ps1 test
powershell -ExecutionPolicy Bypass -File scripts\dev.ps1 test-verbose
powershell -ExecutionPolicy Bypass -File scripts\dev.ps1 lint
powershell -ExecutionPolicy Bypass -File scripts\dev.ps1 format
powershell -ExecutionPolicy Bypass -File scripts\dev.ps1 typecheck
powershell -ExecutionPolicy Bypass -File scripts\dev.ps1 precommit
```

Direct `.\scripts\dev.ps1` execution may be blocked by Windows execution policy. Use the `-ExecutionPolicy Bypass -File` form above.

## Dev Dependencies

Runtime dependencies remain in `requirements.txt`.

Developer-only tools are listed in:

```text
requirements-dev.txt
```

Install them with:

```powershell
python -m pip install -r requirements-dev.txt
```

## Ruff, Mypy, And Pre-Commit

Configuration files:

```text
pyproject.toml
.pre-commit-config.yaml
```

These tools are guardrails. They do not replace the authoritative release gate:

```text
python -m unittest discover -s tests
```

## Schema Guardrail

The schema guardrail verifies:

```text
all codie/db/schema/*.sql files are listed in codie.db.bootstrap.SCHEMA_ORDER
SCHEMA_ORDER has not changed without updating the guardrail
the complete schema bootstraps into an in-memory SQLite database
```

Run it directly:

```powershell
python scripts/check_schema.py
```

It is also covered by:

```text
tests/test_schema_bootstrap_guardrails.py
```

## Architecture Decision Records

Durable architecture decisions live under:

```text
docs/adr/
```

ADRs are governance records. They do not authorize new implementation scope by themselves.
