# Codie Local Alpha README

Status: local alpha documentation

Codie local alpha is a local, evidence-first project state through Phase 30B.
It is meant for local validation and local report workflows, not production
deployment.

## What This Alpha Includes

```text
schema bootstrap validation
unit tests and architecture boundary tests
fixture-backed provider parsing coverage
card identity, canonicalization, analytics, evidence, and evidence-fusion foundations
Phase 13 simulator baseline and review records
Phase 14 simulator review export writer / CLI
Phase 15 deck memory listing and retrieval
Phase 24 chat/intelligence local API boundary
Phase 25 Evidence Fusion packets
Phase 26 Decision Intelligence boundary packets
Phase 27 Weight / Analysis Profile packets
Phase 28 Deck Health / Recommendation Output packets
Phase 29 recommendation report JSON / Markdown writer and CLI wrapper
local share bundle and zip packaging commands from the accepted user-deck CLI
```

## What This Alpha Does Not Include

```text
production deployment
hosted service
final UI
live broad provider backfill
SIM-R full rules simulator revision
Jin-Gitaxias / strategist mode
Tag Graph Lab
Moxfield Frequency Pool Builder implementation
autonomous final recommendation generation
recommendations from raw provider data
```

## Requirements

```text
Git
Python 3.12
PowerShell, Windows Terminal, or another shell
local repository checkout
optional local SQLite database for DB-backed workflows
```

## Install

From the repository root:

```powershell
python -m pip install -r requirements.txt
```

For development tools:

```powershell
python -m pip install -r requirements-dev.txt
```

## Validate

From the repository root:

```powershell
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

Expected:

```text
Schema bootstrap check passed.
OK (skipped=1)
git diff --check exits cleanly
```

## Supported Command Families

See:

```text
docs/LOCAL_ALPHA_COMMANDS.md
```

Command families currently documented:

```text
recommendation output report rendering
simulation review export bundle writing
user deck local workflow commands
user deck memory listing and retrieval
local share bundle build / serve / zip commands
```

## Known Caveats

See:

```text
docs/LOCAL_ALPHA_KNOWN_CAVEATS.md
```

Key caveats:

```text
Hareruya live access can encounter AWS WAF.
Some workflows require a populated local Codie SQLite database.
Some commands require already-built JSON bundle inputs.
SIM-R is deferred.
Mobile delivery remains optional and contract-gated.
Roadmap patches are not alpha features until separately contracted.
```

## Privacy And Evidence Rules

```text
User deck text is local user data.
Raw provider payloads are not report inputs.
Recommendation output must flow through Evidence Fusion and Decision Intelligence boundaries.
Simulator output remains simulator evidence and is not tournament evidence.
No alpha command should generate recommendations directly from raw provider data.
```

