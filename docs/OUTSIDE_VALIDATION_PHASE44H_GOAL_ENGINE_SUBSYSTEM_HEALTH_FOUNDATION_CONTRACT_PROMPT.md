# Outside Validation Prompt - Phase 44H Goal Engine Subsystem Health Foundation Contract

Validate Phase44H as an implementation-contract-only packet from the exact PR
head in a clean checkout.

Return one of:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Only `PASS` or `PASS WITH REVIEW NOTES` may unblock Phase44I.

## Required Review Files

```text
docs/PHASE44H_GOAL_ENGINE_SUBSYSTEM_HEALTH_FOUNDATION_CONTRACT.md
docs/CHECKPOINT_PHASE44H_GOAL_ENGINE_SUBSYSTEM_HEALTH_FOUNDATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE44H_GOAL_ENGINE_SUBSYSTEM_HEALTH_FOUNDATION_CONTRACT_PROMPT.md
docs/GOAL_ENGINE_IMPLEMENTATION_PROGRAM_V1.md
docs/PHASE50C_LOCAL_WORKING_ITERATION_V0_1_CHECKPOINT_FREEZE_CONTRACT.md
docs/PHASE44G_GOAL_ENGINE_STATE_ENGINE_CHECKPOINT_FREEZE_CONTRACT.md
docs/PHASE44E_GOAL_ENGINE_STATE_ENGINE_IMPLEMENTATION_CONTRACT.md
docs/GOAL_ENGINE_V1_SPEC.md
docs/CODIE_V2_CONSTITUTION.md
codie/goal_engine/foundation.py
codie/goal_engine/state_engine.py
codie/goal_engine/__init__.py
tests/test_goal_engine_foundation.py
tests/test_goal_engine_state_engine.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

## Required Gate Checks

Confirm:

```text
Phase50C has exact artifact-backed PASS evidence through merged PR #89
the protected tuple is Phase44H / implementation-contract / INTERMEDIATE_PACKET
the PR does not modify docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
the packet changes only its eight authorized documentation files
the implementation-program edit is status-only
the accepted Phase44-49 sequence and capability roadmap are unchanged
Phase44I remains implementation-only and blocked
Phase44I uses INTERMEDIATE_PACKET
Codie V2 remains primary authority
Goal Engine v1 remains subordinate
Foundation v1 and State Engine v1 remain frozen
the human-governed roadmap remains active
```

## Required Architecture Checks

Confirm the contract accurately records:

```text
codie/goal_engine/foundation.py is the accepted Foundation v1 surface
codie/goal_engine/state_engine.py is the accepted State Engine v1 surface
codie/goal_engine/health.py does not currently exist
no Goal Engine health test module currently exists
FindingIdentifier exists but no durable Finding ledger exists
GoalEvidenceReference is the accepted bounded evidence-reference record
Decision Intelligence retains persisted recommendation/deck-health authority
provider/source health is not Goal Engine subsystem-health authority
deck health is not project/Jin/Theory-Corpus health
repository validation is not the Independent Goal Validator
the evidence graph is not a Build Graph
future Phase44I is isolated to one module, exports, focused tests, and report
```

## Required Domain Separation Checks

Confirm:

```text
the only v1 domains are CODIE, JIN, and THEORY_CORPUS
every definition, observation, manifest, Finding, reference, and assessment has one domain
cross-domain records and references fail closed
there is no GLOBAL, OVERALL, PROJECT, COMBINED, or UNIVERSAL domain
there is no cross-domain assessment or aggregate function
future domains require later contracts
```

Reject any universal health score, overall status, weighted aggregate,
percentage, grade, ranking, comparison, or cross-domain conclusion.

## Required Record Checks

Confirm exact immutable records are defined for:

```text
HealthSignalDefinition
HealthSignalObservation
HealthManifest
HealthFinding
SubsystemHealthAssessmentReference
SubsystemHealthAssessment
```

Confirm exact vocabulary distinguishes:

```text
OBJECTIVE, SEMI_OBJECTIVE, SUBJECTIVE
PASS, DEGRADED, FAIL, UNKNOWN, CONFLICTED, NOT_APPLICABLE
DEGRADATION, FAILURE, EVIDENCE_GAP, EVIDENCE_CONFLICT,
STALE_EVIDENCE, PRIVACY_OR_SECURITY, MANIFEST_GAP
the exact domain-specific CODIE, JIN, and THEORY_CORPUS categories
```

Confirm existing `GoalEvidenceReference` and `FindingIdentifier` are reused
without forking the evidence model or implementing the durable ledger.

## Required Assessment Checks

Confirm future Phase44I is limited to a pure function that:

```text
validates one manifest and one domain at a time
uses only caller-supplied definitions, observations, evidence, policy, and prior references
uses caller-supplied UTC as_of and never reads the wall clock
rejects duplicate, dangling, forbidden, ambiguous, and cross-domain inputs
preserves stale, unknown, conflicted, missing, and not-applicable distinctions
requires evidence for PASS, DEGRADED, and FAIL
requires limitations for UNKNOWN
requires resolvable conflict evidence for CONFLICTED
forbids NOT_APPLICABLE for required signals
requires exactly one observation for every required definition
fails closed on missing or duplicate required observations
emits evidence-gap or manifest-gap Findings for explicit UNKNOWN required signals
emits stale-evidence Findings without rewriting caller signal status
emits evidence-bounded Findings for DEGRADED, FAIL, and CONFLICTED signals
does not emit a problem Finding from PASS or NOT_APPLICABLE alone
derives generated Finding IDs and timestamps deterministically without randomness or wall clock
calculates only exact manifest counts
sorts and serializes deterministically
returns a byte-stable single-domain assessment
```

## Required Evidence And Subjectivity Checks

Confirm:

```text
facts remain separate from human decisions and subjective feedback
objective, semi-objective, and subjective assessments remain distinct
historical validity remains separate from current applicability
supporting evidence remains separate from conflicting evidence
missing or conflicting evidence cannot become PASS
confidence grants no authority
every Finding states disconfirmation criteria and limitations
Findings cannot exceed their source-signal evidence
health Findings remain distinct from validator findings, Ideas, Goals, and recommendations
user feedback controls only that user's Jin communication preference and subjective usefulness
user feedback cannot overwrite Rules, cards, legality, tournaments, or factual evidence
Theory Corpus completeness is bounded to a declared immutable manifest
```

## Required Constitutional Boundary Checks

Confirm the contract preserves:

```text
hard evidence boundaries
local-first, private, zero-cost, standard-library-only behavior
official Scryfall card-truth provenance
public Moxfield and pasted user inputs as non-tournament evidence
Theory and theory-skill human review gates
external Rules and Corrections authority
Hareruya tournament-only provenance
supplemental-only Stream Deck scope with no Phase44I integration
human roadmap, merge, release, and promotion authority
durable ledger, impact, experiment, decision, corpus, validator, and shadow deferrals
Build Graph and CCPM-inspired execution only in conditional Phase48
no Stage 1 or higher authority
```

## Reject If The Packet Authorizes

```text
production implementation in Phase44H
global or cross-domain health scoring
Goal, Goal Contract, Goal candidate, Idea, work item, or recommendation creation
durable Finding persistence or Findings/Idea Ledger behavior
work selection, ranking, activation, scheduling, execution, or reprioritization
runtime mutation, lifecycle transition, authority calculation, or permission checks
repository, filesystem, database, provider, network, process, environment, wall-clock, or model reads
tests, validators, ingestion, retrieval, analytics, simulation, or provider execution
Scryfall, Moxfield, Hareruya, Theory, Rules, or community-source fetching
State Engine v1 or Foundation v1 changes
source-authority, evidence-class, provenance, privacy, or confidence-ceiling changes
subjective preference overriding fact
Theory review bypass, Rules mutation, or Correction activation
Hareruya use outside tournament provenance
schema, migration, persistence, dependency, fixture, workflow, validator, or repair changes
UI, CLI, API, service, worker, queue, scheduler, notification, or Stream Deck behavior
Build Graph, task graph, GitHub Issue state, worktree dispatch, agents, or CCPM
human merge, release, roadmap, approval, or promotion bypass
```

## Required Commands

```text
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -v
```

## Validation Tuple

```text
phase_id: Phase44H
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase44I
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

## Final Gate

Phase44I remains blocked until this exact Phase44H SHA receives artifact-backed
`PASS` or `PASS WITH REVIEW NOTES` and Phase44H is merged by human authority.
