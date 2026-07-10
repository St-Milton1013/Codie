# Phase 30A - Local Alpha Release Checklist Contract

Status: contract and release-readiness checklist only

## Purpose

Phase 30A defines the local alpha release gate for Codie. It does not add a
feature, change schema, implement SIM-R, or expand recommendation behavior.

The goal is to decide whether the current repository is coherent enough for a
local alpha handoff:

```text
fresh checkout
dependencies install
schema bootstrap validates
tests pass
CLI/report paths are documented
known caveats are explicit
roadmap and validation docs agree
future feature patches remain deferred
```

## Scope

Phase 30A may create or update documentation only:

```text
docs/PHASE30A_LOCAL_ALPHA_RELEASE_CHECKLIST_CONTRACT.md
docs/CHECKPOINT_PHASE30A_LOCAL_ALPHA_RELEASE_CHECKLIST_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE30A_LOCAL_ALPHA_RELEASE_CHECKLIST_PROMPT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/POST_PHASE24_PATCH_CONTRACT_BACKLOG.md
```

## Release Candidate Surface

The local alpha covers existing accepted local workflows only:

```text
schema bootstrap
provider fixture parsing tests
Scryfall-backed card identity layers
canonicalization and analytics foundations
evidence layers
simulator baseline through Phase 13
simulator review export writer through Phase 14
deck memory through Phase 15
chat/intelligence packet and local API boundaries through Phase 24
Evidence Fusion through Phase 25
Decision Intelligence boundary packets through Phase 26
Weight / Analysis Profiles through Phase 27
Deck Health / Recommendation Output packet models through Phase 28
Recommendation report document / writer / CLI output chain through Phase 29
```

## Required Checklist

The Phase 30A checkpoint must verify:

```text
repo is on main and clean before edits
remote is configured
CI workflow exists
schema bootstrap command passes
full Python test suite passes
git diff --check passes
active roadmap and validation indexes agree
continuity handoff points to Phase 30A
release blockers are explicit
known caveats are explicit
SIM-R remains deferred
Jin-Gitaxias / strategist mode remains deferred
Tag Graph Lab remains deferred
Moxfield Frequency Pool Builder remains deferred
mobile report delivery extensions remain deferred
no schema changes are introduced
no production code changes are introduced
no new provider/live network behavior is introduced
no recommendation generation is introduced
```

## Local Alpha Acceptance Criteria

Phase 30A can pass only if:

```text
python scripts/check_schema.py passes
python -m unittest discover -s tests passes
git diff --check passes
current status docs identify Phase 30A as current gate
next phase is either Phase 30B local alpha packaging/docs or a separately accepted contract
all release caveats are visible
no roadmap-only patch is accidentally promoted into implementation
```

## Required Outside Validation

Outside validation must inspect the Phase 30A contract, checkpoint, active
roadmap, validation status, continuity handoff, CI workflow, schema checker,
and test output.

## Do Not Do In Phase 30A

```text
do not add production code
do not add schema
do not add repositories
do not add providers
do not add live network calls
do not add UI
do not add LLM calls
do not implement SIM-R
do not implement Jin-Gitaxias / strategist mode
do not implement Tag Graph Lab
do not implement Moxfield Frequency Pool Builder
do not implement new mobile delivery integrations
do not generate recommendations
do not loosen evidence or privacy boundaries
```

## Next Packet

If Phase 30A passes, the recommended next packet is:

```text
Phase 30B - Local Alpha Packaging / Usage Documentation
```

Phase 30B should remain documentation and packaging focused unless a separate
implementation contract is accepted.
