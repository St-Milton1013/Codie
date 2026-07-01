# Phase 14C - Simulation Review Export Usage Documentation Contract

## Objective

Document the local workflow for simulator review export bundles.

This phase adds documentation only. It does not add code, schema, CLI commands,
UI, simulator behavior, DB access, provider access, or recommendation output.

## Scope

Allowed files:

- `docs/USER_GUIDE_SIMULATION_REVIEW_EXPORTS.md`
- `docs/PHASE14C_SIMULATION_REVIEW_EXPORT_USAGE_DOCUMENTATION_CONTRACT.md`
- `docs/PHASE14C_SIMULATION_REVIEW_EXPORT_USAGE_DOCUMENTATION_REPORT.md`
- `docs/NEXT_PHASE_CONTRACT.md`
- `docs/CODEX_CONTINUITY_HANDOFF.md`

## Required Documentation

The guide must explain how to:

- choose the project checkout
- use the bundled Python runtime
- create an output folder
- build a `SimulationReviewExportBundle` from existing Python objects
- write the bundle JSON to a local file
- run `python -m codie.cli.simulation_review export-review-bundle`
- inspect `manifest.json`
- inspect reviewed accuracy summary files
- inspect line review fixture files
- optionally pass generated files into existing local share-bundle workflows
- avoid treating simulator output as tournament evidence

## Required Guardrails

The documentation must state:

- simulator review exports are QA/training artifacts
- review exports do not generate recommendations
- review exports do not prove tournament performance
- unsupported cards must remain visible
- private deck or trace files should not be uploaded unless the user explicitly chooses to share them
- cEDHData reference material remains reference-only

## Schema Impact

None.

## Test Impact

No tests required because this is documentation only.

## Validation

Required checks:

```text
git diff --check
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|you should" docs\USER_GUIDE_SIMULATION_REVIEW_EXPORTS.md
```

The strategic-language scan must return no matches.

## Do Not Do

- do not add code
- do not add schema
- do not query DB
- do not call providers
- do not run simulations
- do not mutate simulator traces
- do not create recommendation output
- do not add UI

## Follow-Up

Recommended next packet:

```text
Phase 14D - Simulator Review Export Checkpoint
```

Prepare a checkpoint report covering Phase 14A through Phase 14C.
