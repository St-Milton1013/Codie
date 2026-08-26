# Phase50B Local Working Iteration v0.1 Usability Override

Status: owner-approved implementation amendment; exact-SHA validation required

Date approved: 2026-08-25

## Authority and purpose

The project owner authorized Codie to fetch a URL and to override the Phase50A
local-file-only product restrictions needed to correct two observed failures:

1. A user could reach the interface without usable card data and then see the
   whole deck reported as unrecognizable.
2. The accepted workflow did not honor the established requirement to accept a
   public Moxfield deck link.

This document is the required separate amendment anticipated by the Phase50A
contract. It supersedes only the conflicting local-file-only and no-provider-
fetch clauses for the two capabilities below. Every other Phase50A boundary and
all higher constitutional, evidence, validation, and human-authority gates
remain controlling.

## Authorized capability 1: prepare card data

After the user presses **Prepare Codie** or **Refresh card data**, the loopback
service may:

- read the official Scryfall bulk-data metadata endpoint;
- download the official `oracle_cards` snapshot, including its current
  compressed JSON Lines format, from a trusted Scryfall HTTPS host;
- enforce a bounded response size, stream through a temporary file, hash the
  complete snapshot, and atomically replace the contained cache;
- reuse that cache without another download until the user requests a refresh;
- validate all card rows before transaction-bounded import; and
- report and skip only structurally valid records whose normalized names are
  empty and therefore cannot participate in safe name matching;
- label the result only as `card_truth`.

The page may not fetch card data on load. No background, scheduled, telemetry,
account, API-key, or paid service behavior is authorized. Card truth may not be
promoted to tournament evidence, Theory, Rules, Corrections, or strategic
advice. The existing explicit local JSON route remains available for fixtures
and recovery but is not part of the normal user interface.

## Authorized capability 2: public Moxfield link import

After the user presses **Import and remember deck**, the loopback service may:

- recognize a public `moxfield.com/decks/<public-id>` URL;
- request that public deck through the existing rate-limited Moxfield client;
- try only the approved public-deck endpoints;
- convert recognized Commander, mainboard, sideboard, and maybeboard card rows
  into the existing deck-import input;
- preserve the canonical public deck URL as source attribution; and
- use the existing atomic lookup and persistence path.

No Moxfield account, authentication material, private deck access, cookies,
primer ingestion, ranking, recommendation, or tournament-evidence promotion is
authorized. Rate limits, network failures, private/unavailable decks, and schema
drift must return a safe message that offers pasted deck text as the fallback.
No partial deck or analysis session may survive a failed import.

## Preserved hard boundaries

```text
loopback-only application and same-origin API
contained local cache, database, and exports
no page-load or hidden remote work
zero-cost runtime and no required account
hard evidence-class separation
Hareruya tournament-only scope
Theory/theory-skill review gates unchanged
Rules and Corrections authority unchanged
supplemental-only Stream Deck support; integration absent
Goal Engine authority and approved Phase44-49 roadmap unchanged
human validation, merge, release, and promotion gates unchanged
```

## Required acceptance evidence

The promotion candidate must prove:

- missing card data produces a preparation instruction, not a deck-wide
  unresolved-name dump;
- official records with no safely matchable normalized name are counted and
  warned instead of blocking every usable card record;
- preparation requires an explicit user action and produces a contained,
  bounded, hashed, integrity-checked, atomic, reusable cache;
- only trusted Scryfall download hosts are accepted;
- a public Moxfield link imports through fixture-injected tests and preserves
  source attribution;
- missing network consent, rate limits, unavailable/private decks, schema
  drift, untrusted sources, and oversized downloads fail closed;
- pasted decklists and explicit local catalog import remain compatible;
- page load performs no provider fetch or mutation; and
- the full repository validator set remains clean relative to the accepted
  baseline.

Promotion still requires an exact-SHA validation result and human merge.
