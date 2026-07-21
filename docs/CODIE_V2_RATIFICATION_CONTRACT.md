# Codie V2 Constitution Ratification Contract

**Status:** Governance-only adoption contract
**Date:** 2026-07-20

## Objective

Adopt `docs/CODIE_V2_CONSTITUTION.md` as Codie's primary constitution while preserving `docs/CODIE_V1_CONSTITUTION.md` unchanged as historical reference.

## Authorized files

```text
docs/CODIE_V2_CONSTITUTION.md
docs/CODIE_V2_CHANGELOG.md
docs/CODIE_V2_COMPATIBILITY_STATEMENT.md
docs/CODIE_V2_RATIFICATION_CONTRACT.md
docs/CHECKPOINT_CODIE_V2_RATIFICATION_REPORT.md
docs/OUTSIDE_VALIDATION_CODIE_V2_RATIFICATION_PROMPT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

`docs/CODIE_V1_CONSTITUTION.md` is read-only in this packet.

## Governance behavior

- V2 becomes authoritative only when the adoption pull request is accepted and merged.
- V1 remains available and unchanged.
- Existing accepted phases remain accepted.
- Active phase tuples and validation scope are not advanced by this governance track.
- No V2 runtime capability is authorized merely by ratification.

## Prohibited scope

```text
production code
schema or migration changes
repository changes
provider or network changes
tests or fixture rewrites
workflow or validator changes
dependency changes
Phase 37 merge or advancement
runtime Jin, theory, exposure, relationship, or correction implementation
```

## Acceptance criteria

- V2 contains every explicit decision recorded through 2026-07-20.
- V1 remains byte-for-byte unchanged from `origin/main`.
- The change log and compatibility statement agree with V2.
- Active roadmap documents state that ratification does not advance Phase 37.
- Architecture and adversarial review find no blocking contradiction.
- Markdown structure and repository whitespace checks pass.
