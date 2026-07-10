# Local Alpha Known Caveats

Status: local alpha caveat list

## Provider Access

```text
Hareruya live access can encounter AWS WAF.
Hareruya remains regional enrichment, not a critical-path provider.
Fixture-backed tests do not imply broad live backfill readiness.
```

## Local Database Requirements

```text
DB-backed workflows require a local Codie SQLite database.
User deck import requires card resolution through existing card lookup data.
Schema bootstrap alone does not populate all card rows.
```

## Recommendation Output

```text
Recommendation report rendering requires an already-built RecommendationOutputBundle JSON.
The report CLI does not discover, rank, score, or generate recommendations.
Recommendation output remains packet/report focused in the alpha surface.
```

## Simulator

```text
Phase 13 simulator baseline exists.
SIM-R full rules simulator revision is deferred.
Simulator output remains simulator evidence, not tournament evidence.
Unsupported-card behavior must remain visible in simulator-related outputs.
```

## UI And Sharing

```text
Minimal local/static report surfaces exist.
Final UI is not complete.
Mobile delivery integrations remain optional and contract-gated.
Local LAN serving is opt-in and should stay local by default.
```

## Roadmap Patches

These are not alpha features until separately contracted:

```text
SIM-R
Tag Graph Lab
Moxfield Frequency Pool Builder
Jin-Gitaxias / strategist mode
Obsidian / Knowledge Vault
advanced dashboard
mobile delivery integrations
```

## Privacy

```text
Private user deck input should not be exported by default.
Raw provider payloads are not report inputs.
Do not include secrets or API keys in alpha docs or examples.
```

