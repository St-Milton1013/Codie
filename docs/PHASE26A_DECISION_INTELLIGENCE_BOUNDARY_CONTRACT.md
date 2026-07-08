# Phase 26A - Decision Intelligence Boundary Contract

## Objective

Define the Decision Intelligence boundary under Codie Architecture Revision III.

This is a contract packet only. It adds no implementation code, schema, DB
access, repository methods, provider calls, source-table reads, raw provider
reads, UI code, file writing, LLM calls, simulator execution, analytics
recalculation, recommendation output, deck health output, replacement output,
or persisted decision records.

## Accepted Inputs

Phase 26A starts after Phase 25 outside validation returned PASS.

Accepted prior layers:

```text
Phase 0-6 storage, canonicalization, and measured analytics foundations
Phase 7 evidence-only syncs
Phase 8 recommendation statistics and innovation foundations
Phase 13 simulator track
Phase 14 simulation review export writer
Phase 15 deck memory
Phase 16-24 interactive intelligence packet layers
Phase 25 Evidence Fusion / Unified Evidence Objects
Codie Architecture Revision III roadmap patch
Post-Phase 24 patch contract backlog
```

## Purpose

Decision Intelligence is the only Codie subsystem allowed to produce
decision-bearing conclusions.

Future outputs may include:

```text
recommendations
deck health assessments
replacement suggestions
package detection conclusions
commander staple conclusions
recommendation confidence
source agreement summaries
evidence explanations
simulator comparisons
historical comparisons
action-first dashboard items
```

Phase 26A defines the boundary only. It does not authorize any of those outputs
to be implemented yet.

## Architecture Position

Codie Architecture Revision III defines:

```text
Class 0 Authority Layer
Class 1 Observational Data
Class 2 Measured Evidence
Primer Context Extraction
Evidence Fusion
Class 3 Decision Intelligence
Class 4 User Context
UI / Reports / Chat / Exports
```

Phase 26A defines Class 3 boundaries.

## Governing Rule

```text
No Codie subsystem may produce recommendations directly from raw provider data.
Every recommendation must flow through Evidence Fusion and Decision Intelligence.
```

## Allowed Inputs

Decision Intelligence may consume:

```text
UnifiedEvidenceObject
UnifiedEvidenceBundle
EvidenceAuthorityRef
EvidenceObservationRef
EvidenceMetricRef
EvidencePrimerContextRef
EvidenceSimulatorRef
EvidenceCaveat
EvidenceConflict
EvidenceSourceAgreement
future versioned Weight Profile packets
future explicit User Context packets
curated registries through future contracted packet readers
```

Allowed inputs must be passed as already-built packets or through future
contracted readers. Phase 26A does not authorize DB reads.

## Forbidden Inputs

Decision Intelligence must not directly read:

```text
raw provider payloads
provider_objects
source_events
source_decks
source_deck_cards
raw Moxfield primer bodies
private deck import text
raw simulator trace files
live provider APIs
live Moxfield pages
live Scryfall API
local SQLite tables without a future repository contract
```

## Boundary Rules

Decision Intelligence:

```text
owns recommendation reasoning
owns deck health reasoning
owns replacement reasoning
owns action-first prioritization
must cite Unified Evidence Object IDs
must expose confidence and caveats
must expose source agreement
must preserve contradiction visibility
must preserve unsupported-card visibility
must preserve speculation visibility
must distinguish tournament evidence from simulator evidence
must distinguish primer context from measured evidence
must distinguish authority facts from performance evidence
```

Decision Intelligence must not:

```text
query source/provider tables directly
query raw provider payloads directly
recalculate analytics
canonicalize source records
resolve source conflicts
mutate simulator traces
execute simulator searches
call LLMs directly
write files
write SQLite
persist recommendations
render UI
send reports
send Discord messages
generate Jin-Gitaxias theory answers
```

## Evidence Hierarchy

Decision Intelligence must respect:

```text
Authority refs > measured evidence refs > primer context refs
```

Rules:

```text
Authority refs define card/rules/combo facts.
Measured evidence refs define observed performance and frequency signals.
Primer context refs may explain evidence but may not override it.
Simulator refs may compare modeled outcomes but may not become tournament evidence.
User context may personalize future output but may not alter global evidence.
```

## Required Future Output Shape

Future Decision Intelligence outputs must be packet-shaped and deterministic.

Required common fields:

```text
decision_id
decision_type
subject
summary
confidence
expected_impact
source_agreement
evidence_object_ids
supporting_ref_ids
contradicting_ref_ids
caveat_ids
speculation_level
generated_at
decision_version
metadata
```

This contract does not implement these models. It defines the required shape
for future Phase 26B or later implementation.

## Forbidden Language

Decision Intelligence outputs must not use unsupported strategic claims.

Forbidden wording includes:

```text
this card is correct
this card breaks the format
this card is secretly optimal
you should play this card
strict upgrade
auto-include
recommended cut
recommended include
```

Allowed wording is evidence-grounded:

```text
This card appears in 42% of matching top-16 decks.
This candidate has mixed source agreement.
This result has low sample size.
This simulator comparison is model-derived and not tournament evidence.
This primer context is explanatory and does not override measured evidence.
```

## Recommended Phase 26B Implementation

Phase 26B should implement in-memory packet models only.

Likely files:

```text
codie/decision_intelligence/__init__.py
codie/decision_intelligence/models.py
codie/decision_intelligence/builders.py
tests/test_decision_intelligence_boundary.py
docs/PHASE26B_DECISION_INTELLIGENCE_BOUNDARY_IMPLEMENTATION_REPORT.md
```

Phase 26B should remain:

```text
pure
in-memory
packet-only
deterministic
evidence-cited
recommendation-output-free unless explicitly contracted
DB-free
provider-free
source-table-free
LLM-call-free
simulator-execution-free
UI-free
file-write-free
```

## Required Phase 26B Tests

Future implementation tests must prove:

```text
decision packets require Unified Evidence Object IDs
decision packets expose confidence
decision packets expose expected impact
decision packets expose source agreement
decision packets expose caveats
decision packets expose speculation level
decision packets preserve contradiction visibility
decision packets distinguish simulator evidence from tournament evidence
decision packets distinguish primer context from measured evidence
decision packets reject raw provider/source/private metadata
decision packets reject unsupported strategic language
Decision Intelligence code imports no providers, DB, repositories, ingestion, canonicalization, analytics recalculation, cards, simulator execution, UI, server frameworks, or LLM SDKs
Decision Intelligence code contains no raw SQL
Decision Intelligence code performs no production file writing
```

## Static Scans For Phase 26B

Future validation should include:

```powershell
rg -n "codie\.db|codie\.providers|codie\.repositories|codie\.ingestion|codie\.canonical|codie\.analytics|codie\.cards|codie\.probability_engine|requests|httpx|sqlite3|openai|anthropic|flask|fastapi|uvicorn|starlette" codie\decision_intelligence tests\test_decision_intelligence_boundary.py
rg -n "source_events|source_decks|source_deck_cards|provider_objects|raw_provider_payload|provider_payload|private_deck_text|full_primer_body|original_import_text" codie\decision_intelligence tests\test_decision_intelligence_boundary.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\decision_intelligence tests\test_decision_intelligence_boundary.py
rg -n "open\(|write_text\(|write_bytes\(|Path\(|mkdir\(|touch\(|unlink\(" codie\decision_intelligence
rg -n "should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\decision_intelligence tests\test_decision_intelligence_boundary.py
```

Expected result:

```text
no production matches, except blocked-key constants or rejection tests where explicitly documented
```

## Do Not Do In Phase 26A

```text
do not implement Decision Intelligence code
do not generate recommendations
do not generate deck health output
do not generate replacement suggestions
do not persist decision records
do not add schema
do not add repositories
do not read SQLite
do not read provider/source tables
do not read raw provider payloads
do not read primer bodies
do not execute simulator logic
do not call LLMs
do not build UI
do not write files
```

## Completion Criteria

Phase 26A is complete when:

```text
this contract is created
handoff docs point to Phase 26B as the next implementation packet
Phase 25 is marked as externally accepted
tests remain passing
working tree is committed and pushed
```
