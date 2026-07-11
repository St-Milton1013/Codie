# Post-Phase 31 Deferred Implementation Priority Plan

Status: planning-only

## Purpose

After Phase 31 closes, Codie should prioritize deferred implementations in a
single deliberate order instead of pulling from patch notes opportunistically.

This document does not authorize implementation, schema changes, repository
changes, provider changes, LLM calls, UI work, file writing, simulator runtime
integration, or recommendation output.

Every item below remains contract-first.

## Current Rule

```text
Finish the active Phase 31 validation chain first.
Then prioritize deferred implementations from this plan.
```

Phase 31 work remains governed by the active SIM-R contracts and validation
gates. Post-31 work must not begin until the Phase 31 closing checkpoint is
accepted.

## Priority Framework

Deferred implementations are ranked by:

```text
1. architectural dependency value
2. risk reduction
3. ability to unlock multiple later features
4. local-alpha usefulness
5. bounded implementation surface
6. validation clarity
```

Lower-risk foundation work should happen before UI, chat, recommendations, or
strategic output.

## Priority 0 - Close Phase 31 Cleanly

Goal:

```text
finish the SIM-R foundation chain without runtime sprawl
```

Likely remaining Phase 31 packets:

```text
Phase 31P - SIM-R behavior transition wiring implementation contract
Phase 31Q - SIM-R behavior transition wiring implementation
Phase 31R - SIM-R foundation checkpoint / freeze
```

Rules:

```text
no full rules engine
no old simulator replacement
no Monte Carlo integration
no recommendation output
no DB persistence unless separately contracted
```

## Priority 1 - Scryfall Bulk Data Foundation

Why:

Scryfall is Class 0 card truth. Bulk snapshots reduce live API dependence,
improve reproducibility, and support Tagger, migration monitoring, card
behavior coverage, and future analysis profiles.

First contract should define:

```text
bulk data discovery
snapshot manifest
atomic local snapshot storage
raw payload preservation
card identity normalization
schema/repository impact
migration compatibility checks
offline lookup behavior
```

Do not yet:

```text
replace existing card lookup behavior
rewrite Scryfall provider logic
add live network dependence to tests
infer recommendations
```

## Priority 2 - Scryfall Migration Monitoring

Why:

Card identity drift can corrupt every downstream layer. Migration monitoring
should detect Scryfall ID/name/oracle changes before analytics or simulator
behavior quietly rot.

First contract should define:

```text
snapshot-to-snapshot diff reports
renamed card detection
oracle ID continuity checks
Scryfall ID replacement detection
manual review queue
replay-safe migration records
```

## Priority 3 - Scryfall Tagger Functional Ontology

Why:

Tag Graph Lab, frequency pools, mana-sink combo interpretation, and functional
deck comparison all need stable functional tags mapped to canonical card
identity.

First contract should define:

```text
Tagger source capture
functional tag namespaces
oracle_id mapping
artwork tag exclusion
provenance
confidence/source fields
manual correction layer
coverage reporting
```

Do not yet:

```text
generate strategic claims
produce recommendations
use LLMs to classify card functions as truth
```

## Priority 4 - Commander Spellbook Interpreter Expansion

Why:

Commander Spellbook is combo authority, but Codie still needs deterministic
interpretation surfaces for prerequisites, outputs, restrictions, and simulator
target compatibility.

First contract should define:

```text
combo prerequisite parsing
combo output classification
restriction classification
infinite draw = win treatment
infinite mana + compatible Tagger sink rule
no combo ranking
no deck-intent inference
```

## Priority 5 - Immutable Deck Snapshot Expansion

Why:

Deck memory, user deck analysis, comparisons, simulator challenges, and local
reports all benefit from replayable snapshots.

First contract should define:

```text
snapshot IDs
deck hash
commander signature
source deck reference
created_at
analysis profile refs
redaction/privacy behavior
replay metadata
```

## Priority 6 - Frequency Pools And Tag Graph Lab

Why:

Frequency pools and Tag Graph Lab turn accepted canonical/evidence layers into
useful comparison surfaces without jumping straight to recommendations.

Suggested order:

```text
Moxfield Frequency Pool Builder
Commander Frequency Pool Builder
Tag Graph Metric Calculator
Tag Graph Export Surfaces
```

Rules:

```text
canonical identities only
user decks never enter commander averages
low coverage labels required
no strategic claims
```

## Priority 7 - Cockatrice Interoperability

Why:

Cockatrice import/export can improve local testing and portability without
requiring cloud integrations.

First contract should define:

```text
supported file formats
deck import/export fields
commander section handling
sideboard/zone handling
card name resolution
unsupported card reporting
privacy boundaries
```

## Priority 8 - Plugin Architecture

Why:

The master architecture patch requires validators to review every changed file
for plugin-style extensions. This should be designed before external extension
surfaces are added.

First contract should define:

```text
plugin manifest
allowed extension points
blocked extension points
validation packet requirements
dependency restrictions
no arbitrary execution by default
```

## Priority 9 - Smart Enrichment And Background Processing

Why:

Demand-driven enrichment can reduce blocking workflows, but it adds state,
queues, and failure modes.

First contract should define:

```text
job records
idempotency
retry policy
failure reporting
source attribution
no silent enrichment
manual review for uncertain enrichment
```

## Priority 10 - Conversation Summaries And Jin Read-Only Surfaces

Why:

Jin should explain deterministic facts and help users navigate evidence, but
must remain read-only and must not become a recommendation source.

First contract should define:

```text
summary packet shape
manual-save workflow
evidence citations
redaction rules
no persisted strategic invention
writer/auditor split
read-only source access
```

## Explicitly Later

These should wait until the foundation above is stable:

```text
full recommendation generation
advanced UI dashboard
mobile delivery integrations
Discord / LocalSend / QR delivery automation
paired simulation runtime
trace v2 runtime integration
performance testing harness
```

## Governance Rule

Every deferred implementation must include:

```text
contract
implementation report
checkpoint
outside validation prompt
tests
static scans
status index update
continuity handoff update
commit
push
outside validation
```

No deferred implementation may use roadmap text as implementation authority
without an accepted phase contract.
