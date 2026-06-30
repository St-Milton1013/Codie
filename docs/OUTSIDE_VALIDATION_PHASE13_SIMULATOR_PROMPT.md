# Outside Validation Prompt - Phase 13 Simulator Track

Use this prompt with an outside reviewer.

```text
Validate Codie Phase 13 Simulator Track against CODIE_V1_CONSTITUTION.md and the Phase 13 contracts/reports.

Review these files:

docs/CHECKPOINT_PHASE13_SIMULATOR_TRACK_REPORT.md
docs/PHASE13_SIMULATOR_CONTRACT_REFRESH.md
docs/PHASE13A_CEDHDATA_REFERENCE_EXTRACTION_AND_CORE_MODEL_DESIGN.md
docs/PHASE13B_PROBABILITY_ENGINE_CORE_MODELS_CONTRACT.md
docs/PHASE13C_SIMULATOR_CARD_DEFINITION_MANAGER_CONTRACT.md
docs/PHASE13E_DECK_AND_TARGET_PARSER_CONTRACT.md
docs/PHASE13G_SEEDED_SHUFFLE_AND_OPENING_HAND_CONTRACT.md
docs/PHASE13I_MULLIGAN_POLICY_CONTRACT.md
docs/PHASE13K_TARGET_ACCESS_SEARCH_CONTRACT.md
docs/PHASE13M_MONTE_CARLO_BATCH_RUNNER_CONTRACT.md
docs/PHASE13O_SIMULATOR_PERSISTENCE_CONTRACT.md
docs/PHASE13Q_CHALLENGE_MODE_CONTRACT.md
docs/PHASE13S_CHALLENGE_LINE_REVIEW_CONTRACT.md
docs/PHASE13U_CHALLENGE_LINE_REVIEW_PERSISTENCE_CONTRACT.md
docs/PHASE13W_REVIEWED_SIMULATOR_ACCURACY_CONTRACT.md
docs/PHASE13Y_SIMULATION_REVIEW_EXPORT_CONTRACT.md
docs/PHASE13Z_SIMULATION_REVIEW_EXPORT_IMPLEMENTATION_REPORT.md

Check:

1. Simulator architecture
- Probability engine is Python-native.
- cEDHData was used only as reference material.
- No copied cEDHData source code exists in Codie.
- Simulator is lightweight target-access search, not a full Magic rules engine.
- Unsupported cards/actions are disclosed, not silently ignored.

2. Boundaries
- Providers do not import simulator modules.
- Pure simulator modules do not import DB/repositories.
- Persistence adapters are the only probability_engine modules that import SimulationRepository.
- No simulator code imports analytics, recommendations, ingestion, cards, providers, requests, or httpx.
- Raw SQL remains inside codie/db.

3. Persistence
- simulation_batches, simulation_batch_results, simulation_traces persist batch results.
- simulation_line_reviews persists annotations only.
- Batch persistence is atomic.
- Line review persistence is atomic.
- Raw simulator traces are not mutated by line review persistence.
- Repeated line review upsert by review_id does not duplicate rows.

4. Challenge Mode
- Challenge hands are deterministic from seed/config.
- Challenge Mode verifies the exact displayed hand.
- User answers are recorded separately from simulator output.
- Unsupported cards/actions are reported.
- Challenge Mode does not generate recommendation language.

5. Line Review
- Reviews annotate simulator output and do not rewrite it.
- Accepted/rejected statuses and reason codes exist.
- Regression fixture export preserves action traces.
- User review is not treated as tournament evidence.

6. Reviewed Accuracy
- Accepted successful lines, rejected successful lines, failures, and unsupported rows are classified from stored simulator/review fields.
- Rates handle zero denominators.
- Filters are explicit.
- Summary generation is read-only.

7. Review Export
- Export builders produce JSON-compatible payloads and Markdown strings.
- Export bundles use deterministic IDs and relative paths.
- Export code does not write files.
- Export code does not query DB.
- Export code does not create recommendation or tournament-evidence claims.

8. Tests
- Confirm reported command:
  python -m unittest discover -s tests
- Confirm reported result:
  Ran 487 tests
  OK (skipped=1)
- Identify missing tests needed before Phase 14.

Reject if:
- simulator output is used as recommendation output
- simulator output is treated as tournament evidence
- unsupported cards are silently ignored
- raw traces are mutated by reviews
- pure simulator modules import DB/repositories
- providers/analytics/recommendations import simulator internals unexpectedly
- cEDHData source code was copied into Codie
- export code writes files or reaches into DB directly

Return:
PASS / PASS WITH REQUIRED FIXES / FAIL

Then list required fixes before Phase 14.
```
