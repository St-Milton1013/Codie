# Codie Local Alpha Release Notes

Status: local alpha release candidate notes

## Release Status

```text
Phase 30A Local Alpha Release Checklist: PASS
Phase 30B Local Alpha Packaging / Usage Documentation: PASS
Phase 30C Local Alpha Release Candidate Checkpoint: PASS
Phase 30D Local Alpha Tag / Release Notes / Handoff Finalization: PASS
```

This is a local alpha. It is not a production release.

## Included Capabilities

```text
schema bootstrap validation
unit and architecture boundary tests
fixture-backed provider parser coverage
Scryfall-backed card identity foundations
canonicalization foundations
analytics foundations
evidence layers
Evidence Fusion packets
Decision Intelligence boundary packets
Weight / Analysis Profile packets
Deck Health / Recommendation Output packets
recommendation report document serialization
safe recommendation report writer
recommendation output CLI wrapper
Phase 13 simulator baseline
simulator review export writer / CLI
deck memory listing and retrieval
local alpha validation docs
local alpha command docs
local alpha caveat docs
```

## Explicit Non-Goals

```text
production deployment
hosted service
final UI
live broad provider backfill
SIM-R full rules simulator revision
Jin-Gitaxias / strategist mode
Tag Graph Lab
Moxfield Frequency Pool Builder implementation
mobile delivery integrations as default behavior
autonomous final recommendation generation
recommendations from raw provider data
```

## Validation

Latest local release-candidate validation:

```text
python scripts/check_schema.py
Schema bootstrap check passed.

python -m unittest discover -s tests
Ran 797 tests in 3.670s
OK (skipped=1)

git diff --check
passed

production touch check:
no codie/tests/scripts/ui/schema/dependency/CI changes
```

Environment note:

```text
The bundled Python runtime required requirements.txt to be installed before
running the full suite because qrcode and bs4 were missing.
```

## Known Caveats

```text
Hareruya live access can encounter AWS WAF.
Some workflows require a populated local Codie SQLite database.
Some commands require already-built JSON bundle inputs.
SIM-R is deferred.
Mobile delivery remains optional and contract-gated.
Roadmap patches are not alpha features until separately contracted.
```

## Recommended Tag

```text
local-alpha-0.1.0
```

Phase 30D outside validation returned PASS. The tag is authorized.

## Next Post-Alpha Choices

After tagging, choose one post-alpha lane contract-first:

```text
SIM-R contract
Tag Graph Lab contract
Moxfield Frequency Pool Builder contract
Jin-Gitaxias / strategist mode boundary contract
advanced local UI/dashboard planning
mobile/local report delivery extension planning
```
