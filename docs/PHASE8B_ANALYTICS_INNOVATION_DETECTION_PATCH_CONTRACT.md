# Phase 8B Analytics Innovation Detection Patch Contract

## Objective

Detect cards that are newly appearing, suddenly reappearing, or spiking in high-performing tournament evidence.

This is an analytics evidence feature, not a recommendation or strategic-claim feature. It must not tell a user what to play.

## Files Created

- `codie/analytics/innovation/__init__.py`
- `codie/analytics/innovation/innovation_detector.py`
- `codie/analytics/innovation/innovation_filters.py`
- `codie/analytics/innovation/innovation_models.py`
- `tests/test_analytics_innovation_detection.py`
- `docs/PHASE8B_ANALYTICS_INNOVATION_DETECTION_PATCH_CONTRACT.md`

## Files Modified

- `codie/analytics/__init__.py`

## Schema Impact

None.

The innovation layer currently returns in-memory `InnovationSignal` records. Persistence would require a separate schema/repository phase.

## Placement

This layer belongs after card performance metrics and before full recommendation candidate generation.

It allows Codie to distinguish:

- generic staple
- commander staple
- performance signal
- new innovation
- regional innovation
- old-card resurgence
- new-release adoption

## Public API

```python
class InnovationObservation: ...
class InnovationSignal: ...
class InnovationFilter: ...

def detect_innovations(observations, filters, *, generated_at: str) -> tuple[InnovationSignal, ...]: ...
def innovation_evidence_line(signal: InnovationSignal) -> str: ...
```

## Signal Types

- `new_innovation`
- `recent_breakout`
- `old_card_resurgence`
- `new_release_adoption`
- `commander_specific_innovation`
- `regional_innovation`

## Default Window

- recent window: `30d`
- default baseline window: `180d`

Supported baseline windows:

- `90d`
- `180d`
- `365d`
- `all_time`

## Required Output Fields

Each `InnovationSignal` includes:

- `innovation_id`
- `oracle_id`
- `scryfall_id`
- `commander_signature`
- `region_code`
- `innovation_type`
- `recent_window`
- `baseline_window`
- `recent_inclusion_rate`
- `baseline_inclusion_rate`
- `usage_delta`
- `recent_topcut_count`
- `recent_winner_count`
- `first_recent_seen_at`
- `last_seen_before_recent_window`
- `card_released_at`
- `is_new_release`
- `sample_size`
- `confidence_score`
- `source_event_ids_json`
- `source_deck_ids_json`
- `generated_at`

## Required Filters

- commander / partner pair
- card type
- color identity
- region
- time window
- minimum event size
- minimum placement
- include/exclude newly released cards
- include/exclude old-card resurgences
- minimum sample size

## Evidence First Rules

Allowed wording:

```text
Card appeared in 2 top-16 Tymna/Kraum decks in the last 30 days after 0 appearances in the prior 180 days.
Card usage rose from 1.2% to 8.7% in the selected window.
Card was released on X and appeared in Y tournament decks within 30 days.
Card has regional adoption in Japan before broader global adoption.
```

Forbidden wording:

```text
This card is the new tech.
This card is correct.
This card breaks the format.
This card is secretly optimal.
You should play this card.
```

## Dependencies

Allowed source data:

- `canonical_decks`
- `canonical_deck_cards`
- `event_deck_entries`
- `canonical_events`
- `cards.released_at`
- `card_performance_metrics`
- `historical_card_metrics`
- `regional_card_metrics`

The current implementation consumes normalized `InnovationObservation` records so repository wiring can remain a separate explicit step.

## Do Not Do

- Do not generate recommendation candidates.
- Do not persist innovation rows.
- Do not create strategic claims.
- Do not read provider payloads.
- Do not use source tables directly in the analytics detector.
