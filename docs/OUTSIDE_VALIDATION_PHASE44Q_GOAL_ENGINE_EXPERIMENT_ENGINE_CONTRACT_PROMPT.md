# Outside Validation — Phase44Q Goal Experiment Engine Contract

Validate the exact pull-request head from a clean checkout.

## Validation Tuple

```text
phase_id: Phase44Q
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase44R
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

## Review Files

```text
docs/PHASE44Q_GOAL_ENGINE_EXPERIMENT_ENGINE_CONTRACT.md
docs/CHECKPOINT_PHASE44Q_GOAL_ENGINE_EXPERIMENT_ENGINE_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE44Q_GOAL_ENGINE_EXPERIMENT_ENGINE_CONTRACT_PROMPT.md
docs/PHASE44P_GOAL_ENGINE_CHANGE_IMPACT_ENGINE_CHECKPOINT_FREEZE_CONTRACT.md
docs/GOAL_ENGINE_V1_SPEC.md
docs/GOAL_ENGINE_IMPLEMENTATION_PROGRAM_V1.md
codie/goal_engine/foundation.py
codie/goal_engine/state_engine.py
codie/goal_engine/health.py
codie/goal_engine/idea_ledger.py
codie/goal_engine/impact.py
docs/CODIE_V2_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Required Review

Confirm that Phase44Q:

```text
is implementation-contract-only
records exact Phase44P acceptance evidence
defines only a future pure immutable caller-input experiment-planning engine
requires explicit question, hypothesis, inputs, boundaries, stop criteria,
cleanup, rollback, approval references, evidence, limitations, observations,
outcomes, and revision history
keeps proposal, approval reference, execution permission, expected observation,
observation, and outcome interpretation separate
does not treat human decision references as proof of approval or permission
does not claim an observation proves execution, causality, success, or safety
keeps cleanup/rollback/validation plans separate from their execution and result
rejects invented evidence, hidden raw content, mutable collections, dangling
references, cross-owner private leakage, and revision rewrite or deletion
contains no runner, executor, scheduler, command, worktree, provider, network,
filesystem, database, model, clock, environment, telemetry, persistence, UI,
CLI, API, service, worker, queue, notification, or Stream Deck behavior
contains no score, rank, priority, recommendation, decision, Goal Contract,
approval, autonomous experiment authority, work order, or authority result
preserves Theory and theory-skill review, Rules/Corrections boundaries, Scryfall
truth, Moxfield/pasted-deck user scope, Hareruya tournament-only provenance,
supplemental-only Stream Deck, local-first privacy and zero-cost rules
keeps Phase44R implementation blocked pending this exact contract acceptance
changes exactly the eight authorized Phase44Q documentation files
does not modify production code, tests, schema, dependencies, workflows,
active scope, validators, providers, UI, CLI, or constitutions
```

Reject the packet if it authorizes an experiment, silently converts a planned
or observed item into truth or permission, weakens hard evidence, bypasses a
review gate, expands source scope, or advances any later roadmap phase.

## Commands

```text
git diff --check
python scripts/check_schema.py
python -m unittest tests.test_goal_engine_impact -v
python -m unittest discover -s tests -p "test_*.py"
```

## Allowed Verdicts

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Phase44R remains blocked until `PASS` or `PASS WITH REVIEW NOTES` and human
merge.
