# Outside Validation Prompt - Phase 42K

Validate Phase 42K as a documentation-only Judge-Training and Curriculum
Contract packet.

## Required tuple

```text
phase_id: Phase42K
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase42L
next_phase_part: outside-validation
next_gate_scope: FINAL_PHASE
```

## Confirm

- judge-style issue spotting uses the accepted seven-step sequence;
- rules, legality, tournament observations, measurements, theory, examples,
  community context, user context, and opinion remain separate;
- theory skills require rights, attribution, immutable version, citation,
  transferability, contradiction, and human review;
- unsupported interactions fail closed or require judge review;
- Codie claims no judge certification or binding tournament authority;
- assessment scoring is deterministic where applicable and does not penalize
  justified abstention on stale, ambiguous, or unsupported items;
- progress remains explicitly confirmed local user context under Phase 42J;
- Hareruya remains tournament-only;
- Stream Deck remains supplemental-only and cannot answer or confirm;
- no production code, lesson content, tests for new behavior, schema,
  persistence, model call, provider access, UI, dependency, workflow, or
  constitution change is present;
- Phase 42L remains blocked.

## Reject

Reject silent theory promotion, invented rulings, certification claims,
required cloud use, live-provider lesson dependencies, automatic progress
writes, cross-user profiling, Stream Deck assessment answers, or runtime work.

Return exactly one verdict:

```text
PASS
PASS WITH REVIEW NOTES
FAIL
```

List required fixes separately from optional review notes.
