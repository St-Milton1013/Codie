# Outside Validation - Phase 41A Tournament Exposure Analyzer Core Contract

Validate Phase 41A from the exact merged `main` SHA.

## Required Validation Tuple

```text
phase_id: Phase41A
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase41B
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Review Files

```text
docs/PHASE41A_TOURNAMENT_EXPOSURE_ANALYZER_CORE_CONTRACT.md
docs/CHECKPOINT_PHASE41A_TOURNAMENT_EXPOSURE_ANALYZER_CORE_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE41A_TOURNAMENT_EXPOSURE_ANALYZER_CORE_CONTRACT_PROMPT.md
docs/CODIE_V2_CONSTITUTION.md
docs/ROADMAP_PATCH_V2_INTELLIGENCE_PROGRAM_INTAKE.md
docs/PHASE40K_RELATIONSHIP_INTELLIGENCE_CORE_CHECKPOINT_FREEZE_CONTRACT.md
docs/CHECKPOINT_PHASE40K_RELATIONSHIP_INTELLIGENCE_CORE_CHECKPOINT_FREEZE_REPORT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

## Required Confirmation

Confirm that:

```text
Phase 40K acceptance evidence is recorded accurately
Phase 41A is contract-only
Tournament Exposure remains separate from Relationship Intelligence
Tournament Exposure remains measured evidence
the independent-seat approximation is labeled explicitly
per-round and event-wide formulas are visible
the default three-opponent-seat assumption remains explicit and configurable
expected attendance and event-size class remain visible context
independent_seat is the only supported core pairing-model identifier
the model warns that it is not Swiss pairing
supported geographic, event, and target scopes match Constitution V2
source population, sample, coverage, confidence, assumptions, and caveats remain visible
metagame share must agree with matching and available population counts
numeric precision and rounding policy are explicit and versioned
canonical population identity and deduplication rules are explicit
local-versus-global and regional-versus-global comparisons preserve compatible inputs
preparation briefs remain deterministic evidence summaries
personal decks do not enter aggregate source populations
Tournament Exposure does not directly generate recommendations
Decision Intelligence consumption requires Unified Evidence
Phase 41B is contract-only and remains blocked
the feature packet does not modify active validation scope
neither constitution is modified
```

## Reject If

Reject the packet if it:

```text
implements production code, tests, fixtures, schema, repositories, or providers
implements exposure calculations in Phase 41A
silently introduces Swiss pairing or standings-aware behavior
models pods, repeat opponents, or byes without a separate contract
infers matchup strength, win rate, placement, or causal effects
hides formula, population, sample, coverage, assumptions, or caveats
reads raw provider payloads or private deck text
allows personal decks into aggregate source populations
creates tag, package, combo, or archetype truth
generates deck changes or recommendations
collapses Tournament Exposure into Relationship Intelligence
adds simulator, Jin, UI, CLI, LLM, live-network, or file-writing behavior
changes dependencies, validators, workflows, active scope, or either constitution
authorizes Phase 41B implementation before Phase 41A is accepted
```

## Commands

Run from a clean checkout at the exact target SHA:

```text
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -v
```

Inspect the merged diff and confirm no undeclared production, test, fixture,
schema, repository, dependency, workflow, active-scope, or constitution file
changed.

## Return

Return:

```text
validated SHA
workflow run ID
artifact name
deterministic result and findings
architecture result and findings
adversarial result and findings
aggregate result
severity totals
skipped validators
unresolved findings
errors
final governance verdict
```

Allowed final verdicts:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Only PASS or PASS WITH REVIEW NOTES unblocks Phase 41B.
