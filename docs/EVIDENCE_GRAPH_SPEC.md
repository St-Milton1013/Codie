# Evidence Graph Specification

Status: roadmap/specification, implementation deferred beyond current in-memory primitives

## Purpose

Provide explainable analytics through graph-shaped evidence data.

Codie already has in-memory evidence graph primitives. This specification
captures future expanded graph usage for UI and analytics explanation.

## Node Types

Future graph surfaces may include:

```text
card
commander
deck
package
tag
recommendation
tournament
primer
simulation_result
metric
```

## Edge Types

Future graph surfaces may include:

```text
included_in
co_occurs_with
supports
contradicts
belongs_to_package
fills_role
recommended_by
missing_from
improves_probability
appears_in_primer
```

## Use Cases

```text
explain recommendations
visualize packages
show tag relationships
show commander staples clusters
show co-occurrence relationships
show why Codie believes a card matters
```

## V1 Storage Direction

```text
SQLite tables if persistence is approved by future schema contract
JSON export for UI graph renderer
no separate graph database in V1
```

## Guardrails

```text
graph data is explanation data, not source truth
all graph claims must cite canonical or approved evidence records
no graph database is approved for V1
no persistence without schema/repository contract
```

## Acceptance Tests

```text
creates card nodes
creates recommendation nodes
creates metric nodes
creates package nodes
creates support edges
exports graph JSON
UI can render graph data
```
