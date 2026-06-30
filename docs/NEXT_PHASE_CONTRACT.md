# Next Phase Contract

Recommended next task: Phase 13T Challenge Line Review Implementation

## Current Status

Phase 13S Challenge Line Review Contract is documented and validated.

Codie now has a Challenge Line Review contract defining immutable annotations,
review statuses, veto reasons, affected cards/actions, reviewed accuracy rules,
and regression fixture export boundaries. It still has no line review
implementation, line review persistence, UI, or recommendation output.

## Files Created Or Modified In Latest Packet

- `.gitignore`
- `ui/`
- `docs/PHASE12D_MINIMAL_UI_SHELL_REPORT.md`
- `docs/PHASE12E_READ_ONLY_UI_DATA_CONTRACT.md`
- `docs/PHASE12F_STATIC_UI_PAGE_MODEL_EXPORT_CONTRACT.md`
- `docs/PHASE12F_STATIC_UI_PAGE_MODEL_EXPORT_REPORT.md`
- `docs/PHASE12G_UI_FIXTURE_LOADER_CONTRACT.md`
- `docs/PHASE12G_UI_FIXTURE_LOADER_REPORT.md`
- `docs/PHASE12H_LOCAL_REPORT_SHARE_BUNDLE_CONTRACT.md`
- `docs/PHASE12H_LOCAL_REPORT_SHARE_BUNDLE_REPORT.md`
- `docs/PHASE12I_SHARE_BUNDLE_QR_PDF_PLANNING_CONTRACT.md`
- `docs/PHASE12I_SHARE_BUNDLE_QR_PDF_PLANNING_REPORT.md`
- `docs/PHASE12J_QR_CODE_ASSET_GENERATION_CONTRACT.md`
- `docs/PHASE12J_QR_CODE_ASSET_GENERATION_REPORT.md`
- `docs/PHASE12K_PDF_READY_SHARE_BUNDLE_CONTRACT.md`
- `docs/PHASE12K_PDF_READY_SHARE_BUNDLE_REPORT.md`
- `docs/PHASE12L_OPTIONAL_DELIVERY_INTEGRATIONS_PLANNING_CONTRACT.md`
- `docs/PHASE12L_OPTIONAL_DELIVERY_INTEGRATIONS_PLANNING_REPORT.md`
- `docs/PHASE12M_DELIVERY_USAGE_DOCUMENTATION_CONTRACT.md`
- `docs/PHASE12M_DELIVERY_USAGE_DOCUMENTATION_REPORT.md`
- `docs/USER_GUIDE_LOCAL_REPORT_SHARING.md`
- `docs/PHASE12N_OPTIONAL_LOCAL_LAN_PREVIEW_CONTRACT.md`
- `docs/PHASE12N_OPTIONAL_LOCAL_LAN_PREVIEW_REPORT.md`
- `docs/PHASE12O_OPTIONAL_LOCAL_LAN_PREVIEW_IMPLEMENTATION_CONTRACT.md`
- `docs/PHASE12O_OPTIONAL_LOCAL_LAN_PREVIEW_IMPLEMENTATION_REPORT.md`
- `docs/PHASE12P_OPTIONAL_OUTBOUND_DELIVERY_CONTRACT.md`
- `docs/PHASE12P_OPTIONAL_OUTBOUND_DELIVERY_REPORT.md`
- `docs/PHASE12Q_SHARE_BUNDLE_ZIP_EXPORT_CONTRACT.md`
- `docs/PHASE12Q_SHARE_BUNDLE_ZIP_EXPORT_REPORT.md`
- `docs/PHASE12R_SHARE_BUNDLE_ZIP_EXPORT_IMPLEMENTATION_CONTRACT.md`
- `docs/PHASE12R_SHARE_BUNDLE_ZIP_EXPORT_IMPLEMENTATION_REPORT.md`
- `docs/PHASE12S_SHARE_BUNDLE_ZIP_USAGE_DOCUMENTATION_CONTRACT.md`
- `docs/PHASE12S_SHARE_BUNDLE_ZIP_USAGE_DOCUMENTATION_REPORT.md`
- `docs/PHASE13_SIMULATOR_CONTRACT_REFRESH.md`
- `docs/PHASE13_SIMULATOR_CONTRACT_REFRESH_REPORT.md`
- `docs/PHASE13A_CEDHDATA_REFERENCE_EXTRACTION_AND_CORE_MODEL_DESIGN.md`
- `docs/PHASE13A_CEDHDATA_REFERENCE_EXTRACTION_AND_CORE_MODEL_DESIGN_REPORT.md`
- `docs/CEDHDATA_SIMULATOR_REFERENCE_CAPTURE_MANIFEST.md`
- `docs/PHASE13B_PROBABILITY_ENGINE_CORE_MODELS_CONTRACT.md`
- `docs/PHASE13B_PROBABILITY_ENGINE_CORE_MODELS_REPORT.md`
- `docs/PHASE13C_SIMULATOR_CARD_DEFINITION_MANAGER_CONTRACT.md`
- `docs/PHASE13C_SIMULATOR_CARD_DEFINITION_MANAGER_REPORT.md`
- `codie/probability_engine/card_definition_manager.py`
- `codie/probability_engine/relevance.py`
- `tests/test_probability_engine_card_definition_manager.py`
- `tests/fixtures/probability_engine/card_definitions/simple_behavior_overlays.json`
- `tests/fixtures/probability_engine/card_definitions/pending_review_seed.json`
- `docs/PHASE13D_SIMULATOR_CARD_DEFINITION_MANAGER_IMPLEMENTATION_REPORT.md`
- `docs/PHASE13E_DECK_AND_TARGET_PARSER_CONTRACT.md`
- `docs/PHASE13E_DECK_AND_TARGET_PARSER_CONTRACT_REPORT.md`
- `codie/probability_engine/deck_parser.py`
- `tests/test_probability_engine_deck_parser.py`
- `tests/fixtures/probability_engine/deck_parser/plaintext_deck.txt`
- `tests/fixtures/probability_engine/deck_parser/moxfield_plaintext_deck.txt`
- `tests/fixtures/probability_engine/deck_parser/malformed_deck.txt`
- `docs/PHASE13F_DECK_AND_TARGET_PARSER_IMPLEMENTATION_REPORT.md`
- `docs/PHASE13G_SEEDED_SHUFFLE_AND_OPENING_HAND_CONTRACT.md`
- `docs/PHASE13G_SEEDED_SHUFFLE_AND_OPENING_HAND_CONTRACT_REPORT.md`
- `codie/probability_engine/shuffle.py`
- `tests/test_probability_engine_shuffle.py`
- `tests/fixtures/probability_engine/shuffle/opening_hand_deck.txt`
- `docs/PHASE13H_SEEDED_SHUFFLE_AND_OPENING_HAND_IMPLEMENTATION_REPORT.md`
- `docs/PHASE13I_MULLIGAN_POLICY_CONTRACT.md`
- `docs/PHASE13I_MULLIGAN_POLICY_CONTRACT_REPORT.md`
- `codie/probability_engine/mulligan.py`
- `tests/test_probability_engine_mulligan.py`
- `tests/fixtures/probability_engine/mulligan/mulligan_deck.txt`
- `docs/PHASE13J_MULLIGAN_POLICY_IMPLEMENTATION_REPORT.md`
- `docs/PHASE13K_TARGET_ACCESS_SEARCH_CONTRACT.md`
- `docs/PHASE13K_TARGET_ACCESS_SEARCH_CONTRACT_REPORT.md`
- `codie/probability_engine/search.py`
- `tests/test_probability_engine_search.py`
- `tests/fixtures/probability_engine/search/target_access_deck.txt`
- `docs/PHASE13L_TARGET_ACCESS_SEARCH_MVP_IMPLEMENTATION_REPORT.md`
- `docs/PHASE13M_MONTE_CARLO_BATCH_RUNNER_CONTRACT.md`
- `docs/PHASE13M_MONTE_CARLO_BATCH_RUNNER_CONTRACT_REPORT.md`
- `codie/probability_engine/batch.py`
- `tests/test_probability_engine_batch.py`
- `tests/fixtures/probability_engine/batch/batch_deck.txt`
- `docs/PHASE13N_MONTE_CARLO_BATCH_RUNNER_IMPLEMENTATION_REPORT.md`
- `docs/PHASE13O_SIMULATOR_PERSISTENCE_CONTRACT.md`
- `docs/PHASE13O_SIMULATOR_PERSISTENCE_CONTRACT_REPORT.md`
- `codie/probability_engine/persistence.py`
- `tests/test_probability_engine_persistence.py`
- `docs/PHASE13P_SIMULATOR_PERSISTENCE_IMPLEMENTATION_REPORT.md`
- `docs/PHASE13Q_CHALLENGE_MODE_CONTRACT.md`
- `docs/PHASE13Q_CHALLENGE_MODE_CONTRACT_REPORT.md`
- `codie/probability_engine/challenge_mode.py`
- `tests/test_probability_engine_challenge_mode.py`
- `tests/fixtures/probability_engine/challenge_mode/challenge_deck.txt`
- `docs/PHASE13R_CHALLENGE_MODE_IMPLEMENTATION_REPORT.md`
- `docs/PHASE13S_CHALLENGE_LINE_REVIEW_CONTRACT.md`
- `docs/PHASE13S_CHALLENGE_LINE_REVIEW_CONTRACT_REPORT.md`
- `codie/probability_engine/__init__.py`
- `codie/probability_engine/models.py`
- `tests/test_probability_engine_models.py`
- `codie/exports/share_bundle_zip.py`
- `codie/delivery/__init__.py`
- `codie/delivery/local_preview.py`
- `tests/test_delivery_local_preview.py`
- `tests/test_exports_share_bundle_zip.py`
- `requirements.txt`
- `codie/exports/share_bundle.py`
- `codie/exports/__init__.py`
- `tests/test_exports_share_bundle.py`
- `codie/pages/export_user_workflow.py`
- `codie/pages/__init__.py`
- `codie/cli/user_deck.py`
- `tests/test_pages_user_workflow_export.py`
- `tests/test_cli_user_deck.py`
- `ui/public/page-models/saved-analysis-list.json`
- `ui/public/page-models/saved-analysis-detail.json`
- `ui/src/data/pageModelLoader.ts`
- `ui/src/types/userWorkflow.ts`
- `ui/src/App.tsx`
- `ui/src/styles.css`
- `docs/CODEX_CONTINUITY_HANDOFF.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes Added

```text
None. Latest packet is contract-only.
```

## Schema Impact

None.

## Validation Command

Use the bundled Python runtime when system Python is unavailable:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Frontend validation:

```powershell
cd ui
npm install
npm run build
```

Static checks:

```text
git diff --check
rg -n "codie\.providers|codie\.db|codie\.ingestion|source_events|source_decks|provider_objects|execute\(|executescript\(|sqlite3" codie\exports
rg -n "codie\.providers|codie\.recommendations|codie\.analytics|codie\.ingestion|source_events|source_decks|provider_objects" codie\user_decks
rg -n "codie\.providers|codie\.recommendations|codie\.analytics|source_events|source_decks|provider_objects" codie\cli
rg -n "sqlite3|source_events|source_decks|provider_objects|codie\.providers|codie\.db|codie\.recommendations|codie\.analytics" ui
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this" ui
```

## Known Caveats / Review Notes

- GitHub remote is configured and Phase 12B was pushed.
- CLI requires a local Codie database with card rows before deck import can resolve cards.
- CLI export docs recommend `--output-root` for normal usage.
- UI loads static generated page-model JSON with fixture fallback.
- Local report bundles can be built from existing export files.
- QR generation is implemented as local PNG asset generation.
- PDF-ready output is implemented as static print-friendly HTML.
- Delivery integrations remain split into future opt-in packets with privacy gates.
- Local report sharing has a PowerShell usage guide.
- Local LAN preview is implemented as selected-bundle read-only static serving.
- Outbound delivery is contract-gated and not implemented.
- Zip export is implemented as local-only deterministic packaging.
- Phase 12 local/mobile report sharing documentation is complete.
- Simulator schema currently stores reproducibility metadata implicitly through JSON payload fields; explicit seed/version columns should be reviewed before broad simulator usage.
- Challenge Mode and line review need future schema contracts before implementation.
- cEDHData reference files remain local research inputs only; do not copy the JavaScript bundle or full card catalog into Codie.
- Simulator Card Definition Manager is accepted as a future roadmap patch and should land after core models, before action search.
- cEDHData public asset metadata and local reference hashes are recorded; full assets remain outside the repo.
- No local UI API exists yet by design.
- Target access search MVP is implemented for exact hands and known library order.
- Monte Carlo batch runner is implemented.
- Simulator persistence is implemented using existing simulator tables.
- Challenge Mode is implemented without persistence or UI.
- Line review is contract-gated but not implemented.
- Line review persistence, UI, and recommendation output are not implemented.

## Recommended Next Packet

Implement Phase 13T Challenge Line Review.

Validation reference:

- `docs/CODEX_CONTINUITY_HANDOFF.md`
- `docs/PHASE12A_USER_WORKFLOW_VIEW_MODELS_CONTRACT.md`
- `docs/CHECKPOINT_PHASE12_UI_PREP_REPORT.md`
- `docs/PHASE12C_UI_SCAFFOLD_CONTRACT.md`
- `docs/PHASE12D_MINIMAL_UI_SHELL_REPORT.md`
- `docs/PHASE12E_READ_ONLY_UI_DATA_CONTRACT.md`
- `docs/PHASE12F_STATIC_UI_PAGE_MODEL_EXPORT_CONTRACT.md`
- `docs/PHASE12F_STATIC_UI_PAGE_MODEL_EXPORT_REPORT.md`
- `docs/PHASE12G_UI_FIXTURE_LOADER_CONTRACT.md`
- `docs/PHASE12G_UI_FIXTURE_LOADER_REPORT.md`
- `docs/PHASE12H_LOCAL_REPORT_SHARE_BUNDLE_CONTRACT.md`
- `docs/PHASE12H_LOCAL_REPORT_SHARE_BUNDLE_REPORT.md`
- `docs/PHASE12I_SHARE_BUNDLE_QR_PDF_PLANNING_CONTRACT.md`
- `docs/PHASE12I_SHARE_BUNDLE_QR_PDF_PLANNING_REPORT.md`
- `docs/PHASE12J_QR_CODE_ASSET_GENERATION_CONTRACT.md`
- `docs/PHASE12J_QR_CODE_ASSET_GENERATION_REPORT.md`
- `docs/PHASE12K_PDF_READY_SHARE_BUNDLE_CONTRACT.md`
- `docs/PHASE12K_PDF_READY_SHARE_BUNDLE_REPORT.md`
- `docs/PHASE12L_OPTIONAL_DELIVERY_INTEGRATIONS_PLANNING_CONTRACT.md`
- `docs/PHASE12L_OPTIONAL_DELIVERY_INTEGRATIONS_PLANNING_REPORT.md`
- `docs/PHASE12M_DELIVERY_USAGE_DOCUMENTATION_CONTRACT.md`
- `docs/PHASE12M_DELIVERY_USAGE_DOCUMENTATION_REPORT.md`
- `docs/USER_GUIDE_LOCAL_REPORT_SHARING.md`
- `docs/PHASE12N_OPTIONAL_LOCAL_LAN_PREVIEW_CONTRACT.md`
- `docs/PHASE12N_OPTIONAL_LOCAL_LAN_PREVIEW_REPORT.md`
- `docs/PHASE12O_OPTIONAL_LOCAL_LAN_PREVIEW_IMPLEMENTATION_CONTRACT.md`
- `docs/PHASE12O_OPTIONAL_LOCAL_LAN_PREVIEW_IMPLEMENTATION_REPORT.md`
- `docs/PHASE12P_OPTIONAL_OUTBOUND_DELIVERY_CONTRACT.md`
- `docs/PHASE12P_OPTIONAL_OUTBOUND_DELIVERY_REPORT.md`
- `docs/PHASE12Q_SHARE_BUNDLE_ZIP_EXPORT_CONTRACT.md`
- `docs/PHASE12Q_SHARE_BUNDLE_ZIP_EXPORT_REPORT.md`
- `docs/PHASE12R_SHARE_BUNDLE_ZIP_EXPORT_IMPLEMENTATION_CONTRACT.md`
- `docs/PHASE12R_SHARE_BUNDLE_ZIP_EXPORT_IMPLEMENTATION_REPORT.md`
- `docs/PHASE12S_SHARE_BUNDLE_ZIP_USAGE_DOCUMENTATION_CONTRACT.md`
- `docs/PHASE12S_SHARE_BUNDLE_ZIP_USAGE_DOCUMENTATION_REPORT.md`
- `docs/PHASE13_SIMULATOR_CONTRACT_REFRESH.md`
- `docs/PHASE13_SIMULATOR_CONTRACT_REFRESH_REPORT.md`
- `docs/PHASE13A_CEDHDATA_REFERENCE_EXTRACTION_AND_CORE_MODEL_DESIGN.md`
- `docs/PHASE13A_CEDHDATA_REFERENCE_EXTRACTION_AND_CORE_MODEL_DESIGN_REPORT.md`
- `docs/ROADMAP_PATCH_SIMULATOR_CARD_DEFINITION_MANAGER.md`
- `docs/PHASE13B_PROBABILITY_ENGINE_CORE_MODELS_CONTRACT.md`
- `docs/PHASE13B_PROBABILITY_ENGINE_CORE_MODELS_REPORT.md`
- `docs/PHASE13C_SIMULATOR_CARD_DEFINITION_MANAGER_CONTRACT.md`
- `docs/PHASE13C_SIMULATOR_CARD_DEFINITION_MANAGER_REPORT.md`
- `docs/PHASE13D_SIMULATOR_CARD_DEFINITION_MANAGER_IMPLEMENTATION_REPORT.md`
- `docs/PHASE13E_DECK_AND_TARGET_PARSER_CONTRACT.md`
- `docs/PHASE13E_DECK_AND_TARGET_PARSER_CONTRACT_REPORT.md`
- `docs/PHASE13F_DECK_AND_TARGET_PARSER_IMPLEMENTATION_REPORT.md`
- `docs/PHASE13G_SEEDED_SHUFFLE_AND_OPENING_HAND_CONTRACT.md`
- `docs/PHASE13G_SEEDED_SHUFFLE_AND_OPENING_HAND_CONTRACT_REPORT.md`
- `docs/PHASE13H_SEEDED_SHUFFLE_AND_OPENING_HAND_IMPLEMENTATION_REPORT.md`
- `docs/PHASE13I_MULLIGAN_POLICY_CONTRACT.md`
- `docs/PHASE13I_MULLIGAN_POLICY_CONTRACT_REPORT.md`
- `docs/PHASE13J_MULLIGAN_POLICY_IMPLEMENTATION_REPORT.md`
- `docs/PHASE13K_TARGET_ACCESS_SEARCH_CONTRACT.md`
- `docs/PHASE13K_TARGET_ACCESS_SEARCH_CONTRACT_REPORT.md`
- `docs/PHASE13L_TARGET_ACCESS_SEARCH_MVP_IMPLEMENTATION_REPORT.md`
- `docs/PHASE13M_MONTE_CARLO_BATCH_RUNNER_CONTRACT.md`
- `docs/PHASE13M_MONTE_CARLO_BATCH_RUNNER_CONTRACT_REPORT.md`
- `docs/PHASE13N_MONTE_CARLO_BATCH_RUNNER_IMPLEMENTATION_REPORT.md`
- `docs/PHASE13O_SIMULATOR_PERSISTENCE_CONTRACT.md`
- `docs/PHASE13O_SIMULATOR_PERSISTENCE_CONTRACT_REPORT.md`
- `docs/PHASE13P_SIMULATOR_PERSISTENCE_IMPLEMENTATION_REPORT.md`
- `docs/PHASE13Q_CHALLENGE_MODE_CONTRACT.md`
- `docs/PHASE13Q_CHALLENGE_MODE_CONTRACT_REPORT.md`
- `docs/PHASE13R_CHALLENGE_MODE_IMPLEMENTATION_REPORT.md`
- `docs/PHASE13S_CHALLENGE_LINE_REVIEW_CONTRACT.md`
- `docs/PHASE13S_CHALLENGE_LINE_REVIEW_CONTRACT_REPORT.md`

Define:

```text
Phase 13T - Challenge Line Review Implementation
```

Implement serializable line review annotations and regression fixture export.
Keep persistence, schema changes, UI, recommendation output, and simulator
result mutation out of scope.

## Do Not Do

- Do not scaffold UI before view models are accepted.
- Do not call providers.
- Do not read source/provider tables.
- Do not add strategic claim language.
- Do not start simulator integration.
- Do not add schema without explicit migration contract.
- Do not generate final recommendations before updated Phase 10 outside validation.
- Do not let UI access SQLite directly.
- Do not add a local API server without a contract.
- Do not make frontend fixtures private user deck data.
- Do not add hosted/mobile sharing without a separate privacy contract.
- Do not add hosted/mobile delivery integrations without an opt-in planning contract.
- Do not add outbound delivery or public tunnels during local LAN preview implementation.
- Do not make zip export send files anywhere.
- Do not implement simulator search before core models are accepted.
- Do not implement Challenge Mode before action execution and trace validation
  exist.
- Do not copy cEDHData source code or full reference payloads into Codie.
- Do not make the simulator model every card; use target relevance and unsupported reporting.

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
