# Phase 30B - Local Alpha Packaging / Usage Documentation Planning Draft

Status: superseded by `docs/PHASE30B_LOCAL_ALPHA_PACKAGING_USAGE_CONTRACT.md`

Phase 30A outside validation returned PASS. Phase 30B was converted from this
planning draft into local alpha packaging / usage documentation.

## Purpose

Phase 30B should turn the accepted local alpha checklist into a practical local
handoff package:

```text
how to install
how to validate
how to run supported local commands
how to export local reports
what is included
what is excluded
what caveats remain
```

This packet should be documentation and packaging focused. It should not add new
runtime behavior unless a separate implementation contract is accepted.

## Recommended Files

```text
docs/PHASE30B_LOCAL_ALPHA_PACKAGING_USAGE_CONTRACT.md
docs/LOCAL_ALPHA_README.md
docs/LOCAL_ALPHA_COMMANDS.md
docs/LOCAL_ALPHA_KNOWN_CAVEATS.md
docs/LOCAL_ALPHA_VALIDATION_STEPS.md
docs/CHECKPOINT_PHASE30B_LOCAL_ALPHA_PACKAGING_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE30B_LOCAL_ALPHA_PACKAGING_PROMPT.md
```

## Candidate User Flow

```text
1. clone or pull repository
2. install Python dependencies
3. run schema bootstrap check
4. run test suite
5. inspect accepted local capabilities
6. run supported CLI examples using local fixtures or existing local data
7. generate local JSON / Markdown recommendation-output report files from a
   prepared RecommendationOutputBundle JSON
8. review known caveats and deferred features
```

## Required Local Alpha Docs

### Install

```text
Python version expectation
dependency install command
where to run commands from
how to verify Git branch / commit
```

### Validate

```text
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

### Supported Local Workflows

```text
schema bootstrap validation
unit test validation
fixture-backed provider parsing
deck memory read/listing where local DB exists
simulator baseline objects and review exports
recommendation output packet serialization
recommendation report JSON / Markdown writer
recommendation output CLI wrapper
local report bundle artifacts from accepted export paths
```

### Explicit Non-Goals

```text
no production deployment
no hosted service
no final UI
no live broad backfill
no SIM-R implementation
no strategist mode
no Tag Graph Lab
no Moxfield Frequency Pool Builder implementation
no final autonomous recommendation engine
no recommendations from raw provider data
```

## Required Caveats

```text
Hareruya live access can encounter AWS WAF.
Some workflows require a populated local SQLite database.
Some CLI examples require prepared bundle JSON or local fixture data.
Phase 13 simulator baseline exists, but SIM-R full rules revision is deferred.
Mobile delivery remains optional and contract-gated.
No roadmap-only patch is alpha-supported until separately contracted.
```

## Acceptance Criteria

Phase 30B can pass only if:

```text
usage docs are accurate
commands are copy/paste friendly
no unsupported workflow is advertised as alpha-ready
known caveats are visible
deferred features remain clearly deferred
validation commands pass
docs do not include private local paths except where explicitly marked as local
docs do not include secrets
```

## Do Not Do In Phase 30B

```text
do not implement new production code
do not add schema
do not add repositories
do not add providers
do not add live network behavior
do not add LLM calls
do not add final UI
do not implement SIM-R
do not implement strategist mode
do not generate recommendations
do not weaken privacy or evidence boundaries
```
