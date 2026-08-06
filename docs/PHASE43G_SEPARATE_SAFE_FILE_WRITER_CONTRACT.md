# Phase 43G Separate Safe File Writer Contract

## Validation tuple

```text
phase_id: Phase43G
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase43H
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 43H is reserved for the Accessibility, Privacy, and Adversarial
Checkpoint and remains blocked until Phase 43G outside validation passes.

## Status and authority

```text
document_type: contract-only packet
implementation_authorized: no
schema_authorized: no
CLI_authorized: no
API_authorized: no
filesystem_write_authorized: no
persistence_authorized: no
active_scope_base: 44b985f5f21a7105ad2de92a2d52bc8e11fcbbfb
```

This packet defines a future safe file writer boundary only. It does not
authorize an implementation, command, API, repository adapter, export route,
writer service, filesystem mutation, or Knowledge Vault delivery.

## Writer purpose

The future writer may consume already-rendered artifact bytes and an accepted
write request from a separately approved producer. It owns path validation,
collision policy, atomic local write behavior, receipts, and recovery. It does
not render content, select records, redact content, decide privacy, calculate
hashes for authority, or publish externally.

## Accepted input envelope

A writer request must include:

- request ID, producer, phase/source contract, and creation time;
- immutable payload hash, byte length, media type, and encoding;
- proposed filename, extension, artifact class, and local destination intent;
- allowed-root identifier and user-visible resolved destination preview;
- collision policy, overwrite policy, retention policy, and idempotency key;
- privacy/redaction declaration from the producer;
- expected receipt destination and recovery behavior.

The writer rejects missing payload hashes, unresolved roots, ambiguous paths,
unknown artifact classes, unsupported extensions, mismatched byte length, stale
requests, expired requests, or requests lacking a current explicit write
authorization.

## Path validation

The writer resolves destination paths before writing. It must reject:

- absolute paths outside an approved root;
- `..` traversal, symlink/junction escape, alternate data streams, device paths,
  UNC paths, drive-root writes, home-directory broad writes, and environment
  variable expansion surprises;
- hidden writes to repository source, `.git`, `.agents`, `.codex`, runner
  directories, credential locations, or broad workspace roots unless a future
  contract explicitly allows that exact destination class;
- filenames that are empty, reserved, control-character-bearing, normalized to a
  different visible name, or unsupported by the local filesystem.

The validated path must remain inside the allowed root after normalization,
symlink/junction resolution, parent creation checks, and final pre-commit check.

## Collision and overwrite policy

Default behavior is no overwrite. A collision must produce a visible blocked
state unless the request has an explicit accepted policy:

- fail if exists;
- create unique sibling name;
- overwrite exact prior receipt target only when payload, identity, and user
  confirmation match the accepted overwrite policy.

Overwrite cannot be implied by filename selection, retry, Stream Deck action,
Jin output, prior approval, or stale confirmation.

## Atomic write behavior

When future implementation is separately authorized, writes must be local,
single-target, and atomic where the filesystem supports it:

1. validate request and destination;
2. write bytes to a temporary file under the same allowed root;
3. flush and verify byte length and payload hash;
4. atomically move/rename to the final path according to collision policy;
5. re-read or stat final output for receipt verification;
6. emit an immutable receipt.

Partial files, temporary files, and failed writes must not masquerade as
success. Recovery may clean only writer-owned temporary files that are proven to
be inside the allowed root and associated with the request ID.

## Receipts and audit

The receipt records request ID, idempotency key, producer, artifact class,
payload hash, byte length, final resolved path, collision policy, overwrite
decision, actor, timestamp, result, warnings, and recovery actions. A success
receipt means the verified final file exists at the recorded path. A failure
receipt cannot claim success or invent a new destination.

Receipt paths may be private and must observe the same redaction and export
rules as the artifact itself.

## Local-first privacy and export boundaries

- The writer is local-first and cannot require cloud, sync, or network access.
- It cannot transmit, publish, share, upload, open, or preview files externally.
- It cannot include private deck text, notes, corrections, conversations,
  Theory excerpts, local-meta material, secrets, tokens, credentials, raw traces,
  prompts, or chain-of-thought unless the already-rendered payload and accepted
  producer declaration explicitly allow the relevant non-secret class.
- Secrets, tokens, credentials, raw traces, private prompts, and chain-of-thought
  are always blocked.

## Theory, Rules, Corrections, Hareruya, and providers

The writer has no authority over Theory, Rules, Corrections, Hareruya,
providers, deck snapshots, recommendations, experiments, or vault content. It
cannot promote content, alter citations, change rights labels, resolve
conflicts, or write back to Moxfield, Archidekt, Hareruya, Cockatrice, Discord,
cloud storage, Obsidian sync, or another external destination.

Hareruya remains tournament-only evidence provenance and cannot become an export
destination or file-authority source.

## Stream Deck boundary

Stream Deck remains optional and supplemental-only. A future adapter may navigate
to a prepared write review or display writer status. It cannot choose a path,
approve private content, confirm overwrite, create an idempotency key, retry,
cancel cleanup, write files, publish, sync, or bypass privacy and path gates.

## Accessibility and deterministic behavior

- Destination previews, collision warnings, overwrite decisions, privacy blocks,
  and failure states are available to keyboard and screen-reader users.
- Status does not rely on color alone.
- The same request, payload, root state, and collision state produce the same
  validated destination decision.
- Blocked, pending, writing, verifying, succeeded, failed, partial, recovered,
  duplicate, stale, expired, collision, privacy-blocked, and path-blocked states
  are explicit.

## Acceptance criteria

1. The writer is separately bounded from planners, renderers, exports, and
   providers.
2. No filesystem write is authorized by this contract.
3. Future writes require accepted producer requests and current explicit write
   authorization.
4. Destination paths are normalized, resolved, and proven inside an allowed root.
5. Traversal, symlink/junction escape, device/UNC paths, broad roots, and
   protected directories are rejected.
6. Default collision behavior is no overwrite.
7. Atomic same-root temp-to-final behavior and hash verification are required.
8. Receipts are immutable and truthfully describe the result.
9. Recovery cleans only proven writer-owned temporary files inside the allowed
   root.
10. Local-first privacy and secret blocking remain mandatory.
11. Provider write-back and external publication are prohibited.
12. Hareruya remains tournament-only.
13. Stream Deck remains supplemental-only and cannot confirm.
14. Phase 43H remains blocked.

## Explicit exclusions

No code, schema, CLI, API, repository adapter, writer service, path resolver,
filesystem write, directory creation, overwrite, cleanup implementation, export,
publish, sync, cloud delivery, provider write-back, model call, retrieval,
mobile delivery, Stream Deck adapter, dependency, workflow automation, or
active-scope edit is authorized.
