# ADR-004: Simulator Evidence Boundary

Status: accepted

## Context

Codie's simulator can produce useful probability, trace, challenge, and line-review data. Simulator output is model-derived, not tournament-observed evidence.

## Decision

Simulator output is not tournament evidence.

Simulator traces, challenge results, and reviewed lines may support training, QA, and future comparison panels, but they must not directly become tournament evidence or raw recommendation truth.

## Consequences

- Simulation results require provenance and reproducible seeds/configuration.
- User review annotations do not rewrite original simulator traces.
- Future recommendation phases may reference simulator comparisons only through contracted Decision Intelligence boundaries.

## Validation

Boundary tests must prevent simulator output from entering source/provider, canonical tournament, or measured tournament-evidence tables as if it were observational data.
