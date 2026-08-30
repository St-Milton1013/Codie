# Outside Validation - Phase44T Read-Only Decision Core Contract

Validate the exact PR head from a clean checkout.

## Required Review

Confirm that Phase44T is contract-only; changes exactly its authorized eight
documentation files; preserves the accepted Phase44S baseline; permits only a
pure, immutable, caller-input Phase44U Decision Core; defines the nine required
assessment questions; treats `HEALTHY_IDLE` as successful; permits only an
advisory candidate and draft contract; keeps fact, decision, policy, authority,
candidate, Goal, priority, selection, work order, approval, and execution
separate; preserves explicit conflicts, limitations, provenance, privacy, and
evidence ceilings; and keeps the human roadmap canonical.

Reject if it creates actual Goals, selects/ranks/schedules work, grants
authority, permits execution/persistence/I/O/models/sources, weakens Theory or
theory-skill review, Scryfall/Moxfield/Hareruya boundaries, or adds a Stream
Deck control path. Confirm Phase44U remains limited to its four named files and
all later phases remain blocked.

## Commands

```text
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -p "test_*.py"
```

Allowed verdicts: `PASS`, `PASS WITH REVIEW NOTES`, `PASS WITH REQUIRED FIXES`,
or `FAIL`. Phase44U remains blocked until PASS/PASS WITH REVIEW NOTES and human
merge.
