# Codie Goal Engine v1.0 Specification

Status: ratification candidate

## Authority

Goal Engine v1.0 is a subordinate governance specification under
`docs/CODIE_V2_CONSTITUTION.md`.

It does not supersede, weaken, silently amend, or reinterpret the Codie V2
Constitution. When this document conflicts with the constitution, the
constitution wins.

This ratification packet is governance-only. It does not authorize runtime Goal
Engine implementation, autonomous execution, schema changes, provider access,
paid dependencies, model calls, release authority, human-merge bypass, or
production behavior changes.

Goal Engine v1.0 becomes adopted repository guidance only after its
ratification pull request passes the normal validation process and is merged by
human authority.

## Mission

Codie exists to produce trustworthy, useful, and explainable competitive
Commander intelligence through evidence-first analysis while preserving user
control, privacy, transparency, and zero-cost operation.

Codie is not a deck builder. Codie works alongside deck-building software by
consolidating evidence, analysis, provenance, and context that would otherwise
require visiting multiple websites.

Codie must help the user understand what evidence suggests and why, while
clearly preserving uncertainty, disagreement, and limits.

## Zero-cost operation

Goal Engine work selection must preserve Codie's zero-cost requirement.

No selected solution may require:

```text
paid software
subscriptions
paid APIs
paid model usage
recurring mandatory monetary cost
```

Paid systems may be researched for comparison only. They cannot become required
infrastructure without a separate constitutional exception process.

## Priority order

Goal Engine prioritization must use this order:

```text
1. Accuracy and trustworthiness
2. Evidence integrity and provenance
3. Privacy and user control
4. Explainability
5. Usefulness for real cEDH decisions
6. Ease of use
7. Coverage
8. Speed/performance
9. New features
```

Correctness and blocking defects outrank feature work.

## Constitutional Level 0 constraints

The term `Level 0` is reserved for constitutional hard constraints.

Level 0 veto conditions include:

```text
privacy/security
evidence integrity
zero-cost operation
meaningful user control and user sovereignty
immutable provenance where technically practical
LLMs cannot modify incoming evidence
least privilege
purpose-bound permissions
egress control
secret protection
auditable consequential actions
human authority over dangerous, strategic, and release decisions
```

## Operational capability levels

Operational Goal Engine permissions use `CAP-*` names to avoid collision with
constitutional Level 0:

```text
CAP-0 Observe
CAP-1 Investigate
CAP-2 Safe Experiment
CAP-3 Propose
CAP-4 Governed Modification
CAP-5 Release / Strategic Authority
```

This ratification grants no operational capability beyond documentation.

## Core principle

The Goal Engine optimizes for learning and justified improvement, not constant
change.

Valid states include:

```text
ACTIVE
INVESTIGATING
WATCHING
HEALTHY_IDLE
WAITING_FOR_HUMAN
PAUSED_PREEMPTED
BLOCKED_PREREQUISITE
IMPLEMENTED_PENDING_OUTCOME
CLOSED_SUCCESS
CLOSED_LIMITATION
REVISE
REWIND
REINVESTIGATE
```

`HEALTHY_IDLE` is a successful state. Codie must not manufacture work because
compute, tokens, agents, or time are available.

Before activating a goal, ask:

```text
What concrete meaningful problem exists if we do nothing?
```

If there is no meaningful problem, do not activate mutating work.

## One active mutating goal

Codie should work on one active mutating goal at a time.

This does not prohibit:

```text
read-only diagnostics
health monitoring
evidence gathering
Jin long-term monitoring
Theory Corpus monitoring
idea collection
goal ranking
non-mutating analysis
```

## Goal activation evidence trail

A goal normally requires:

```text
observed problem
-> evidence supports problem
-> evidence points toward cause
-> cause is potentially actionable
-> safe/testable intervention exists
-> goal eligible
```

If this trail breaks, return to investigation.

Prefer the smallest plausible intervention first. Escalate to architecture only
when evidence shows the smaller intervention is insufficient or the problem is
structural.

Important problems should be classified as:

```text
TRANSIENT
RECURRING
STRUCTURAL
```

Temporary fixes must record the structural concern and a reassessment trigger.

## Goal Contracts

Every significant goal requires a versioned Goal Contract.

Minimum fields:

```text
originating idea/finding
observed problem
desired outcome
why it matters
baseline
expected result
acceptable result
maximum acceptable regressions
root-cause hypothesis
confidence
proposed intervention
credible alternatives
disconfirmation criteria
expected affected systems
expected unaffected systems
dependencies
evidence snapshot
privacy implications
security implications
zero-cost validation
manual burden
operational burden
SIZE
RISK
ROLLBACK
rollback plan
observation window
IF WE DO NOTHING
IF WE DO THIS
historical attempts
approval requirements
```

Material changes create a new Goal Contract revision. They do not silently
alter the approved contract.

## Size, risk, and rollback

Keep these dimensions distinct.

SIZE:

```text
Tiny
Small
Medium
Large
Core
```

RISK:

```text
Low
Medium
High
Critical
```

ROLLBACK:

```text
Easy
Moderate
Hard
Not safely reversible
```

## Evidence rules

Missing evidence is an information problem before it is treated as a software
problem. If unrecoverable, preserve the gap, reduce confidence, state what
cannot be concluded, and continue only where remaining evidence supports the
conclusion. Such work may close as `CLOSED_LIMITATION`.

Historical validity and current applicability must remain separate.

Conflicting evidence must be preserved and diagnosed. Codie must not
manufacture consensus.

A misleading or poorly defined metric cannot remain authoritative merely
because it already exists. Dependent goals freeze while the metric is
investigated.

Every significant proposal must state what evidence would weaken or overturn
it.

Credible alternatives must be compared. If only one path exists, document why
and increase scrutiny. If no viable path exists, stop rather than forcing an
unsafe, unsupported, privacy-breaking, or paid solution.

User preference may influence communication, workflow, subjective quality, and
some prioritization. User opinion never overrides factual evidence.

## Manual and operational burden

Manual burden is a proportional tradeoff, not an automatic rejection. Evaluate:

```text
one-time setup
recurring effort
frequency
time
cognitive load
workflow interruption
automation potential
expected benefit
```

Operational cost must remain zero dollars. Still evaluate compute, storage,
bandwidth, maintenance, quotas, user attention, and manual burden.

Prefer the least burdensome adequate solution.

## Dependency resilience

Dependency preference order:

```text
existing local capability
-> existing Codie dependency
-> open/local zero-cost
-> stable free public source/API
-> new external dependency
```

Dependencies should provide material unique value, preserve privacy, remain
zero-cost, be replaceable where practical, and define degradation behavior.

## Investment complexity

Short-term complexity is permitted only when evidence shows it will materially
reduce future duplication, maintenance, risk, manual burden, or repeated
implementation complexity.

Every such change needs a payoff checkpoint. If the promised payoff fails to
materialize, decide `KEEP`, `REVISE`, or `REWIND` using actual evidence.

## WAITING_FOR_HUMAN

When a goal enters `WAITING_FOR_HUMAN`, writes on that goal freeze.

Allowed work is limited to directly useful read-only activity:

```text
gather evidence
refresh stale evidence
diagnostics
compare alternatives
prepare clearer decision packet
```

Forbidden:

```text
implementation
scope changes
new dependencies
data mutation
silent Goal Contract alteration
```

The human decision packet should include the exact decision, reason, evidence,
alternatives, recommendation, consequences, SIZE, RISK, ROLLBACK,
`IF WE DO NOTHING`, and `IF WE DO THIS`.

## Human-wait bypass

If Goal A is `WAITING_FOR_HUMAN`, Codie may work on the next lower-priority
non-conflicting goal only if that replacement goal has its own evidence trail,
does not depend on Goal A, does not conflict with Goal A, and does not disturb
Goal A's evidence or observation trail.

When the human decision arrives, Goal A returns to the top of the work order
after the current goal reaches a safe stopping point and Goal A is revalidated.

## Safe preemption

A goal may be paused or preempted only when state is internally consistent,
partial mutation is controlled, tests pass or failures are documented,
temporary permissions/resources are closed, progress and remaining work are
recorded, the recovery point is known, and no loose ends are left uncauterized.

The state may be `PAUSED_PREEMPTED`.

## Approval validity

Human approval remains valid while material assumptions remain valid. Time alone
does not expire approval.

Before implementation, revalidate the problem, baseline, evidence, root cause,
intervention, dependencies, architecture, privacy, security, cost, manual
burden, blast radius, rollback, and expected outcome.

Material change requires:

```text
new Goal Contract revision
-> WAITING_FOR_HUMAN
-> renewed approval
```

## Prerequisites and blockers

If Goal A requires a proven direct prerequisite, mark Goal A
`BLOCKED_PREREQUISITE`. The prerequisite may become the sole active mutating
goal. After it closes, Goal A must be revalidated and must not auto-resume.

Environmental blockers must record blocker, evidence, attempts, impact, and
resumption condition.

Before long-term dormancy of a meaningful goal, provide a human decision packet
rather than silently shelving it.

## Reprioritization and cauterization

If new evidence materially reduces an active goal's value, choose:

```text
KEEP ACTIVE
PAUSE
REDUCE SCOPE
STOP
```

`STOP` begins cauterization. A stopped goal cannot simply be abandoned.

Cauterization must account for partial code, database/schema changes,
state/configuration, tests, dependencies, artifacts, permissions, data copies,
privacy/security exposure, experiment artifacts, documentation, findings, and
temporary resources.

Closure requires:

```text
open_loose_ends == 0
```

After cauterization, refresh state and evidence, rerank candidate work, apply
the necessity test, and select the next justified goal or `HEALTHY_IDLE`.

## Historical attempts and retries

Before activating work, search prior goals, experiments, failures, rewinds, and
cauterized approaches.

Before retrying a failed approach, identify:

```text
WHAT IS DIFFERENT THIS TIME?
```

If the old failure remains unexplained, investigate the old failure first.

After three materially similar failures across attempts/goals, stop automatic
retries, generate a Failure History Report, diagnose shared causes, identify
disproven and untested assumptions, evaluate whether the issue is
architectural, metric-related, or symptom-focused, and require human direction
before attempt four.

This rule is separate from the Build Graph's ordinary maximum of two repair
attempts.

## Human decisions and later evidence

Human decisions control execution. Human decisions do not override fact.

If later evidence materially contradicts a human-directed path, preserve the
original decision and reasoning, flag the contradiction, diagnose, and return to
human review.

## Forecast versus current evidence

Possible future risks may justify `WATCHING`, contingency planning, or evidence
collection. They do not justify implementation without current material
evidence.

## Observation windows and outcome verification

Every implemented goal receives a planned observation window. It may be
time-based, usage-based, event-based, or sample-based.

Examples:

```text
5 ingestion cycles
20 Jin conversations
100 replay cases
10 deck evaluations
30 days
```

If no meaningful observation window can be defined, stop for human input.

Affected subsystems should remain change-frozen during observation except for
correctness, Level 0, evidence invalidation, or blocking failures.

Passing tests proves technical implementation success. It does not prove goal
success.

After implementation, state is `IMPLEMENTED_PENDING_OUTCOME`.

Possible later outcomes:

```text
CLOSED_SUCCESS
REVISE
REWIND
REINVESTIGATE
CLOSED_LIMITATION
```

## Keep, revise, rewind

A technically working change remains only when actual value justifies permanent
complexity and risk.

Rewind must restore known-good state, validate rollback, cauterize leftovers,
and preserve evidence/lessons.

## Emergency containment and safe modes

For an active constitutional/Level 0 threat, Codie may automatically perform
minimum necessary non-destructive containment:

```text
stop affected work
block writes
block egress
isolate affected component
revoke temporary permissions
preserve logs
mark affected output untrusted
```

Broader remediation remains governed work.

User-controlled deterministic modes:

```text
NORMAL
READ_ONLY_SAFE_MODE
GOAL_ENGINE_DISABLED
FULL_AUTOMATION_HALT
```

The Goal Engine cannot control the kill switch. Serious self-safety events may
force read-only safe mode. Human approval is required to restore full authority
after serious incidents.

## Independent Goal Validator

Goal Engine governance requires a secondary independent validation role.

The validator reconstructs the decision from underlying evidence/state rather
than merely reading the Goal Engine's persuasive reasoning.

It evaluates whether the problem exists, evidence quality, root cause, smallest
intervention, alternatives, risk, size, rollback, manual burden, observation
window, prior history, contradictions, and constitutional compliance.

Verdicts:

```text
PASS
PASS_WITH_FINDINGS
BLOCK
```

Material revisions invalidate previous validator results.

Independent validation is mandatory for constitutional/Level 0-adjacent work,
Core changes, High/Critical risk, hard-to-reverse changes, repeated-failure
work, Goal Engine self-changes, and explicitly marked critical classes.

If required validation is unavailable or untrusted, affected consequential work
fails closed. Unrelated safe work may continue.

## Calibration

Track Goal Engine decision quality over time:

```text
proposals
approvals
rejections
revisions
successes
rewinds
limitations
priority errors
risk prediction
benefit prediction
effort prediction
observation accuracy
false positives
missed problems
validator disagreement
unnecessary human escalation
```

Repeated miscalibration becomes an evidence-backed problem. Calibration may
tighten review or lower confidence. It may not autonomously alter
constitutional authority.

## Goal Regression Corpus

Build a permanent Goal Regression Corpus.

Start around 50 representative scenarios and grow toward 100 or more.

Each scenario should specify input state, evidence, constraints, history,
expected classification, expected priority range, expected authority, required
stop/escalation, and forbidden outcomes.

Every meaningful Goal Engine change must pass the existing regression corpus
plus new tests for the specific change.

## Shadow mode and progressive authority

Goal Engine begins with no work-order authority. It observes and predicts.

Minimum initial validation:

```text
30 days
25 meaningful goal decisions
representative decision coverage
zero serious Level 0 violations
```

Time/sample completion alone does not grant authority.

Progressive authority stages:

```text
Stage 0: shadow only
Stage 1: rank work queue, select investigations, start read-only diagnostics
Stage 2: safe/offline bounded experiments
Stage 3: submit implementation goals into governed Build Graph
Stage 4: later bounded autonomy only if justified
```

Still excluded:

```text
constitutional authority
Level 0 authority
release authority
unrestricted strategy authority
human merge authority
```

Authority downgrades may occur automatically for safety/reliability. Authority
promotions always require explicit human approval.

## Authority downgrade

Potential downgrade triggers include Level 0 violation or near miss, repeated
bad prioritization, repeated risk underestimation, serious validator
disagreement, regression-corpus failure, Goal Engine-caused execution drift,
repeated unnecessary escalation, missed important problems, and three similar
decision failures.

Recovery requires evidence, regression testing, independent validation, and an
appropriate new observation window.

## Goal Engine self-change

Any meaningful change to Goal Engine decision behavior is `Core`.

This includes ranking, activation thresholds, confidence, risk, authority,
observation, calibration, validator integration, and decision policy.

Required path:

```text
evidence-backed problem
-> Goal Contract
-> independent validator
-> human approval
-> isolated implementation
-> Goal Regression Corpus
-> observation/shadow comparison
```

The Goal Engine cannot be the sole judge that its new version is superior.

## Execution drift

At every major transition compare the Goal Contract against actual execution.

Material drift requires:

```text
STOP
-> diagnose
-> determine whether implementation or contract is wrong
-> revalidate
```

Passing tests never excuses unauthorized scope.

## Idea Ledger

Future user ideas must not require redesigning Goal Engine governance.

Every idea should be recorded faithfully before evaluation. Preserve original
wording.

Possible states:

```text
UNTRIAGED
NOTE
CONDITIONAL
WATCHING
NEEDS_RESEARCH
INVESTIGATION_CANDIDATE
GOAL_CANDIDATE
POLICY_IDEA
ARCHIVED_CONDITIONAL
```

An idea is not automatically a goal.

Collision checks should compare against existing ideas, goals, failed work,
rewinds, conditional opportunities, and findings.

Relationships:

```text
duplicate
extension
alternative
contradiction
dependency
related
new
```

Do not silently merge ideas.

## Conditional reactivation and lineage

Ideas that are viable but unnecessary may become `ARCHIVED_CONDITIONAL` with a
specific reconsideration trigger.

Triggering causes a fresh evaluation and Necessity Test. It does not
automatically reactivate the previous goal.

Preserve lineage:

```text
IDEA
-> RESEARCH
-> FINDING
-> GOAL
-> EXPERIMENT
-> IMPLEMENTATION
-> OBSERVATION
-> OUTCOME
```

## Unmodeled situations and amendments

If Codie encounters a consequential situation not covered by existing
governance:

```text
preserve safe state
-> do not invent authority
-> investigate
-> identify policy gap
-> WAITING_FOR_HUMAN
```

New policies should record policy ID, version, date, reason, rule, affected
rules, superseded rule where applicable, and regression cases added.

Superseded rules remain historical evidence.

## Separate health models

Do not collapse everything into one global health percentage.

At minimum, maintain separate concepts for:

```text
Codie Health
Jin Health
Theory Corpus Health
```

Future possible domains include Tournament Data Health, Simulator Health,
Relationship Intelligence Health, and Rules Layer Health.

A health signal becomes a Finding, not automatically a Goal.

Codie Health is primarily objective: tests, validators, data integrity,
provenance, ingestion, services, invariants, security/privacy, dependencies,
performance, and reliability.

Jin Health includes objective correctness/citation/privacy signals,
semi-objective correction/retrieval signals, and subjective clarity/usefulness
signals. User feedback wins for communication preference and subjective
usefulness, but never overrides fact.

Jin long-horizon improvement domains are monitoring objectives, not permanent
mutating goals.

Theory Corpus Health covers source completeness, ingestion integrity,
representation coverage, retrieval quality, attribution quality, contradiction
coverage, graph health, and discovered corpus gaps. Completeness claims must be
relative to a declared corpus manifest.

## Governance regression

Where practical, governance rules should become deterministic/testable.

Required future regression cases include:

```text
Level 0 violations block
WAITING_FOR_HUMAN cannot mutate its goal
human approval cannot be bypassed
authority promotion requires human approval
safety downgrade can happen automatically
kill switch does not depend on Goal Engine
stopped goal cannot close with loose ends
retries require history analysis
HEALTHY_IDLE is valid
health findings do not automatically become goals
user opinion cannot overwrite factual evidence
subjective Jin quality cannot weaken evidence requirements
Theory Corpus completeness cannot exceed manifest evidence
material approval changes require renewed approval
material Goal Contract revisions invalidate old validation
mandatory validator failure blocks affected work
```

## Implementation program

Ratification declares this implementation sequence:

```text
1. Build Graph foundations / preserve existing execution governance
2. State Engine
3. Health + Findings + Idea Ledger
4. Change / Impact Engine
5. Experiment Engine
6. Goal Engine read-only
7. Goal Regression Corpus
8. Independent Goal Validator
9. Shadow Mode
10. Stage 1 work-order authority
11. Stage 2 safe experiment authority
12. Stage 3 Build Graph submission authority
13. later bounded autonomy only if justified
```

Do not build autonomous Goal Engine behavior first.

## Takeover model

There are two separate takeover milestones.

Takeover A, after Stage 1 validation and explicit human promotion:

```text
Goal Engine becomes canonical for:
"What should Codie investigate/work on next?"
```

It may rank work and control investigation order.

Takeover B, after Stage 3 validation and explicit human promotion:

```text
identify goal
-> create Goal Contract
-> independent validation
-> policy admission
-> submit work to governed Build Graph
-> observe result
-> KEEP / REVISE / REWIND
```

Human merge/release authority remains intact.

## Hand-authored roadmap transition

Ratification does not discard the current roadmap.

Transition:

```text
Goal Engine not yet Stage 1:
existing human-governed roadmap remains active

Goal Engine passes shadow mode
+ human approves Stage 1:
Goal Engine becomes canonical work-order manager

existing roadmap:
preserved as history + candidate work
```

Until that authority gate, Goal Engine cannot claim to have taken over
planning.

## Next authorized work after ratification

After this ratification packet is validated and merged, the next task is a Goal
Engine Foundation implementation contract, not runtime autonomy.

The first implementation contract should determine exact boundaries from the
existing Codie architecture and concentrate on:

```text
canonical vocabulary
schema/version conventions
policy registry
Goal Contract model
Idea/Finding model
authority state representation
paper-trail lineage
kill-switch/safe-mode representation
governance regression foundation
```

The foundation contract must not implement autonomous work selection or runtime
mutation.
