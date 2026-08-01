# Phase 42K Judge-Training and Curriculum Contract

## Validation tuple

```text
phase_id: Phase42K
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase42L
next_phase_part: outside-validation
next_gate_scope: FINAL_PHASE
```

Phase 42L is reserved for the Jin / Theory / Rules / Corrections Program
Checkpoint and Release Acceptance. It remains blocked until Phase 42K outside
validation returns `PASS` or `PASS WITH REVIEW NOTES`.

## Status and authority

```text
document_type: contract-only packet
implementation_authorized: no
schema_authorized: no
lesson_generation_authorized: no
assessment_execution_authorized: no
progress_persistence_authorized: no
model_or_network_execution_authorized: no
active_scope_base: d0e8788aeec9e0c5f2c894a4655bc8cdf564a654
```

This contract defines the educational trust boundary for judge-style issue
spotting, cEDH curriculum, lesson packets, assessments, explanations, and
progress candidates. It creates no lessons or runtime behavior.

## Purpose

The curriculum may teach:

```text
cEDH fundamentals
resource and tempo theory
table politics
threat assessment
priority and stack mechanics
judge-program-style rules reasoning
common logical fallacies
rhetorical pressure
contextual use of wheels and other strategic tools
package and conversion analysis
```

Lessons must distinguish rules facts, tournament evidence, measured evidence,
theory, examples, community context, user context, and opinion.

## Authority hierarchy

Lesson content must preserve this order:

```text
current official rules and card authority
accepted legality and rules-layer interpretations
canonicalized tournament observations
reproducible measurements
reviewed and attributed theory
labeled examples and hypotheticals
community and user context
model-generated explanation
```

A lower class cannot silently override or become a higher class. A lesson is a
presentation surface, not independent authority.

## Judge-style issue-spotting sequence

Rules lessons must use the constitutional sequence:

1. identify objects and zones;
2. identify rules and effects;
3. identify timestamps and dependencies;
4. identify costs and targets;
5. apply effects;
6. explain the result;
7. cite authority.

If the accepted Rules Layer cannot resolve an interaction within its bounded
capability manifest, the lesson must return `UNSUPPORTED` or
`REQUIRES_JUDGE_REVIEW`. It may not improvise a ruling.

## No-certification boundary

Codie may provide judge-style education but must not claim to:

- certify a user as a tournament judge;
- replace an event judge or official appeal process;
- issue binding tournament rulings;
- represent endorsement by a judge program or tournament organizer;
- guarantee that an assessment score proves rules competence.

Event-specific policy questions must identify the governing document/version
or direct the user to event staff.

## Curriculum packet

A future curriculum packet must identify:

```text
curriculum_id
title
revision
learning_objectives
lesson_ids
prerequisite_ids
rules_authority_versions
theory_corpus_version
correction_ledger_version
target_audience
scope_and_limitations
review_status
```

Revision identity must be immutable. A new revision may supersede an older one
but must not silently rewrite historical lesson or assessment records.

## Lesson packet

Each future lesson packet must contain:

```text
lesson_id
curriculum_id
revision
learning_objectives
content_sections
content_class_labels
rules_citations
evidence_references
theory_claim_references
examples_and_counterexamples
format_and_date_limitations
prerequisites
assessment_refs
reflection_prompt
review_status
```

Every substantive statement must be class-labeled. Rules citations must point
to accepted versioned authority. Measured claims must cite reproducible
artifacts. Theory claims must cite reviewed, attributed, rights-cleared,
immutable source versions.

## Theory-skill review gate

A strategic framework, heuristic, or theory skill may enter a lesson only when
its source and claims have passed the accepted Phase 42F and Phase 42G gates:

```text
author and work identified
rights and storage class accepted
immutable source version retained
direct citation available
format transferability reviewed
claim typed and scoped
contradictions and counterexamples visible
human review state recorded
```

An author's framework remains attributed theory, not truth authority. Literal
heuristics must not be generalized beyond their source context.

## Examples and hypotheticals

Examples must be explicitly marked as one of:

```text
RULES_EXAMPLE
CANONICAL_TOURNAMENT_EXAMPLE
MEASURED_EXAMPLE
SIMULATED_EXAMPLE
THEORY_EXAMPLE
HYPOTHETICAL
USER_CONTEXT_EXAMPLE
```

Synthetic examples cannot become tournament observations. Simulator examples
must retain seed, assumptions, capability coverage, unsupported items, and
trace validity. A hypothetical must never be cited as empirical support.

Hareruya may appear only through canonicalized tournament, event, or deck
observations. It is not a curriculum authority, theory source, or community
signal source. Live access and WAF behavior are never lesson prerequisites.

## Assessment contract

Assessments may use issue spotting, ordering, multiple choice, short response,
scenario comparison, source identification, and uncertainty recognition.

Every assessment item must contain:

```text
assessment_item_id
lesson_revision_ref
prompt
content_class
expected_elements
accepted_authority_refs
scoring_rule
partial_credit_rule
unsupported_or_ambiguous_behavior
explanation
review_status
```

Scoring must be deterministic when the item format is deterministic. Free-text
evaluation cannot silently become authoritative; model-assisted feedback must
be labeled, bounded by a rubric, and unable to change accepted answers.

Ambiguous, stale, unsupported, or authority-conflicted items must be withdrawn
or scored as non-penalizing. The system must not teach confidence by punishing
appropriate abstention.

## Lesson progress boundary

Lesson progress is user context governed by Phase 42J. A future progress write
requires explicit user confirmation, narrow owner scope, local-first storage,
an explicit retention choice, and deletion behavior.

Progress may record completion, attempts, score, reviewed explanations, and
user reflection. It may not become canonical evidence, a global model-training
record, a correction, a recommendation, or public judge certification.

## Corrections and version changes

An accepted Correction Ledger entry may flag affected lessons or assessments
for review. It cannot silently rewrite historical revisions or scores.

When a rules, legality, theory, or correction version changes:

```text
identify impacted items
block stale authority-sensitive items when required
create a new reviewed revision
retain historical replay identity
show the user what changed
```

## Local-first and privacy boundary

- Required lesson and assessment workflows must have a complete local path.
- No paid API, live provider, or cloud model may be required.
- Private deck examples and progress remain local unless expressly exported.
- Cloud processing is deny-by-default and requires payload-specific consent.
- Tests must use fixed offline fixtures and must not download models or sources.
- Lesson analytics must not create surveillance or cross-user profiling.

## Supplemental integration boundary

Stream Deck may later navigate to a lesson, repeat an instruction, or open an
existing assessment. It may not answer an assessment, confirm progress writes,
reveal private content, change scores, or bypass prerequisites and review gates.
The standalone Stream Deck Game Tracker remains outside Codie.

## Deterministic statuses

Future curriculum evaluation must use explicit states:

```text
READY
PARTIAL
BLOCKED_MISSING_AUTHORITY
BLOCKED_STALE_AUTHORITY
BLOCKED_RIGHTS
BLOCKED_REVIEW
UNSUPPORTED
REQUIRES_JUDGE_REVIEW
RETIRED
```

Missing information must not become an incorrect answer, zero score, or silent
lesson omission.

## Acceptance requirements

Outside validation must confirm:

1. The seven-step judge-style issue-spotting sequence is preserved.
2. Rules, evidence, theory, examples, community context, and opinion remain
   visibly distinct.
3. Theory skills require rights, attribution, version, citation,
   transferability, contradiction, and human-review gates.
4. Codie does not claim judge certification or binding tournament authority.
5. Assessment scoring handles ambiguity, staleness, and unsupported states
   without penalizing justified abstention.
6. Lesson progress remains confirmed, local user context under Phase 42J.
7. Hareruya remains tournament-only.
8. Stream Deck remains supplemental-only.
9. No runtime, persistence, schema, model, provider, UI, dependency, workflow,
   or constitution change is included.
10. Phase 42L remains blocked pending outside acceptance.

## Explicit non-authorization

This phase does not authorize production code, tests for new behavior, lesson
content, assessments, schemas, repositories, progress persistence, models,
prompts, provider access, rules-engine expansion, simulation, UI, CLI, API,
exports, Stream Deck implementation, dependencies, workflows, or changes to a
constitution.
