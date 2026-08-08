# Phase44A Goal Engine v1.0 Ratification Report

Status: internal ratification packet

## Objective

Ratify `docs/GOAL_ENGINE_V1_SPEC.md` as Codie's next governing program of work
after Phase43Z closure, subordinate to `docs/CODIE_V2_CONSTITUTION.md`.

This packet is governance-only. It prepares the repository to validate Goal
Engine v1.0 as future work-selection and improvement-governance architecture.

## Phase43Z baseline

Phase43Z is closed separately and is not modified, reopened, expanded, or
interfered with by this packet.

```text
Phase43Z closure PR: #79
Phase43Z closure merge commit: 5d5736d5a790ea517cc59c0415d5c4a4647ec713
Phase43Z closure artifact: codie-pr-validation-5241d9dafe46a8feaf9a86ba8ead01113994a1e2
Phase43Z closure artifact ID: 9016202071
Phase43Z closure artifact digest: sha256:9db6bce56e19f62ab08456222a852ab9da282123da1c5138052e0bc45d12c195
Phase43Z closure result: CLEAN_PASS
```

## Files

```text
docs/GOAL_ENGINE_V1_SPEC.md
docs/GOAL_ENGINE_V1_RATIFICATION_REPORT.md
docs/GOAL_ENGINE_V1_OUTSIDE_VALIDATION_PROMPT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

## Work completed

- Added the Goal Engine v1.0 governance specification.
- Preserved Codie V2 Constitution authority as higher authority.
- Preserved existing roadmap/history as historical evidence and candidate work.
- Declared that Goal Engine runtime behavior is not authorized by ratification.
- Declared staged implementation and takeover gates.
- Declared the first next task after ratification as a Phase44B Goal Engine
  Foundation implementation contract.
- Prepared outside-validation material for the normal validator process.
- Updated compact roadmap/status/handoff records.

## Prohibited scope preserved

This packet does not add or modify:

```text
runtime Goal Engine code
autonomous execution
production schemas
database migrations
provider integrations
network behavior
CLI behavior
UI behavior
workflow automation
validator implementation
paid dependencies
model calls
evidence hierarchy
privacy policy
human merge/release authority
Phase43Z implementation or closure scope
```

## Design decisions

- `Level 0` is reserved for constitutional hard constraints.
- Goal Engine operational permissions use `CAP-0` through `CAP-5`.
- `HEALTHY_IDLE` is a valid successful state.
- One active mutating goal remains the default operating model.
- Health signals become Findings, not automatic Goals.
- Goal Engine begins with no work-order authority and must pass shadow mode.
- Authority promotions require explicit human approval.
- Goal Engine self-change is treated as `Core`.
- The old roadmap is preserved and does not disappear at ratification.

## Local validation

Local validation passed:

```text
git diff --check: PASS
scripts/check_schema.py: CLEAN_PASS
python -m unittest discover -s tests: PASS, 1254 tests, 1 expected skip
focused boundary scans for runtime/autonomy/schema/provider/privacy/cost/Phase43Z scope: PASS
```

## Next step

Open a draft pull request and stop at the human merge gate. Goal Engine v1.0 is
not ratified until the PR passes deterministic, architecture, adversarial, and
aggregate validation and is merged by human authority.
