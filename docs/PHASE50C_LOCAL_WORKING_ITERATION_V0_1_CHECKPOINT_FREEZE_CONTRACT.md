# Phase50C Codie Local Working Iteration v0.1 Checkpoint / Freeze Contract

Status: checkpoint and freeze only

## Validation Tuple

```text
phase_id: Phase50C
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase44H
next_phase_part: implementation-contract
next_gate_scope: INTERMEDIATE_PACKET
```

Phase44H is reserved for the Subsystem Health Foundation Contract. It remains
blocked until Phase50C outside validation returns `PASS` or
`PASS WITH REVIEW NOTES` and this checkpoint is merged through human authority.

## Purpose

Phase50C closes and freezes Codie Local Working Iteration v0.1 after the
accepted Phase50A contract and Phase50B implementation.

The frozen working iteration is:

```text
documented local setup
-> one loopback-only Codie process
-> explicit user-triggered official Scryfall preparation or refresh
-> public Moxfield URL or pasted-deck import
-> local SQLite persistence
-> saved comparison and evidence/provenance inspection
-> deterministic JSON and Markdown export
-> explicit shutdown with no remaining listener
```

Phase50C is documentation-only. It changes no production code, tests, schema,
repositories, dependencies, workflows, active scope, providers, UI, CLI,
Stream Deck integration, model behavior, or runtime authority.

## Phase50A Acceptance Evidence

```text
pull request: 87
validated SHA: 597f2e9531b1ab8666bb89054e3e516e67ee97e5
workflow run ID: 31780486668
artifact ID: 9211499937
artifact digest: sha256:1e0101358896a70d6508dfc91dfe3a30fb159173321037967e3a900eaf5bc5b2
merge commit: b5b1b4b5bf815f3d6d1cdf2106697fa3bb007dc4
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: CLEAN_PASS
aggregate: CLEAN_PASS
findings: 0
errors: 0
skipped validators: 0
```

## Phase50B Acceptance Evidence

```text
pull request: 88
validated SHA: 651cda193186b4e4f410de3d5e8e58ef7429be5f
workflow run ID: 32975408263
artifact: codie-pr-validation-651cda193186b4e4f410de3d5e8e58ef7429be5f
artifact ID: 9610763003
artifact digest: sha256:909dac79d2ac87e809cd3fefc6fbf53f4b40e7227d5690ae4f4812f900f4468f
merge commit: 041f061ac31504a97ebc6af39d3587bc1345d1fc
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: CLEAN_PASS
aggregate: CLEAN_PASS
findings: 0
errors: 0
skipped validators: 0
```

The protected Phase50C tuple was established separately on `main` by commit
`37968cecf1938dbd3b1376e5a006665e388f9203` before this packet was published.

## Frozen Surfaces

The following accepted Phase50B surfaces are frozen as Local Working Iteration
v0.1:

```text
codie/local_app/__init__.py
codie/local_app/__main__.py
codie/local_app/server.py
codie/local_app/service.py
codie/local_app/sources.py
scripts/run-codie.ps1
scripts/setup-codie-ui.ps1
ui/index.html
ui/src/App.tsx
ui/src/api/localAppClient.ts
ui/src/styles.css
ui/src/types/localApp.ts
tests/test_local_working_iteration.py
tests/test_local_working_iteration_http.py
tests/test_local_working_iteration_sources.py
docs/PHASE50A_LOCAL_WORKING_ITERATION_V0_1_CONTRACT.md
docs/PHASE50B_LOCAL_WORKING_ITERATION_V0_1_USABILITY_OVERRIDE.md
docs/PHASE50B_LOCAL_WORKING_ITERATION_V0_1_IMPLEMENTATION_REPORT.md
docs/LOCAL_WORKING_ITERATION_V0_1_USAGE.md
```

Future semantic changes require a new accepted contract, focused tests, full
regression, exact-SHA artifact validation, and human merge authority.

## Frozen Local-First And Source Rules

```text
bind only to loopback by default
persist project state only in the user-selected local workspace
perform no page-load, background, timer, retry, or speculative provider fetch
fetch only after an explicit user action
use only official Scryfall bulk-data metadata and payloads for card truth
stream, bound, hash, atomically cache, and integrity-check card-data downloads
accept both supported official JSON and compressed JSON Lines bulk formats
report and skip only official records whose normalized card name is empty
fail closed and roll back on structural or integrity failures
accept only public Moxfield deck URLs through the approved bounded client
preserve pasted decklists as user-supplied source material
keep Moxfield and pasted-deck provenance distinct from card truth
store no credential, cookie, token, private deck content, or provider session
```

The 2026-08-25 owner-approved usability amendment remains narrow. It authorizes
only explicit card-data preparation and public Moxfield deck import. It does
not authorize additional providers, private-deck access, background fetching,
evidence promotion, or autonomous execution.

## Frozen Evidence And Governance Rules

```text
fact is separate from human decision and authority
card truth is separate from deck-source evidence
deck-source evidence is separate from theory and tournament evidence
historical validity is separate from current applicability
unknown is separate from absent and false
confidence is separate from authority
passing tests is separate from user outcome and promotion
```

Local-first and privacy requirements remain mandatory. Theory and theory-skill
review gates remain external and mandatory. Rules authority, legality, and
Corrections remain external. Hareruya remains tournament-only provenance.
Stream Deck remains absent and supplemental-only. Human roadmap, merge,
release, and promotion gates remain unchanged.

## Explicit Deferrals

Phase50C adds no Goal Engine capability and satisfies no Phase44-49 gate. It
contains no autonomous work selection, provider expansion, private Moxfield
access, background refresh, telemetry, remote persistence, universal health
score, Theory promotion, Rules mutation, Correction activation, Hareruya scope
expansion, Stream Deck control path, merge, release, or authority promotion.

Subsystem Health remains reserved for Phase44H-J. Ledger, impact, experiment,
decision, regression-corpus, independent-validation, shadow, authority, Build
Graph, and CCPM-inspired capabilities remain in their approved roadmap phases.

## Backtracking Audit

No Phase50A or Phase50B semantic correction is required. The Phase50B
implementation required only the owner-approved usability amendment and
compatibility with the current official Scryfall bulk-data representation.
Both are contained within the accepted Phase50B SHA and artifact. No later
Goal Engine capability was implemented early.

## Phase44H Boundary

After Phase50C acceptance and merge, work returns to Phase44H. Phase44H may
define only the Subsystem Health Foundation Contract. It must keep CODIE, JIN,
and THEORY_CORPUS separate; may define evidence-backed health signals or
findings; may not create a universal health score or produce Goals directly;
and remains contract-only.

## Authorized Phase50C Files

```text
docs/PHASE50C_LOCAL_WORKING_ITERATION_V0_1_CHECKPOINT_FREEZE_CONTRACT.md
docs/CHECKPOINT_PHASE50C_LOCAL_WORKING_ITERATION_V0_1_CHECKPOINT_FREEZE_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE50C_LOCAL_WORKING_ITERATION_V0_1_CHECKPOINT_FREEZE_PROMPT.md
docs/GOAL_ENGINE_IMPLEMENTATION_PROGRAM_V1.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

The roadmap edits are status-only. They do not change the accepted Phase44-49
sequence, capability roadmap, authority gates, Stage 4 disposition, or
conditional Phase48 CCPM placement.

## Forbidden Phase50C Work

Phase50C must not modify production code, tests, fixtures, schema, repositories,
dependencies, workflows, active scope, validators, providers, UI, CLI, either
constitution, or any accepted Phase50A/Phase50B surface. It must not implement
Phase44H or a later packet.

## Gate

Phase44H may begin only after Phase50C outside validation returns `PASS` or
`PASS WITH REVIEW NOTES` and this checkpoint is merged through human authority.
