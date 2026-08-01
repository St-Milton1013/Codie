# Outside Validation Prompt - Phase 43A

Validate Phase 43A as a documentation-only Shared Read-Model and View-Model
Boundary Contract.

Confirm immutable projection-only behavior; retained content classes,
provenance, uncertainty, conflicts, privacy, staleness, and replay identity;
and strict ownership of state-changing actions.

Reject any evidence calculation, confidence strengthening, rules resolution,
correction activation, recommendation creation, model/retrieval call,
persistence, silent refresh, private-data leakage, required cloud dependency,
Hareruya scope expansion, Stream Deck confirmation, or runtime implementation.

Required tuple:

```text
phase_id: Phase43A
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase43B
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Return `PASS`, `PASS WITH REVIEW NOTES`, or `FAIL`, with required fixes listed
separately. Phase 43B remains blocked unless Phase 43A passes.
