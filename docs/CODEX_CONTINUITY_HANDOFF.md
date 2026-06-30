# Codex Continuity Handoff

## Purpose

This document is the recovery packet for continuing Codie after Codex context/rate limits.

Use the repository and this handoff as the source of truth. Do not rely on prior chat history.

## Repository

```text
GitHub: https://github.com/St-Milton1013/Codie
Local path: C:\Users\Main\Documents\Codex\2026-06-22\next-phase-contract-recommended-next-task
Branch: main
Latest pushed commit before local Phase 13S work: d508363 Add Phase 13R challenge mode
```

## Current Validation Baseline

Latest full-suite result:

```text
Ran 436 tests in 2.977s

OK (skipped=1)
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
Phase 12P Optional Outbound Delivery Contract: PASS
Phase 12Q Share Bundle Zip Export Contract: PASS
Phase 12R Share Bundle Zip Export Implementation: PASS
Phase 12S Share Bundle Zip Usage Documentation: PASS
Phase 12 Local UI/Report Sharing Track: COMPLETE
Phase 13 Simulator Contract Refresh: PASS
Phase 13A cEDHData Reference Extraction And Core Model Design: PASS
Phase 13B Probability Engine Core Models: PASS
Phase 13C Simulator Card Definition Manager Contract: PASS
Phase 13D Simulator Card Definition Manager Implementation: PASS
Phase 13E Deck And Target Parser Contract: PASS
Phase 13F Deck And Target Parser Implementation: PASS
Phase 13G Seeded Shuffle And Opening Hand Contract: PASS
Phase 13H Seeded Shuffle And Opening Hand Implementation: PASS
Phase 13I Mulligan Policy Contract: PASS
Phase 13J Mulligan Policy Implementation: PASS
Phase 13K Target Access Search Contract: PASS
Phase 13L Target Access Search MVP Implementation: PASS
Phase 13M Monte Carlo Batch Runner Contract: PASS
Phase 13N Monte Carlo Batch Runner Implementation: PASS
Phase 13O Simulator Persistence Contract: PASS
Phase 13P Simulator Persistence Implementation: PASS
Phase 13Q Challenge Mode Contract: PASS
Phase 13R Challenge Mode Implementation: PASS
Phase 13S Challenge Line Review Contract: PASS
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
Phase 13T - Challenge Line Review Implementation
```

Alternate next safe option:

```text
Phase 13U - Challenge Line Review Persistence Contract
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
docs/PHASE12P_OPTIONAL_OUTBOUND_DELIVERY_CONTRACT.md
docs/PHASE12P_OPTIONAL_OUTBOUND_DELIVERY_REPORT.md
docs/PHASE12Q_SHARE_BUNDLE_ZIP_EXPORT_CONTRACT.md
docs/PHASE12Q_SHARE_BUNDLE_ZIP_EXPORT_REPORT.md
docs/PHASE12R_SHARE_BUNDLE_ZIP_EXPORT_IMPLEMENTATION_CONTRACT.md
docs/PHASE12R_SHARE_BUNDLE_ZIP_EXPORT_IMPLEMENTATION_REPORT.md
docs/PHASE12S_SHARE_BUNDLE_ZIP_USAGE_DOCUMENTATION_CONTRACT.md
docs/PHASE12S_SHARE_BUNDLE_ZIP_USAGE_DOCUMENTATION_REPORT.md
docs/PHASE13_SIMULATOR_CONTRACT_REFRESH.md
docs/PHASE13_SIMULATOR_CONTRACT_REFRESH_REPORT.md
docs/PHASE13A_CEDHDATA_REFERENCE_EXTRACTION_AND_CORE_MODEL_DESIGN.md
docs/PHASE13A_CEDHDATA_REFERENCE_EXTRACTION_AND_CORE_MODEL_DESIGN_REPORT.md
docs/PHASE13B_PROBABILITY_ENGINE_CORE_MODELS_CONTRACT.md
docs/PHASE13B_PROBABILITY_ENGINE_CORE_MODELS_REPORT.md
docs/PHASE13C_SIMULATOR_CARD_DEFINITION_MANAGER_CONTRACT.md
docs/PHASE13C_SIMULATOR_CARD_DEFINITION_MANAGER_REPORT.md
docs/PHASE13D_SIMULATOR_CARD_DEFINITION_MANAGER_IMPLEMENTATION_REPORT.md
docs/PHASE13E_DECK_AND_TARGET_PARSER_CONTRACT.md
docs/PHASE13E_DECK_AND_TARGET_PARSER_CONTRACT_REPORT.md
docs/PHASE13F_DECK_AND_TARGET_PARSER_IMPLEMENTATION_REPORT.md
docs/PHASE13G_SEEDED_SHUFFLE_AND_OPENING_HAND_CONTRACT.md
docs/PHASE13G_SEEDED_SHUFFLE_AND_OPENING_HAND_CONTRACT_REPORT.md
docs/PHASE13H_SEEDED_SHUFFLE_AND_OPENING_HAND_IMPLEMENTATION_REPORT.md
docs/PHASE13I_MULLIGAN_POLICY_CONTRACT.md
docs/PHASE13I_MULLIGAN_POLICY_CONTRACT_REPORT.md
docs/PHASE13J_MULLIGAN_POLICY_IMPLEMENTATION_REPORT.md
docs/PHASE13K_TARGET_ACCESS_SEARCH_CONTRACT.md
docs/PHASE13K_TARGET_ACCESS_SEARCH_CONTRACT_REPORT.md
docs/PHASE13L_TARGET_ACCESS_SEARCH_MVP_IMPLEMENTATION_REPORT.md
docs/PHASE13M_MONTE_CARLO_BATCH_RUNNER_CONTRACT.md
docs/PHASE13M_MONTE_CARLO_BATCH_RUNNER_CONTRACT_REPORT.md
docs/PHASE13N_MONTE_CARLO_BATCH_RUNNER_IMPLEMENTATION_REPORT.md
docs/PHASE13O_SIMULATOR_PERSISTENCE_CONTRACT.md
docs/PHASE13O_SIMULATOR_PERSISTENCE_CONTRACT_REPORT.md
docs/PHASE13P_SIMULATOR_PERSISTENCE_IMPLEMENTATION_REPORT.md
docs/PHASE13Q_CHALLENGE_MODE_CONTRACT.md
docs/PHASE13Q_CHALLENGE_MODE_CONTRACT_REPORT.md
docs/PHASE13R_CHALLENGE_MODE_IMPLEMENTATION_REPORT.md
docs/PHASE13S_CHALLENGE_LINE_REVIEW_CONTRACT.md
docs/PHASE13S_CHALLENGE_LINE_REVIEW_CONTRACT_REPORT.md
```

Latest Phase 13K packet:

```text
docs/PHASE13K_TARGET_ACCESS_SEARCH_CONTRACT.md
docs/PHASE13K_TARGET_ACCESS_SEARCH_CONTRACT_REPORT.md
```

Phase 13K defines the bounded deterministic target access search MVP, including
state shape, action categories, target condition modes, trace shape,
unsupported behavior handling, and termination rules. It adds no implementation
code.

Latest Phase 13L packet:

```text
codie/probability_engine/search.py
tests/test_probability_engine_search.py
tests/fixtures/probability_engine/search/target_access_deck.txt
docs/PHASE13L_TARGET_ACCESS_SEARCH_MVP_IMPLEMENTATION_REPORT.md
```

Phase 13L implements bounded deterministic target access search for exact hands
and known library order. It reports success, failure, unsupported behavior,
invalid targets, and limits with serializable traces.

Latest Phase 13M packet:

```text
docs/PHASE13M_MONTE_CARLO_BATCH_RUNNER_CONTRACT.md
docs/PHASE13M_MONTE_CARLO_BATCH_RUNNER_CONTRACT_REPORT.md
```

Phase 13M defines deterministic batch execution over seeded games, connecting
shuffle, mulligan policy, and target access search while preserving trace
samples, reproducibility metadata, and unsupported behavior accounting. It adds
no implementation code.

Latest Phase 13N packet:

```text
codie/probability_engine/batch.py
tests/test_probability_engine_batch.py
tests/fixtures/probability_engine/batch/batch_deck.txt
docs/PHASE13N_MONTE_CARLO_BATCH_RUNNER_IMPLEMENTATION_REPORT.md
```

Phase 13N implements deterministic batch execution over seeded games, connecting
shuffle, mulligan policy, and target access search. It reports aggregate status
counts, trace samples, unsupported behavior, and reproducibility metadata.

Latest Phase 13O packet:

```text
docs/PHASE13O_SIMULATOR_PERSISTENCE_CONTRACT.md
docs/PHASE13O_SIMULATOR_PERSISTENCE_CONTRACT_REPORT.md
```

Phase 13O defines simulator persistence boundaries using existing
`simulation_batches`, `simulation_batch_results`, and `simulation_traces` tables
through `SimulationRepository`. It adds no implementation code and no schema
changes.

Latest Phase 13P packet:

```text
codie/probability_engine/persistence.py
tests/test_probability_engine_persistence.py
docs/PHASE13P_SIMULATOR_PERSISTENCE_IMPLEMENTATION_REPORT.md
```

Phase 13P implements simulator batch-result persistence using existing simulator
tables and `SimulationRepository`. It preserves seed/version/config metadata in
JSON columns, wraps batch/result/trace writes in a savepoint, and does not write
analytics, evidence_counts, or recommendations.

Latest Phase 13Q packet:

```text
docs/PHASE13Q_CHALLENGE_MODE_CONTRACT.md
docs/PHASE13Q_CHALLENGE_MODE_CONTRACT_REPORT.md
```

Phase 13Q defines Challenge Mode as a serializable prompt/answer/verification
layer over existing shuffle and target access search. It adds no implementation,
no schema changes, no persistence, and no UI.

Latest Phase 13R packet:

```text
codie/probability_engine/challenge_mode.py
tests/test_probability_engine_challenge_mode.py
tests/fixtures/probability_engine/challenge_mode/challenge_deck.txt
docs/PHASE13R_CHALLENGE_MODE_IMPLEMENTATION_REPORT.md
```

Phase 13R implements serializable Challenge Mode prompt, answer, and
verification models using existing shuffle and target access search. It adds no
persistence, line review, UI, or recommendation output.

Latest Phase 13S packet:

```text
docs/PHASE13S_CHALLENGE_LINE_REVIEW_CONTRACT.md
docs/PHASE13S_CHALLENGE_LINE_REVIEW_CONTRACT_REPORT.md
```

Phase 13S defines Challenge Line Review as immutable annotations over simulator
output, including review statuses, veto reasons, affected cards/actions,
reviewed accuracy rules, and regression fixture export boundaries. It adds no
implementation, no persistence, no schema changes, and no UI.

Next UI implementation packet:

```text
Phase 12 local UI/report sharing track is complete. Return to UI only after
Phase 13 simulator contracts or a new UI/API contract is explicitly selected.
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
- Outbound delivery is contract-gated and not implemented.
- Zip export is implemented as local-only deterministic packaging.
- Phase 12 local/mobile report sharing documentation is complete.
- No local UI API exists yet.
- No simulator implementation exists yet.
- Simulator contract refresh and pure core models are complete.
- Probability engine currently has core dataclasses, card definition manager,
  deck/target parsing, seeded shuffle/opening hands, mulligan policy, and target
  access search, Monte Carlo batch execution, and simulator persistence. It has
  no Challenge Mode or line review.
- cEDHData reference files were inspected locally only; do not copy the JavaScript bundle or full card catalog into Codie.
- Simulator Card Definition Manager implementation is complete. It is
  in-memory only and does not execute card actions.
- Deck and target parser contract is complete.
- Deck and target parser implementation is complete.
- Seeded shuffle and opening-hand contract is complete.
- Seeded shuffle and opening-hand implementation is complete.
- Mulligan policy contract is complete.
- Mulligan policy implementation is complete.
- Target access search MVP contract is complete.
- Target access search MVP implementation is complete.
- Monte Carlo batch runner contract is complete.
- Monte Carlo batch runner implementation is complete.
- Simulator persistence contract is complete.
- Simulator persistence implementation is complete.
- Challenge Mode contract is complete.
- Challenge Mode implementation is complete.
- Challenge Line Review contract is complete.
- Next packet should implement Challenge Line Review without persistence, schema
  changes, UI, or simulator-result mutation.
- cEDHData public asset metadata and local reference hashes are recorded in docs/CEDHDATA_SIMULATOR_REFERENCE_CAPTURE_MANIFEST.md.
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
