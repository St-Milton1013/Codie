# Phase 43M Presentation/Export Renderer Implementation Contract

```text
phase_id: Phase43M
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase43N
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase 43M defines the next implementation boundary for deterministic, in-memory
presentation/export rendering from accepted Phase 43K packet models. It
authorizes a future Phase 43N renderer implementation target only; it does not
implement renderer code in this packet.

The renderer may convert already-built `PresentationPacket` values into inert
rendered bytes or text payloads for approved local formats. It must not write
files, choose paths, create directories, publish, sync, upload, call providers,
call models, or bypass the separate safe file writer.

## Future implementation files

Phase 43N may create:

```text
codie/presentation_export/renderers.py
tests/test_presentation_export_renderers.py
docs/PHASE43N_PRESENTATION_EXPORT_RENDERER_IMPLEMENTATION_REPORT.md
```

Phase 43N may modify:

```text
codie/presentation_export/__init__.py
```

## Future public interface

Phase 43N may define:

```text
PresentationRenderError
PresentationRenderOptions
RenderedPresentationArtifact
render_presentation_packet(...)
render_presentation_packet_json(...)
render_presentation_packet_markdown(...)
rendered_presentation_artifact_to_dict(...)
```

Names may be adjusted during implementation only if the same boundaries remain
explicit and tests prove the same behavior.

## Renderer input boundary

The renderer may accept only an already-validated `PresentationPacket` and
renderer options. It cannot:

- read databases;
- read provider payloads;
- call provider APIs;
- read local deck files;
- read private notes, prompts, traces, cookies, or credentials;
- calculate recommendations;
- run simulations;
- review or promote Theory;
- mutate Rules or Corrections;
- infer missing evidence.

If the packet is invalid, stale without a status, privacy-blocked without a
status, missing accessibility text, or contains forbidden metadata, rendering
must fail deterministically.

## Renderer output boundary

Rendered output may be:

- UTF-8 JSON bytes;
- UTF-8 Markdown text/bytes;
- an in-memory artifact record containing payload bytes, media type, encoding,
  payload hash, byte length, artifact class, and provenance.

Rendered output remains inert. It is not a file, receipt, provider mutation,
publication, sync, upload, share, or user confirmation. A future safe writer must
own any path, overwrite, collision, atomic write, receipt, or recovery behavior.

## Privacy and redaction

The renderer must preserve explicit privacy states from the packet. Redacted,
omitted, blocked, unavailable, and secret-blocked states must remain visible in
JSON and Markdown. The renderer cannot replace redacted content with fabricated
evidence or weaker unlabeled summaries.

Private decks, user notes, conversations, corrections, experiments, Theory
excerpts, local-meta material, prompts, traces, secrets, tokens, credentials,
cookies, and sessions cannot appear in rendered output.

## Accessibility

Markdown and JSON renderings must preserve text status for blocking, warning,
redacted, omitted, stale, conflict, legality, unsupported, and success states.
Color, icon, hover, layout position, or animation cannot be the only carrier of
meaning.

The renderer does not implement UI components, DOM focus behavior, browser
layouts, or screen-reader runtime behavior.

## Theory, Rules, Corrections, Hareruya, and providers

Reviewed Theory remains labeled with review state and cannot become measured
evidence, hidden authority, or export permission. Unreviewed Theory remains
blocked by the packet layer and cannot be revived by rendering.

Rules and Corrections retain authority/version/state fields already present in
the packet model. Rendering cannot override legality, unsupported, correction
conflict, or authority-ceiling states.

Hareruya remains tournament-only evidence provenance. Rendering cannot convert
Hareruya into Theory, rules, correction, curriculum, user context, export
authority, provider mutation, or write target.

Provider write-back remains prohibited. Rendering cannot fetch, mutate, upload,
sync, publish, or call Moxfield, Archidekt, Hareruya, Cockatrice, Discord, or any
other external provider.

## Stream Deck boundary

Stream Deck remains optional and supplemental-only. Rendering may include a
read-only navigation/status label already present in the packet. It cannot render
or imply Stream Deck confirmation, consent, write, retry, evidence selection,
privacy override, legality override, provider mutation, file write, or validation
bypass.

## Determinism

The same packet and options must produce byte-identical output. Output field
ordering, Markdown section ordering, hashes, byte lengths, and unsupported/failure
states must be deterministic.

## Do not do in Phase 43N

```text
do not add schema
do not add UI components
do not add routes or APIs
do not add filesystem writes
do not implement the safe file writer
do not create directories or output files
do not add persistence
do not read databases
do not read providers
do not call providers
do not write back to providers
do not publish, sync, upload, or share externally
do not call LLM/model APIs
do not generate recommendations
do not run simulator logic
do not ingest or promote Theory
do not mutate Rules authority
do not activate Corrections
do not implement Stream Deck adapters
do not add workflow automation
do not add dependencies
do not edit active validation scope
```

## Acceptance requirements

Phase 43N must include tests proving:

1. deterministic JSON rendering;
2. deterministic Markdown rendering;
3. payload hash and byte length are derived from rendered bytes;
4. private/local-only/redacted/omitted/blocked states remain explicit;
5. recursive secret/token/credential exclusion remains enforced;
6. accessibility status text appears in both formats;
7. content-class, confidence, and source-agreement separation is preserved;
8. Theory, Rules, Correction, Hareruya, provider, and Stream Deck boundaries are
   preserved;
9. renderer output has no path, overwrite, receipt, provider-write, publish,
   sync, API, or safe-writer authority;
10. invalid packets fail deterministically.

## Not authorized

This packet does not authorize implementation code, schema changes, UI, routes,
APIs, filesystem writes, safe-writer behavior, persistence, provider access,
provider write-back, publication, model calls, recommendation generation,
simulation, Stream Deck adapters, dependencies, workflow automation, or
active-scope edits.

