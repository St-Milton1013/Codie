# Phase51K Structured Concrete-Defect Disposition Contract

Status: design contract only

## Validation Tuple

```text
phase_id: Phase51K
phase_part: design-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase51L
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase51K replaces the held Phase51J post-hoc free-text classifier design; it
does not accept or modify Phase51J. Independent adversarial probes against
the local-only Phase51J heads proved that phrase and regex matching can
suppress realistic concrete findings outside any reviewed vocabulary. That
cannot meet Phase51I's requirement that a named concrete deficiency remain
blocking.

The future Phase51L implementation must obtain a structured disposition from
the architecture validator for every finding. The gate must make suppression
decisions from that disposition and trusted deterministic evidence, never by
searching the finding prose for security vocabulary. The raw model finding and
its structured disposition remain auditable evidence; neither grants merge,
repair, product, or human-decision authority.

## Authorized Phase51L Boundary

```text
codie/validation/local_gate.py
tests/test_validation_local_gate.py
docs/PHASE51L_STRUCTURED_CONCRETE_DEFECT_DISPOSITION_IMPLEMENTATION_REPORT.md
```

Only the validation-gate prompt, model-response parsing/validation, immutable
suppressed-finding audit representation, and focused tests may change inside
that boundary. No product, database, provider, model selection, severity,
aggregation, repair policy, workflow, UI, CLI, source registry, scope
authority, or Phase44U file change is authorized.

## Required Structured Disposition

For each architecture-model finding, the future validator response must carry
all of the following fields in addition to the existing finding fields:

```text
claim_kind: generic_validation_absence | concrete_defect | ambiguous
concrete_defect_categories: zero or more category tokens
specific_defect_summary: string or null
```

`generic_validation_absence` is valid only when the finding asserts solely a
generic lack of validation and identifies no behavior, test, assertion,
coverage area, vulnerability, threat, attack, security property, data issue,
authentication, authorization, access-control failure, artifact, policy,
scope, source, human decision, outside review, or other specific deficiency.

`concrete_defect` is mandatory whenever any specific deficiency is named.
`ambiguous` is mandatory whenever the model cannot determine the distinction.
An omitted field, unknown value, malformed category list, contradictory
combination, or unsupported validator response is fail-closed and remains an
open finding. The implementation must not infer a disposition by keyword,
phrase, stem, regex, or natural-language reclassification after parsing.

## Suppression Rule

The gate may audit-preservingly suppress a finding only when every condition
below is true:

```text
validator is architecture
exactly one affected changed production module is named
one or more changed tests directly import that module
deterministic full suite is CLEAN_PASS
claim_kind is exactly generic_validation_absence
concrete_defect_categories is empty
specific_defect_summary is null
the finding contains no mixed or uncertain claim
```

All other findings remain blocking. In particular, `concrete_defect`,
`ambiguous`, malformed, missing, mixed, multi-module, non-architecture, or
insufficient-evidence findings may not be suppressed. Each suppression must
retain the canonical hash, original finding text, exact structured disposition,
direct-test evidence, deterministic result, and machine-readable suppression
reason in the immutable audit record.

## Required Tests

Phase51L must prove all of the following without consulting finding prose for
the disposition decision:

- the exact Phase44U generic correctness/security wording suppresses and is
  audited only when every trusted condition and an explicit generic disposition
  are present;
- representative concrete defects, including data exfiltration, object-level
  authorization failure, session hijacking, open redirect, unencrypted secret
  storage, behavior, test, assertion, coverage, architecture, scope, source,
  policy, artifact, human decision, and outside review remain blocking when
  structured as concrete;
- ambiguous, absent, malformed, contradictory, and unknown dispositions remain
  blocking;
- non-architecture validator output, missing direct import, non-clean
  deterministic result, and multi-module findings remain blocking;
- the original text and structured disposition survive in the immutable audit
  record; and
- existing Phase51E/H tests remain intact, schema bootstrap passes, and the
  full suite passes.

## Hard Boundaries And Gate

This contract does not accept the held Phase51J implementation, alter Phase44U
PR #105, rerun validation, or authorize a merge. Theory/theory-skill,
Scryfall, Moxfield, Hareruya tournament-only, supplemental-only Stream Deck,
local-first/zero-cost, evidence, and human-authority boundaries remain
unchanged. Phase51L and any Phase44U rerun remain blocked until this exact
contract is independently artifact-validated and human-merged.
