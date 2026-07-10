# Local Alpha Validation Steps

Status: local alpha validation guide

Run from the repository root.

## 1. Confirm Git State

```powershell
git status -sb
```

Expected:

```text
current branch is main
no unexpected local changes before validation
```

## 2. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

For development tooling:

```powershell
python -m pip install -r requirements-dev.txt
```

## 3. Schema Bootstrap Check

```powershell
python scripts/check_schema.py
```

Expected:

```text
Schema bootstrap check passed.
```

## 4. Test Suite

```powershell
python -m unittest discover -s tests
```

Expected:

```text
OK
```

The exact runtime may differ by machine.

## 5. Diff Check

```powershell
git diff --check
```

Expected: no errors.

## 6. Release Gate Scan

```powershell
rg -n "Phase 30B.*INTERNAL PASS|blocked until Phase 30B|send Phase 30B outside validation|Current Phase 30B Outside Validation" docs\ACTIVE_ROADMAP_INDEX.md docs\VALIDATION_STATUS_INDEX.md docs\NEXT_PHASE_CONTRACT.md docs\CODEX_CONTINUITY_HANDOFF.md
```

Expected: no matches after Phase 30B outside validation is accepted.

## 7. Production Touch Check For Phase 30B

```powershell
git diff --name-only -- codie tests scripts ui .github requirements.txt requirements-dev.txt pyproject.toml docs\SCHEMA_SPEC.md codie\db
```

Expected: no matches for Phase 30B documentation-only work.
