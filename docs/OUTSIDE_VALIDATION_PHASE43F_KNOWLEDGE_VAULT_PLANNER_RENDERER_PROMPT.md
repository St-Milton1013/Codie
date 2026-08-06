# Outside Validation Prompt - Phase 43F

Validate Phase 43F as a documentation-only Knowledge Vault Planner and Renderer
Contract.

Confirm that the Knowledge Vault remains an exported, non-canonical projection;
planning selects only accepted records; rendering is deterministic and read-only;
private content is excluded by default; redaction occurs before rendering or
boundary crossing; secrets, tokens, traces, prompts, and chain-of-thought are
prohibited; Theory, Rules, Corrections, rights, provenance, conflicts, caveats,
and staleness remain visible; Hareruya remains tournament-only; Stream Deck is
supplemental-only; and file writing remains blocked for Phase 43G.

Reject canonical mutation, hidden authority promotion, unreviewed Theory,
provider write-back, raw private material, cloud/sync/export delivery, path
writing, Stream Deck export approval, Hareruya scope expansion, or runtime
implementation.

```text
phase_id: Phase43F
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase43G
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Return `PASS`, `PASS WITH REVIEW NOTES`, or `FAIL`, listing required fixes
separately. Phase 43G remains blocked unless Phase 43F passes.
