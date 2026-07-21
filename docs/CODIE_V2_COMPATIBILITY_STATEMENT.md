# Codie V2 Compatibility Statement

**Status:** Ratification compatibility record
**Date:** 2026-07-20

## Verdict

Codie V2 is architecturally compatible with completed V1 work. No accepted phase must be rolled back or rewritten merely because V2 is adopted.

## Retained foundations

V2 explicitly retains:

- canonical card, commander, deck, event, and source identity;
- source/canonical separation and repository-owned persistence;
- raw-source preservation, source lineage, and deterministic provenance;
- Scryfall, Scryfall Tagger, Commander Spellbook, and date-aware legality foundations;
- tournament ingestion, canonicalization, deduplication, historical and regional analytics;
- immutable deck snapshots and strict zone separation;
- Evidence Graph, source-conflict, unsupported-card, chat-planning, and answer-packet foundations;
- Evidence Fusion, Decision Intelligence, weight profiles, deck-health packets, reports, and safe writers;
- simulator foundations, deterministic seeds, trace review, persistence, SIM-R value objects, and regression fixtures;
- validation automation, phase gates, completion reports, and PR-only governed changes.

## Completed-phase policy

Accepted V1 phases remain accepted. V2 does not retroactively relabel roadmap-only ideas as prior implementation authority.

Where V2 introduces a stricter rule, new work must comply immediately and existing runtime behavior is reviewed only when a dedicated compatibility contract identifies a concrete conflict.

## Active Phase 37 policy

The V2 ratification track does not advance, merge, validate, or replace Phase 37 work.

Repository `main` at branch creation contains the accepted Phase 37B implementation-contract merge. Draft PR #6 contains later Phase 37C–37E work on its own branch and remains independently governed.

After Phase 37 closes through its established gates, the next roadmap packet must be checked against V2 before implementation begins.

## V1 reference policy

`docs/CODIE_V1_CONSTITUTION.md` remains unchanged and readable. It may be used to recover historical intent, terminology, original table definitions, and accepted V1 boundaries.

When V1 and V2 conflict after adoption, V2 governs. When V2 is silent, retained V1 capability intent remains useful context subject to current contracts and source policy.

## No runtime impact in the ratification change

The adoption packet introduces no production code, schema, repository, provider, database, UI, workflow, validator, simulator, model, or dependency changes.
