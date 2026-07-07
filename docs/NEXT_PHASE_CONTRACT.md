# Next Phase Contract

Recommended next task: Phase 23B - Chat/Intelligence UI/API Boundary Packet Implementation

## Current Status

Phase 14 has passed outside validation.

Phase 15B deck memory listing and retrieval is implemented.

Phase 15C deck memory CLI contract is complete.

Phase 15D deck memory CLI implementation is complete.

Phase 15E deck memory CLI usage documentation contract is complete.

Phase 15F deck memory CLI usage documentation is complete.

Phase 15G deck memory track checkpoint is complete.

Phase 15 outside validation is accepted.

Phase 16 interactive intelligence planning is complete.

Phase 16A evidence graph contract is complete.

Phase 16B evidence graph implementation is complete.

Phase 16C evidence graph checkpoint is complete.

Phase 16 outside validation is accepted.

Phase 17 interactive intelligence input assembly planning is complete.

Phase 17A evidence graph input assembly contract is complete.

Phase 17B evidence graph input assembly implementation is complete.

Phase 17C evidence graph input assembly checkpoint is complete.

Phase 17 outside validation is accepted.

Phase 18 source conflict report planning is complete.

Phase 18A source conflict report contract is complete.

Phase 18B source conflict report implementation is complete.

Phase 18C source conflict report checkpoint is complete.

Phase 18 outside validation is accepted.

Phase 19 unsupported relevant card queue planning is complete.

Phase 19A unsupported relevant card queue contract is complete.

Phase 19B unsupported relevant card queue implementation is complete.

Phase 19C unsupported relevant card queue checkpoint is complete.

Phase 19 outside validation is accepted.

Phase 20 chat query planner planning is complete.

Phase 20A chat query planner contract is complete.

Phase 20B chat query planner implementation is complete.

Phase 20C chat query planner checkpoint is complete.

Phase 20 outside validation is accepted.

Phase 21 may proceed contract-first.

Phase 21 chat answer builder planning is complete.

Phase 21A chat answer builder contract is complete.

Phase 21B chat answer builder implementation is complete.

Phase 21C chat answer builder checkpoint is complete.

Phase 21 outside validation is accepted.

Phase 22 may proceed contract-first.

Phase 22 LLM writer/auditor planning is complete.

Phase 22A LLM writer/auditor boundary contract is complete.

Phase 22B LLM writer/auditor packet implementation is complete.

Phase 22C LLM writer/auditor checkpoint packet is complete.

Phase 22 outside validation is accepted.

Phase 23 may proceed contract-first.

Phase 23A Chat/Intelligence UI/API Boundary Contract is complete.

Roadmap patch logged:

```text
docs/ROADMAP_PATCH_MOXFIELD_FREQUENCY_POOL_BUILDER.md
docs/ROADMAP_PATCH_TAG_GRAPH_LAB.md
docs/PATCH_EVIDENCE_INTELLIGENCE_AND_LOCAL_REPORTS.md
```

Phase 15 planning is complete:

```text
docs/PHASE15_PLANNING_CONTRACT.md
docs/PHASE15A_DECK_MEMORY_LISTING_RETRIEVAL_CONTRACT.md
docs/PHASE15B_DECK_MEMORY_LISTING_RETRIEVAL_IMPLEMENTATION_REPORT.md
docs/PHASE15C_DECK_MEMORY_CLI_CONTRACT.md
docs/PHASE15C_DECK_MEMORY_CLI_CONTRACT_REPORT.md
docs/PHASE15D_DECK_MEMORY_CLI_IMPLEMENTATION_REPORT.md
docs/PHASE15E_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_CONTRACT.md
docs/PHASE15E_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_CONTRACT_REPORT.md
docs/USER_GUIDE_DECK_MEMORY_CLI.md
docs/PHASE15F_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_REPORT.md
docs/CHECKPOINT_PHASE15_DECK_MEMORY_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE15_DECK_MEMORY_PROMPT.md
docs/PHASE16_INTERACTIVE_INTELLIGENCE_PLANNING_CONTRACT.md
docs/PHASE16_INTERACTIVE_INTELLIGENCE_PLANNING_REPORT.md
docs/PHASE16A_EVIDENCE_GRAPH_CONTRACT.md
docs/PHASE16A_EVIDENCE_GRAPH_CONTRACT_REPORT.md
codie/intelligence/__init__.py
codie/intelligence/evidence_graph.py
tests/test_intelligence_evidence_graph.py
docs/PHASE16B_EVIDENCE_GRAPH_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE16_EVIDENCE_GRAPH_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE16_EVIDENCE_GRAPH_PROMPT.md
docs/ROADMAP_PATCH_MOXFIELD_FREQUENCY_POOL_BUILDER.md
docs/ROADMAP_PATCH_TAG_GRAPH_LAB.md
docs/PATCH_EVIDENCE_INTELLIGENCE_AND_LOCAL_REPORTS.md
docs/REPO_REFERENCE_CATALOG.md
docs/FEATURE_SCOPE_REMOVALS.md
docs/LOCAL_REPORT_DELIVERY.md
docs/EVIDENCE_GRAPH_SPEC.md
docs/CO_OCCURRENCE_METRICS_SPEC.md
docs/FREQUENCY_POOL_SPEC.md
docs/COMMANDER_STAPLES_SPEC.md
docs/CODIE_CHAT_SPEC.md
docs/PHASE17_INTERACTIVE_INTELLIGENCE_INPUT_ASSEMBLY_PLANNING_CONTRACT.md
docs/PHASE17_INTERACTIVE_INTELLIGENCE_INPUT_ASSEMBLY_PLANNING_REPORT.md
docs/PHASE17A_EVIDENCE_GRAPH_INPUT_ASSEMBLY_CONTRACT.md
docs/PHASE17A_EVIDENCE_GRAPH_INPUT_ASSEMBLY_CONTRACT_REPORT.md
codie/intelligence/evidence_inputs.py
tests/test_intelligence_evidence_inputs.py
docs/PHASE17B_EVIDENCE_GRAPH_INPUT_ASSEMBLY_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE17_INPUT_ASSEMBLY_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE17_INPUT_ASSEMBLY_PROMPT.md
docs/PHASE18_SOURCE_CONFLICT_REPORT_PLANNING_CONTRACT.md
docs/PHASE18_SOURCE_CONFLICT_REPORT_PLANNING_REPORT.md
docs/PHASE18A_SOURCE_CONFLICT_REPORT_CONTRACT.md
docs/PHASE18A_SOURCE_CONFLICT_REPORT_CONTRACT_REPORT.md
codie/intelligence/source_conflicts.py
tests/test_intelligence_source_conflicts.py
docs/PHASE18B_SOURCE_CONFLICT_REPORT_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE18_SOURCE_CONFLICT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE18_SOURCE_CONFLICT_PROMPT.md
docs/PHASE19_UNSUPPORTED_RELEVANT_CARD_QUEUE_PLANNING_CONTRACT.md
docs/PHASE19_UNSUPPORTED_RELEVANT_CARD_QUEUE_PLANNING_REPORT.md
docs/PHASE19A_UNSUPPORTED_RELEVANT_CARD_QUEUE_CONTRACT.md
docs/PHASE19A_UNSUPPORTED_RELEVANT_CARD_QUEUE_CONTRACT_REPORT.md
codie/intelligence/unsupported_cards.py
tests/test_intelligence_unsupported_cards.py
docs/PHASE19B_UNSUPPORTED_RELEVANT_CARD_QUEUE_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE19_UNSUPPORTED_CARD_QUEUE_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE19_UNSUPPORTED_CARD_QUEUE_PROMPT.md
docs/PHASE20_CHAT_QUERY_PLANNER_PLANNING_CONTRACT.md
docs/PHASE20_CHAT_QUERY_PLANNER_PLANNING_REPORT.md
docs/PHASE20A_CHAT_QUERY_PLANNER_CONTRACT.md
docs/PHASE20A_CHAT_QUERY_PLANNER_CONTRACT_REPORT.md
codie/intelligence/query_planner.py
tests/test_intelligence_query_planner.py
docs/PHASE20B_CHAT_QUERY_PLANNER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE20_CHAT_QUERY_PLANNER_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE20_CHAT_QUERY_PLANNER_PROMPT.md
docs/PHASE21_CHAT_ANSWER_BUILDER_PLANNING_CONTRACT.md
docs/PHASE21_CHAT_ANSWER_BUILDER_PLANNING_REPORT.md
docs/PHASE21A_CHAT_ANSWER_BUILDER_CONTRACT.md
docs/PHASE21A_CHAT_ANSWER_BUILDER_CONTRACT_REPORT.md
codie/intelligence/answer_builder.py
tests/test_intelligence_answer_builder.py
docs/PHASE21B_CHAT_ANSWER_BUILDER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE21_CHAT_ANSWER_BUILDER_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE21_CHAT_ANSWER_BUILDER_PROMPT.md
docs/PHASE22_LLM_WRITER_AUDITOR_PLANNING_CONTRACT.md
docs/PHASE22_LLM_WRITER_AUDITOR_PLANNING_REPORT.md
docs/PHASE22A_LLM_WRITER_AUDITOR_CONTRACT.md
docs/PHASE22A_LLM_WRITER_AUDITOR_CONTRACT_REPORT.md
docs/PHASE22B_LLM_WRITER_AUDITOR_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE22_LLM_WRITER_AUDITOR_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE22_LLM_WRITER_AUDITOR_PROMPT.md
docs/PHASE23A_CHAT_INTELLIGENCE_UI_API_BOUNDARY_CONTRACT.md
docs/PHASE23A_CHAT_INTELLIGENCE_UI_API_BOUNDARY_CONTRACT_REPORT.md
codie/intelligence/llm_writer_auditor.py
tests/test_intelligence_llm_writer_auditor.py
```

## Phase 15 Direction

Start with deck memory over existing user tables before building chat or LLM
features.

Use existing tables first:

```text
user_decks
user_deck_cards
analysis_sessions
saved_analysis
```

Do not add schema in Phase 15B.

## Files Created Or Modified In Latest Packet

```text
codie/db/repositories/user.py
codie/user_decks/deck_memory.py
codie/user_decks/__init__.py
tests/test_user_deck_memory.py
docs/PHASE15B_DECK_MEMORY_LISTING_RETRIEVAL_IMPLEMENTATION_REPORT.md
docs/PHASE15C_DECK_MEMORY_CLI_CONTRACT.md
docs/PHASE15C_DECK_MEMORY_CLI_CONTRACT_REPORT.md
codie/cli/user_deck_memory.py
tests/test_cli_user_deck_memory.py
docs/PHASE15D_DECK_MEMORY_CLI_IMPLEMENTATION_REPORT.md
docs/PHASE15E_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_CONTRACT.md
docs/PHASE15E_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_CONTRACT_REPORT.md
docs/USER_GUIDE_DECK_MEMORY_CLI.md
docs/PHASE15F_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_REPORT.md
docs/CHECKPOINT_PHASE15_DECK_MEMORY_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE15_DECK_MEMORY_PROMPT.md
docs/PHASE16_INTERACTIVE_INTELLIGENCE_PLANNING_CONTRACT.md
docs/PHASE16_INTERACTIVE_INTELLIGENCE_PLANNING_REPORT.md
docs/PHASE16A_EVIDENCE_GRAPH_CONTRACT.md
docs/PHASE16A_EVIDENCE_GRAPH_CONTRACT_REPORT.md
codie/intelligence/__init__.py
codie/intelligence/evidence_graph.py
tests/test_intelligence_evidence_graph.py
docs/PHASE16B_EVIDENCE_GRAPH_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE16_EVIDENCE_GRAPH_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE16_EVIDENCE_GRAPH_PROMPT.md
docs/ROADMAP_PATCH_MOXFIELD_FREQUENCY_POOL_BUILDER.md
docs/PHASE17_INTERACTIVE_INTELLIGENCE_INPUT_ASSEMBLY_PLANNING_CONTRACT.md
docs/PHASE17_INTERACTIVE_INTELLIGENCE_INPUT_ASSEMBLY_PLANNING_REPORT.md
docs/PHASE17A_EVIDENCE_GRAPH_INPUT_ASSEMBLY_CONTRACT.md
docs/PHASE17A_EVIDENCE_GRAPH_INPUT_ASSEMBLY_CONTRACT_REPORT.md
codie/intelligence/evidence_inputs.py
tests/test_intelligence_evidence_inputs.py
docs/PHASE17B_EVIDENCE_GRAPH_INPUT_ASSEMBLY_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE17_INPUT_ASSEMBLY_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE17_INPUT_ASSEMBLY_PROMPT.md
docs/PHASE18_SOURCE_CONFLICT_REPORT_PLANNING_CONTRACT.md
docs/PHASE18_SOURCE_CONFLICT_REPORT_PLANNING_REPORT.md
docs/PHASE18A_SOURCE_CONFLICT_REPORT_CONTRACT.md
docs/PHASE18A_SOURCE_CONFLICT_REPORT_CONTRACT_REPORT.md
codie/intelligence/source_conflicts.py
tests/test_intelligence_source_conflicts.py
docs/PHASE18B_SOURCE_CONFLICT_REPORT_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE18_SOURCE_CONFLICT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE18_SOURCE_CONFLICT_PROMPT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Schema Impact

None.

## Completed Phase 15B Scope

Phase 15B added:

```text
codie/user_decks/deck_memory.py
codie/user_decks/__init__.py
tests/test_user_deck_memory.py
docs/PHASE15B_DECK_MEMORY_LISTING_RETRIEVAL_IMPLEMENTATION_REPORT.md
```

## Required Behavior

Implement:

```text
DeckMemoryReadError
DeckMemoryFilters
DeckMemorySummary
DeckMemoryCard
DeckMemoryAnalysisSummary
DeckMemorySessionSummary
DeckMemoryDetail
list_deck_memory(...)
get_deck_memory_detail(...)
```

The implementation:

```text
list saved/imported user decks
filter by commander_hash
filter by deck_hash
filter temporary vs persistent deck records
show deck memory detail
include linked saved_analysis summaries
include linked analysis_sessions
include resolved card rows
include raw_input only in detail view
```

## Completed Phase 15C Scope

Phase 15C defined the contract for:

```text
Deck Memory CLI Contract
```

Required future CLI behavior:

```text
list remembered decks
show one remembered deck detail
filter by commander_hash
filter by deck_hash
include/exclude temporary decks
output JSON only by default
do not export raw_input unless explicitly requested
```

## Completed Phase 15D Scope

Phase 15D added:

```text
codie/cli/user_deck_memory.py
tests/test_cli_user_deck_memory.py
docs/PHASE15D_DECK_MEMORY_CLI_IMPLEMENTATION_REPORT.md
```

Commands:

```text
list-deck-memory
show-deck-memory
```

Phase 15D behavior:

```text
list remembered deck summaries as JSON
show one remembered deck detail as JSON
omit raw_input by default
include raw_input only with --include-raw-input
fail cleanly for missing database paths
fail cleanly for unknown user_deck_id
```

## Completed Phase 15E Scope

Phase 15E defined the contract for:

```text
Deck Memory CLI Usage Documentation Contract
```

Required future documentation:

```text
docs/USER_GUIDE_DECK_MEMORY_CLI.md
docs/PHASE15F_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_REPORT.md
```

The usage guide should explain:

```text
how to list remembered decks
how to show a remembered deck
privacy warning for --include-raw-input
JSON output examples
that user deck memory is not tournament evidence
that CLI does not generate recommendations
```

## Completed Phase 15F Scope

Phase 15F added:

```text
docs/USER_GUIDE_DECK_MEMORY_CLI.md
docs/PHASE15F_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_REPORT.md
```

Phase 15F must document:

```text
list-deck-memory usage
show-deck-memory usage
privacy warning for --include-raw-input
JSON examples using synthetic data only
failure behavior
that user deck memory is local user data
that user deck memory is not tournament evidence
that no recommendations are generated
```

## Completed Phase 15G Scope

Phase 15G created:

```text
docs/CHECKPOINT_PHASE15_DECK_MEMORY_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE15_DECK_MEMORY_PROMPT.md
```

The checkpoint should cover:

```text
Phase 15 planning
Phase 15B deck memory read layer
Phase 15D deck memory CLI
Phase 15F usage documentation
privacy defaults
no schema changes
no provider/source reads
no recommendations
full test output
boundary scans
```

## Completed Phase 15 Validation Scope

Phase 15 outside validation accepted:

```text
PASS
```

## Completed Phase 16 Planning Scope

Phase 16 planning created:

```text
docs/PHASE16_INTERACTIVE_INTELLIGENCE_PLANNING_CONTRACT.md
docs/PHASE16_INTERACTIVE_INTELLIGENCE_PLANNING_REPORT.md
```

Planning decision:

```text
Start with Phase 16A - Evidence Graph Contract.
Do not start with chat UI or LLM calls.
```

## Completed Phase 16A Scope

Phase 16A defined:

```text
Evidence Graph Contract
```

Future implementation files:

```text
codie/intelligence/__init__.py
codie/intelligence/evidence_graph.py
tests/test_intelligence_evidence_graph.py
docs/PHASE16B_EVIDENCE_GRAPH_IMPLEMENTATION_REPORT.md
```

## Completed Phase 16B Scope

Phase 16B implemented:

```text
EvidenceGraph
EvidenceNode
EvidenceEdge
EvidenceCitation
EvidenceCaveat
EvidenceGraphBuildError
graph construction inputs
serialization shape
allowed node/edge types
privacy flags
confidence/caveat fields
strategic-language restrictions
tests for future implementation
```

Phase 16B remains:

```text
in-memory
deterministic
JSON-compatible
privacy-aware
evidence-first
```

## Next Checkpoint Scope

Phase 16C should create:

```text
docs/CHECKPOINT_PHASE16_EVIDENCE_GRAPH_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE16_EVIDENCE_GRAPH_PROMPT.md
```

The checkpoint should cover:

```text
Phase 16 planning
Phase 16A contract
Phase 16B implementation
evidence graph boundaries
privacy metadata rejection
no schema changes
no DB access
no provider/source reads
no LLM calls
no recommendation generation
full test output
static scans
```

## Completed Phase 18C Scope

Phase 18C created:

```text
docs/CHECKPOINT_PHASE18_SOURCE_CONFLICT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE18_SOURCE_CONFLICT_PROMPT.md
```

The checkpoint covers:

```text
Phase 18 planning
Phase 18A source conflict contract
Phase 18B source conflict implementation
source conflict boundaries
private metadata rejection
sensitive evidence filtering
resolved conflict filtering
blocking conflict preservation
conversion to EvidenceInputRecord values
no schema changes
no DB access
no provider/source reads
no LLM calls
no recommendation generation
full test output
static scans
```

Phase 18 outside validation returned:

```text
PASS
```

Phase 19 may proceed contract-first.

## Completed Phase 19 Planning Scope

Phase 19 planning created:

```text
docs/PHASE19_UNSUPPORTED_RELEVANT_CARD_QUEUE_PLANNING_CONTRACT.md
docs/PHASE19_UNSUPPORTED_RELEVANT_CARD_QUEUE_PLANNING_REPORT.md
```

Planning decision:

```text
Start with Phase 19A - Unsupported Relevant Card Queue Contract.
Do not start with chat UI, LLM calls, persistence, card behavior implementation,
or recommendation generation.
```

## Completed Phase 19A Scope

Phase 19A created:

```text
docs/PHASE19A_UNSUPPORTED_RELEVANT_CARD_QUEUE_CONTRACT.md
docs/PHASE19A_UNSUPPORTED_RELEVANT_CARD_QUEUE_CONTRACT_REPORT.md
```

Future implementation files:

```text
codie/intelligence/unsupported_cards.py
tests/test_intelligence_unsupported_cards.py
docs/PHASE19B_UNSUPPORTED_RELEVANT_CARD_QUEUE_IMPLEMENTATION_REPORT.md
```

Future public interface:

```text
UnsupportedCardQueueBuildError
UnsupportedCardEvidenceRef
UnsupportedCardQueueItem
UnsupportedCardQueue
UnsupportedCardQueueOptions
build_unsupported_card_queue(...)
unsupported_card_queue_to_input_records(...)
unsupported_card_queue_to_dict(...)
```

## Do Not Do In Phase 19B

```text
do not add schema
do not add DB reads or writes
do not add repository imports
do not call providers
do not read source/provider payloads directly
do not add UI
do not call LLMs
do not run simulator logic
do not implement card behavior
do not calculate analytics
do not generate recommendations
do not write files
do not export private raw_input
```

## Completed Phase 19B Scope

Phase 19B implemented:

```text
UnsupportedCardQueueBuildError
UnsupportedCardEvidenceRef
UnsupportedCardQueueItem
UnsupportedCardQueue
UnsupportedCardQueueOptions
build_unsupported_card_queue(...)
unsupported_card_queue_to_input_records(...)
unsupported_card_queue_to_dict(...)
```

Phase 19B remains:

```text
pure
in-memory
sanitized-input only
deterministic
privacy-aware
evidence-first
```

## Completed Phase 19C Scope

Phase 19C created:

```text
docs/CHECKPOINT_PHASE19_UNSUPPORTED_CARD_QUEUE_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE19_UNSUPPORTED_CARD_QUEUE_PROMPT.md
```

The checkpoint covers:

```text
Phase 19 planning
Phase 19A unsupported-card queue contract
Phase 19B unsupported-card queue implementation
unsupported-card queue boundaries
private metadata rejection
sensitive evidence filtering
resolved item filtering
blocking item preservation
conversion to EvidenceInputRecord values
no schema changes
no DB access
no provider/source reads
no LLM calls
no simulator execution
no card behavior implementation
no recommendation generation
full test output
static scans
```

Phase 19 outside validation returned:

```text
PASS
```

Phase 20 may proceed contract-first.

## Completed Phase 20 Planning Scope

Phase 20 planning created:

```text
docs/PHASE20_CHAT_QUERY_PLANNER_PLANNING_CONTRACT.md
docs/PHASE20_CHAT_QUERY_PLANNER_PLANNING_REPORT.md
```

Planning decision:

```text
Start with Phase 20A - Chat Query Planner Contract.
Do not start with chat UI, LLM calls, answer generation, persistence, or
recommendation generation.
```

## Completed Phase 20A Scope

Phase 20A created:

```text
docs/PHASE20A_CHAT_QUERY_PLANNER_CONTRACT.md
docs/PHASE20A_CHAT_QUERY_PLANNER_CONTRACT_REPORT.md
```

Future implementation files:

```text
codie/intelligence/query_planner.py
tests/test_intelligence_query_planner.py
docs/PHASE20B_CHAT_QUERY_PLANNER_IMPLEMENTATION_REPORT.md
```

Future public interface:

```text
ChatQueryPlanBuildError
ChatQueryRequest
ChatQuerySubject
ChatEvidenceNeed
ChatQueryConstraint
ChatQueryPlan
ChatQueryPlannerOptions
build_chat_query_plan(...)
chat_query_plan_to_dict(...)
```

## Do Not Do In Phase 20B

```text
do not add schema
do not add DB reads or writes
do not add repository imports
do not call providers
do not read source/provider payloads directly
do not add UI
do not call LLMs
do not generate final answer text
do not run simulator logic
do not implement card behavior
do not calculate analytics
do not generate recommendations
do not write files
do not export private raw_input
```

## Completed Phase 20B Scope

Phase 20B implemented:

```text
ChatQueryPlanBuildError
ChatQueryRequest
ChatQuerySubject
ChatEvidenceNeed
ChatQueryConstraint
ChatQueryPlan
ChatQueryPlannerOptions
build_chat_query_plan(...)
chat_query_plan_to_dict(...)
```

Phase 20B remains:

```text
pure
in-memory
sanitized-input only
deterministic
privacy-aware
evidence-first
```

## Completed Phase 20C Scope

Phase 20C created:

```text
docs/CHECKPOINT_PHASE20_CHAT_QUERY_PLANNER_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE20_CHAT_QUERY_PLANNER_PROMPT.md
```

The checkpoint covers:

```text
Phase 20 planning
Phase 20A chat query planner contract
Phase 20B chat query planner implementation
query planner boundaries
private metadata rejection
privacy-scope blockers
unknown-question caveats
no schema changes
no DB access
no provider/source reads
no LLM calls
no answer generation
no simulator execution
no recommendation generation
full test output
static scans
```

## Phase 21 Gate

```text
Phase 20 outside validation returned PASS.
Phase 21 may proceed contract-first.
Do not start answer generation, chat UI, LLM workflows, persistence, simulator integration, or recommendations without a Phase 21 contract.
```

## Completed Phase 21 Planning Scope

Phase 21 planning created:

```text
docs/PHASE21_CHAT_ANSWER_BUILDER_PLANNING_CONTRACT.md
docs/PHASE21_CHAT_ANSWER_BUILDER_PLANNING_REPORT.md
```

Planning decision:

```text
Start with Phase 21A - Chat Answer Builder Contract.
Do not start with chat UI, LLM calls, answer persistence, DB/repository readers,
provider calls, source/provider payload reads, simulator execution, analytics,
or recommendation generation.
```

Recommended Phase 21A contract files:

```text
docs/PHASE21A_CHAT_ANSWER_BUILDER_CONTRACT.md
docs/PHASE21A_CHAT_ANSWER_BUILDER_CONTRACT_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Future implementation files, after contract acceptance:

```text
codie/intelligence/answer_builder.py
tests/test_intelligence_answer_builder.py
docs/PHASE21B_CHAT_ANSWER_BUILDER_IMPLEMENTATION_REPORT.md
```

## Completed Phase 21A Scope

Phase 21A created:

```text
docs/PHASE21A_CHAT_ANSWER_BUILDER_CONTRACT.md
docs/PHASE21A_CHAT_ANSWER_BUILDER_CONTRACT_REPORT.md
```

Future implementation files:

```text
codie/intelligence/answer_builder.py
tests/test_intelligence_answer_builder.py
docs/PHASE21B_CHAT_ANSWER_BUILDER_IMPLEMENTATION_REPORT.md
```

Future public interface:

```text
ChatAnswerBuildError
ChatAnswerInput
ChatAnswerSection
ChatAnswerCitation
ChatAnswerCaveat
ChatAnswerMissingEvidence
ChatAnswer
ChatAnswerBuilderOptions
build_chat_answer(...)
chat_answer_to_dict(...)
```

## Do Not Do In Phase 21B

```text
do not add schema
do not add DB reads or writes
do not add repository imports
do not call providers
do not read source/provider payloads directly
do not add UI
do not call LLMs
do not run simulator logic
do not implement card behavior
do not calculate analytics
do not generate recommendations
do not write files
do not export private raw_input
```

## Completed Phase 21B Scope

Phase 21B implemented:

```text
ChatAnswerBuildError
ChatAnswerInput
ChatAnswerSection
ChatAnswerCitation
ChatAnswerCaveat
ChatAnswerMissingEvidence
ChatAnswer
ChatAnswerBuilderOptions
build_chat_answer(...)
chat_answer_to_dict(...)
```

Phase 21B remains:

```text
pure
in-memory
sanitized-input only
deterministic
privacy-aware
evidence-first
```

## Completed Phase 21C Scope

Phase 21C created:

```text
docs/CHECKPOINT_PHASE21_CHAT_ANSWER_BUILDER_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE21_CHAT_ANSWER_BUILDER_PROMPT.md
```

The checkpoint covers:

```text
Phase 21 planning
Phase 21A chat answer builder contract
Phase 21B chat answer builder implementation
answer builder boundaries
citation requirements
missing-evidence handling
source-conflict caveat preservation
unsupported-card caveat preservation
unknown-question caveats
private metadata rejection
no schema changes
no DB access
no provider/source reads
no LLM calls
no simulator execution
no recommendation generation
full test output
static scans
```

## Phase 22 Gate

```text
Phase 21 outside validation returned PASS.
Phase 22 may proceed contract-first.
Do not start LLM writer/auditor workflows, chat UI, persistence, simulator integration, analytics, or recommendations without a Phase 22 contract.
```

## Completed Phase 22 Planning Scope

Phase 22 planning created:

```text
docs/PHASE22_LLM_WRITER_AUDITOR_PLANNING_CONTRACT.md
docs/PHASE22_LLM_WRITER_AUDITOR_PLANNING_REPORT.md
```

Planning decision:

```text
Start with Phase 22A - LLM Writer/Auditor Boundary Contract.
Do not start with real LLM calls, chat UI, cloud provider wiring, answer
persistence, DB/repository readers, provider calls, source/provider payload
reads, simulator execution, analytics, or recommendation generation.
```

Recommended Phase 22A contract files:

```text
docs/PHASE22A_LLM_WRITER_AUDITOR_CONTRACT.md
docs/PHASE22A_LLM_WRITER_AUDITOR_CONTRACT_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Future implementation files, after contract acceptance:

```text
codie/intelligence/llm_writer_auditor.py
tests/test_intelligence_llm_writer_auditor.py
docs/PHASE22B_LLM_WRITER_AUDITOR_IMPLEMENTATION_REPORT.md
```

## Completed Phase 22A Scope

Phase 22A created:

```text
docs/PHASE22A_LLM_WRITER_AUDITOR_CONTRACT.md
docs/PHASE22A_LLM_WRITER_AUDITOR_CONTRACT_REPORT.md
```

Future implementation files:

```text
codie/intelligence/llm_writer_auditor.py
tests/test_intelligence_llm_writer_auditor.py
docs/PHASE22B_LLM_WRITER_AUDITOR_IMPLEMENTATION_REPORT.md
```

Future public interface:

```text
LLMWriterAuditorBuildError
LLMWriterInput
LLMWriterDraft
LLMAuditFinding
LLMAuditResult
LLMWriterAuditorOptions
build_writer_input_from_answer(...)
validate_writer_draft(...)
audit_writer_draft(...)
llm_writer_input_to_dict(...)
llm_writer_draft_to_dict(...)
llm_audit_result_to_dict(...)
```

## Do Not Do In Phase 22B

```text
do not add schema
do not add DB reads or writes
do not add repository imports
do not call providers
do not read source/provider payloads directly
do not add UI
do not call real LLM APIs
do not import LLM SDKs
do not run simulator logic
do not implement card behavior
do not calculate analytics
do not generate recommendations
do not write files
do not export private raw_input
```

## Completed Phase 22B Scope

Phase 22B created:

```text
codie/intelligence/llm_writer_auditor.py
tests/test_intelligence_llm_writer_auditor.py
docs/PHASE22B_LLM_WRITER_AUDITOR_IMPLEMENTATION_REPORT.md
```

Phase 22B modified:

```text
codie/intelligence/__init__.py
```

Implemented public interface:

```text
LLMWriterAuditorBuildError
LLMWriterInput
LLMWriterDraft
LLMAuditFinding
LLMAuditResult
LLMWriterAuditorOptions
build_writer_input_from_answer(...)
validate_writer_draft(...)
audit_writer_draft(...)
llm_writer_input_to_dict(...)
llm_writer_draft_to_dict(...)
llm_audit_result_to_dict(...)
```

Phase 22C created:

```text
docs/CHECKPOINT_PHASE22_LLM_WRITER_AUDITOR_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE22_LLM_WRITER_AUDITOR_PROMPT.md
```

## Completed Phase 22C Scope

Phase 22C created:

```text
docs/CHECKPOINT_PHASE22_LLM_WRITER_AUDITOR_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE22_LLM_WRITER_AUDITOR_PROMPT.md
```

Phase 22 outside validation packet:

```text
docs/CHECKPOINT_PHASE22_LLM_WRITER_AUDITOR_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE22_LLM_WRITER_AUDITOR_PROMPT.md
docs/PHASE22_LLM_WRITER_AUDITOR_PLANNING_CONTRACT.md
docs/PHASE22A_LLM_WRITER_AUDITOR_CONTRACT.md
docs/PHASE22B_LLM_WRITER_AUDITOR_IMPLEMENTATION_REPORT.md
codie/intelligence/llm_writer_auditor.py
tests/test_intelligence_llm_writer_auditor.py
codie/intelligence/answer_builder.py
codie/intelligence/__init__.py
```

## Completed Phase 23A Scope

Phase 23A created:

```text
docs/PHASE23A_CHAT_INTELLIGENCE_UI_API_BOUNDARY_CONTRACT.md
docs/PHASE23A_CHAT_INTELLIGENCE_UI_API_BOUNDARY_CONTRACT_REPORT.md
```

Future implementation files:

```text
codie/intelligence/ui_api_boundary.py
tests/test_intelligence_ui_api_boundary.py
docs/PHASE23B_CHAT_INTELLIGENCE_UI_API_BOUNDARY_IMPLEMENTATION_REPORT.md
```

Future public interface:

```text
ChatUIBoundaryBuildError
ChatUIRequestPacket
ChatUIResponsePacket
ChatUIErrorPacket
ChatUIBoundaryOptions
build_chat_ui_request_packet(...)
build_chat_ui_response_packet(...)
build_chat_ui_error_packet(...)
chat_ui_request_packet_to_dict(...)
chat_ui_response_packet_to_dict(...)
chat_ui_error_packet_to_dict(...)
```

## Do Not Do In Phase 23B

```text
do not add schema
do not add DB reads or writes
do not add repository imports
do not call providers
do not read source/provider payloads directly
do not add UI
do not add an HTTP server
do not call real LLM APIs
do not import LLM SDKs
do not run simulator logic
do not implement card behavior
do not calculate analytics
do not generate recommendations
do not write files
do not export private raw_input
```

## Completed Phase 17C Scope

Phase 17C created:

```text
docs/CHECKPOINT_PHASE17_INPUT_ASSEMBLY_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE17_INPUT_ASSEMBLY_PROMPT.md
```

The checkpoint covers:

```text
Phase 17 planning
Phase 17A input assembly contract
Phase 17B input assembly implementation
input assembly boundaries
private metadata rejection
sensitive filtering
local_user_data privacy preservation
no schema changes
no DB access
no provider/source reads
no LLM calls
no recommendation generation
full test output
static scans
```

Phase 18 is blocked until Phase 17 outside validation returns:

```text
PASS
PASS WITH REVIEW NOTES
```

## Do Not Do Before Phase 17 Outside Validation

```text
do not start Phase 18
do not add chat UI
do not add LLM calls
do not add evidence graph persistence
do not connect input assembly to DB/repository reads
do not connect input assembly to provider/source payloads
do not generate recommendations
do not export private raw_input
```

## Completed Phase 17 Outside Validation

Phase 17 outside validation returned:

```text
PASS
```

Phase 18 may proceed contract-first.

## Completed Phase 18 Planning Scope

Phase 18 planning created:

```text
docs/PHASE18_SOURCE_CONFLICT_REPORT_PLANNING_CONTRACT.md
docs/PHASE18_SOURCE_CONFLICT_REPORT_PLANNING_REPORT.md
```

Planning decision:

```text
Start with Phase 18A - Source Conflict Report Contract.
Do not start with chat UI, LLM calls, persistence, or recommendation generation.
```

## Completed Phase 18A Scope

Phase 18A created:

```text
docs/PHASE18A_SOURCE_CONFLICT_REPORT_CONTRACT.md
docs/PHASE18A_SOURCE_CONFLICT_REPORT_CONTRACT_REPORT.md
```

Future implementation files:

```text
codie/intelligence/source_conflicts.py
tests/test_intelligence_source_conflicts.py
docs/PHASE18B_SOURCE_CONFLICT_REPORT_IMPLEMENTATION_REPORT.md
```

Future public interface:

```text
SourceConflictBuildError
SourceConflictEvidenceRef
SourceConflictItem
SourceConflictReport
SourceConflictReportOptions
build_source_conflict_report(...)
source_conflict_report_to_input_records(...)
source_conflict_report_to_dict(...)
```

## Do Not Do In Phase 18B

```text
do not add schema
do not add DB reads or writes
do not add repository imports
do not call providers
do not read source/provider payloads directly
do not add UI
do not call LLMs
do not run simulator logic
do not calculate analytics
do not generate recommendations
do not write files
do not export private raw_input
```

## Completed Phase 18B Scope

Phase 18B implemented:

```text
SourceConflictBuildError
SourceConflictEvidenceRef
SourceConflictItem
SourceConflictReport
SourceConflictReportOptions
build_source_conflict_report(...)
source_conflict_report_to_input_records(...)
source_conflict_report_to_dict(...)
```

Phase 18B remains:

```text
pure
in-memory
sanitized-input only
deterministic
privacy-aware
evidence-first
```

## Next Checkpoint Scope

Phase 18C should create:

```text
docs/CHECKPOINT_PHASE18_SOURCE_CONFLICT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE18_SOURCE_CONFLICT_PROMPT.md
```

The checkpoint should cover:

```text
Phase 18 planning
Phase 18A source conflict contract
Phase 18B source conflict implementation
source conflict boundaries
private metadata rejection
sensitive evidence filtering
resolved conflict filtering
blocking conflict preservation
conversion to EvidenceInputRecord values
no schema changes
no DB access
no provider/source reads
no LLM calls
no recommendation generation
full test output
static scans
```

## Completed Phase 16C Scope

Phase 16C created:

```text
docs/CHECKPOINT_PHASE16_EVIDENCE_GRAPH_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE16_EVIDENCE_GRAPH_PROMPT.md
```

The checkpoint covers:

```text
Phase 16 planning
Phase 16A evidence graph contract
Phase 16B evidence graph implementation
evidence graph boundaries
privacy metadata rejection
deterministic serialization
no schema changes
no DB access
no provider/source reads
no LLM calls
no recommendation generation
full test output
static scans
```

Phase 17 is blocked until Phase 16 outside validation returns:

```text
PASS
PASS WITH REVIEW NOTES
```

## Validation Command

Use the bundled Python runtime when system Python is unavailable:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Static checks for Phase 15B:

```text
git diff --check
rg -n "codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|codie\.probability_engine|codie\.canonical|requests|httpx|sqlite3" codie\user_decks\deck_memory.py tests\test_user_deck_memory.py
rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\user_decks\deck_memory.py tests\test_user_deck_memory.py
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\user_decks\deck_memory.py tests\test_user_deck_memory.py
```

Static checks for Phase 15D:

```text
git diff --check
rg -n "codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|codie\.probability_engine|codie\.canonical|requests|httpx|sqlite3" codie\cli\user_deck_memory.py tests\test_cli_user_deck_memory.py
rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\cli\user_deck_memory.py tests\test_cli_user_deck_memory.py
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\cli\user_deck_memory.py tests\test_cli_user_deck_memory.py
```

## Known Caveats / Review Notes

- Deck memory is user-local only.
- User decks are not tournament evidence.
- User deck memory must not read source/provider tables.
- Chat UI and LLM features remain deferred.
- Private deck text must not be exported or uploaded without explicit user
  action and a future contract.

## Do Not Do In Phase 15B

```text
do not add schema
do not add CLI
do not add UI
do not export private deck text
do not call providers
do not read source/provider tables
do not run simulator
do not calculate recommendations
do not call LLMs
do not treat user decks as tournament evidence
```

## Do Not Do In Phase 15C Contract

```text
do not implement CLI code until the contract is accepted
do not add schema
do not add UI
do not call LLMs
do not export private deck text by default
do not generate recommendations
```

## Do Not Do In Phase 15D

```text
do not add schema
do not add UI
do not call LLMs
do not call providers
do not read source/provider tables
do not run simulator
do not calculate analytics
do not generate recommendations
do not export private deck text by default
```

## Do Not Do In Phase 15E Contract

```text
do not implement new code
do not add schema
do not add UI
do not call providers
do not call LLMs
do not generate recommendations
do not tell users to upload or share raw deck text
```

## Do Not Do In Phase 15F

```text
do not add code
do not add schema
do not add UI
do not call providers
do not call LLMs
do not generate recommendations
do not include real private deck text in examples
do not tell users to upload or share raw deck text
```

## Do Not Do In Phase 15G

```text
do not add code
do not add schema
do not add UI
do not call providers
do not call LLMs
do not generate recommendations
do not weaken raw_input privacy defaults
```

## Do Not Do In Phase 16C

```text
do not add schema
do not add implementation code
do not add UI
do not add DB reads or writes
do not call providers
do not call LLMs
do not generate recommendations
do not read source/provider payloads directly
do not export private raw_input
do not import recommendation generation or persistence
```

## Do Not Do Before Phase 16 Outside Validation

```text
do not start Phase 17
do not add evidence graph persistence
do not add chat UI
do not add LLM writer/auditor workflows
do not connect evidence graphs to recommendation output
do not treat roadmap-only Moxfield Frequency Pool Builder as approved implementation scope
```

## Completed Phase 16 Outside Validation

Phase 16 outside validation returned:

```text
PASS
```

Phase 17 may proceed contract-first.

## Completed Phase 17 Planning Scope

Phase 17 planning created:

```text
docs/PHASE17_INTERACTIVE_INTELLIGENCE_INPUT_ASSEMBLY_PLANNING_CONTRACT.md
docs/PHASE17_INTERACTIVE_INTELLIGENCE_INPUT_ASSEMBLY_PLANNING_REPORT.md
```

Planning decision:

```text
Start with Phase 17A - Evidence Graph Input Assembly Contract.
Do not start with chat UI, LLM calls, persistence, or recommendation generation.
```

## Completed Phase 17A Scope

Phase 17A created:

```text
docs/PHASE17A_EVIDENCE_GRAPH_INPUT_ASSEMBLY_CONTRACT.md
docs/PHASE17A_EVIDENCE_GRAPH_INPUT_ASSEMBLY_CONTRACT_REPORT.md
```

Future implementation files:

```text
codie/intelligence/evidence_inputs.py
tests/test_intelligence_evidence_inputs.py
docs/PHASE17B_EVIDENCE_GRAPH_INPUT_ASSEMBLY_IMPLEMENTATION_REPORT.md
```

Future public interface:

```text
EvidenceInputBuildError
EvidenceRecordRef
EvidenceInputRecord
EvidenceInputBundle
EvidenceGraphAssemblyOptions
evidence_record_from_dict(...)
validate_evidence_input_bundle(...)
build_graph_input_from_records(...)
```

## Do Not Do In Phase 17B

```text
do not add schema
do not add DB reads or writes
do not add repository imports
do not call providers
do not read source/provider payloads directly
do not add UI
do not call LLMs
do not run simulator logic
do not calculate analytics
do not generate recommendations
do not write files
do not export private raw_input
```

## Completed Phase 17B Scope

Phase 17B implemented:

```text
EvidenceInputBuildError
EvidenceRecordRef
EvidenceInputRecord
EvidenceInputBundle
EvidenceGraphAssemblyOptions
evidence_record_from_dict(...)
validate_evidence_input_bundle(...)
build_graph_input_from_records(...)
```

Phase 17B remains:

```text
pure
in-memory
sanitized-input only
deterministic
privacy-aware
evidence-first
```

## Next Checkpoint Scope

Phase 17C should create:

```text
docs/CHECKPOINT_PHASE17_INPUT_ASSEMBLY_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE17_INPUT_ASSEMBLY_PROMPT.md
```

The checkpoint should cover:

```text
Phase 17 planning
Phase 17A contract
Phase 17B implementation
input assembly boundaries
private metadata rejection
sensitive filtering
local_user_data privacy preservation
no schema changes
no DB access
no provider/source reads
no LLM calls
no recommendation generation
full test output
static scans
```
