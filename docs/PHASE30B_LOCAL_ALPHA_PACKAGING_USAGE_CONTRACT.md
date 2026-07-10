# Phase 30B - Local Alpha Packaging / Usage Documentation Contract

Status: documentation and packaging only

## Purpose

Phase 30B turns the accepted Phase 30A local alpha checklist into practical
usage documentation for a local user.

The output should answer:

```text
what is included
what is excluded
how to install
how to validate
which accepted local commands exist
what each command requires
what caveats remain
```

## Scope

Phase 30B may create or update documentation only:

```text
docs/PHASE30B_LOCAL_ALPHA_PACKAGING_USAGE_CONTRACT.md
docs/LOCAL_ALPHA_README.md
docs/LOCAL_ALPHA_COMMANDS.md
docs/LOCAL_ALPHA_KNOWN_CAVEATS.md
docs/LOCAL_ALPHA_VALIDATION_STEPS.md
docs/CHECKPOINT_PHASE30B_LOCAL_ALPHA_PACKAGING_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE30B_LOCAL_ALPHA_PACKAGING_PROMPT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Local Alpha Included Surface

The local alpha documentation may describe only accepted local workflows:

```text
schema bootstrap validation
unit test validation
fixture-backed provider parsing tests
Scryfall-backed card identity foundations
canonicalization and analytics foundations
evidence and evidence-fusion packet layers
Phase 13 simulator baseline and review outputs
Phase 14 simulator review export writer / CLI
Phase 15 deck memory listing / retrieval
Phase 24 local API boundary documentation
Phase 25 Evidence Fusion packets
Phase 26 Decision Intelligence boundary packets
Phase 27 Weight / Analysis Profile packets
Phase 28 Deck Health / Recommendation Output packets
Phase 29 recommendation report document / safe writer / CLI output chain
local share bundle and zip commands already present in accepted user-deck CLI
```

## Required Documentation

Phase 30B must produce:

```text
local alpha README
local alpha command guide
local alpha known caveats
local alpha validation steps
outside validation prompt
checkpoint report
```

## Command Documentation Rules

Command docs must:

```text
use python -m module invocation
state required inputs
state output behavior
state privacy caveats
state local database prerequisites when needed
state when an input must already be built by another accepted workflow
avoid advertising unsupported live backfills
avoid advertising final recommendation generation
avoid advertising SIM-R behavior
```

## Do Not Do In Phase 30B

```text
do not add production code
do not add schema
do not add repositories
do not add providers
do not add live network behavior
do not add LLM calls
do not add final UI
do not implement SIM-R
do not implement strategist mode
do not implement Tag Graph Lab
do not implement Moxfield Frequency Pool Builder
do not generate recommendations
do not weaken privacy or evidence boundaries
do not claim production readiness
```

## Acceptance Criteria

Phase 30B can pass only if:

```text
all usage docs are documentation-only
validation commands are accurate
supported commands match existing CLI modules
known caveats are visible
deferred features remain clearly deferred
no private local-only path is required for generic usage
no secrets are included
schema bootstrap passes
full Python test suite passes
git diff --check passes
no production code, tests, schema, dependency, or CI files are changed
```

## Next Packet

If Phase 30B passes, the recommended next packet is:

```text
Phase 30C - Local Alpha Release Candidate Checkpoint
```

Phase 30C should verify the release docs, packaging docs, validation status, and
handoff state together before any post-alpha feature work begins.

