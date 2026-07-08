# Phase 28A - Deck Health / Recommendation Output Contract

## Objective

Define the boundary, output packet shape, evidence requirements, and forbidden
behavior for future deck health and recommendation output.

This is a contract packet only. It adds no implementation code, schema, DB
access, repository methods, provider calls, source-table reads, raw provider
reads, UI code, file writing, LLM calls, simulator execution, analytics
recalculation, persistence, deck health output, recommendation output, or
replacement output.

## Accepted Inputs

Phase 28A starts after Phase 27 outside validation returned PASS.

Accepted prior layers:

```text
Phase 25 Evidence Fusion / Unified Evidence Objects
Phase 26 Decision Intelligence Boundary
Phase 27 Weight Profile / Analysis Profile
Codie Architecture Revision III roadmap patch
Post-Phase 24 patch contract backlog
```

## Purpose

Deck health and recommendation output are the first future user-facing
decision layers.

They must be action-first, evidence-backed, reproducible, and explicitly
caveated. They must not become a shortcut around Evidence Fusion, Decision
Intelligence, or versioned Weight Profiles.

Phase 28A defines the contract only. It does not authorize actual
recommendation generation.

## Architecture Position

Future output must flow through:

```text
Canonical Truth
Measured Evidence
Evidence Fusion
Decision Intelligence
Weight / Analysis Profile
Deck Health / Recommendation Output
Reports / CLI / UI
```

No subsystem may produce recommendation output directly from raw provider data,
source tables, primer text, simulator traces, or LLM text.

## Allowed Future Input Packets

Future Phase 28B may consume already-built packet objects only:

```text
UnifiedEvidenceObject
UnifiedEvidenceBundle
DecisionPacket
DecisionPacketBundle
WeightProfile
AnalysisProfile
future explicit UserContext packet
future explicitly contracted curated registry packets
```

## Forbidden Inputs

Phase 28A and future Phase 28B must not read:

```text
raw provider payloads
provider_objects
source_events
source_decks
source_deck_cards
raw Moxfield primer bodies
private deck import text
raw simulator traces
live provider APIs
live Scryfall
live Moxfield
SQLite without a future repository contract
LLM output as evidence
```

## Required Future Public Interface

Future implementation should define packet objects equivalent to:

```text
RecommendationOutputBuildError
DeckHealthPacket
DeckHealthFinding
RecommendationCandidatePacket
ReplacementSuggestionPacket
PackageGapPacket
EvidenceExplanationPacket
RecommendationOutputBundle
RecommendationOutputOptions
build_deck_health_packet(...)
build_recommendation_candidate_packet(...)
build_replacement_suggestion_packet(...)
build_recommendation_output_bundle(...)
recommendation_output_to_dict(...)
validate_recommendation_output_bundle(...)
```

Names may change only if the implementation report documents the mapping.

## Common Required Fields

Every future output packet must expose:

```text
output_id
output_type
subject
summary
confidence
expected_impact
source_agreement
evidence_object_ids
decision_ids
weight_profile_id
weight_profile_version
analysis_profile_id
analysis_profile_version
supporting_ref_ids
contradicting_ref_ids
caveat_ids
speculation_level
generated_at
output_version
metadata
```

## Deck Health Fields

Deck health findings should expose:

```text
health_category
severity
finding_label
finding_summary
affected_cards
affected_roles
supporting_ref_ids
contradicting_ref_ids
caveat_ids
```

Allowed health categories:

```text
mana
card_advantage
interaction
win_condition
resilience
speed
consistency
package
legality
data_quality
```

Allowed severity values:

```text
info
warning
blocking
```

## Recommendation Candidate Fields

Recommendation candidates should expose:

```text
candidate_card_oracle_id
candidate_card_scryfall_id
candidate_card_name
recommendation_type
role_tags
confidence
expected_impact
evidence_summary
supporting_ref_ids
contradicting_ref_ids
caveat_ids
```

Allowed recommendation types:

```text
consider_include
consider_replace
monitor
investigate
no_action
```

`monitor`, `investigate`, and `no_action` are valid outputs. Low-confidence or
low-coverage evidence should prefer these categories over include/cut language.

## Replacement Suggestion Fields

Replacement suggestions should expose:

```text
replace_card_oracle_id
replace_card_scryfall_id
replace_card_name
candidate_card_oracle_id
candidate_card_scryfall_id
candidate_card_name
shared_role_tags
reason_summary
impact_summary
confidence
supporting_ref_ids
contradicting_ref_ids
caveat_ids
```

Replacement suggestions must cite both the proposed replacement and the card
being considered for replacement. Replacement suggestions should be preferred
over isolated additions only when a shared role or package relationship is
supported by evidence.

## Evidence Rules

Every future output must:

```text
cite at least one DecisionPacket ID
cite at least one UnifiedEvidenceObject ID
cite the weight profile ID and version
cite the analysis profile ID and version
keep source agreement visible
keep caveats visible
keep contradictions visible
keep speculation level visible
keep unsupported-card caveats visible
label low sample size visibly
label low coverage visibly
preserve simulator refs as simulator evidence only
preserve primer context as explanatory context only
preserve authority refs as highest-priority facts
```

User context may personalize future output, but it must not alter global
evidence, canonical records, source records, or measured metrics.

## Confidence Gate

Future confidence calculation must be explicit and reproducible.

Rules:

```text
high confidence requires strong or mixed source agreement
high confidence requires measured evidence through DecisionPacket / Evidence refs
medium or high confidence requires visible sample size or coverage evidence
high speculation cannot pair with medium or high confidence
low sample size must create a visible caveat
low coverage ratio must create a visible caveat
confidence must consider coverage ratio when available, not only absolute deck count
```

When available, coverage-sensitive confidence should consider:

```text
matching_deck_count / available_deck_count
coverage_ratio
minimum_sample_size
minimum_coverage_ratio
```

## Allowed Wording

Future output may use evidence-first language such as:

```text
This card appears in 42% of matching top finishes.
Codie found evidence supporting consideration of this card.
This slot differs from matching top finishes.
Low sample size: treat this as a review candidate.
Simulator comparison is model-derived and not tournament evidence.
Primer context is explanatory only.
```

## Forbidden Wording

Future output must reject unsupported strategic claims such as:

```text
you should play
should be played
should be cut
must include
correct card
strict upgrade
auto-include
recommended cut
recommended include
secretly optimal
breaks the format
best card
strictly better
```

Tests must reject these phrases in production output.

## Simulator Boundary

Simulator-derived refs may support modeled comparisons, but:

```text
simulator refs are not tournament evidence
simulator refs do not prove a card is correct
unsupported cards must be disclosed
raw simulator traces are not allowed inputs
simulator execution is not allowed in Phase 28B unless separately contracted
```

## Primer Context Boundary

Primer context may explain evidence, but it must not:

```text
override authority refs
override measured evidence
create tournament evidence
create recommendation confidence by itself
store or expose primer bodies
store or expose mulligan guides
store or expose strategy paragraphs
```

## Persistence Boundary

Phase 28A authorizes no persistence.

Future persistence of deck health or recommendation outputs requires a separate
schema, repository, and migration contract.

## Phase 28B Recommended Implementation Scope

If Phase 28A is accepted, Phase 28B should implement only pure in-memory
packet models and validators:

```text
codie/recommendation_output/__init__.py
codie/recommendation_output/models.py
tests/test_recommendation_output_boundary.py
docs/PHASE28B_DECK_HEALTH_RECOMMENDATION_OUTPUT_IMPLEMENTATION_REPORT.md
```

Phase 28B should remain:

```text
pure
in-memory
packet-only
deterministic
evidence-cited
version-cited
DB-free
provider-free
source-table-free
LLM-call-free
simulator-execution-free
UI-free
file-write-free
recommendation-engine-free beyond packet validation
```

## Required Phase 28B Tests

Future Phase 28B tests should prove:

```text
output requires DecisionPacket IDs
output requires UnifiedEvidenceObject IDs
output exposes confidence
output exposes expected impact
output exposes source agreement
output exposes caveats
output exposes contradictions
output exposes speculation level
output cites weight_profile_id and weight_profile_version
output cites analysis_profile_id and analysis_profile_version
low coverage creates a visible caveat
low sample size creates a visible caveat
simulator refs are labeled model-derived and not tournament evidence
primer context remains explanatory only
forbidden strategic wording is rejected
high confidence requires source agreement
high speculation cannot pair with medium or high confidence
replacement suggestion requires replaced-card and candidate-card IDs
monitor, investigate, and no_action outputs are allowed
private metadata is rejected
serialization is deterministic
```

## Required Phase 28B Static Scans

Future implementation should run:

```text
rg -n "codie\.db|codie\.providers|codie\.repositories|codie\.ingestion|codie\.canonical|codie\.analytics|codie\.cards|codie\.probability_engine|requests|httpx|sqlite3|openai|anthropic|flask|fastapi|uvicorn|starlette" codie\recommendation_output tests\test_recommendation_output_boundary.py
rg -n "source_events|source_decks|source_deck_cards|provider_objects|raw_provider_payload|provider_payload|private_deck_text|full_primer_body|original_import_text" codie\recommendation_output tests\test_recommendation_output_boundary.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\recommendation_output tests\test_recommendation_output_boundary.py
rg -n "open\(|write_text\(|write_bytes\(|Path\(|mkdir\(|touch\(|unlink\(" codie\recommendation_output
rg -n "you should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include|best card|strictly better" codie\recommendation_output tests\test_recommendation_output_boundary.py
git diff --name-only -- codie/db/schema docs/SCHEMA_SPEC.md codie/db/repositories
```

Expected result:

```text
no production matches, except blocked-key constants or rejection tests where explicitly documented
no schema or repository drift
```

## Do Not Do In Phase 28A

```text
do not implement recommendation output
do not implement deck health output
do not implement replacement suggestions
do not add schema
do not add repositories
do not read DB tables
do not read source/provider tables
do not read raw provider payloads
do not read primer bodies
do not run simulator logic
do not call LLMs
do not add UI
do not write files
do not calculate analytics
do not persist outputs
```

## Acceptance Criteria

Phase 28A is accepted when:

```text
contract exists
Phase 27 outside validation is recorded as PASS
active roadmap index points to Phase 28B after Phase 28A review
validation index records Phase 28A as contract complete
handoff records Phase 28A status and next gate
git diff --check passes
full test suite passes
```
