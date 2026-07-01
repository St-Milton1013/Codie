# Outside Validation Prompt - Phase 13 Simulator Track

Use this prompt with an outside reviewer.

```text
Validate Codie Phase 13 Simulator Track against CODIE_V1_CONSTITUTION.md and the Phase 13 contracts, reports, implementation files, schema, repositories, and tests.

Important:
- Do not validate docs only.
- Inspect implementation code.
- Run the test suite from a clean checkout.
- Run import/boundary scans.
- Reject if code behavior disagrees with checkpoint claims.

Review these documentation files:

docs/CHECKPOINT_PHASE13_SIMULATOR_TRACK_REPORT.md
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
docs/PHASE13T_CHALLENGE_LINE_REVIEW_IMPLEMENTATION_REPORT.md
docs/PHASE13U_CHALLENGE_LINE_REVIEW_PERSISTENCE_CONTRACT.md
docs/PHASE13U_CHALLENGE_LINE_REVIEW_PERSISTENCE_CONTRACT_REPORT.md
docs/PHASE13V_CHALLENGE_LINE_REVIEW_PERSISTENCE_IMPLEMENTATION_REPORT.md
docs/PHASE13W_REVIEWED_SIMULATOR_ACCURACY_CONTRACT.md
docs/PHASE13W_REVIEWED_SIMULATOR_ACCURACY_CONTRACT_REPORT.md
docs/PHASE13X_REVIEWED_SIMULATOR_ACCURACY_IMPLEMENTATION_REPORT.md
docs/PHASE13Y_SIMULATION_REVIEW_EXPORT_CONTRACT.md
docs/PHASE13Y_SIMULATION_REVIEW_EXPORT_CONTRACT_REPORT.md
docs/PHASE13Z_SIMULATION_REVIEW_EXPORT_IMPLEMENTATION_REPORT.md

Review these implementation files:

codie/probability_engine/models.py
codie/probability_engine/card_definition_manager.py
codie/probability_engine/relevance.py
codie/probability_engine/deck_parser.py
codie/probability_engine/shuffle.py
codie/probability_engine/mulligan.py
codie/probability_engine/search.py
codie/probability_engine/batch.py
codie/probability_engine/persistence.py
codie/probability_engine/challenge_mode.py
codie/probability_engine/line_review.py
codie/probability_engine/line_review_persistence.py
codie/probability_engine/reviewed_accuracy.py
codie/probability_engine/review_export.py
codie/probability_engine/__init__.py

Review these database/repository files:

codie/db/schema/simulation.sql
codie/db/schema/indexes.sql
codie/db/repositories/simulation.py
codie/db/repositories/base.py
codie/db/bootstrap.py
docs/SCHEMA_SPEC.md

Review these tests:

tests/test_probability_engine_models.py
tests/test_probability_engine_card_definition_manager.py
tests/test_probability_engine_deck_parser.py
tests/test_probability_engine_shuffle.py
tests/test_probability_engine_mulligan.py
tests/test_probability_engine_search.py
tests/test_probability_engine_batch.py
tests/test_probability_engine_persistence.py
tests/test_probability_engine_challenge_mode.py
tests/test_probability_engine_line_review.py
tests/test_probability_engine_line_review_persistence.py
tests/test_probability_engine_reviewed_accuracy.py
tests/test_probability_engine_review_export.py
tests/test_schema.py

Run the full test suite from a clean checkout:

python -m unittest discover -s tests

Confirm:
- reported result is reproducible:
  Ran 487 tests
  OK (skipped=1)
- no local-only state is required
- no generated SQLite DB artifact is required
- no ignored/cache file is required
- skipped test reason is acceptable
- tests pass after removing __pycache__ directories

Run import boundary scans across the repo.

Reject if:
- any pure probability_engine module imports codie.db, repositories, providers, analytics, recommendations, ingestion, cards, requests, httpx, urllib, aiohttp, or external network clients
- providers, analytics, recommendations, or ingestion import simulator internals unexpectedly
- raw SQL appears outside codie/db
- review_export imports persistence, repository, or db modules
- review_export writes files or queries DB directly

Suggested scans:

rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|requests|httpx|urllib|aiohttp" codie/probability_engine
rg -n "probability_engine" codie/providers codie/analytics codie/recommendations codie/ingestion
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie tests
rg -n "codie\.db|SimulationRepository|repositories|persistence" codie/probability_engine/review_export.py

Interpretation:
- persistence.py and line_review_persistence.py may import SimulationRepository.
- reviewed_accuracy.py should remain pure when possible.
- If reviewed_accuracy.py imports SimulationRepository, it must be read-only and must not mutate simulator, review, analytics, recommendation, evidence, source, provider, or user tables.
- raw SQL is allowed inside codie/db only.
- test files may contain SQL for assertions, but production raw SQL must stay in codie/db.

Check simulator architecture:
- Probability engine is Python-native.
- cEDHData was used only as reference material.
- No copied cEDHData source code exists in Codie.
- Simulator is lightweight target-access search, not a full Magic rules engine.
- Unsupported cards/actions are disclosed, not silently ignored.

Check schema constraints:
- simulation_batches has stable batch identity and config metadata.
- simulation_batch_results links correctly to batches.
- simulation_traces links correctly to batch/result records.
- simulation_line_reviews links to traces or stable trace/action identifiers.
- review_id is unique.
- repeated upsert by review_id does not duplicate rows.
- foreign keys or equivalent integrity checks prevent orphaned linked reviews.
- nullable challenge-only review linkage is intentional and tested.

Verify raw trace immutability by test or direct inspection:
- persist a simulator trace
- apply accepted and vetoed line reviews
- reload the original trace
- confirm trace payload/hash/action sequence is unchanged
- confirm reviews are stored separately

Confirm unsupported-card negative tests exist for:
- unsupported card in opening hand
- unsupported card needed for target access
- unsupported action inside a generated trace
- unsupported card included in review export or fixture payload
- unsupported rows included in reviewed accuracy summaries

Verify deterministic behavior:
- same deck + target + config + seed produces same opening hand
- same challenge config produces same displayed hand
- same batch config produces stable deterministic IDs where promised
- same review export input plus exported_at produces same bundle_id
- card input order is preserved intentionally or normalized explicitly

Check Challenge Mode:
- challenge hands are deterministic from seed/config
- Challenge Mode verifies the exact displayed hand
- user answers are recorded separately from simulator output
- unsupported cards/actions are reported
- Challenge Mode does not generate recommendation language

Check Line Review:
- reviews annotate simulator output and do not rewrite it
- accepted/rejected statuses and reason codes exist
- regression fixture export preserves action traces
- user review is not treated as tournament evidence

Check Reviewed Accuracy:
- accepted successful lines, rejected successful lines, failures, and unsupported rows are classified from stored simulator/review fields
- rates handle zero denominators
- filters are explicit
- summary generation is read-only

Check Review Export:
- export builders produce JSON-compatible payloads and Markdown strings
- export bundles use deterministic IDs and relative paths
- export code does not write files
- export code does not query DB
- export code does not create recommendation or tournament-evidence claims

Reject if:
- simulator output is used as recommendation output
- simulator output is treated as tournament evidence
- unsupported cards are silently ignored
- raw traces are mutated by reviews
- pure simulator modules import DB/repositories
- providers/analytics/recommendations import simulator internals unexpectedly
- cEDHData source code was copied into Codie
- export code writes files or reaches into DB directly
- schema omits required simulator tables or constraints
- deterministic replay is not stable where promised

Return:
PASS / PASS WITH REQUIRED FIXES / FAIL

Then list required fixes before Phase 14.
```
