# Hareruya Fixture Notes

Date recorded: 2026-06-21

These fixtures are local contract samples for the Hareruya adapter. They cover metagame/event metadata, regional defaults, deck metadata, explicit commander metadata, Commander-confirmed fallback commander handling, Japanese/raw card names, missing optional fields, missing required identities, unavailable decklists, malformed HTML, and raw HTML preservation.

`live_metagame_page_7.html` is a sanitized fixture based on the live Commander metagame page at `https://www.hareruyamtg.com/en/deck/7/metagame/`. It preserves the current `common-headline--deckSearch` and `deckSearch-metaList__list__item` structure without storing the full page.

`live_deck_page_100000.html` is a sanitized fixture based on the live deck page at `https://www.hareruyamtg.com/en/deck/100000/show/`. It preserves the current `deckSearch-deckList__information__flex__list` metadata structure and `deckSearch-deckList__deckList__container__text` card sections without storing the full page.

Live `deck/result` pages may return an AWS WAF `202` challenge for basic clients. The Hareruya client maps that response to a retryable `RateLimitError`.
