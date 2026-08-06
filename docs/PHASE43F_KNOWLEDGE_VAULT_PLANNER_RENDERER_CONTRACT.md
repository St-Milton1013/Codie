# Phase 43F Knowledge Vault Planner and Renderer Contract

## Validation tuple

```text
phase_id: Phase43F
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase43G
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 43G is reserved for the Separate Safe File Writer Contract and remains
blocked until Phase 43F outside validation passes.

## Status and authority

```text
document_type: contract-only packet
implementation_authorized: no
schema_authorized: no
UI_authorized: no
API_authorized: no
file_write_authorized: no
persistence_authorized: no
active_scope_base: c4e851f234ec034d68b0945c6c477348bb2a4949
```

The Knowledge Vault is an exported, non-canonical projection. This packet
defines planning and rendering boundaries only. It does not authorize a file
writer, repository, export command, sync service, cloud destination, mutation
endpoint, or runtime implementation.

## Vault purpose

The planner selects already accepted records for a vault package. The renderer
turns that plan into deterministic read-only artifacts. Neither component
creates evidence, changes authority, resolves conflicts, modifies user context,
activates corrections, or commits files.

Permitted content classes include deck reports, decision summaries, experiment
receipts, correction receipts, rules answer references, reviewed Theory notes,
lessons, user-selected notes, source/provenance summaries, and validation
reports.

## Planning boundary

A vault plan retains:

- plan ID, source request, creator, generated time, and status;
- deck, snapshot, analysis run, decision, experiment, correction, lesson, and
  answer-packet identities;
- content class, authority, privacy, rights, redaction, and retention labels;
- source version, provenance, replay identity, conflicts, caveats, and
  staleness;
- explicit include/exclude decisions for private deck text, notes, corrections,
  conversations, Theory excerpts, and local-meta material;
- proposed artifact names and destination intent without performing writes.

Planning cannot silently include private content, full traces, tokens, raw model
prompts, chain-of-thought, unreviewed Theory, unresolved corrections, or provider
credentials.

## Rendering boundary

Rendering consumes one immutable vault plan and accepted Phase 43A projections.
For the same plan and projection set, output ordering, section headings,
provenance labels, redactions, warnings, and cross-links are deterministic.

Rendered artifacts remain read-only. They cannot expose database mutation
routes, hidden execution controls, provider write-back, confirmation actions, or
live model/retrieval behavior. A rendered link may point to a source identity or
local record reference, but it cannot become authority for a new record.

## Redaction and privacy

- Local-first vault planning and rendering are mandatory.
- Private content is excluded by default and included only by explicit current
  user selection.
- Redaction occurs before rendering and before any separately approved boundary
  crossing.
- The rendered artifact records whether private deck text, notes, corrections,
  conversations, Theory excerpts, or local-meta material were included.
- Secrets, tokens, credentials, raw traces, private prompts, and unredacted
  route details are prohibited.
- Cross-user and cross-profile leakage is prohibited.

## Theory, Rules, Corrections, and Hareruya

Reviewed Theory retains author, work, immutable version, citation, rights class,
transferability, contradiction, and review state. It remains explanation or
lesson context, not measured evidence or recommendation authority.

Rules references retain authority version and unsupported states. Corrections
retain scope, authority ceiling, review state, conflicts, and receipts. A vault
render cannot broaden either.

Hareruya may appear only as provenance for canonicalized tournament, event, or
deck observations. It cannot become a Theory, rules, curriculum, correction,
user-context, export destination, or vault authority source.

## Knowledge Vault lessons and notes

Lesson and note rendering must distinguish rules facts, measured evidence,
Theory, examples, opinion, user context, and unresolved questions. A lesson may
reference judge-training material only with its accepted phase identity and
source version. User notes remain user context unless separately promoted by an
accepted authority path.

## Destination and safe writer handoff

Phase 43F may name a proposed local destination, artifact type, and filename
plan. It cannot create directories, write files, overwrite files, publish,
sync, share, or open external delivery. The future Phase 43G safe writer owns
path validation, collision policy, atomic writes, receipts, and recovery.

## Stream Deck boundary

Stream Deck remains optional and supplemental-only. A future adapter may
navigate to an existing vault plan or rendered local artifact. It cannot select
private content, approve redactions, write files, export, sync, publish, or
bypass privacy and authority gates.

## Accessibility and deterministic behavior

- Rendered headings, sections, tables, links, warnings, and citations are
  semantic and keyboard/screen-reader friendly.
- Content class, privacy, rights, conflict, caveat, and staleness do not rely on
  color alone.
- Missing, stale, redacted, rights-blocked, privacy-blocked, unsupported,
  superseded, partial, and error states are explicit.
- Cross-links preserve exact source identities and do not imply stronger
  authority than the target record has.

## Acceptance criteria

1. The Knowledge Vault remains an exported, non-canonical projection.
2. Planning selects accepted records without creating or mutating records.
3. Rendering is deterministic and read-only.
4. Private content is excluded by default and inclusion is explicit.
5. Redaction happens before rendering or boundary crossing.
6. Secrets, tokens, raw traces, prompts, and chain-of-thought are prohibited.
7. Theory, Rules, Corrections, and source provenance retain their gates.
8. Hareruya remains tournament-only.
9. Stream Deck remains supplemental-only.
10. No file writing is authorized.
11. Phase 43G remains blocked.

## Explicit exclusions

No code, schema, component, renderer implementation, route, API, repository,
database write, export command, local file write, directory creation, overwrite,
sync, publish, cloud delivery, model call, retrieval, mobile delivery, Stream
Deck adapter, dependency, workflow automation, or active-scope edit is
authorized.
