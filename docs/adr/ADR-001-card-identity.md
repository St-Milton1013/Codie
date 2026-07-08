# ADR-001: Card Identity

Status: accepted

## Context

Codie stores individual card print/card-object records and also needs analytics grouped across prints and faces.

## Decision

`scryfall_id` is the enforced card identity for persisted card references.

`oracle_id` is an analytics grouping key and is not treated as a unique enforced card identity.

## Consequences

- Source and canonical deck card records should resolve to `scryfall_id`.
- Analytics may group by `oracle_id`.
- Schema should not add a unique foreign key from `oracle_id` to `cards(oracle_id)`.

## Validation

Schema, repository, canonicalization, and analytics tests must preserve this distinction.
