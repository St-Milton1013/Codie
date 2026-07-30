# Outside Validation - Phase 42D Local-First Model Profile, Redaction, Consent, and Routing

Validate Phase 42D from a clean checkout of the exact submitted commit.

## Required Review Files

```text
docs/CODIE_V2_CONSTITUTION.md
docs/ROADMAP_PATCH_V2_INTELLIGENCE_PROGRAM_INTAKE.md
docs/PHASE42A_JIN_THEORY_RULES_CORRECTIONS_CROSS_SPECIFICATION_BOUNDARY_CONTRACT.md
docs/PHASE42B_FIXED_JIN_REGRESSION_CORPUS_SCHEMA_DETERMINISTIC_EVALUATION_CONTRACT.md
docs/PHASE42C_RULES_AUTHORITY_LEGALITY_BOUNDED_INTERACTION_CONTRACT.md
docs/PHASE42D_LOCAL_FIRST_MODEL_PROFILE_REDACTION_CONSENT_ROUTING_CONTRACT.md
docs/CHECKPOINT_PHASE42D_LOCAL_FIRST_MODEL_PROFILE_REDACTION_CONSENT_ROUTING_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE42D_LOCAL_FIRST_MODEL_PROFILE_REDACTION_CONSENT_ROUTING_PROMPT.md
docs/design_inputs/v2_intelligence_program/CODIE_V2_MODEL_PROFILE_PROPOSAL.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

Treat the constitution and accepted contracts as governing authority. Treat
the model-profile proposal as preserved design input only.

## Confirm Scope

Confirm Phase 42D:

```text
is contract-only
records Phase 42C artifact-backed acceptance
defines Phase42D / outside-validation / INTERMEDIATE_PACKET
defines Phase42E / outside-validation / INTERMEDIATE_PACKET as next
keeps Phase 42E blocked
changes no active validation scope in the PR
```

Reject if this phase adds production code, tests, fixtures, schema,
repositories, providers, dependencies, workflows, prompts, models, network
calls, credentials, consent persistence, redaction runtime, audit storage,
Jin output, recommendations, simulator behavior, UI, CLI, file writing, or
constitution changes.

## Confirm Privacy And Local-First Decisions

Confirm the contract:

```text
makes local_strict the default logical profile
requires offline_deterministic fallback
keeps cloud disabled and deny-by-default
admits no cloud provider in Phase 42D
forbids paid-model dependency for core workflows
defines D0 through D12 and strictest-class handling
forbids D10 secrets to every model target
denies D4 restricted theory to cloud
denies private classes by default
does not treat redaction as automatic declassification
limits initial private cloud consent to a request or immutable snapshot
does not admit full_private_context initially
requires deterministic redaction before adapter invocation
requires exact preview identity for transmitted content
blocks on consent, rights, redaction, secret, or preview failure
forbids silent local-to-cloud fallback
```

## Confirm Routing And Output Boundaries

Confirm:

```text
eligibility is evaluated before route scoring
an ineligible target cannot be rescued by score
retries cannot add data classes or detail
paid targets are ineligible under zero-cost policy
profile, consent, rights, provider policy, capability, and runtime are gates
provider aliases are not claimed as exactly reproducible
model output remains untrusted
model output cannot mutate protected records
Rules, legality, evidence, citation, contradiction, and schema gates remain downstream
metadata_only is the default logging mode
audit metadata preserves replay identity without storing forbidden content
```

## Confirm Deferred Decisions

Confirm exact local runtimes, model files, quantization tiers, cloud providers,
provider SDKs, retention adapters, encrypted storage, and benchmarking
thresholds remain deferred without weakening the restrictive defaults.

## Run

```text
git diff --check
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe scripts/check_schema.py
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest discover -s tests -v
```

Inspect the submitted diff for undeclared changes. Tests must not require
network access or paid credentials.

## Verdict

Return one:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

List findings by severity, affected file, governing rule, and required
correction. Phase 42E remains blocked unless the verdict is PASS or PASS WITH
REVIEW NOTES.
