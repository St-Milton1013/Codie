# Checkpoint - Phase 13 Simulator Track Report

## Verdict

```text
Phase 13 Simulator Track Internal Checkpoint: PASS
Status: Ready for outside validation before Phase 14
```

This is an internal checkpoint, not external proof. Phase 14 should not start
until the outside validation packet is reviewed and accepted.

## Scope Reviewed

This checkpoint covers the simulator/probability work from Phase 13 through
Phase 13Z:

```text
Phase 13 Simulator Contract Refresh
Phase 13A cEDHData Reference Extraction And Core Model Design
Phase 13B Probability Engine Core Models
Phase 13C Simulator Card Definition Manager Contract
Phase 13D Simulator Card Definition Manager Implementation
Phase 13E Deck And Target Parser Contract
Phase 13F Deck And Target Parser Implementation
Phase 13G Seeded Shuffle And Opening Hand Contract
Phase 13H Seeded Shuffle And Opening Hand Implementation
Phase 13I Mulligan Policy Contract
Phase 13J Mulligan Policy Implementation
Phase 13K Target Access Search Contract
Phase 13L Target Access Search MVP Implementation
Phase 13M Monte Carlo Batch Runner Contract
Phase 13N Monte Carlo Batch Runner Implementation
Phase 13O Simulator Persistence Contract
Phase 13P Simulator Persistence Implementation
Phase 13Q Challenge Mode Contract
Phase 13R Challenge Mode Implementation
Phase 13S Challenge Line Review Contract
Phase 13T Challenge Line Review Implementation
Phase 13U Challenge Line Review Persistence Contract
Phase 13V Challenge Line Review Persistence Implementation
Phase 13W Reviewed Simulator Accuracy Contract
Phase 13X Reviewed Simulator Accuracy Implementation
Phase 13Y Simulation Review Export Contract
Phase 13Z Simulation Review Export Implementation
```

## What Exists Now

```text
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
```

## Architecture Summary

The Phase 13 simulator track is implemented as a lightweight, deterministic
target-access simulator stack.

Pure simulator layers:

```text
models
card definition manager
deck/target parser
seeded shuffle/opening hands
mulligan policy
target access search
Monte Carlo batch runner
Challenge Mode
line review annotation models
reviewed accuracy summaries
review export payload builders
```

Persistence adapters:

```text
probability_engine.persistence -> SimulationRepository
probability_engine.line_review_persistence -> SimulationRepository
```

Read-only repository readers:

```text
probability_engine.reviewed_accuracy -> SimulationRepository
```

`reviewed_accuracy.py` should remain pure when possible. If it imports
`SimulationRepository`, it is limited to read-only summary generation and must
not mutate simulator, review, analytics, recommendation, evidence, source,
provider, or user tables.

Repository-owned tables:

```text
simulation_batches
simulation_batch_results
simulation_traces
simulation_line_reviews
```

## Boundary Findings

The simulator track preserves the intended boundaries:

```text
providers do not participate
analytics are not written
recommendations are not generated
source/provider tables are not read
Scryfall/card lookup is not called by simulator modules
raw simulator traces are immutable
line reviews annotate simulator output instead of rewriting it
reviewed accuracy is QA metadata only
review exports are pure payload builders and do not write files
```

## cEDHData Reference Handling

The cEDHData files were used only as reference material.

Codie does not copy cEDHData source code into the project. The implementation is
Python-native and uses local architecture decisions:

```text
clean card behavior overlay model
unsupported-card reporting
deterministic shuffle/seed model
bounded target-access search
structured trace format
review annotation layer
```

## Persistence Summary

Simulator batch persistence writes:

```text
simulation_batches
simulation_batch_results
simulation_traces
```

Line review persistence writes:

```text
simulation_line_reviews
```

Atomicity is required and tested for simulator batch persistence and line review
persistence. Failed writes leave no partial simulator batch or line review rows.

## Evidence And Recommendation Safety

Simulator outputs remain simulator evidence only. They are not tournament
evidence and do not feed final recommendation output directly.

Forbidden behavior remains absent:

```text
no direct play/cut instruction output
no strategic claims from simulator results
no recommendation output
no analytics writes
no Evidence Stack writes from simulation
no user review treated as tournament evidence
```

## Review / Challenge Mode

Challenge Mode now supports:

```text
deterministic challenge prompt generation
exact opening hand verification
user answer recording
user answer comparison
unsupported card/action disclosure
```

Line review now supports:

```text
accepted and veto statuses
reason codes
affected cards/actions
deterministic review IDs
regression fixture export
line review persistence
reviewed accuracy summaries
JSON/Markdown export payloads
```

## Validation Performed

Full suite:

```text
python -m unittest discover -s tests

Ran 487 tests in 3.145s

OK (skipped=1)
```

Representative focused tests added across Phase 13:

```text
test_probability_engine_models.py
test_probability_engine_card_definition_manager.py
test_probability_engine_deck_parser.py
test_probability_engine_shuffle.py
test_probability_engine_mulligan.py
test_probability_engine_search.py
test_probability_engine_batch.py
test_probability_engine_persistence.py
test_probability_engine_challenge_mode.py
test_probability_engine_line_review.py
test_probability_engine_line_review_persistence.py
test_probability_engine_reviewed_accuracy.py
test_probability_engine_review_export.py
```

Static checks:

```text
git diff --check
```

passed.

Boundary scans:

```text
review_export DB/provider/analytics/recommendation scan: no matches
review_export raw SQL scan: no matches
review_export strategic-language scan: no matches
```

## Remaining Caveats

```text
Challenge Mode has no UI yet.
Simulator review exports are payload builders only; no file writer yet.
Simulator behavior coverage is still intentionally narrow.
Unsupported-card behavior must remain visible, never silently ignored.
Simulation results remain QA/training metadata, not tournament evidence.
Broad simulator accuracy depends on future card behavior overlay expansion.
```

## Recommendation

```text
Proceed to outside validation for Phase 13.
Do not start Phase 14 until the simulator track review is accepted.
```

The outside validation prompt requires documentation review, implementation-file
review, schema/repository inspection, clean-checkout test execution, import
boundary scans, raw trace immutability checks, unsupported-card negative test
review, and deterministic replay checks.
