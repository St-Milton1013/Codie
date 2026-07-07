# Local Report Delivery Specification

Status: roadmap/specification, implementation deferred

## Purpose

Add local report sending after Codie generates export files.

LocalSend is the preferred reference for local delivery research.

## Supported Outputs

```text
deck report
commander staples report
frequency pool
simulation report
evidence graph export
Obsidian markdown bundle
CSV export
PDF-ready report
```

## Implementation Rule

```text
1. Generate file locally.
2. Save to Codie exports folder.
3. Offer LocalSend delivery to detected device.
4. Log delivery success/failure.
```

Report generation must not depend on LocalSend.

## References

```text
localsend/localsend
localsend/protocol
```

The protocol repository is the most important reference because Codie needs a
stable delivery contract.

## Future Tables

Potential future tables:

```text
export_jobs
localsend_delivery_logs
```

These are not approved schema.

## Acceptance Tests

```text
generates report before delivery
detects delivery failure
logs delivery result
does not delete local report after sending
works without LocalSend installed by preserving export file
```
