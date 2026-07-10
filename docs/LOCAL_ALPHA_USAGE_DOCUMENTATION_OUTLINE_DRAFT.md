# Local Alpha Usage Documentation Outline

Status: draft only

This outline is preparation for Phase 30B. It is not the final alpha README.

## 1. What Codie Local Alpha Is

```text
Codie local alpha is a local evidence and report workflow for the accepted
architecture through Phase 29.
```

Include:

```text
evidence-first architecture
local-only validation
fixture-backed tests
report/export surfaces
explicit caveats
```

Avoid:

```text
claims of production readiness
claims of autonomous final recommendation generation
claims that SIM-R is implemented
claims that live broad ingestion is ready
```

## 2. Requirements

```text
Git
Python 3.12
PowerShell or shell
local repository checkout
optional local SQLite data depending on workflow
```

## 3. Setup

```powershell
cd "C:\Users\Main\Documents\Codex\2026-06-22\next-phase-contract-recommended-next-task"
python -m pip install -r requirements.txt
```

Use a generic clone path in public docs. Keep the local Windows path only in
handoff-oriented docs.

## 4. Validate

```powershell
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

Expected:

```text
Schema bootstrap check passed.
OK (skipped=1)
git diff --check exits cleanly
```

## 5. Supported Commands To Document

Document only commands that already exist and are accepted:

```text
recommendation output report rendering CLI
simulation review export CLI, if accepted usage docs already exist
deck memory CLI, if local DB prerequisites are clearly stated
share bundle / zip commands, if accepted usage docs already exist
```

Each command should include:

```text
purpose
input requirements
example command
expected output files
known failure modes
privacy note
```

## 6. Recommendation Output Report Example

Document:

```text
input is an already-built RecommendationOutputBundle JSON
CLI does not generate recommendations
CLI delegates to safe writer
JSON / Markdown / manifest output
output-root containment
overwrite rules
```

Do not imply:

```text
CLI discovers cards
CLI ranks cards
CLI chooses cuts
CLI creates recommendations
```

## 7. Known Caveats

```text
Hareruya WAF/access caveat
local database required for DB-backed workflows
fixture-first tests do not imply live provider backfill readiness
SIM-R deferred
mobile delivery optional and contract-gated
final UI not complete
roadmap patches are not alpha features
```

## 8. Troubleshooting

Include:

```text
Python not found
dependency install failed
schema check failed
test failure
missing local database
CLI missing required argument
unsafe output path rejected
unsupported output format
```

## 9. What To Send For Validation

```text
Phase 30A outside validation packet
test output
schema check output
git status
known caveats
```

## 10. Phase 30B Exit Criteria

```text
Local alpha docs are complete.
Supported command examples are accurate.
Validation commands pass.
Deferred features remain deferred.
Outside validation packet is ready.
```

