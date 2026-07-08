# Phase 25A - Evidence Fusion / Unified Evidence Objects Contract

## Objective

Define the boundary and object model for Evidence Fusion under Codie
Architecture Revision III.

This is a contract packet. It adds no implementation code, schema, DB access,
repository methods, provider calls, source-table reads, raw provider reads, UI
code, file writing, LLM calls, Strategist/Jin-Gitaxias theory generation,
simulator execution, analytics recalculation, or recommendation output.

## Accepted Inputs

Phase 25A starts after Phase 24 outside validation returned PASS.

Accepted prior layers:

```text
Phase 0-6 storage, canonicalization, analytics foundations
Phase 7 evidence-only syncs
Phase 8 recommendation statistics and innovation foundations
Phase 13 simulator track
Phase 14 simulation review export writer
Phase 15 deck memory
Phase 16-24 interactive intelligence packet layers
Codie Architecture Revision III roadmap patch
Post-Phase 24 patch contract backlog
```

## Purpose

Evidence Fusion creates common, structured evidence packets for downstream
systems.

Every downstream reasoning surface should consume Unified Evidence Objects
instead of reading raw source/provider data or inventing its own reasoning path.

Downstream consumers may include future:

```text
Decision Intelligence
chat answers
reports
exports
dashboard panels
recommendation explanations
source agreement summaries
confidence summaries
```

## Architecture Position

Codie Architecture Revision III defines:

```text
Class 0 Authority Layer
  Class 0A Rules & Card Authority
  Class 0B Combo Authority

Class 1 Observational Data

Class 2 Measured Evidence

Primer Context Extraction

Evidence Fusion

Class 3 Decision Intelligence

Class 4 User Context
```

Phase 25A defines the contract for the Evidence Fusion boundary only.

## Recommended Phase 25B Implementation

Phase 25B should implement in-memory packet models only.

Likely files:

```text
codie/evidence_fusion/__init__.py
codie/evidence_fusion/models.py
codie/evidence_fusion/builders.py
tests/test_evidence_fusion_models.py
docs/PHASE25B_EVIDENCE_FUSION_UNIFIED_EVIDENCE_OBJECTS_IMPLEMENTATION_REPORT.md
```

Phase 25B must not add persistence, repositories, schema, provider reads,
analytics queries, recommendation scoring, LLM calls, UI rendering, file
writing, simulator execution, or Jin-Gitaxias theory output.

## Public Interface For Phase 25B

Future implementation should define:

```text
EvidenceFusionBuildError
EvidenceAuthorityRef
EvidenceObservationRef
EvidenceMetricRef
EvidencePrimerContextRef
EvidenceSimulatorRef
EvidenceCaveat
EvidenceConflict
EvidenceSourceAgreement
UnifiedEvidenceSubject
UnifiedEvidenceObject
UnifiedEvidenceBundle
EvidenceFusionOptions
build_unified_evidence_object(...)
build_unified_evidence_bundle(...)
unified_evidence_object_to_dict(...)
unified_evidence_bundle_to_dict(...)
validate_unified_evidence_bundle(...)
```

## EvidenceAuthorityRef

Purpose:

Reference Class 0 authority without copying or overriding authority data.

Required fields:

```text
authority_ref_id
authority_type
authority_source
authority_key
authority_label
authority_url
authority_version
generated_at
metadata
```

Allowed authority_type values:

```text
scryfall_card
scryfall_ruling
scryfall_legality
commander_spellbook_combo
official_rules
official_oracle_ruling
official_release_note
official_ban_announcement
```

Rules:

```text
Scryfall refs may identify cards, oracle IDs, scryfall IDs, legalities, rulings, and search syntax.
Commander Spellbook refs may identify combo existence, requirements, outcomes, and variants.
Authority refs must not be edited by Evidence Fusion.
Authority refs must not be treated as measured performance evidence.
```

## EvidenceObservationRef

Purpose:

Reference Class 1 observational records without reading raw provider payloads.

Required fields:

```text
observation_ref_id
observation_type
source_system
source_record_id
canonical_record_id
source_label
source_url
observed_at
generated_at
metadata
```

Allowed observation_type values:

```text
canonical_event
canonical_deck
canonical_deck_card
event_deck_entry
user_deck_snapshot
primer_metadata
source_conflict
unsupported_card_queue_item
```

Rules:

```text
Observation refs point to already-approved records or sanitized input refs.
Observation refs must not embed raw provider payloads.
Observation refs must not embed private deck text.
Observation refs must not produce conclusions.
```

## EvidenceMetricRef

Purpose:

Reference Class 2 measured evidence.

Required fields:

```text
metric_ref_id
metric_type
metric_name
metric_value
metric_unit
scope_type
scope_key
window_start
window_end
sample_size
coverage_ratio
generated_at
metadata
```

Allowed metric_type values:

```text
frequency
inclusion_rate
win_rate
top_cut_rate
trend_delta
co_occurrence
lift
support
confidence
similarity
package_frequency
card_performance
innovation_signal
simulator_statistic
commander_staple_statistic
```

Rules:

```text
Metric refs must be reproducible.
Metric refs must identify scope and sample size when available.
Metric refs must expose low-sample or low-coverage caveats.
Metric refs must not recalculate analytics inside Evidence Fusion.
```

## EvidencePrimerContextRef

Purpose:

Reference primer context as explanatory context, not truth.

Required fields:

```text
primer_context_ref_id
primer_ref_id
context_type
context_label
commander_signature
source_url
generated_at
metadata
```

Allowed context_type values:

```text
archetype_hint
strategy_summary
mulligan_philosophy
pilot_priority
meta_assumption
flex_slot_explanation
```

Rules:

```text
Primer context may explain evidence.
Primer context may never override authority or measured evidence.
Primer context refs must not include full primer body text.
Primer context refs must not include private deck text.
```

## EvidenceSimulatorRef

Purpose:

Reference simulator results or reviewed simulator traces as supporting evidence.

Required fields:

```text
simulator_ref_id
simulation_type
result_id
deck_hash
target_label
success_rate
sample_size
unsupported_cards_count
review_status
generated_at
metadata
```

Rules:

```text
Simulator refs are not tournament evidence.
Simulator refs must disclose unsupported-card counts when available.
Reviewed rejected lines must not be treated as successful simulator evidence.
Evidence Fusion must not execute simulator logic.
```

## EvidenceCaveat

Purpose:

Represent visible uncertainty.

Required fields:

```text
caveat_id
caveat_type
severity
message
related_ref_ids
generated_at
metadata
```

Allowed caveat_type values:

```text
low_sample
low_coverage
source_conflict
unsupported_card
stale_data
primer_context_only
simulator_limitation
regional_bias
missing_authority_ref
```

## EvidenceConflict

Purpose:

Preserve conflicts instead of resolving them silently.

Required fields:

```text
conflict_id
conflict_type
summary
ref_ids
requires_manual_review
generated_at
metadata
```

Rules:

```text
Evidence Fusion may surface conflicts.
Evidence Fusion must not choose winner records.
Evidence Fusion must not canonicalize data.
Evidence Fusion must not mutate source or canonical records.
```

## EvidenceSourceAgreement

Purpose:

Represent source agreement labels without generating recommendations.

Required fields:

```text
agreement_id
agreement_label
supporting_ref_ids
conflicting_ref_ids
coverage_ratio
sample_size
generated_at
metadata
```

Allowed agreement_label values:

```text
strong
mixed
weak
unknown
```

Rules:

```text
Agreement labels summarize evidence availability and consistency.
Agreement labels do not decide recommendations.
Detailed agreement breakdown remains expandable.
```

## UnifiedEvidenceSubject

Purpose:

Identify the thing evidence is about.

Required fields:

```text
subject_id
subject_type
subject_key
display_name
commander_signature
oracle_id
scryfall_id
region_code
generated_at
metadata
```

Allowed subject_type values:

```text
card
commander
partner_pair
deck
package
combo
archetype
event
simulation_target
tag
```

## UnifiedEvidenceObject

Purpose:

Merge authority, measured evidence, primer context, simulator context, caveats,
conflicts, and source agreement into one deterministic object.

Required fields:

```text
evidence_object_id
subject
authority_refs
observation_refs
metric_refs
primer_context_refs
simulator_refs
caveats
conflicts
source_agreement
evidence_level
speculation_level
coverage_ratio
sample_size
generated_at
evidence_version
metadata
```

Allowed evidence_level values:

```text
high
medium
low
unknown
```

Allowed speculation_level values:

```text
none
low
medium
high
```

Rules:

```text
evidence_level may not exceed available evidence quality.
speculation_level must be visible.
private metadata keys are forbidden.
serialization must be deterministic.
object construction must not access DB or provider layers.
object construction must not generate recommendations.
```

## UnifiedEvidenceBundle

Purpose:

Group unified evidence objects for a downstream consumer.

Required fields:

```text
bundle_id
bundle_type
subject
evidence_objects
caveats
conflicts
generated_at
evidence_version
metadata
```

Allowed bundle_type values:

```text
deck_analysis
commander_profile
card_profile
package_profile
recommendation_input
chat_context
report_context
dashboard_context
simulation_context
```

Rules:

```text
Bundles are input packets for downstream systems.
Bundles are not recommendation outputs.
Bundles are not persisted unless a future repository/schema contract approves persistence.
```

## Privacy And Metadata Rules

Forbidden metadata keys include:

```text
raw_input
private_deck_text
full_primer_body
raw_provider_payload
provider_payload
original_import_text
```

Rules:

```text
Forbidden keys must be rejected, including nested keys.
Metadata must be JSON-compatible.
Stack traces must not be exposed.
Private user deck text must not be exported through evidence objects.
```

## Evidence Fusion Options

Required fields and defaults:

```text
allow_sensitive = false
allow_local_user_data = false
allow_primer_context = true
allow_simulator_refs = true
allow_conflicts = true
maximum_refs_per_object = 256
maximum_objects_per_bundle = 512
evidence_version = phase25a-contract
```

Rules:

```text
allow_sensitive defaults false.
allow_local_user_data defaults false.
maximum limits must be positive.
```

## Allowed Dependencies For Future Implementation

Future implementation may import:

```text
standard library
codie.intelligence.evidence_inputs
codie.intelligence.evidence_graph
codie.intelligence.source_conflicts
codie.intelligence.unsupported_cards
codie.intelligence.query_planner
```

Future implementation must not import:

```text
codie.db
codie.providers
codie.ingestion
codie.cards
codie.analytics
codie.recommendations
codie.canonical
codie.probability_engine
sqlite3
requests
httpx
openai
anthropic
flask
fastapi
uvicorn
starlette
```

## Required Tests For Phase 25B

Future implementation should test:

```text
authority refs serialize deterministically
observation refs reject raw provider payload metadata
metric refs require sample or coverage visibility when available
primer context refs reject full primer body text
simulator refs preserve unsupported-card counts
caveats remain visible
conflicts remain visible
source agreement labels serialize deterministically
unified evidence object preserves all ref categories
unified evidence object rejects private metadata keys
unified evidence bundle serializes deterministically
low evidence cannot produce high evidence_level
speculation_level remains visible
options reject invalid limits
module has no forbidden imports
module has no raw SQL
module has no file writes
module has no server framework imports
module has no LLM SDK imports
full test suite passes
```

## Non-Goals

Do not in Phase 25B:

```text
add schema
add repositories
read SQLite
read provider payloads
read source tables directly
recalculate analytics
generate recommendations
score recommendations
run simulator logic
generate Jin-Gitaxias theory answers
call LLMs
import LLM SDKs
add UI
write files
persist evidence objects
```

## Completion Gate

Phase 25A is complete when:

```text
this contract exists
docs/NEXT_PHASE_CONTRACT.md points to Phase 25B implementation
docs/CODEX_CONTINUITY_HANDOFF.md records the Phase 25A contract
git diff --check passes
full tests pass
```
