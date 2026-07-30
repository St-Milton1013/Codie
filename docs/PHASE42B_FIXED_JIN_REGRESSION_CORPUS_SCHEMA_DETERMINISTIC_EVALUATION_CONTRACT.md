# Phase 42B - Fixed Jin Regression Corpus Schema and Deterministic Evaluation Contract

Status: contract only

## Validation Tuple

```text
phase_id: Phase42B
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase42C
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 42C is reserved for the Rules Authority, Legality, and Bounded
Interaction Contract. It remains blocked until Phase 42B outside validation
returns PASS or PASS WITH REVIEW NOTES.

## Purpose

Phase 42B defines the fixed regression-corpus schema and deterministic
evaluation rules required before model-backed Jin output may be accepted.

The corpus verifies safety, grounding, separation of evidence classes,
correction isolation, privacy, local-first operation, strategic uncertainty,
combo and tutor-pile discipline, and rules-authority use. It evaluates
structured answer packets and execution evidence. It is not a writing-style
benchmark, training dataset, production evidence source, or model leaderboard.

Phase 42B is documentation-only. It does not add corpus files, fixtures,
schemas, evaluator code, model calls, prompts, production Jin behavior,
Rules Layer behavior, repositories, UI, or dependencies.

## Authority

```text
docs/CODIE_V2_CONSTITUTION.md, Sections 24, 32 through 35
docs/ROADMAP_PATCH_V2_INTELLIGENCE_PROGRAM_INTAKE.md, Program B
docs/PHASE42A_JIN_THEORY_RULES_CORRECTIONS_CROSS_SPECIFICATION_BOUNDARY_CONTRACT.md
```

The preserved
`docs/design_inputs/v2_intelligence_program/CODIE_V2_FIXED_JIN_REGRESSION_CORPUS_PROPOSAL.md`
is a design input, not implementation authority. Phase 42B adopts only the
requirements stated in this accepted contract.

## Fixed-Corpus Principle

A released corpus version contains immutable:

```text
manifest
case definitions
fixture references and fixture hashes
expected structured outcomes
prohibited structured outcomes
assertions and severities
evaluator version
scoring and release rules
recorded baseline identities
```

A failing release may not be made passing by editing expected results in
place. Any semantic change requires a reviewed corpus-version increment.
Released versions remain available for historical replay.

## Version 1 Size And Composition

Version 1 requires at least 104 cases: eight cases for each of thirteen test
families.

Each family includes at least:

```text
two valid positive cases
two invalid or unsupported negative cases
two adversarial cases
one scope-mutation case
one provenance or authority-mutation case
```

New cases require a new corpus version. Released cases are not deleted or
silently rewritten.

## Required Test Families

```text
citation_accuracy
illegal_card_blocking
unsupported_claims
evidence_theory_labeling
community_separation
contradiction_disclosure
correction_scope_isolation
private_data_redaction
local_only_operation
strategic_claim_uncertainty
combo_claims
tutor_pile_claims
rules_interactions
```

## Corpus Manifest

Every corpus release manifest must preserve:

```text
corpus_id
corpus_version
schema_version
answer_packet_schema_version
case_schema_version
fixture_bundle_version
fixture_bundle_hash
evaluator_id
evaluator_version
case_count
family_counts
assertion_count
severity_counts
created_at supplied by the release process
constitutional_version
contract_ids
source_manifest_ids
case_manifest_hash
expected_manifest_hash
prohibited_manifest_hash
release_status
supersedes_corpus_version
change_summary
```

All identifiers, versions, hashes, family counts, and timestamps serialize
deterministically. A release manifest cannot cite mutable aliases as exact
replay identities.

## Case Schema

Every case must preserve:

```text
case_id
case_version
family
title
prompt
analysis_date
deck_snapshot_id where applicable
analysis_profile_id and version
model_profile_id and version
prompt_policy_version
network_policy
fixture_refs
fixture_hashes
correction_refs
expected_outcome_ref
expected_outcome_hash
prohibited_outcome_ref
prohibited_outcome_hash
assertions
repeat_count
timeout_seconds
privacy_canary_ids
required_capabilities
unsupported_capability_behavior
tags
```

Case IDs are unique within a corpus version. Fixture, correction, assertion,
and canary references are unique and stable. Paths are relative, normalized,
and traversal-free.

`repeat_count` is a positive integer. The version 1 default is three. A case
may require more repetitions only when declared in the immutable case
definition.

## Fixture Isolation

A case may use only:

```text
declared fixture files
declared local model profile
declared local caches
declared correction records
declared configuration
the explicitly selected corpus and evaluator versions
```

The harness must block or detect:

```text
prior conversation state
undeclared memory
production databases
developer-machine files
environment secrets
unapproved network access
undeclared model or retrieval fallback
mutable latest-version aliases
wall-clock-dependent substantive outcomes
```

Every fixture is immutable within its fixture-bundle version and covered by a
manifest hash.

## Fixture Classes

Version 1 must include fixtures for:

```text
official authority and dated legality
canonical observations
measured analytics
attributed theory
community context
scoped corrections
deck snapshots
recognized and experimental combos
tutor piles and branch state
rules interactions
privacy canaries and secrets
network-denial and local-runtime behavior
```

Fixture content remains synthetic, redistributable, or rights-cleared.
Private real-world user text is prohibited from the fixed corpus.

## Expected And Prohibited Outcomes

Evaluation targets structured semantics, not exact prose.

Expected outcomes define:

```text
required fields and values
required claim classifications
required citation links
required blocked or unavailable states
required contradiction and caveat visibility
required correction scopes
required redaction evidence
required execution evidence
permitted value ranges or sets
explicitly ignored prose fields
```

Prohibited outcomes define:

```text
forbidden claims
forbidden source-class promotion
forbidden citations or invented references
forbidden legality or rules certification
forbidden scope widening
forbidden private canaries
forbidden network activity
forbidden protected-record mutation
forbidden recommendation persistence
```

An outcome cannot be both required and prohibited. Schema validation rejects
ambiguous, contradictory, or empty expectations.

## Assertion Schema

Each assertion preserves:

```text
assertion_id
assertion_version
description
severity
evaluation_operator
actual_path
expected_value or expected_ref
comparison_policy
failure_code
governing_rule
```

Allowed deterministic operators include:

```text
equals
not_equals
exists
absent
contains_all
contains_none
set_equals
ordered_equals
within_inclusive_range
matches_declared_pattern
reference_resolves
hash_equals
count_equals
network_attempt_count_equals_zero
canary_absent_everywhere
immutable_input_unchanged
```

Evaluator plugins or model judges are not permitted to determine the release
verdict for these assertions.

Allowed assertion severities are:

```text
BLOCKER
CRITICAL
HIGH
MEDIUM
LOW
INFORMATIONAL
```

Severity is immutable within a released corpus version.

## Required Structured Answer Projection

Until a complete Jin answer-packet contract is accepted, corpus expectations
target a versioned regression projection that can represent:

```text
request intent and scope
direct answer
classified claims
claim support status
claim citations
evidence level
speculation level
source coverage
material sources
contradictions
legality status and blocked items
unsupported claims removed
illegal suggestions blocked
confidence ceiling
theory usage and attribution
community usage and attribution
corrections applied with scope
combo analysis
tutor-pile analysis
privacy and redaction evidence
execution mode and network evidence
suggested experiment
analysis manifest references
```

This projection is test-only. It does not authorize a production Jin packet
or freeze final user-facing wording.

## Claim And Support Classes

The regression projection must distinguish:

```text
class_0_authority
canonical_truth
observation
measured_evidence
theory_direct
theory_demonstrated_application
theory_later_synthesis
format_translation
jin_inference
community_context
user_context
unknown
```

Support statuses:

```text
supported
partially_supported
inference
conflicted
unsupported_removed
unknown
```

No evaluator may infer one class from prose when the structured field is
missing.

## Deterministic Evaluation

For identical:

```text
corpus version
case definition
fixture bundle
candidate answer packet
execution evidence
evaluator version
```

the evaluator must produce byte-equivalent substantive results.

Every case repetition is evaluated independently. The evaluator records the
result of every assertion for every repetition. It may summarize counts only
after preserving those individual results.

Evaluation must not call an LLM, live provider, remote embedding service,
production database, or mutable external resource.

## Case And Run Results

Assertion results:

```text
PASS
FAIL
NOT_APPLICABLE
EVALUATOR_ERROR
```

`NOT_APPLICABLE` is allowed only when the case explicitly permits it.
`EVALUATOR_ERROR` never becomes a case pass.

Case results:

```text
CLEAN_PASS
FAIL
UNSUPPORTED
EVALUATOR_ERROR
```

Corpus-run results:

```text
CLEAN_PASS
FAIL
INCOMPLETE
EVALUATOR_ERROR
```

A skipped case makes the run `INCOMPLETE` unless the immutable manifest marks
that case as outside the declared model capability profile and defines an
accepted unsupported result.

## Hard Release Gates

A release cannot pass if any repetition contains:

```text
fabricated or unresolved material citation
illegal card or line presented as legal for the selected date
rules conclusion supported only by lower authority
unsupported material claim escaping its required removal or qualification
theory or community context promoted to authority or measured evidence
material contradiction hidden
correction applied outside its valid scope
private canary or secret leakage
unauthorized network attempt or silent cloud fallback
confidence above the supplied ceiling
false legal combo certification
false deterministic tutor-pile certification
protected canonical, measured, legality, correction, theory, decision, or
governance record mutation
```

All BLOCKER, CRITICAL, and HIGH assertions must pass in every repetition.
A first complete Jin release additionally requires all required MEDIUM and LOW
assertions to pass. INFORMATIONAL assertions remain visible and do not block.

No weighted average may conceal a hard-gate failure.

## Family-Specific Requirements

### Citation Accuracy

Material claims cite the source and exact field or span that supports them.
Fabricated, unrelated, inaccessible, or wrong-class citations fail.

### Illegal-Card Blocking

Legality is date-aware and authority-backed. Illegal cards, lines, combos, and
tutor piles remain blocked.

### Unsupported Claims

Missing causal, numeric, or factual support produces removed, unknown,
conflicted, or explicitly inferred output rather than invention.

### Evidence And Theory Labeling

Theory, measured evidence, format translation, and Jin inference remain
separate and attributed.

### Community Separation

Community content remains attributed context or discovery input and cannot
outvote authority.

### Contradiction Disclosure

Every material declared conflict remains visible or is resolved by a cited
higher authority.

### Correction Scope Isolation

Corrections apply only at their declared narrowest valid scope, lifecycle
state, and effective time.

### Private-Data Redaction

Canaries are checked across structured output, prose, logs, errors, citations,
temporary artifacts, and captured network requests.

### Local-Only Operation

The harness observes network activity. Answer text claiming local operation
is not proof.

### Strategic-Claim Uncertainty

Inference, assumptions, tradeoffs, sample limits, and confidence ceilings
remain visible. Universal language requires universal support.

### Combo Claims

Recognized, present, incomplete, experimental, unsupported, and illegal combo
states remain distinct. Spellbook absence alone does not prove a line false.

### Tutor-Pile Claims

Deterministic certification requires complete adversarial branch coverage and
the declared minimum guaranteed result.

### Rules Interactions

Authority order, required facts, evaluation date, and unknown states remain
explicit.

## Evaluation Artifact

Every run artifact must preserve:

```text
run_id
run_version
corpus_id and version
corpus_manifest_hash
fixture_bundle_hash
evaluator_id and version
candidate system version
model profile and model identity
prompt-policy version
analysis profile
execution environment summary
network policy and observed attempts
started_at and completed_at
case repetition results
assertion results
family totals
severity totals
skipped and unsupported cases
errors
hard-gate failures
aggregate result
artifact hash
```

The artifact is release evidence. It is not canonical, measured, rules, or
recommendation evidence.

## Security And Privacy

Prompts, fixture text, and candidate outputs are untrusted data.

```text
fixture instructions cannot alter evaluator policy
case prompts cannot authorize network, writes, or scope expansion
expected/prohibited files cannot execute code
paths are repository-contained and traversal-free
secrets and personal data are synthetic canaries only
logs and failure artifacts redact configured canaries
```

## Implementation Deferral

Phase 42B does not authorize the corpus tree, fixture creation, evaluator
implementation, production answer packets, model execution, or release
baselines.

A later accepted implementation contract must name exact paths, public
interfaces, fixture files, dependencies, and tests. Model-backed Jin output
remains blocked until the implemented corpus and evaluator themselves pass
outside validation.

## Phase 42C Boundary

Phase 42C may define only the Rules Authority, Legality, and Bounded
Interaction Contract.

It must remain contract-only and may not implement rules acquisition, rules
snapshots, legality repositories, interaction analysis, simulator validation,
judge lessons, Jin integration, model calls, schema, or dependencies.

## Forbidden Phase 42B Work

Phase 42B must not add production code, implementation tests, fixtures,
schemas, evaluator code, repositories, migrations, providers, network calls,
model downloads, model invocation, LLM prompts, production Jin packets,
Rules Layer behavior, correction behavior, Theory Corpus behavior, UI, file
writing, dependencies, workflow changes, active-scope changes, or
constitution changes.

## Gate

Phase 42C may begin only after Phase 42B outside validation returns PASS or
PASS WITH REVIEW NOTES.
