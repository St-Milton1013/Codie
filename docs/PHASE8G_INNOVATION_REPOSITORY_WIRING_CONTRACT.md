# Phase 8G - Innovation Repository Wiring Contract

Date: 2026-06-22

## Objective

Wire analytics innovation detection to canonical repository reads without creating persistence, recommendations, or schema.

## Implemented Surface

- `AnalyticsRepository.list_innovation_observation_rows(...)`
- `innovation_observations_from_rows(...)`
- `detect_innovations_from_repository(...)`

## Data Boundary

The repository method reads only canonical tournament/deck/card records and card metadata:

- `canonical_events`
- `canonical_decks`
- `canonical_deck_cards`
- `event_deck_entries`
- `cards`
- `canonical_event_sources`
- `canonical_deck_sources`

It does not read source tables, provider objects, provider payload fields, primer text, recommendation runs, or recommendation candidates.

## Behavior

Repository rows include canonical event/deck identity, source event/deck identity when available, event date, commander signature, region/country, placement, top cut, winner, player count, card identity, card display metadata, and `cards.released_at`.

The mapper converts those rows into `InnovationObservation` records. Source deck/event IDs are emitted as stable strings when present, with canonical ID strings as fallback evidence identities.

The orchestration helper computes the repository read window from `InnovationFilter`, maps rows, and calls `detect_innovations` in memory.

## Non-Goals

- No innovation tables.
- No snapshot persistence.
- No recommendation candidate generation.
- No recommendation runs.
- No strategic recommendation wording.
