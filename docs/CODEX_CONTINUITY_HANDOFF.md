# Codex Continuity Handoff

## Purpose

This document is the recovery packet for continuing Codie after Codex context/rate limits.

Use the repository and this handoff as the source of truth. Do not rely on prior chat history.

## Repository

```text
GitHub: https://github.com/St-Milton1013/Codie
Local path: C:\Users\Main\Documents\Codex\2026-06-22\next-phase-contract-recommended-next-task
Branch: main
Latest pushed commit at handoff creation: 6c6ad63 Add Phase 12 UI prep checkpoint
```

## Current Validation Baseline

Latest full-suite result:

```text
Ran 283 tests in 0.723s

OK
```

Latest static check:

```text
git diff --check
```

passed.

Latest relevant boundary scan:

```text
rg -n "codie\.providers|codie\.db|codie\.recommendations|codie\.analytics|source_events|source_decks|provider_objects|sqlite3" codie\pages
```

returned:

```text
pages: no matches
```

## Completed Phase Status

```text
Phase 0: PASS
Phase 1: PASS
Phase 2: PASS
Phase 3: PASS
Phase 4A TopDeck: PASS
Phase 4B EDHTop16: PASS
Phase 4C MTGTop8: PASS
Phase 4D MTGDecks: PASS
Phase 4E Hareruya: PASS WITH ACCESS CAVEAT
Phase 5 Canonicalization: PASS
Phase 6 Analytics Foundations: PASS
Phase 7A Spellbook Evidence: PASS
Phase 7B Moxfield Primer Metadata: PASS
Phase 8 Readiness/Recommendation Foundations/Innovation: PASS
Phase 9 Export Surfaces: PASS
Phase 10 User Deck Workflow: PASS WITH REVIEW NOTES
Phase 11 User Workflow Retrieval: READY FOR OUTSIDE VALIDATION
Phase 12 UI Preparation/View Models: READY FOR OUTSIDE VALIDATION
```

## Recent Commits

```text
6c6ad63 Add Phase 12 UI prep checkpoint
7f928c1 Add user workflow view models
d6c89bd Add Phase 12 UI planning contract
d256c3a Add Phase 11 retrieval checkpoint
3dacbfa Add saved analysis retrieval
c039ec0 Add Phase 11 planning contract
174e0c8 Document CLI output root guidance
b322119 Update Phase 10 checkpoint for saved analysis
aed9bc8 Add saved user deck analysis persistence
9ed6871 Update Phase 10 checkpoint for CLI
2ae69ac Add user deck CLI wrapper
cfabf94 Add Phase 10 user deck workflow checkpoint
```

## Current Outside Validation Packets

Send Phase 11:

```text
docs/CHECKPOINT_PHASE11_USER_WORKFLOW_RETRIEVAL_REPORT.md
docs/PHASE11_PLANNING_CONTRACT.md
docs/PHASE11A_SAVED_ANALYSIS_RETRIEVAL_CONTRACT.md
```

Send Phase 12:

```text
docs/CHECKPOINT_PHASE12_UI_PREP_REPORT.md
docs/PHASE12_UI_PLANNING_CONTRACT.md
docs/PHASE12A_USER_WORKFLOW_VIEW_MODELS_CONTRACT.md
```

Phase 10 reference packet:

```text
docs/CHECKPOINT_PHASE10_USER_DECK_WORKFLOW_REPORT.md
docs/PHASE10A_USER_DECK_IMPORT_CONTRACT.md
docs/PHASE10B_USER_DECK_ANALYSIS_INPUT_CONTRACT.md
docs/PHASE10C_USER_DECK_EVIDENCE_COMPARISON_CONTRACT.md
docs/PHASE10D_USER_DECK_COMPARISON_EXPORT_CONTRACT.md
docs/PHASE10E_USER_DECK_COMPARISON_FILE_WRITER_CONTRACT.md
docs/PHASE10G_USER_DECK_CLI_CONTRACT.md
docs/PHASE10I_SAVED_ANALYSIS_PERSISTENCE_CONTRACT.md
```

## Resume Prompt For A New Codex Session

Paste this into a new session:

```text
Read docs/CODEX_CONTINUITY_HANDOFF.md and docs/NEXT_PHASE_CONTRACT.md.

Continue Codie from the recommended next packet.

Do not start final recommendation output, simulator integration, or React/Vite UI scaffold unless the relevant contract and outside validation gates are already present.

Before editing, inspect git status and the latest checkpoint docs.
After editing, run focused tests, full tests, relevant boundary scans, commit, and push.
```

## Commands To Run At Start Of A New Session

```powershell
cd "C:\Users\Main\Documents\Codex\2026-06-22\next-phase-contract-recommended-next-task"
git status
git pull
git log --oneline -10
type docs\CODEX_CONTINUITY_HANDOFF.md
type docs\NEXT_PHASE_CONTRACT.md
```

Use bundled Python if system Python is unavailable:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests
```

## Architecture Boundaries To Preserve

Providers:

```text
fetch/parse only
emit candidate models only
no db/repository/sqlite/analytics/recommendations imports
```

User deck workflow:

```text
local user-layer only
resolve cards before persistence
savepoint atomicity for imports
evidence-only comparison language
saved analyses store summaries, not recommendations
```

Pages/view models:

```text
pure transformations
JSON-compatible output
no DB/repository connections
no providers
no recommendations generation
no analytics ownership
no source/provider table reads
```

UI:

```text
React + TypeScript + Vite is constitutionally selected for later.
Do not scaffold UI until Phase 12 view-model boundary is validated.
UI must never issue raw SQL.
UI must consume application/page models, not own data.
```

Recommendations:

```text
Final recommendation output remains separate.
Do not generate "you should play/cut" language.
Evidence wording must preserve source, sample size, generated_at, and provenance.
```

Simulator:

```text
Do not start simulator integration without a refreshed simulator contract.
Simulation evidence must not enter Evidence Stack unless constitution thresholds are satisfied.
```

## Next Safe Options

Preferred next move:

```text
Outside validation for Phase 11 and Phase 12.
```

If continuing implementation after validation:

```text
Phase 12C - UI Scaffold Contract
```

or:

```text
Phase 13 - Simulator Contract Refresh
```

Avoid starting:

```text
React/Vite scaffold without Phase 12 validation
final recommendation output
simulator implementation
provider live backfills
schema changes
```

## Known Caveats

- Hareruya live access can hit AWS WAF; treat Hareruya as regional enrichment, not critical path.
- CLI requires a local Codie SQLite database with card rows before user deck import can resolve cards.
- CLI export docs recommend `--output-root` for normal usage.
- No UI exists yet.
- No simulator implementation exists yet.
- Final recommendation output remains intentionally separate.

## Quality Gate

Every future packet must include:

```text
contract -> code -> tests -> validation -> completion report -> handoff -> commit -> push
```

Minimum closure checks:

```powershell
git diff --check
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests
```

Run relevant boundary scans whenever touching:

```text
providers/
user_decks/
exports/
cli/
pages/
recommendations/
analytics/
```
