# Next Phase Contract

Recommended next task: Phase 13E Deck And Target Parser Contract

## Current Status

Phase 13D Simulator Card Definition Manager Implementation is implemented and
validated.

Codie now has an in-memory card definition manager that loads declarative
behavior overlays, classifies target relevance, reports unsupported relevant
and irrelevant cards, emits pending-review records, and produces confidence
summaries without executing simulator actions.

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
CardRelevanceResult
CardDefinitionStatus
UnsupportedCardRecord
CardDefinitionLoadResult
CardDefinitionManager
classify_card_relevance
load_behavior_overlay_rows
build_card_definition_load_result
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

## Recommended Next Packet

Write Phase 13E Deck And Target Parser Contract.

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

Define:

```text
Phase 13E - Deck And Target Parser Contract
```

Define how user deck inputs, commander rows, unresolved cards, target card,
target zone, target turn, and target condition type become the Phase 13B
in-memory `SimulationDeck` and `SimulationTargetCondition` models. Keep it
contract-only before parsing implementation, opening-hand generation, seeded
shuffle, mulligans, target search, action execution, and Challenge Mode.

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
