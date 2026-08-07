# Phase 43P Presentation/Export Safe Writer Integration Contract

## Purpose

Define the future Phase 43Q implementation boundary for writing Phase 43N
rendered presentation/export artifacts to caller-approved local files through a
narrow safe-writer integration.

This packet is contract-only. It does not implement file writing, CLI behavior,
UI behavior, provider integration, publishing, sync, Stream Deck adapters, or
any schema/runtime changes.

## Prior accepted foundation

```text
Phase 43K: accepted PresentationPacket model
Phase 43L: accepted packet-model checkpoint
Phase 43M: accepted renderer implementation contract
Phase 43N: accepted deterministic in-memory renderer implementation
Phase 43O: accepted renderer checkpoint
```

Future Phase 43Q may only consume `RenderedPresentationArtifact` values created
from already-validated `PresentationPacket` values. It must not reconstruct,
reinterpret, enrich, or regenerate recommendation content.

## Future module boundary

Future implementation may add:

```text
codie/presentation_export/writers.py
tests/test_presentation_export_writers.py
docs/PHASE43Q_PRESENTATION_EXPORT_SAFE_WRITER_INTEGRATION_REPORT.md
```

Future implementation may modify only:

```text
codie/presentation_export/__init__.py
```

No CLI, UI, route/API, provider adapter, workflow automation, database,
repository, schema, model, simulator, recommendation, Stream Deck, or active
validation-scope file may be changed in Phase 43Q.

## Required future interface

Future Phase 43Q should define a small explicit interface, such as:

```text
PresentationArtifactWriteError
PresentationArtifactWriteOptions
PresentationArtifactWriteReceipt
write_rendered_presentation_artifact(...)
rendered_presentation_write_receipt_to_dict(...)
```

The final names may vary only if the implementation report explains why the
contract semantics are preserved.

## Input authority

The writer may accept only:

```text
RenderedPresentationArtifact
caller-approved output root
caller-approved basename or filename stem
explicit overwrite flag defaulting to false
optional writer metadata that is inert and serializable
```

The writer must verify the artifact payload hash and byte length before any
write. Tampered payloads, missing hashes, unsupported encodings, unsupported
media types, path-bearing artifact metadata, unsafe filenames, absolute output
filenames, parent-directory traversal, duplicate target paths, and existing
targets without explicit overwrite must fail before writing.

## Output authority

Future Phase 43Q may write only local files under the caller-approved output
root. It may write:

```text
rendered JSON artifact payload
rendered Markdown artifact payload
manifest or receipt JSON describing local writes
```

The manifest or receipt must be deterministic and must include artifact ID,
source packet ID, source snapshot ID, media type, encoding, payload hash, byte
length, relative local paths, writer version, overwrite policy, and generated
receipt identity. It must not include private raw inputs, hidden provider
metadata, credentials, model prompts, or unreviewed context beyond what already
exists in the rendered artifact metadata.

## Ordering and atomicity

Future implementation must prepare and validate all planned writes before
writing any file. If it writes multiple files, the receipt/manifest must be
written last. Existing targets must be rejected unless overwrite is explicitly
true. Partial writes should be avoided through temporary-file replacement or an
equivalent local-first safe-write mechanism.

## Privacy and hard evidence boundaries

The writer must preserve the privacy and evidence states already encoded in the
rendered artifact. It must not:

```text
unredact redacted data
fill omitted data
downgrade blocked data
invent evidence
promote unreviewed Theory
mutate Rules authority
activate Correction state
expand Hareruya beyond tournament-only labels
write provider receipts
publish or sync artifacts
```

## Stream Deck boundary

Stream Deck support remains supplemental-only. Future Phase 43Q must not add
Stream Deck adapters, Stream Deck write actions, live button/profile updates,
automation hooks, or device APIs. It may preserve inert Stream Deck labels that
already exist in accepted packet/rendered metadata.

## Provider and publication boundary

The writer is local-file-only. It must not call Moxfield, Archidekt, Hareruya,
Scryfall, GitHub, cloud storage, email, chat, webhook, browser automation,
provider APIs, publish endpoints, or sync endpoints. A successful local write is
not evidence of provider delivery, publication, or user sharing.

## Exclusions for Phase 43Q

Future Phase 43Q must not implement:

```text
schema changes
CLI command
desktop UI
route/API
workflow automation
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
deck import/export beyond local rendered artifacts
active validation-scope edits
```

## Acceptance requirements

Future Phase 43Q implementation must include tests for:

```text
successful JSON artifact local write
successful Markdown artifact local write
deterministic receipt/manifest
payload hash verification before write
byte length verification before write
unsupported media type rejection
unsupported encoding rejection
unsafe basename/path traversal rejection
absolute filename rejection
duplicate target rejection
existing target rejection by default
explicit overwrite behavior
receipt/manifest written last
no provider/publish/sync/Stream Deck/API imports
privacy/redaction/omission/blocking preservation
Theory/Rules/Correction/Hareruya boundary preservation
artifact metadata with forbidden write/provider authority rejected
writer does not mutate artifact input
```

## Validation tuple

```text
phase_id: Phase43P
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase43Q
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```
