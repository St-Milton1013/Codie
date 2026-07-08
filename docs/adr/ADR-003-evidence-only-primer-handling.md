# ADR-003: Evidence-Only Primer Handling

Status: accepted

## Context

Moxfield primers and deck descriptions may contain useful context, but they are subjective and often include strategy claims, sideboard-like notes, or author preference.

## Decision

Primer sync stores metadata only. Primer body text, strategy paragraphs, mulligan guides, combo explanations, and copied descriptions are not persisted.

Primer context may explain evidence in future phases, but it may not override canonical truth or measured evidence.

## Consequences

- Primer text is not used as tournament evidence.
- Primer metadata can support provenance, discovery, and future context extraction.
- Any future primer-context feature requires a contract and must preserve evidence-only rules.

## Validation

Tests and static scans must reject private/full-text primer fields in persisted or exported objects.
