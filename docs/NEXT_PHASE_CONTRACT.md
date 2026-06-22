# Next Phase Contract

Recommended next task: Phase 10A - User Deck Import / Analysis Contract

## Current Status

Phase 9C is locally implemented and validated.

Phase 9C added deterministic checkpoint report generation from already-built export payloads and validation metadata. It did not add DB reads, providers, UI, schema, or live network dependencies.

## Files Created Or Modified In Latest Packet

- `codie/exports/checkpoints.py`
- `codie/exports/__init__.py`
- `tests/test_exports_checkpoints.py`
- `docs/PHASE9C_CHECKPOINT_EXPORT_GENERATOR_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes Added

- `ValidationSummary`
- `CheckpointExport`
- `build_checkpoint_export(...)`
- `checkpoint_markdown(...)`
- `write_checkpoint_markdown(...)`

## Schema Impact

None.

## Validation Command

Use the bundled Python runtime when system Python is unavailable:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Static checks:

```text
git diff --check
rg -n "codie\.providers|codie\.db|codie\.ingestion|source_events|source_decks|provider_objects|execute\(|executescript\(|sqlite3" codie\exports
```

## Known Caveats / Review Notes

- GitHub remote is configured, but first push is still blocked on interactive GitHub HTTPS authentication.
- Export/checkpoint layers are pure transforms and file writers.
- No UI exists yet.

## Recommended Next Packet

Phase 10A - User Deck Import / Analysis Contract.

This should be contract-first. Before implementation, define:

- accepted user deck input format
- card resolution behavior
- repository writes to `user_decks` / `user_deck_cards`
- analysis session lifecycle
- failure behavior for unresolved cards
- no provider/source table reads

## Do Not Do

- Do not build UI before user-deck contracts are accepted.
- Do not call providers.
- Do not read source/provider tables.
- Do not add strategic claim language.
- Do not start simulator integration.
- Do not add schema without explicit migration contract.

## Required Phase Packet Shape

Every follow-up phase packet must include:

- contract document before code
- complete implementation files
- focused tests and fixture data where relevant
- full validation command and actual output
- static architecture checks where relevant
- completion report
- updated handoff or next-phase document
- clean commit after validation passes

Use this packet order:

```text
contract -> code -> tests -> validation -> completion report -> handoff -> commit
```
