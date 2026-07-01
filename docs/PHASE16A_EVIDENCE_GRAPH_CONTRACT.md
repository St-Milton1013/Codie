# Phase 16A - Evidence Graph Contract

## Objective

Define an in-memory evidence graph model for future Interactive Intelligence
surfaces.

The evidence graph should give future chat, UI, and report builders a
structured way to explain claims with nodes, edges, citations, confidence, and
caveats before any LLM phrasing layer exists.

This is a contract packet. It adds no implementation code, schema, UI, LLM
calls, provider access, source-table reads, simulator execution, recommendation
generation, or persistence.

## Scope

Future implementation files:

```text
codie/intelligence/__init__.py
codie/intelligence/evidence_graph.py
tests/test_intelligence_evidence_graph.py
docs/PHASE16B_EVIDENCE_GRAPH_IMPLEMENTATION_REPORT.md
```

Current contract files:

```text
docs/PHASE16A_EVIDENCE_GRAPH_CONTRACT.md
docs/PHASE16A_EVIDENCE_GRAPH_CONTRACT_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Public Classes And Functions

Future implementation should define:

```text
EvidenceGraphBuildError
EvidenceCitation
EvidenceCaveat
EvidenceNode
EvidenceEdge
EvidenceGraph
EvidenceGraphInput
build_evidence_graph(...)
validate_evidence_graph(...)
evidence_graph_to_dict(...)
```

## EvidenceGraph

Required fields:

```text
graph_id
claim_type
claim_text
subject_type
subject_id
generated_at
nodes
edges
caveats
metadata
```

Rules:

```text
graph_id is required and deterministic from caller-provided input
claim_text must pass strategic-language validation
nodes must contain at least one node
node IDs must be unique
edge IDs must be unique
edges may only reference existing node IDs
caveats must be preserved, not hidden
metadata must be JSON-compatible
```

## EvidenceNode

Required fields:

```text
node_id
node_type
label
summary
confidence
citations
privacy_scope
metadata
```

Allowed `node_type` values:

```text
card
commander
deck
package
tournament_stat
regional_stat
historical_stat
innovation_signal
primer_metadata
combo_evidence
simulation_result
unsupported_card
source_conflict
user_deck_memory
saved_analysis
manual_note
```

Allowed `privacy_scope` values:

```text
public
local
local_user_data
sensitive
```

Rules:

```text
node_id is required
node_type must be allowed
label is required
summary must pass strategic-language validation
confidence must be between 0 and 1
citations must contain at least one citation unless node_type is manual_note
local_user_data and sensitive nodes must not include raw_input by default
metadata must be JSON-compatible
```

## EvidenceEdge

Required fields:

```text
edge_id
source_node_id
target_node_id
edge_type
summary
confidence
metadata
```

Allowed `edge_type` values:

```text
supports
contradicts
qualifies
derived_from
same_card_as
same_commander_as
observed_in
linked_to
requires_caveat
```

Rules:

```text
source_node_id must exist
target_node_id must exist
edge_type must be allowed
self-edges are rejected unless edge_type is qualifies
summary must pass strategic-language validation
confidence must be between 0 and 1
metadata must be JSON-compatible
```

## EvidenceCitation

Required fields:

```text
citation_id
source_type
source_name
source_record_id
source_url
observed_at
```

Allowed `source_type` values:

```text
canonical
analytics
recommendation_candidate
innovation_snapshot
combo
primer_metadata
simulation
deck_memory
saved_analysis
curated
manual
```

Rules:

```text
citation_id is required
source_type must be allowed
source_name is required
source_record_id or source_url is required
citations must not embed raw provider payloads
citations must not embed raw_input
```

## EvidenceCaveat

Required fields:

```text
caveat_id
caveat_type
message
severity
related_node_ids
metadata
```

Allowed `caveat_type` values:

```text
low_sample
missing_data
unsupported_card
unsupported_simulator_behavior
source_conflict
privacy_redaction
stale_data
manual_review_required
```

Allowed `severity` values:

```text
info
warning
blocking
```

Rules:

```text
caveat_id is required
caveat_type must be allowed
message must pass strategic-language validation
related_node_ids must reference existing nodes when supplied
blocking caveats must be preserved in serialized output
```

## EvidenceGraphInput

Future implementation may accept already-built read-model objects from:

```text
recommendation evidence bundles
recommendation candidate packets
innovation snapshots
combo evidence records
primer metadata records
simulation review summaries
deck memory summaries
saved analysis summaries
manual notes
```

The input must not accept:

```text
raw provider payloads
raw source table rows
raw_input by default
unbounded free-form LLM text
```

## Serialization Shape

`evidence_graph_to_dict(...)` should produce deterministic JSON-compatible
output:

```json
{
  "graph_id": "graph:example",
  "claim_type": "card_evidence",
  "claim_text": "Mystic Remora has observed inclusion evidence.",
  "subject_type": "card",
  "subject_id": "oracle-example",
  "generated_at": "2026-07-01T00:00:00+00:00",
  "nodes": [],
  "edges": [],
  "caveats": [],
  "metadata": {}
}
```

Ordering:

```text
nodes sorted by node_id
edges sorted by edge_id
caveats sorted by caveat_id
citations sorted by citation_id
metadata sorted by JSON serializer
```

## Strategic-Language Rules

Evidence graph text may describe evidence.

Allowed wording:

```text
Card appeared in 12 of 40 comparable canonical decks.
This node is derived from a saved local deck analysis.
Simulation result has unsupported-card caveats.
Primer metadata mentions this package.
```

Forbidden wording:

```text
This card should be played.
This card should be cut.
This card is correct.
This card is optimal.
This deck must include this package.
```

Future implementation should reuse or mirror existing strategic-claim
validation from:

```text
codie.recommendations.evidence.validate_claim_text
```

without importing recommendation generation or persistence layers.

## Privacy Rules

Evidence graphs must preserve privacy boundaries:

```text
raw_input excluded by default
private user deck text excluded by default
local_user_data nodes marked explicitly
sensitive nodes marked explicitly
privacy redactions represented as caveats
cloud LLM context not authorized
```

Future implementation must reject graph metadata containing:

```text
raw_input
full primer body
raw provider payload
private deck text
```

unless a future explicit opt-in contract approves it.

## Boundary Rules

Evidence graph implementation may import:

```text
standard library
codie.recommendations.evidence.validate_claim_text
```

It must not import:

```text
codie.db
codie.providers
codie.analytics
codie.recommendations.generation
codie.recommendations.persistence
codie.ingestion
codie.cards
codie.probability_engine
codie.canonical
requests
httpx
sqlite3
```

No raw SQL is allowed.

## Failure Modes

Future implementation should raise `EvidenceGraphBuildError` for:

```text
missing graph_id
missing claim_text
forbidden strategic language
unsupported node_type
unsupported edge_type
unsupported source_type
unsupported caveat_type
invalid confidence
duplicate node_id
duplicate edge_id
edge references missing node
caveat references missing node
non JSON-compatible metadata
raw_input or forbidden private text in metadata
empty nodes
```

## Required Tests For Phase 16B

```text
valid graph serializes deterministically
nodes sort by node_id
edges sort by edge_id
caveats sort by caveat_id
citations sort by citation_id
duplicate node IDs fail cleanly
duplicate edge IDs fail cleanly
edge referencing missing node fails cleanly
caveat referencing missing node fails cleanly
unsupported node type fails cleanly
unsupported edge type fails cleanly
unsupported source type fails cleanly
invalid confidence fails cleanly
forbidden strategic claim text fails cleanly
manual_note may omit citation
non-manual nodes require citation
raw_input metadata is rejected by default
local_user_data node is preserved with privacy_scope
blocking caveat is preserved in serialized output
module has no forbidden imports
module has no raw SQL
full suite passes
```

## Do Not Do In Phase 16A

```text
do not implement evidence graph code
do not add schema
do not add DB reads or writes
do not add UI
do not call providers
do not call LLMs
do not read source/provider payloads directly
do not run simulator logic
do not mutate simulator traces
do not generate recommendations
do not export private raw_input
```

## Recommended Next Packet

```text
Phase 16B - Evidence Graph Implementation
```
