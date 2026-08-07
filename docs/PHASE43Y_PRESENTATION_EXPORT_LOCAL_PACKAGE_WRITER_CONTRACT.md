# Phase 43Y Presentation/Export Local Package Writer Contract

## Purpose

Define the future Phase 43Z implementation boundary for writing an already-built
Phase 43W `PresentationPackageManifest` to a caller-approved local manifest file.

This packet is contract-only. It does not implement package writing, zip/archive
behavior, copying artifacts, CLI behavior, UI behavior, provider integration,
publishing, sync, Stream Deck adapters, dependencies, workflow automation, or
any schema/runtime changes.

## Prior accepted foundation

```text
Phase 43K: accepted PresentationPacket model
Phase 43N: accepted deterministic in-memory renderer
Phase 43Q: accepted local-only safe writer for rendered artifacts
Phase 43T: accepted local CLI wrapper
Phase 43W: accepted deterministic in-memory local package manifest
Phase 43X: accepted local package manifest checkpoint
```

Future Phase 43Z may only consume an already-built and already-validated
`PresentationPackageManifest`. It must not reconstruct, reinterpret, enrich,
regenerate, re-render, rewrite, copy, zip, upload, publish, sync, or share
presentation content.

## Future files

Future implementation may add:

```text
codie/presentation_export/package_writers.py
tests/test_presentation_export_package_writers.py
docs/PHASE43Z_PRESENTATION_EXPORT_LOCAL_PACKAGE_WRITER_REPORT.md
```

Future implementation may modify only:

```text
codie/presentation_export/__init__.py
```

No CLI, UI, route/API, provider adapter, workflow automation, database,
repository, schema, model, simulator, recommendation, Stream Deck, dependency,
renderer, packet model, package manifest model, artifact writer, or active
validation-scope file may be changed in Phase 43Z.

## Required future interface

Future Phase 43Z should define a small explicit interface, such as:

```text
PresentationPackageWriteError
PresentationPackageWriteOptions
PresentationPackageWriteReceipt
write_presentation_package_manifest(...)
presentation_package_write_receipt_to_dict(...)
```

The final names may vary only if the implementation report explains why the
contract semantics are preserved.

## Input authority

The package writer may accept only:

```text
PresentationPackageManifest
caller-approved output root
caller-approved manifest basename or filename stem
explicit overwrite flag defaulting to false
optional inert writer metadata
```

The writer must validate the manifest before planning any write. It must reject
tampered aggregate hashes, tampered byte totals, unsafe package labels, unsafe
manifest basenames, absolute filenames, parent-directory traversal, path-bearing
metadata, duplicate target paths, existing targets without explicit overwrite,
secret/token/credential metadata, provider write-back metadata,
publish/sync/upload/share metadata, Stream Deck action metadata, model prompt
metadata, trace metadata, cookie/session metadata, raw private deck text,
unreviewed Theory excerpts, database/repository references, and hidden local
context metadata.

The writer must not read databases, repositories, provider caches, artifact
files, arbitrary deck sources, browser state, environment secrets, Stream Deck
profiles, model prompt logs, or hidden local context.

## Output authority

Future Phase 43Z may write only local files under the caller-approved output
root. It may write:

```text
presentation-package-manifest JSON
manifest write receipt JSON
```

The manifest write receipt must be deterministic and must include manifest ID,
manifest version, package label, manifest payload hash, manifest byte length,
relative local paths, writer version, overwrite policy, and receipt identity.
It must not include private raw inputs, hidden provider metadata, credentials,
model prompts, unreviewed context, absolute paths, cloud URLs, provider delivery
state, publication state, sync state, upload state, or sharing state.

The manifest receipt must be written last. The writer must prepare and validate
all planned writes before writing any file. Existing targets must be rejected
unless overwrite is explicitly true. Partial writes should be avoided through
temporary-file replacement or an equivalent local-first safe-write mechanism.

## Not package creation

This writer is not a package-directory builder, zip/archive builder, artifact
copier, QR-code generator, preview server, provider delivery mechanism, share
sheet, cloud uploader, or publication/sync tool. It writes only the package
manifest JSON and its local receipt.

Any future directory packaging, artifact copying, zip/archive behavior, QR code,
local preview server, LAN sharing, cloud movement, or external sharing requires
a separate accepted contract.

## Privacy and hard evidence boundaries

The writer must preserve the privacy and evidence states already encoded in the
accepted package manifest. It must not:

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

## Accessibility

Manifest write receipts must preserve deterministic text status for success,
warnings, blocked states, unsupported states, and local write results. Color,
icon, hover, animation, path position, filename, or package order cannot be the
only carrier of meaning.

The package writer does not implement UI components, DOM focus behavior,
browser layouts, screen-reader runtime behavior, local preview surfaces, or
accessibility rendering.

## Theory, Rules, Corrections, Hareruya, and providers

Reviewed Theory remains labeled with review state and cannot become measured
evidence, hidden authority, or export permission. Unreviewed Theory remains
blocked and cannot be revived by package writing.

Rules and Corrections retain authority/version/state fields already present in
accepted manifests. Package writing cannot override legality, unsupported,
correction conflict, or authority-ceiling states.

Hareruya remains tournament-only evidence provenance. The package writer cannot
convert Hareruya into Theory, rules, correction, curriculum, user context,
export authority, provider mutation, or write target.

Provider write-back remains prohibited. The writer cannot fetch, mutate, upload,
sync, publish, or call Moxfield, Archidekt, Hareruya, Cockatrice, Discord,
cloud storage, webhooks, browser automation, or any other external provider.

## Stream Deck boundary

Stream Deck remains optional and supplemental-only. Future Phase 43Z may
preserve inert read-only navigation/status labels already present in accepted
manifest metadata. It cannot represent or imply Stream Deck confirmation,
consent, write, retry, evidence selection, privacy override, legality override,
provider mutation, package creation, sync, upload, or validation bypass.

## Exclusions for Phase 43Z

Future Phase 43Z must not implement:

```text
schema changes
CLI command
desktop UI
route/API
artifact file reads
artifact copying
package directory creation
zip/archive creation
QR code generation
preview server
safe artifact writer changes
renderer changes
packet model changes
package manifest model changes
workflow automation
provider access
provider write-back
publication/sync/upload/share behavior
Stream Deck adapter
recommendation generation
model call
simulator execution
Theory ingestion or promotion
Rules mutation
Correction activation
Hareruya scope expansion
database persistence
deck import/export beyond inert manifest writing
dependency changes
active validation-scope edits
```

## Acceptance requirements

Future Phase 43Z implementation must include tests for:

```text
successful manifest JSON local write
successful manifest receipt local write
deterministic manifest payload serialization
deterministic receipt serialization
manifest validation before write
aggregate hash verification before write
aggregate byte total verification before write
unsafe basename rejection
absolute filename rejection
parent-directory traversal rejection
existing target rejection by default
explicit overwrite behavior
receipt written last
no artifact file reads
no artifact copying
no package directory creation
no zip/archive creation
no provider/publish/sync/upload/share/API imports
no database/repository/model/simulator imports
recursive secret/token/credential rejection
privacy/redaction/omission/blocking preservation
accessibility status preservation
Theory/Rules/Correction/Hareruya boundary preservation
Stream Deck supplemental-only preservation
writer does not mutate manifest input
```

## Validation tuple

```text
phase_id: Phase43Y
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase43Z
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```
