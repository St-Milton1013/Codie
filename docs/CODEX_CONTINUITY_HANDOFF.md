# Codex Continuity Handoff

## Purpose

This document is the recovery packet for continuing Codie after Codex context/rate limits.

Use the repository and this handoff as the source of truth. Do not rely on prior chat history.

## Repository

```text
GitHub: https://github.com/St-Milton1013/Codie
Local path: C:\Users\Main\Documents\Codex\2026-06-22\next-phase-contract-recommended-next-task
Branch: main
Latest pushed commit before Phase 12O closure: e2e3a6a Add Phase 12N LAN preview contract
```

## Current Validation Baseline

Latest full-suite result:

```text
Ran 311 tests in 2.847s

OK
```

Latest static check:

```text
git diff --check
```

passed.

Latest relevant boundary scan:

```text
rg -n "codie\.providers|codie\.recommendations|codie\.analytics|source_events|source_decks|provider_objects" codie\pages codie\cli
```

returned:

```text
pages/cli: no matches
```

Latest UI boundary scans:

```text
rg -n "sqlite3|source_events|source_decks|provider_objects|codie\.providers|codie\.db|codie\.recommendations|codie\.analytics" ui
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this" ui
```

returned:

```text
ui: no matches
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
Phase 12 UI Preparation/View Models: PASS
Phase 12C UI Scaffold Contract: PASS
Phase 12D Minimal React/Vite Local UI Shell: PASS
Phase 12E Read-Only Local UI Data Contract: PASS
Phase 12F Static UI Page Model Export: PASS
Phase 12G UI Fixture Loader / Generated Export Preview: PASS
Phase 12H Local Report Share Bundle: PASS
Phase 12I Share Bundle QR/PDF Planning Contract: PASS
Phase 12J QR Code Asset Generation: PASS
Phase 12K PDF-Ready Share Bundle Output: PASS
Phase 12L Optional Delivery Integrations Planning: PASS
Phase 12M Delivery Usage Documentation: PASS
Phase 12N Optional Local LAN Preview Contract: PASS
Phase 12O Optional Local LAN Preview Implementation: PASS
```

## Recent Commits

```text
702c3a9 Add Phase 12E UI data contract
651a48b Ignore UI dev server logs
ca2b6fd Add Phase 12D minimal UI shell
cd93b42 Add Phase 12C UI scaffold contract
1da325e Add Phase 11 12 validation prompt
f431115 Add LLM naming audit workflow
77059ed Add user workflow roadmap patch
8938b7e Add mobile report access roadmap
6c6ad63 Add Phase 12 UI prep checkpoint
7f928c1 Add user workflow view models
```

## Current Outside Validation Packets

Use this combined validation prompt:

```text
docs/OUTSIDE_VALIDATION_PHASE11_12_PROMPT.md
```

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
React + TypeScript + Vite scaffold exists under ui/.
Current UI is fixture-backed only.
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
Phase 12P - Optional Outbound Delivery Contract
```

Alternate next safe option:

```text
Phase 13 - Simulator Contract Refresh
```

Avoid starting:

```text
final recommendation output
simulator implementation
provider live backfills
schema changes
direct UI database access
```

Current UI packets:

```text
docs/PHASE12C_UI_SCAFFOLD_CONTRACT.md
docs/PHASE12D_MINIMAL_UI_SHELL_REPORT.md
docs/PHASE12E_READ_ONLY_UI_DATA_CONTRACT.md
docs/PHASE12F_STATIC_UI_PAGE_MODEL_EXPORT_CONTRACT.md
docs/PHASE12F_STATIC_UI_PAGE_MODEL_EXPORT_REPORT.md
docs/PHASE12G_UI_FIXTURE_LOADER_CONTRACT.md
docs/PHASE12G_UI_FIXTURE_LOADER_REPORT.md
docs/PHASE12H_LOCAL_REPORT_SHARE_BUNDLE_CONTRACT.md
docs/PHASE12H_LOCAL_REPORT_SHARE_BUNDLE_REPORT.md
docs/PHASE12I_SHARE_BUNDLE_QR_PDF_PLANNING_CONTRACT.md
docs/PHASE12I_SHARE_BUNDLE_QR_PDF_PLANNING_REPORT.md
docs/PHASE12J_QR_CODE_ASSET_GENERATION_CONTRACT.md
docs/PHASE12J_QR_CODE_ASSET_GENERATION_REPORT.md
docs/PHASE12K_PDF_READY_SHARE_BUNDLE_CONTRACT.md
docs/PHASE12K_PDF_READY_SHARE_BUNDLE_REPORT.md
docs/PHASE12L_OPTIONAL_DELIVERY_INTEGRATIONS_PLANNING_CONTRACT.md
docs/PHASE12L_OPTIONAL_DELIVERY_INTEGRATIONS_PLANNING_REPORT.md
docs/PHASE12M_DELIVERY_USAGE_DOCUMENTATION_CONTRACT.md
docs/PHASE12M_DELIVERY_USAGE_DOCUMENTATION_REPORT.md
docs/USER_GUIDE_LOCAL_REPORT_SHARING.md
docs/PHASE12N_OPTIONAL_LOCAL_LAN_PREVIEW_CONTRACT.md
docs/PHASE12N_OPTIONAL_LOCAL_LAN_PREVIEW_REPORT.md
docs/PHASE12O_OPTIONAL_LOCAL_LAN_PREVIEW_IMPLEMENTATION_CONTRACT.md
docs/PHASE12O_OPTIONAL_LOCAL_LAN_PREVIEW_IMPLEMENTATION_REPORT.md
```

Next UI implementation packet:

```text
Phase 12P - Optional Outbound Delivery Contract
```

## Known Caveats

- Hareruya live access can hit AWS WAF; treat Hareruya as regional enrichment, not critical path.
- CLI requires a local Codie SQLite database with card rows before user deck import can resolve cards.
- CLI export docs recommend `--output-root` for normal usage.
- Minimal static-export-backed UI exists under `ui/`.
- Static local report bundles can be built from existing export files.
- QR/PDF/mobile report sharing has a planning contract and must remain opt-in.
- QR generation is local-only and encodes explicit targets only.
- PDF-ready output is static HTML only; no PDF binary generation yet.
- Delivery integrations are planning-only and disabled by default.
- Local report sharing has a PowerShell-oriented usage guide.
- Local LAN preview is implemented as selected-bundle read-only static serving.
- No local UI API exists yet.
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
