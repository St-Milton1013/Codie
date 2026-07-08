# ADR-005: Evidence Fusion Before Decision Intelligence

Status: accepted

## Context

Codie has multiple evidence-producing systems: canonical tournament records, analytics metrics, source agreement, conflicts, simulator outputs, user context, and primer metadata/context.

## Decision

Decision Intelligence consumes unified Evidence Fusion objects. It must not reason directly from raw providers, source tables, provider payloads, primer bodies, or simulator traces.

## Consequences

- Evidence Fusion creates deterministic, provenance-rich evidence packets.
- Decision Intelligence owns reasoning and recommendation conclusions.
- Other subsystems should not duplicate recommendation reasoning.

## Validation

Recommendation and Decision Intelligence boundary tests must block direct access to raw provider/source layers and private evidence inputs.
