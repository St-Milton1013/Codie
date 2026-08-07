# Phase 43V Presentation/Export Local Package Manifest Contract

## Purpose

Define the future Phase 43W implementation boundary for a deterministic local
package manifest over already-rendered and already-written presentation/export
artifacts.

This packet is contract-only. It does not implement package code, file writing,
CLI behavior, UI behavior, provider integration, publishing, sync, Stream Deck
adapters, dependencies, workflow automation, or any schema/runtime changes.

## Prior accepted foundation

```text
Phase 43K: accepted PresentationPacket model
Phase 43N: accepted deterministic in-memory renderer
Phase 43Q: accepted local-only safe writer
Phase 43T: accepted local CLI wrapper
Phase 43U: accepted local CLI checkpoint
```

Future Phase 43W may only consume deterministic local write receipts and
metadata for artifacts produced by the accepted renderer/writer/CLI chain. It
must not reconstruct, reinterpret, enrich, regenerate, re-render, or rewrite
presentation content.

## Future files

Future implementation may add:

```text
codie/presentation_export/packages.py
tests/test_presentation_export_packages.py
docs/PHASE43W_PRESENTATION_EXPORT_LOCAL_PACKAGE_MANIFEST_REPORT.md
```

Future implementation may modify only:

```text
codie/presentation_export/__init__.py
```

No CLI, UI, route/API, provider adapter, workflow automation, database,
repository, schema, model, simulator, recommendation, Stream Deck, dependency,
or active validation-scope file may be changed in Phase 43W.

## Required future interface

Future Phase 43W should define a small explicit interface, such as:

```text
PresentationPackageManifestError
PresentationPackageArtifactRef
PresentationPackageManifestOptions
PresentationPackageManifest
build_presentation_package_artifact_ref(...)
build_presentation_package_manifest(...)
presentation_package_artifact_ref_to_dict(...)
presentation_package_manifest_to_dict(...)
validate_presentation_package_manifest(...)
```

The final names may vary only if the implementation report explains why the
contract semantics are preserved.

## Input boundary

The package manifest builder may accept only inert local receipt metadata and
artifact references for files already written under caller-approved local roots
by the accepted safe writer or accepted local CLI.

Permitted input fields include:

```text
artifact_id
source_packet_id
source_snapshot_id
receipt_id
relative local path
media type
encoding
payload hash
byte length
artifact class
writer version
renderer version
created-at value supplied by caller or receipt
optional deterministic package label
```

The builder must reject:

```text
absolute artifact paths
parent-directory traversal
path separators in package labels
duplicate relative paths
duplicate artifact IDs with conflicting hashes
missing payload hashes
missing byte lengths
unsupported media types
unsupported encodings
secret/token/credential fields anywhere in recursive input
provider write-back metadata
publish/sync/upload/share metadata
Stream Deck confirmation, consent, write, retry, or device metadata
model prompt, trace, cookie, session, or hidden local context metadata
raw private deck text
unreviewed Theory excerpts
```

The manifest builder must not read databases, repositories, provider caches,
artifact files, arbitrary deck sources, browser state, environment secrets,
Stream Deck profiles, model prompt logs, or hidden local context.

## Output boundary

Future Phase 43W may produce only an in-memory serializable manifest describing
an already-local package. The manifest may include:

```text
manifest_id
manifest_version
package_label
source_packet_ids
source_snapshot_ids
artifact_refs
receipt_ids
relative local paths
media types
encodings
payload hashes
byte lengths
aggregate payload hash
aggregate byte length
privacy summary
accessibility summary
writer versions
renderer versions
```

The manifest is not a zip file, directory, file write, receipt, provider
delivery, publication, sync, upload, share, or user confirmation. A future
separate writer/packager contract must own any package-file creation, copying,
zip behavior, QR code behavior, preview server behavior, cloud movement, or
external sharing behavior.

## Determinism

The same artifact references and options must produce byte-identical manifest
serialization. Artifact ordering, field ordering, aggregate hash calculation,
byte totals, duplicate detection, unsupported/failure states, and error messages
must be deterministic.

Aggregate hashes must be derived only from stable manifest inputs, not from
wall-clock time, host paths, filesystem metadata, random IDs, environment
variables, or machine-specific state.

## Privacy and hard evidence boundaries

The package manifest must preserve the privacy and evidence states already
encoded in accepted packets, rendered artifacts, and write receipts. It must not:

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

The manifest may summarize privacy/accessibility states but cannot replace
explicit redacted, omitted, blocked, unavailable, secret-blocked, stale,
conflict, legality, unsupported, warning, or success states with weaker
unlabeled text.

## Accessibility

Every manifest-level blocking, warning, omitted, redacted, stale, conflict,
legality, unsupported, unavailable, and success state must include deterministic
text status suitable for assistive technology. Color, icon, hover, animation,
layout position, package order, or filename alone cannot be the only carrier of
meaning.

The package manifest does not implement UI components, DOM focus behavior,
browser layouts, screen-reader runtime behavior, or local preview surfaces.

## Theory, Rules, Corrections, Hareruya, and providers

Reviewed Theory remains labeled with review state and cannot become measured
evidence, hidden authority, or export permission. Unreviewed Theory remains
blocked and cannot be revived by packaging metadata.

Rules and Corrections retain authority/version/state fields already present in
accepted artifacts. Packaging metadata cannot override legality, unsupported,
correction conflict, or authority-ceiling states.

Hareruya remains tournament-only evidence provenance. The manifest cannot
convert Hareruya into Theory, rules, correction, curriculum, user context,
export authority, provider mutation, or write target.

Provider write-back remains prohibited. The manifest cannot fetch, mutate,
upload, sync, publish, or call Moxfield, Archidekt, Hareruya, Cockatrice,
Discord, cloud storage, webhooks, browser automation, or any other external
provider.

## Stream Deck boundary

Stream Deck remains optional and supplemental-only. Future Phase 43W may
preserve inert read-only navigation/status labels already present in accepted
artifact metadata. It cannot represent or imply Stream Deck confirmation,
consent, write, retry, evidence selection, privacy override, legality override,
provider mutation, file write, package creation, sync, upload, or validation
bypass.

## Exclusions for Phase 43W

Future Phase 43W must not implement:

```text
schema changes
CLI command
desktop UI
route/API
filesystem writes
package directory creation
zip/archive creation
safe file writer changes
renderer changes
packet model changes
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
deck import/export beyond inert local artifact references
dependency changes
active validation-scope edits
```

## Acceptance requirements

Future Phase 43W implementation must include tests for:

```text
successful manifest build from JSON and Markdown write receipts
deterministic manifest serialization
deterministic aggregate hash and byte totals
stable artifact ordering independent of input order
relative local path preservation
absolute path rejection
parent-directory traversal rejection
unsafe package label rejection
duplicate path rejection
conflicting duplicate artifact rejection
missing hash rejection
missing byte length rejection
unsupported media type rejection
unsupported encoding rejection
recursive secret/token/credential rejection
privacy/redaction/omission/blocking preservation
accessibility status summary preservation
Theory/Rules/Correction/Hareruya boundary preservation
Stream Deck supplemental-only preservation
no provider/publish/sync/upload/API imports
no database/repository/model/simulator imports
manifest builder does not read artifact files
manifest builder does not mutate input references
```

## Validation tuple

```text
phase_id: Phase43V
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase43W
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```
