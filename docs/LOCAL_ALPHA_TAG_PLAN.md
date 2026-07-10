# Local Alpha Tag Plan

Status: tag plan only

## Recommended Tag

```text
local-alpha-0.1.0
```

## Tag Timing

Create the tag only after:

```text
Phase 30D outside validation returns PASS or PASS WITH REVIEW NOTES
git status is clean
schema bootstrap passes
full suite passes
git diff --check passes
```

## Pre-Tag Commands

```powershell
git status -sb
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

## Create Tag

```powershell
git tag -a local-alpha-0.1.0 -m "Codie local alpha 0.1.0"
```

## Push Tag

```powershell
git push origin local-alpha-0.1.0
```

## Verify Tag

```powershell
git tag --list local-alpha-0.1.0
git show --stat local-alpha-0.1.0
```

## Local Rollback Before Push

If a local tag was created by mistake and has not been pushed:

```powershell
git tag -d local-alpha-0.1.0
```

Do not delete a pushed tag without an explicit recovery plan.

