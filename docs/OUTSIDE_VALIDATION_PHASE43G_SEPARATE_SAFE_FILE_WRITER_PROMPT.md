# Outside Validation Prompt - Phase 43G

Validate Phase 43G as a documentation-only Separate Safe File Writer Contract.

Confirm that the writer remains separate from planners, renderers, exports, and
providers; no filesystem write is authorized; future writes require accepted
producer requests and current explicit authorization; paths are normalized,
resolved, and proven inside an allowed root; traversal, symlink/junction escape,
device/UNC paths, broad roots, and protected directories are rejected; collisions
default to no overwrite; atomic same-root temp-to-final behavior and hash
verification are required; receipts are truthful and immutable; recovery cleans
only writer-owned temporary files; local-first privacy and secret blocking remain
mandatory; provider write-back and external publication are prohibited; Hareruya
remains tournament-only; and Stream Deck remains supplemental-only.

Reject any runtime implementation, path-writing authority, implicit overwrite,
unsafe cleanup, export/publish/sync behavior, provider mutation, secret leakage,
Hareruya scope expansion, Stream Deck confirmation, or active-scope edit.

```text
phase_id: Phase43G
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase43H
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Return `PASS`, `PASS WITH REVIEW NOTES`, or `FAIL`, listing required fixes
separately. Phase 43H remains blocked unless Phase 43G passes.
