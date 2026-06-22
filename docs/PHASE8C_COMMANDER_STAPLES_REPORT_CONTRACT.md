# Phase 8C Commander Staples Report Contract

## Objective

Create a reproducible commander staples report foundation from canonical tournament observations.

Phase 8C does not generate recommendations. It produces evidence rows showing which cards appear in matching canonical decks, with frequency, weighted usage, finish/date summaries, and source breakdowns.

## Files Created

- `codie/recommendations/staples.py`
- `tests/test_commander_staples_report.py`
- `docs/PHASE8C_COMMANDER_STAPLES_REPORT_CONTRACT.md`

## Files Modified

- `codie/recommendations/__init__.py`

## Schema Impact

None.

Phase 8C must not write:

- `recommendation_runs`
- `recommendation_candidates`
- canonical records
- source records

## Public API

```python
class StapleObservation: ...
class StapleReportRow: ...
class CommanderStaplesReport: ...

def build_commander_staples_report(...) -> CommanderStaplesReport: ...
```

## Input Contract

Inputs are already-selected canonical tournament observations.

The report layer does not query:

- provider payloads
- source tables
- raw scraper output
- primer text

## Required Output Fields

Each row includes:

- card name
- Scryfall ID
- Oracle ID
- card type line
- color identity
- number of matching decks using the card
- total matching decks
- inclusion percentage
- total copies observed
- average copies per deck
- placement-weighted usage
- best finish observed
- top 16 count
- winner count
- most recent appearance date
- first appearance date in selected window
- source deck links
- source event links
- provider breakdown
- region breakdown

Color identity values are normalized to WUBRG order.

## Sorting

Default sort:

1. matching deck count descending
2. placement-weighted usage descending
3. Oracle ID ascending

## Failure Modes

- Missing commander signature raises `ValueError`.
- Missing deck ID, Oracle ID, or card name raises `ValueError`.
- Non-positive quantity raises `ValueError`.
- Negative entry weight raises `ValueError`.
- `total_matching_decks` cannot be smaller than observed deck count.

## Do Not Do

- Do not generate recommendation candidates.
- Do not rank by subjective strategic value.
- Do not use provider/source records directly.
- Do not persist report rows.
- Do not create strategic advice.
