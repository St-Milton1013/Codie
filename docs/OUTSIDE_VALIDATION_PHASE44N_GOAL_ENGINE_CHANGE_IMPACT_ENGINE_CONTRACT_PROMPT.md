# Outside Validation - Phase 44N Goal Engine Change / Impact Engine Contract

Validate the exact PR head from a clean checkout.

## Validation Tuple

```text
phase_id: Phase44N
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase44O
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

## Review Files

```text
docs/PHASE44N_GOAL_ENGINE_CHANGE_IMPACT_ENGINE_CONTRACT.md
docs/CHECKPOINT_PHASE44N_GOAL_ENGINE_CHANGE_IMPACT_ENGINE_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE44N_GOAL_ENGINE_CHANGE_IMPACT_ENGINE_CONTRACT_PROMPT.md
docs/PHASE44M_GOAL_ENGINE_FINDINGS_IDEA_LEDGER_CHECKPOINT_FREEZE_CONTRACT.md
docs/GOAL_ENGINE_V1_SPEC.md
docs/GOAL_ENGINE_IMPLEMENTATION_PROGRAM_V1.md
codie/goal_engine/foundation.py
codie/goal_engine/state_engine.py
codie/goal_engine/health.py
codie/goal_engine/idea_ledger.py
tests/test_goal_engine_foundation.py
tests/test_goal_engine_state_engine.py
tests/test_goal_engine_health.py
tests/test_goal_engine_idea_ledger.py
docs/CODIE_V2_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Required Review

Confirm Phase44N:

```text
is implementation-contract-only
records exact artifact-backed Phase44M acceptance evidence
defines only the future pure immutable caller-input Change / Impact Engine v1
uses exact schemas, vocabularies, existing Foundation evidence/Goal/rollback
records, and Ledger entity references without forked authority or evidence types
keeps direct, indirect, possible, affected, untouched, unknown, expected, and
observed dimensions distinct
makes dependency, privacy, security, zero-cost, manual, operational, validation,
rollback, assumptions, limitations, conflicts, and history visible
keeps explicit untouched subjects as expectations rather than guarantees
keeps rollback analysis separate from execution or rollback success
keeps validation requirements separate from validation execution and results
keeps historical attempt comparison bounded, explicit, and non-retry-authorizing
rejects invented evidence, hidden raw content, mutable collections, dangling
references, cross-owner private leakage, and revision rewrite/deletion
contains no impact score, aggregate risk score, rank, priority, recommendation,
decision, work order, Goal Contract, approval, execution, or authority result
contains no filesystem, database, repository, provider, network, model, clock,
process, environment, telemetry, analytics, persistence, notification, UI,
CLI, API, service, worker, queue, scheduler, or Stream Deck behavior
preserves local-first, private, zero-cost, standard-library, caller-input-only behavior
preserves Theory and theory-skill review gates, Rules and Corrections boundaries,
official Scryfall truth, Moxfield/pasted-deck user scope, Hareruya tournament-only
provenance, supplemental-only Stream Deck, and human governance gates
keeps Experiment, Decision, Corpus, Validator, Shadow, Stage 1+ authority,
Build Graph, and CCPM work deferred
changes exactly the eight authorized Phase44N documentation files
does not modify production code, tests, schema, repositories, dependencies,
workflows, active scope, validators, providers, UI, CLI, or either constitution
records the exact Phase44N to Phase44O validation tuple
keeps Phase44O implementation-only and blocked until Phase44N acceptance
```

Reject the packet if it infers scope or causality, creates storage or authority,
conflates expected impact with outcome, silently turns untouched into safe,
turns historical attempts into automatic retries, weakens hard evidence,
expands Hareruya beyond tournament provenance, adds a Stream Deck control path,
bypasses Theory review, or authorizes a later roadmap phase early.

## Commands

```text
git diff --check
python scripts/check_schema.py
python -m unittest tests.test_goal_engine_idea_ledger -v
python -m unittest tests.test_goal_engine_foundation tests.test_goal_engine_state_engine tests.test_goal_engine_health tests.test_goal_engine_idea_ledger -v
python -m unittest discover -s tests -p "test_*.py"
```

## Allowed Verdicts

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Phase44O remains blocked until `PASS` or `PASS WITH REVIEW NOTES` and human
merge.
