# Phase 31B - SIM-R Current Simulator Freeze Contract

Status: contract/checkpoint packet only

## Purpose

Phase 31B freezes the current Phase 13/14 simulator implementation as the
baseline that future SIM-R work must preserve.

This phase does not implement SIM-R. It records the current simulator surfaces,
validation commands, compatibility expectations, and rejection rules for future
SIM-R phases.

## Authorized Scope

```text
simulator freeze contract
current simulator surface inventory
test inventory
compatibility requirements
outside validation packet
checkpoint documentation
active roadmap/status updates
```

## Not Authorized

```text
production simulator changes
schema changes
repository changes
database reads or writes
Forge integration
Forge dependency installation
behavior module implementation
state engine implementation
resource ledger implementation
compound target implementation
trace v2 implementation
paired simulation implementation
LLM behavior generation
recommendation generation
UI work
live network calls
```

## Frozen Simulator Runtime Surfaces

Future SIM-R work must preserve the behavior of these current runtime modules
unless a later compatibility migration contract explicitly approves a versioned
change:

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
codie/probability_engine/review_export_writer.py
codie/probability_engine/__init__.py
codie/cli/simulation_review.py
```

## Frozen Database Surfaces

Future SIM-R work must preserve existing simulation storage compatibility:

```text
codie/db/schema/simulation.sql
codie/db/repositories/simulation.py
```

Existing simulation rows and historical traces must not be silently
reinterpreted.

## Frozen Fixture / Reference Surfaces

The following fixtures and references remain validation inputs, not production
dependencies:

```text
reference/cedhdata_simulator/
reference/rhystic_simulator_traces/
tests/fixtures/probability_engine/
docs/CEDHDATA_SIMULATOR_REFERENCE_CAPTURE_MANIFEST.md
```

Codie must not copy external simulator source code into production.

## Frozen Behavior Guarantees

Future SIM-R work must preserve:

```text
deterministic seeded shuffle
deterministic opening-hand generation
current deck parser behavior
current target condition parsing behavior
current London mulligan policy behavior
current target-access search results for existing fixtures
current batch runner result shape
current challenge mode reproducibility
current line review annotation behavior
current reviewed accuracy summary behavior
current review export payload behavior
current review export writer safety behavior
current simulation persistence compatibility
unsupported-card reporting
raw trace immutability
evidence-only simulator posture
```

## Future Compatibility Rule

If SIM-R introduces new state, trace, target, or behavior formats, it must add
versioned formats rather than silently replacing historical formats.

Required future version labels:

```text
simulator_version
trace_version
card_model_version
mulligan_policy_version
target_condition_version
behavior_profile_version
```

## Required Regression Test Groups

The current test suite must remain green before any SIM-R implementation phase:

```text
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
tests/test_probability_engine_review_export_writer.py
tests/test_cli_simulation_review.py
```

## Reject Future SIM-R Work If

Reject future SIM-R work if it:

```text
breaks existing simulator tests without an accepted compatibility migration
silently changes historical trace meaning
silently ignores unsupported cards or unsupported actions
treats simulator output as tournament evidence
generates recommendations from simulator output
adds Forge runtime execution
adds LLM-generated executable behavior
rewrites persistence without migration and replay rules
changes CLI output contracts without a versioned contract
```

## Gate

Phase 31C is blocked until Phase 31B outside validation returns PASS or PASS
WITH REVIEW NOTES.

