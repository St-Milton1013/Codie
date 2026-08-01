# Outside Validation Prompt - Phase 42J

Validate the Phase 42J Experiment and Permitted User-Context Write Contract as
a documentation-only intermediate packet.

## Required tuple

```text
phase_id: Phase42J
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase42K
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Validate

- changed-file scope is documentation/governance only;
- exactly six permitted user-context record families are defined;
- raw writer/auditor output cannot initiate a write;
- explicit payload-specific user confirmation is mandatory;
- canonical evidence, measurements, rules, confidence, sources, corrections,
  and recommendations remain immutable;
- correction candidates cannot activate corrections;
- theory review, rights, attribution, version, citation, and transferability
  gates remain intact;
- Hareruya is tournament-only;
- local-only operation is complete and cloud use remains optional;
- Stream Deck is supplemental and cannot confirm or bypass gates;
- retention is explicit, cancellation creates no write, and deletion is bounded;
- no implementation, schema, repository, model, network, UI, dependency,
  workflow, or constitution change is present.

## Reject

Reject any packet that permits silent persistence, implicit confirmation,
globalization of deck-specific context, theory promotion without review,
canonical or measured mutation, active correction creation, required cloud
processing, Stream Deck confirmation, live Hareruya expansion, or runtime work.

Return exactly one governance verdict:

```text
PASS
PASS WITH REVIEW NOTES
FAIL
```

List required fixes separately from optional review notes. Phase 42K remains
blocked unless the verdict is `PASS` or `PASS WITH REVIEW NOTES`.
