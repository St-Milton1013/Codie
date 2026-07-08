# ADR-002: Provider Boundaries

Status: accepted

## Context

Codie ingests data from multiple external providers. Provider code is high-risk because it can accidentally mix parsing, persistence, canonicalization, analytics, and recommendation behavior.

## Decision

Providers fetch and parse only. Providers emit candidate models only.

Provider modules must not import database, repository, ingestion, cards, analytics, canonicalization, recommendations, simulator, or UI layers.

## Consequences

- Persistence happens through ingestion/repository layers.
- Provider tests remain fixture-first and do not require live network access.
- Static boundary scans are required for provider packages.

## Validation

Architecture boundary tests and outside validation prompts must continue scanning provider modules for forbidden imports.
