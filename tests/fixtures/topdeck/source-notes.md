# TopDeck Fixture Notes

Date recorded: 2026-06-21

Most fixtures are local contract samples for TopDeck event/deck parsing, failure behavior, and client transport tests.

`live_structured_deck_event.json` was captured from the live TopDeck API using a free API key and sanitized down to one structured deck plus hidden standings. It preserves a real `deckObj` shape with `Commanders`, `Mainboard`, and `metadata` keys so parser tests prove real card rows are parsed and metadata is not converted into cards.

Tests must not make live network calls. Refresh this fixture manually when TopDeck changes its exposed structured deck shape.
