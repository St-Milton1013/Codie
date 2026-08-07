# Phase 43S Presentation/Export Local CLI Contract

## Purpose

Define the future Phase 43T implementation boundary for a narrow local CLI that
loads an already-built PresentationPacket JSON file, renders it through the
accepted Phase 43N renderer, and writes it through the accepted Phase 43Q local
safe writer.

This packet is contract-only. It does not implement CLI code, schema changes,
UI, routes, APIs, provider access, provider write-back, publication, sync,
uploads, Stream Deck adapters, model calls, simulator execution, recommendation
generation, or workflow automation.

## Prior accepted foundation

```text
Phase 43K: accepted PresentationPacket model
Phase 43N: accepted deterministic in-memory renderer
Phase 43Q: accepted local-only safe writer
Phase 43R: accepted safe-writer checkpoint
```

Future Phase 43T may only orchestrate those accepted pieces. It must not
reinterpret packet evidence, enrich content, generate recommendations, call
providers, or bypass the local safe writer.

## Future files

Future implementation may add:

```text
codie/cli/presentation_export.py
tests/test_cli_presentation_export.py
docs/PHASE43T_PRESENTATION_EXPORT_LOCAL_CLI_IMPLEMENTATION_REPORT.md
```

Future implementation may modify only:

```text
codie/cli/__init__.py
```

No packet model, renderer, writer, schema, UI, provider, workflow, dependency,
Stream Deck, database, repository, simulator, recommendation, or active
validation-scope files may be changed in Phase 43T.

## Required CLI behavior

Future Phase 43T should expose a narrow command entry surface equivalent to:

```text
codie-presentation-export render --packet-json <path> --format json|markdown --output-root <path>
```

Permitted optional flags:

```text
--basename <safe local basename>
--overwrite
--create-output-root
--no-metadata
```

The final command spelling may vary only if the implementation report explains
how the same authority boundary is preserved.

## Input boundary

The CLI may read only a caller-supplied local packet JSON file. It must
reconstruct and validate a `PresentationPacket` from that file before rendering.

The CLI must reject:

```text
missing packet file
malformed JSON
wrong packet shape
invalid packet state
secret/token/credential metadata
unsupported render format
unsafe basename
missing output root unless creation is explicit
existing targets unless overwrite is explicit
```

The CLI must not read databases, repositories, provider caches, arbitrary deck
sources, browser state, environment secrets, Stream Deck profiles, model prompt
logs, or hidden local context.

## Output boundary

The CLI may write only through `write_rendered_presentation_artifact(...)`.
It must print a deterministic concise JSON result to stdout containing:

```text
artifact_id
source_packet_id
source_snapshot_id
render_format
media_type
payload_hash
byte_length
receipt_id
files
writer_version
```

It must not print private raw inputs, credentials, provider metadata, absolute
paths unless already returned by the writer contract, model prompts, hidden
context, or unreviewed local data.

## Privacy and evidence boundaries

The CLI must preserve privacy and evidence states already encoded in the
validated packet and rendered artifact. It must not:

```text
unredact redacted data
fill omitted data
downgrade blocked data
invent evidence
promote unreviewed Theory
mutate Rules authority
activate Correction state
expand Hareruya beyond tournament-only labels
publish or sync outputs
```

## Stream Deck boundary

Stream Deck support remains supplemental-only. Future Phase 43T must not add
Stream Deck commands, adapters, write actions, profile updates, automation
hooks, or device APIs. It may preserve inert Stream Deck labels already present
in accepted packet metadata.

## Provider and publication boundary

The CLI is local-file-only. It must not call Moxfield, Archidekt, Hareruya,
Scryfall, GitHub, cloud storage, email, chat, webhook, browser automation,
provider APIs, publish endpoints, sync endpoints, or upload endpoints.

Successful CLI execution is not evidence of provider delivery, publication,
sharing, or user consent beyond the explicit local output path.

## Exclusions for Phase 43T

Future Phase 43T must not implement:

```text
schema changes
desktop UI
route/API
provider access
provider write-back
publication/sync/upload
Stream Deck adapter
recommendation generation
model call
simulator execution
Theory ingestion or promotion
Rules mutation
Correction activation
Hareruya scope expansion
database persistence
deck import/export beyond local packet JSON input
workflow automation
dependency changes
active validation-scope edits
```

## Acceptance requirements

Future Phase 43T implementation must include tests for:

```text
JSON packet input to JSON artifact write
JSON packet input to Markdown artifact write
deterministic stdout JSON result
missing packet file rejection
malformed JSON rejection
wrong packet shape rejection
invalid packet rejection
unsupported format rejection
unsafe basename rejection
existing target rejection by default
explicit overwrite behavior
create-output-root behavior
no-metadata render option
privacy/redaction/omission/blocking preservation
Theory/Rules/Correction/Hareruya boundary preservation
no provider/publish/sync/Stream Deck/API imports
no database/repository/model/simulator imports
```

## Validation tuple

```text
phase_id: Phase43S
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase43T
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```
