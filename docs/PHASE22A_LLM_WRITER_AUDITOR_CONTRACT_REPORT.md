# Phase 22A - LLM Writer/Auditor Boundary Contract Report

## Status

```text
Phase 22A LLM Writer/Auditor Boundary Contract: COMPLETE
Recommended next task: Phase 22B - LLM Writer/Auditor Packet Implementation
```

## Files Created

```text
docs/PHASE22A_LLM_WRITER_AUDITOR_CONTRACT.md
docs/PHASE22A_LLM_WRITER_AUDITOR_CONTRACT_REPORT.md
```

## Contract Summary

Phase 22A defines a boundary for optional language-model presentation over
structured answer payloads:

```text
structured ChatAnswer -> writer input -> mock writer draft -> audit result
```

The contract keeps writer/auditor behavior separate from retrieval, databases,
providers, real LLM APIs, simulator execution, analytics, persistence, UI, and
recommendation generation.

## Future Public Interface

Phase 22B should implement:

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

## Future Implementation Files

```text
codie/intelligence/llm_writer_auditor.py
tests/test_intelligence_llm_writer_auditor.py
docs/PHASE22B_LLM_WRITER_AUDITOR_IMPLEMENTATION_REPORT.md
```

## Boundary Rules

The future implementation may consume:

```text
ChatAnswer
ChatAnswerSection
ChatAnswerCitation
ChatAnswerCaveat
ChatAnswerMissingEvidence
explicit user opt-in metadata
```

The future implementation must not:

```text
query SQLite
import repositories
call providers
read source/provider tables
read raw provider payloads
call real LLM APIs
import LLM SDKs
run simulator logic
implement card behavior
calculate analytics
generate recommendations
persist chat records
write files
export private raw_input
```

## Writer Rules

The contract permits a future writer to rephrase structured answer sections for
readability while preserving:

```text
citations
caveats
missing_evidence
blockers
uncertainty language
section order
```

The writer must not add claims, hide caveats, hide missing evidence, change
citation meaning, or generate recommendation/deck-construction language.

## Auditor Rules

The contract requires the future auditor to reject or flag:

```text
uncited factual additions
missing citation visibility
hidden caveats
hidden missing_evidence
hidden blockers
private/raw metadata
forbidden strategic language
unsupported cards treated as modeled
source conflicts resolved by prose
recommendation or deck-construction language
structure violations
```

## Privacy Rules

The contract requires:

```text
cloud LLM use disabled by default
local_user_data blocked by default
sensitive scope blocked by default
raw_input never sent
private_deck_text never sent
full_primer_body never sent
raw_provider_payload never sent
provider_payload never sent
original_import_text never sent
```

## Required Phase 22B Tests

Phase 22B must test:

```text
writer input is built only from structured ChatAnswer fields
writer input preserves citations
writer input preserves caveats
writer input preserves missing_evidence
writer input preserves blockers
local_user_data is blocked by default
sensitive scope is blocked by default
mock writer draft with supported wording validates
mock writer draft adding uncited claim is rejected by audit
mock writer draft hiding caveat is rejected by audit
mock writer draft hiding missing_evidence is rejected by audit
mock writer draft hiding blocker is rejected by audit
mock writer draft using forbidden strategic language is rejected
mock writer draft treating unsupported card as modeled is rejected
mock writer draft resolving source conflict is rejected
private metadata keys fail cleanly
nested private metadata keys fail cleanly
cloud/provider imports are absent
no live LLM calls exist
serialization is deterministic
module has no forbidden imports, raw SQL, DB reads, provider calls, file writes, or LLM SDK imports
```

## Schema Impact

```text
None.
```

Phase 22A is contract-only.

## Next Step

Proceed to:

```text
Phase 22B - LLM Writer/Auditor Packet Implementation
```

Do not start real LLM calls, chat UI, provider wiring, persistence, DB
retrieval, provider calls, simulator integration, analytics, or recommendation
generation from this contract.
