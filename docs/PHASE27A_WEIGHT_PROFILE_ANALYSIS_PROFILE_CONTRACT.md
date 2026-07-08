# Phase 27A - Weight Profile / Analysis Profile Contract

## Objective

Define configurable, versioned, reproducible weight profiles for future
Decision Intelligence.

This is a contract packet only. It adds no implementation code, schema, DB
access, repository methods, provider calls, source-table reads, raw provider
reads, UI code, file writing, LLM calls, simulator execution, analytics
recalculation, recommendation output, deck health output, replacement output,
or persisted analysis profiles.

## Accepted Inputs

Phase 27A starts after Phase 26 outside validation returned PASS.

Accepted prior layers:

```text
Phase 25 Evidence Fusion / Unified Evidence Objects
Phase 26 Decision Intelligence Boundary
Codie Architecture Revision III roadmap patch
Post-Phase 24 patch contract backlog
```

Phase 27A supersedes older roadmap numbering that listed Weight Profile /
Analysis Profile as Phase 26B. Phase 26B is now the Decision Intelligence
Boundary Packet Implementation.

## Purpose

Weight profiles make evidence weighting configurable and reproducible.

Future Decision Intelligence must not hardcode hidden weights. Every future
decision-bearing packet should be able to cite the profile that shaped its
confidence, expected impact, prioritization, or caveats.

## Architecture Position

Weight Profiles sit between:

```text
Evidence Fusion
Decision Intelligence
User Context
```

They are configuration packets, not evidence.

They may influence future Decision Intelligence calculations, but they do not
create authority facts, measured evidence, observations, or recommendations by
themselves.

## Required Future Public Interface

Future implementation should define:

```text
WeightProfileBuildError
WeightComponent
WeightProfile
AnalysisProfile
WeightProfileCompatibilityReport
build_weight_profile(...)
build_analysis_profile(...)
weight_profile_to_dict(...)
analysis_profile_to_dict(...)
validate_weight_profile(...)
validate_analysis_profile(...)
compare_weight_profile_versions(...)
```

## WeightProfile Required Fields

```text
profile_id
profile_name
profile_version
profile_label
profile_description
components
normalization_rule
minimum_confidence
minimum_coverage_ratio
minimum_sample_size
generated_at
analysis_version
metadata
```

## WeightComponent Required Fields

```text
component_id
component_name
component_type
weight
enabled
minimum_threshold
maximum_threshold
applies_to_decision_types
description
metadata
```

Allowed component types:

```text
authority
measured_metric
source_agreement
coverage
sample_size
tournament_performance
regional_signal
historical_signal
innovation_signal
simulator_comparison
primer_context
user_context
caveat_penalty
conflict_penalty
unsupported_card_penalty
speculation_penalty
```

## AnalysisProfile Required Fields

```text
analysis_profile_id
analysis_profile_name
analysis_profile_version
weight_profile_id
weight_profile_version
decision_version
evidence_version
analysis_scope
default_filters
generated_at
metadata
```

## Default Profiles

Phase 27B should define these default profile packets:

```text
Competitive Default
Tournament Heavy
Simulation Heavy
Primer Aware
Budget Aware
```

Default profiles must be deterministic, versioned, and serializable.

## Reproducibility Rules

```text
Profile IDs must be stable.
Profile versions must be explicit.
Profile serialization must be deterministic.
Old analyses must remain reproducible with their original profile version.
Profile updates must create a new version, not mutate prior version meaning.
Analysis profiles must record both decision_version and evidence_version.
```

## Evidence Boundary Rules

Weight profiles:

```text
may weight Unified Evidence refs
may weight caveats
may weight conflicts
may weight simulator comparison refs as simulator evidence only
may weight primer context refs as explanatory context only
must not create measured evidence
must not override authority refs
must not treat primer context as measured evidence
must not treat simulator refs as tournament evidence
must not hide low sample or low coverage caveats
must not suppress contradictions silently
```

## User Context Boundary Rules

Future user context may personalize analysis profiles, but must not mutate
global profiles.

Examples:

```text
budget-aware profile may downweight expensive options
collection-aware profile may add user-context caveats
local-meta profile may adjust prioritization
```

Rules:

```text
global profile definitions remain immutable
user-specific profile overlays require future contract
user context cannot alter global measured evidence
user context cannot alter canonical or source records
```

## Forbidden Behavior

Phase 27A and future Phase 27B must not:

```text
generate recommendations
generate deck health output
generate replacement suggestions
read raw provider data
read source tables
read provider_objects
read primer bodies
read private deck text
execute simulator logic
call LLMs
write SQLite
write files
render UI
send reports
hide caveats
hide conflicts
silently drop unsupported-card evidence
```

## Recommended Phase 27B Implementation

Phase 27B should implement in-memory packet models only.

Likely files:

```text
codie/weight_profiles/__init__.py
codie/weight_profiles/models.py
codie/weight_profiles/defaults.py
tests/test_weight_profiles.py
docs/PHASE27B_WEIGHT_PROFILE_IMPLEMENTATION_REPORT.md
```

Phase 27B should remain:

```text
pure
in-memory
packet-only
deterministic
versioned
recommendation-output-free
DB-free
provider-free
source-table-free
LLM-call-free
simulator-execution-free
UI-free
file-write-free
```

## Required Phase 27B Tests

Future implementation tests must prove:

```text
weight profile serializes deterministically
analysis profile serializes deterministically
profile IDs and versions are required
component IDs are unique within a profile
component weights are numeric and bounded
disabled components remain visible
default profiles exist
profile version is preserved
analysis profile records weight_profile_id and weight_profile_version
analysis profile records decision_version and evidence_version
old profile version replay data remains distinguishable from new version
primer context component cannot override measured metric components
simulator component remains simulator-only
caveat/conflict penalty components remain visible
private metadata is rejected
nested private metadata is rejected
unsupported strategic language is rejected
production code imports no DB, repositories, providers, ingestion, canonicalization, analytics recalculation, cards, simulator execution, UI, server frameworks, or LLM SDKs
production code contains no raw SQL
production code performs no production file writing
```

## Static Scans For Phase 27B

Future validation should include:

```powershell
rg -n "codie\.db|codie\.providers|codie\.repositories|codie\.ingestion|codie\.canonical|codie\.analytics|codie\.cards|codie\.probability_engine|requests|httpx|sqlite3|openai|anthropic|flask|fastapi|uvicorn|starlette" codie\weight_profiles tests\test_weight_profiles.py
rg -n "source_events|source_decks|source_deck_cards|provider_objects|raw_provider_payload|provider_payload|private_deck_text|full_primer_body|original_import_text" codie\weight_profiles tests\test_weight_profiles.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\weight_profiles tests\test_weight_profiles.py
rg -n "open\(|write_text\(|write_bytes\(|Path\(|mkdir\(|touch\(|unlink\(" codie\weight_profiles
rg -n "should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\weight_profiles tests\test_weight_profiles.py
```

Expected result:

```text
no production matches, except blocked-key constants or rejection tests where explicitly documented
```

## Do Not Do In Phase 27A

```text
do not implement weight profile code
do not generate recommendations
do not generate deck health output
do not generate replacement suggestions
do not add schema
do not add repositories
do not read SQLite
do not read providers
do not read source/provider tables
do not execute simulator logic
do not call LLMs
do not build UI
do not write files
```

## Completion Criteria

Phase 27A is complete when:

```text
this contract is created
handoff docs point to Phase 27B as the next implementation packet
Phase 26 is marked as externally accepted
tests remain passing
working tree is committed and pushed
```
