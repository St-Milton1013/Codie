# Phase50B Codie Local Working Iteration v0.1 Implementation Report

Status: internally complete; exact-SHA outside validation required

## Validation tuple

```text
phase_id: Phase50B
phase_part: implementation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase50C
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase50C remains blocked until Phase50B receives exact-SHA artifact-backed
`PASS` or `PASS WITH REVIEW NOTES` and human merge.

## Phase50A acceptance evidence

```text
pull request: 87
validated SHA: 597f2e9531b1ab8666bb89054e3e516e67ee97e5
final ready-for-review workflow run ID: 31780486668
artifact: codie-pr-validation-597f2e9531b1ab8666bb89054e3e516e67ee97e5
artifact ID: 9211499937
artifact digest: sha256:1e0101358896a70d6508dfc91dfe3a30fb159173321037967e3a900eaf5bc5b2
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: CLEAN_PASS
aggregate: CLEAN_PASS
findings: 0
errors: 0
skipped validators: 0
merge commit: b5b1b4b5bf815f3d6d1cdf2106697fa3bb007dc4
```

The earlier draft-state workflow run `31780056074` also returned a full
`CLEAN_PASS`. The ready-for-review run above is the Phase50A checkpoint source
of truth.

## Implemented vertical slice

Phase50B replaces the static page-model preview with one same-origin,
user-operated local workflow:

```text
built React UI
-> loopback-only Python standard-library HTTP adapter
-> contained local application service
-> user-initiated bounded card-data preparation or public Moxfield import
-> existing Scryfall, Moxfield client, card lookup, deck import, evidence comparison,
   saved-analysis, export, repository, and SQLite surfaces
```

The slice allows a user to:

```text
prepare an idempotent contained SQLite workspace and locally cached card data
reuse or explicitly refresh the bounded, hashed, trusted card-data snapshot
paste or load a public Moxfield URL and atomically import a Commander deck
see unresolved names without partial persistence
select an explicit local evidence-candidate JSON packet
run and save an evidence-only present/absent comparison
reload and retrieve the same deck and analysis from SQLite
inspect evidence type, score, sample size, and provenance
download JSON and Markdown representations
stop the foreground service without leaving a loopback listener
```

## Runtime and safety boundary

```text
default binding: 127.0.0.1:8765
non-loopback configuration: rejected
non-loopback Host request: rejected
same-origin requests only; no CORS grant
database path: contained below configured workspace root
server networking: Python standard library only
normal launch/page load: no package install, provider fetch, mutation, API key,
  account, telemetry, LAN binding, or background work
remote work: only after explicit Prepare/Refresh or deck-import action; official
  Scryfall bulk data and public Moxfield deck endpoints only
remote cache: contained, bounded, hashed, temporary-file streamed, atomic
request body: JSON object, explicit Content-Length, application/json,
  configured 256 MiB maximum
errors: structured and redacted; no traceback response
mutations: transaction-bounded and fail closed
raw deck input: absent from listings and default detail
```

The UI performs only readiness and listing `GET` requests on page load. No
database bootstrap, catalog import, deck import, comparison, export, provider
fetch, or other mutation runs merely because the page loads.

## Evidence boundaries

Phase50B preserves the exact source class supplied by the user. Scryfall is
reported only as `card_truth`. Evidence candidates retain their declared
evidence type and provenance. Strategic-advice evidence types fail closed.
Presence and absence remain descriptive and cannot become cuts, additions,
rankings, optimization, or recommendations.

Hareruya URLs fail closed unless the declared evidence type remains tournament
evidence. The only remote reads are the two user-initiated sources authorized
by `docs/PHASE50B_LOCAL_WORKING_ITERATION_V0_1_USABILITY_OVERRIDE.md`. No
Hareruya provider client, Theory/Jin/Rules/Corrections behavior, simulation
promotion, Goal Engine behavior, or Stream Deck control path exists in the
local application.

## Implementation files

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
ui/src/styles.css
ui/src/api/localAppClient.ts
ui/src/types/localApp.ts
tests/test_local_working_iteration.py
tests/test_local_working_iteration_http.py
tests/test_local_working_iteration_sources.py
docs/LOCAL_WORKING_ITERATION_V0_1_USAGE.md
docs/PHASE50B_LOCAL_WORKING_ITERATION_V0_1_USABILITY_OVERRIDE.md
```

Governance and review-packet files advanced only to the Phase50B validation
boundary:

```text
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/GOAL_ENGINE_IMPLEMENTATION_PROGRAM_V1.md
docs/PHASE50B_LOCAL_WORKING_ITERATION_V0_1_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE50B_LOCAL_WORKING_ITERATION_V0_1_PROMPT.md
```

No schema, repository, dependency declaration, workflow, existing provider client,
Goal Engine, Jin, Theory, Rules, Corrections, simulation, recommendation,
constitution, or Stream Deck file changed.

## Local validation

```text
python scripts/check_schema.py
PASS - Schema bootstrap check passed.

python -m pytest -q tests/test_local_working_iteration.py \
  tests/test_local_working_iteration_http.py \
  tests/test_local_working_iteration_sources.py
PASS - 26 tests

python -m pytest -q
PASS - 1344 tests, 1 skipped

python -m ruff check codie/local_app \
  tests/test_local_working_iteration.py \
  tests/test_local_working_iteration_http.py \
  tests/test_local_working_iteration_sources.py
PASS

python -m mypy --follow-imports=skip codie/local_app
PASS - no issues in 5 source files

npm.cmd run build
PASS - TypeScript no-emit and Vite production build

PowerShell parser validation for scripts/run-codie.ps1 and
scripts/setup-codie-ui.ps1
PASS

git diff --check
PASS
```

The exact unqualified `python -m mypy codie/local_app` command follows imported
legacy modules and reports 13 inherited findings in five untouched files. The
focused `--follow-imports=skip` command proves the four new local-app modules
clean without concealing the whole-repository inventory.

## Whole-repository non-regression inventories

```text
python -m ruff check .
488 inherited findings - unchanged from Phase50A baseline

python -m mypy codie
316 inherited errors in 37 files - unchanged from Phase50A baseline

npm ci audit summary
2 high-severity findings in the unchanged locked UI development dependency set
runtime dependency additions: none
```

Phase50B does not repair or suppress inherited debt outside its authorized
change boundary. The production UI is compiled to static assets and served by
the loopback-only Python adapter; normal runtime does not run Vite or install
the development dependency set.

## Browser acceptance evidence

The built UI was exercised in the Codex in-app browser against
`http://127.0.0.1:8765/` using a fresh contained ignored workspace.

```text
service and UI readiness: PASS
page-load mutation check: PASS
one-click workspace and official card-data preparation: PASS
current compressed JSON Lines bulk format: PASS
contained cache reuse without another download: PASS
38,624 safely matchable card records imported: PASS
2 structurally valid but unmatchable-name records reported and skipped: PASS
resolved 4-card pasted Commander deck import: PASS
live public Moxfield URL import with 133 persisted card rows: PASS
remembered-deck selection: PASS
local two-candidate evidence packet selection: PASS
comparison persistence: PASS
visible community_signal and tournament_evidence types: PASS
visible source record IDs and source URL: PASS
present and absent rows: PASS
page reload persistence: PASS - 2 current-flow decks restored from SQLite;
  prior evidence-flow acceptance restored 1 deck and 1 analysis
saved-analysis retrieval: PASS
JSON export action: PASS
Markdown export action: PASS
browser console errors or warnings: none
foreground server stop/listener release: PASS in focused HTTP lifecycle test
write outside workspace: none
```

The tested workspace remains ignored runtime data and is not part of the
repository diff.

## Hard boundary audit

```text
hard evidence class separation: preserved
local-first/private/zero-cost runtime: preserved
workspace containment: enforced
supplemental-only Stream Deck: preserved; integration absent
Theory/theory-skill review gate: preserved; Theory untouched
Hareruya tournament-only scope: enforced
Rules and Corrections authority: unchanged
Goal Engine runtime and authority: unchanged
human roadmap, merge, release, and promotion gates: unchanged
Phase44H-49 roadmap and conditional Phase48 capability placement: unchanged
```

## Recommendation

Proceed to exact-SHA outside validation of Phase50B. Do not begin Phase50C
until the implementation is accepted and merged through human authority.
