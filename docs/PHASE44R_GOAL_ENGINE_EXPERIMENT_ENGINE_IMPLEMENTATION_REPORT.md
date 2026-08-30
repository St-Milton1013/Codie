# Phase44R Goal Engine Experiment Engine Implementation Report

Status: local implementation packet; not externally validated or accepted

## Scope

Phase44R implements only the accepted Phase44Q Goal Experiment Engine v1
contract. It provides pure, immutable, caller-input records, exact-field
parsers, canonical serialization, semantic hashes, reference validation, and
revision validation. It is an in-memory planning and observation record
surface, not an execution or authority surface.

## Changed Files

```text
codie/goal_engine/experiment.py
tests/test_goal_engine_experiment.py
docs/PHASE44R_GOAL_ENGINE_EXPERIMENT_ENGINE_IMPLEMENTATION_REPORT.md
```

## Implemented Boundary

The implementation adds the exact Phase44Q v1 schemas for experiment
questions, hypotheses, inputs, boundaries, stop criteria, cleanup plans,
approval references, observations, outcomes, experiment references, and goal
experiments. It preserves caller-supplied expected observations separately
from caller-supplied observations and outcome interpretations. It does not
convert any record into causality, truth, success, permission, approval, or
authority.

`build_goal_experiment(...)` consumes only explicit caller values and a
caller-supplied UTC `as_of` value. It requires an explicit question,
hypothesis, bounded inputs, boundaries, stop criteria, cleanup plan, rollback
analysis, limitations, and evidence links. Validation rejects duplicate IDs,
dangling evidence and observation references, malformed hashes, mutable
collections, revision rewrites, and revision deletions. Revision one cannot
name a predecessor; later revisions require the immediately prior semantic
hash and preserve the immutable core while allowing only append-only approval
references and observations.

Approval references and observations record caller-supplied statements only.
They neither verify a human decision nor prove execution, causality, safety,
or success. Stop criteria, cleanup plans, rollback analyses, and validation
requirement identifiers remain declarations; the implementation does not
detect a stop condition, execute cleanup or rollback, or run validation.

## Explicit Non-Goals

This packet does not discover inputs, retrieve information, create or revise a
Goal Contract, grant authority, execute an experiment, run validation,
interpret a result as permission, persist data, access a filesystem,
repository, environment, process, network, provider, model, clock, UUID,
random source, UI, CLI, API, scheduler, worker, or Stream Deck integration.

Hard evidence boundaries remain unchanged:

```text
fact != human decision != policy != authority
proposal != approval reference != execution permission
hypothesis != expected observation != observed fact != outcome interpretation
stop criterion != stop detection != stopping an experiment
cleanup plan != cleanup execution != cleanup success
rollback analysis != rollback execution or recovery success
validation requirement != validation execution or result
```

Theory and theory-skill review gates remain external and mandatory. Official
Scryfall card truth, user-initiated public Moxfield inputs, Hareruya
tournament-only provenance, local-first behavior, zero-cost behavior, and
supplemental-only Stream Deck policy are unchanged.

## Local Verification

The focused Phase44R test suite covers canonical round trips, exact-field
parsing, schema and vocabulary validation, evidence and observation reference
resolution, required boundary coverage, revision-one and immediate
hash-linked revision rules, append-only revision protection, immutable record
fields, builder validation, and import boundaries.

Schema bootstrap, focused tests, lint, and the configured full suite were run
locally. The full suite has its existing Windows symbolic-link skip. A focused
Mypy invocation reaches 13 pre-existing errors in `state_engine.py`; it reports
no error in the new experiment module.

The implementation is not accepted until it has an exact-SHA pull-request
artifact with the required validators and a separate human merge approval.
