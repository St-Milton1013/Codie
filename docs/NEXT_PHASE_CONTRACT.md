# Next Phase Contract

Recommended next task: Phase 14D - Simulator Review Export Checkpoint

## Current Status

Phase 13 through Phase 13Z is implemented, checkpointed, and externally
accepted with review notes.

Phase 14A through 14C are implemented:

```text
Simulation Review Export File Writer
Simulation Review Export CLI
Simulation Review Export Usage Documentation
```

The simulator review export track now includes:

```text
reviewed accuracy summaries
line review regression fixtures
pure JSON/Markdown export payload builders
deterministic export bundle metadata
safe local file writer for accepted bundles
CLI wrapper for writing accepted bundle JSON files
usage guide for local export and review workflow
```

## Files Created Or Modified In Latest Packet

```text
docs/USER_GUIDE_SIMULATION_REVIEW_EXPORTS.md
docs/PHASE14C_SIMULATION_REVIEW_EXPORT_USAGE_DOCUMENTATION_CONTRACT.md
docs/PHASE14C_SIMULATION_REVIEW_EXPORT_USAGE_DOCUMENTATION_REPORT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Schema Impact

None.

## Validation Command

Use the bundled Python runtime when system Python is unavailable:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Documentation static checks:

```text
git diff --check
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|you should" docs\USER_GUIDE_SIMULATION_REVIEW_EXPORTS.md
```

## Known Caveats / Review Notes

- Challenge Mode has no UI yet.
- Simulator behavior coverage is intentionally narrow.
- Unsupported-card behavior must remain visible.
- Simulation results remain QA/training metadata, not tournament evidence.
- Final recommendation output remains intentionally separate.
- The Phase 14B CLI accepts already-built local bundle JSON only; it does not
  query DB, build review summaries, run simulations, or call providers.
- Phase 14C is documentation-only.
- cEDHData reference files remain local research inputs only; do not copy the
  JavaScript bundle or full card catalog into Codie.

## Recommended Next Packet

```text
Phase 14D - Simulator Review Export Checkpoint
```

Prepare a checkpoint report covering:

```text
Phase 14A file writer
Phase 14B CLI
Phase 14C usage docs
tests and static scans
boundary compliance
remaining review notes
```

Do not add schema, DB reads, provider calls, UI, recommendations, or simulator
behavior changes in Phase 14D.
