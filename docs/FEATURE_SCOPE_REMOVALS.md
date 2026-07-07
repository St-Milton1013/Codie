# Feature Scope Removals

Status: roadmap governance

## Removed From Codie V1

The following are removed from active Codie V1 scope:

```text
Stream Deck Game Tracker
SpellBot live-game tracking
Convoke live-game tracking
Commander tax / life / storm / treasure live UI
real-time game-state controller
replay logger from live game buttons
```

## Reason

These features define a separate live-game companion product. They require:

```text
hardware-specific development
live game-state synchronization
real-time multiplayer logic
custom in-game UI
maintenance outside Codie's deck-analysis mission
```

## Future Reconsideration

The idea may be reconsidered only as a separate app that exports logs into
Codie. It must not compete with Codie V1 work on deck intelligence, canonical
analytics, evidence graphs, reports, simulation support, or local-first chat.

## Guardrail

No Phase may add Stream Deck or live-game tracking work unless a future roadmap
explicitly reopens it as a separate product.
