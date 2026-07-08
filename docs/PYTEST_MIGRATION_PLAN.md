# Pytest Migration Plan

Status: planning only

Codie currently uses `unittest` as the authoritative test runner. Keep `python -m unittest discover -s tests` as the release gate until a future contract changes it.

## Why Add Pytest Support

Pytest can improve:

```text
fixture reuse
parametrized parser cases
cleaner failure output
focused test selection
property-based testing integration
```

## Migration Rules

```text
Do not remove unittest compatibility.
Do not rewrite existing tests just for style.
New parser, analytics, and boundary tests may use pytest only after the test runner contract is updated.
CI must continue running unittest until pytest is formally promoted.
```

## Suggested Future Steps

```text
1. Add pytest to dev dependencies.
2. Confirm pytest can collect existing unittest tests.
3. Add one fixture-heavy provider test using pytest.
4. Add property-based tests for deterministic identity/math helpers.
5. Update CI only after outside validation accepts the runner change.
```
