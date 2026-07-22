# Phase 37E - Tag Graph Export / Report Contract

Status: contract prepared; validation required

Phase 37E defines the future export and report boundary for already-built Tag
Graph metric packets. It does not implement export code, chart rendering, UI,
file writing, CLI behavior, report builders, schema changes, repository access,
provider access, analytics recalculation, LLM calls, simulator runtime, or
recommendation output.

Phase 37E exists to prevent future export/report work from changing the meaning
of Phase 37C Frequency Pool packets or Phase 37D Tag Graph metric packets.

## Validation Tuple

```text
phase_id: Phase37E
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase38A
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 38A is reserved for the next roadmap-priority contract packet after
Phase 37 closes. Based on the post-31 priority plan, that next priority is the
Moxfield Frequency Pool Builder contract. Phase 37E does not authorize Phase
38A implementation work.

## Accepted Dependencies

Phase 37E depends on:

```text
Phase 37A Frequency Pools / Tag Graph Lab Contract: accepted with review notes
Phase 37B Frequency Pools / Tag Graph Lab Implementation Contract: accepted with review notes
Phase 37C Frequency Pool Packet Models and Validators: PR validated
Phase 37D Tag Graph Metric Packet Models and Validators: PR validated
```

Phase 37C and Phase 37D still require final phase-ledger acceptance before
being recorded as externally complete on `main`.

## Future Authorized Scope

A later accepted implementation contract may define local, deterministic
export/report surfaces for already-built Tag Graph packets, such as:

```text
Tag Graph report document packets
Tag Graph Markdown report serialization
Tag Graph JSON report serialization
Tag Graph CSV numeric-table serialization
Tag Graph card-list serialization
Tag Graph chart-data serialization
Obsidian-compatible Markdown sections
export manifest packets
report caveat summaries
source provenance summaries
```

Future implementation must consume already-built `TagGraphPacket` objects and
must not calculate metrics from source/provider data.

## Future Public Interface Guidance

A later implementation contract may authorize interfaces similar to:

```text
TagGraphReportBuildError
TagGraphReportOptions
TagGraphReportSection
TagGraphReportDocument
TagGraphExportManifest
build_tag_graph_report_document(...)
validate_tag_graph_report_document(...)
tag_graph_report_document_to_dict(...)
tag_graph_report_document_to_markdown(...)
tag_graph_numeric_tables_to_csv_rows(...)
tag_graph_card_lists_to_csv_rows(...)
```

These names are guidance only. Phase 37E does not add production files or public
Python symbols.

## Required Future Visibility

Future export/report packets must preserve:

```text
packet_id
packet_version
generated_at
scope_type
scope_key
subject labels
comparison refs
selected tags
graph_type
numeric tables
card lists
source_packet_ids
caveat_ids
tag source provenance
coverage_ratio
matching_deck_count
available_deck_count
tag_confidence
unknown coverage markers
low sample caveats
low coverage caveats
user-local labels
```

Exports must not hide the underlying numeric tables or card lists when the
source packet includes them. If options omit a table or card list, the omission
must be explicit and auditable.

## Privacy And Evidence Boundaries

Future export/report implementation must preserve Phase 36C privacy rules and
the Phase 37A evidence boundary:

```text
raw imported deck text is never exported
private notes are never exported
primer body text is never exported
raw provider payloads are never exported
blocked private/raw keys are rejected recursively
user-local metrics remain labeled user-local
user-local metrics do not enter commander averages
simulator output is not tournament evidence
tag graphs do not produce strategic claims
LLMs may not generate single-deck advice from Tag Graph reports
```

## Forbidden In Phase 37E

Phase 37E must not add:

```text
production export code
production report builder code
chart rendering
UI work
CLI work
file writing
schema changes
repository changes
provider reads
source table reads
raw provider payload reads
analytics recalculation
metric calculation
frequency pool calculation
Tagger import
Moxfield Frequency Pool Builder
recommendation generation
deck health output
replacement output
LLM calls
simulator runtime
dependency changes
validator changes
workflow changes
constitution changes
```

## Future Required Tests

A later implementation contract should require tests proving:

```text
report document serialization is deterministic
report document round-trips through dictionary form
Markdown output preserves required evidence fields
JSON output preserves required evidence fields
CSV numeric-table output preserves metric values
CSV card-list output preserves oracle IDs and tag refs
Obsidian Markdown remains local text only
private/raw metadata is rejected recursively
strategic/action-advice language is rejected
omitted tables are explicitly labeled
omitted card lists are explicitly labeled
user-local labels remain visible
low sample caveats remain visible
low coverage caveats remain visible
no provider/database/LLM/UI/file-writing imports exist
```

## Outside Validation Packet

Phase 37E outside validation should review:

```text
docs/PHASE37E_TAG_GRAPH_EXPORT_REPORT_CONTRACT.md
docs/CHECKPOINT_PHASE37E_TAG_GRAPH_EXPORT_REPORT_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE37E_TAG_GRAPH_EXPORT_REPORT_CONTRACT_PROMPT.md
docs/PHASE37D_TAG_GRAPH_METRIC_MODELS_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE37D_TAG_GRAPH_METRIC_MODELS_IMPLEMENTATION_REPORT.md
docs/PHASE37C_FREQUENCY_POOL_MODELS_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE37C_FREQUENCY_POOL_MODELS_IMPLEMENTATION_REPORT.md
docs/PHASE37B_FREQUENCY_POOLS_TAG_GRAPH_LAB_IMPLEMENTATION_CONTRACT.md
docs/PHASE37A_FREQUENCY_POOLS_TAG_GRAPH_LAB_CONTRACT.md
docs/CODIE_V1_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Final Governance Summary

Phase 37E is complete only when this contract, checkpoint, outside-validation
prompt, and governance records are internally consistent and accepted by the
required validation path. It is a contract-only phase and does not implement Tag
Graph exports or reports.
