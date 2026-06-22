# Phase 1 Schema And Repository Foundation Contract

## Objective

Create Codie's local SQLite schema foundation, repository-only persistence paths, commander signature helper, and schema verification tests.

## Files Created

- `codie/db/schema/core.sql`
- `codie/db/schema/source.sql`
- `codie/db/schema/canonical.sql`
- `codie/db/schema/curated.sql`
- `codie/db/schema/analytics.sql`
- `codie/db/schema/regional.sql`
- `codie/db/schema/simulation.sql`
- `codie/db/schema/user.sql`
- `codie/db/schema/indexes.sql`
- `codie/db/connection.py`
- `codie/db/pragmas.py`
- `codie/db/bootstrap.py`
- `codie/db/repositories/*.py`
- `codie/canonical/signature.py`
- `tests/test_schema.py`

## Public Functions And Classes

- `codie.db.connection.connect`
- `codie.db.pragmas.apply_pragmas`
- `codie.db.pragmas.foreign_keys_enabled`
- `codie.db.bootstrap.bootstrap`
- `codie.db.bootstrap.bootstrap_database`
- `codie.db.repositories.CoreRepository`
- `codie.db.repositories.CuratedRepository`
- `codie.db.repositories.SourceRepository`
- `codie.db.repositories.CanonicalRepository`
- `codie.db.repositories.AnalyticsRepository`
- `codie.db.repositories.RegionalRepository`
- `codie.db.repositories.SimulationRepository`
- `codie.db.repositories.UserRepository`
- `codie.canonical.signature.normalize_commander_name`
- `codie.canonical.signature.commander_signature`

## Schema Impact

Creates the Phase 1 schema from `docs/SCHEMA_SPEC.md`, split by ownership domain. Tables cover core cards, source preservation, canonical records, curated registries/primers/combos/packages, analytics, regional metrics, simulation persistence, and user analysis records.

## Dependencies

Uses only Python standard library modules and local SQLite. No paid services, network calls, external APIs, or third-party packages are required.

## Failure Modes

- Missing required repository fields raise `RepositoryError`.
- Foreign key violations raise `sqlite3.IntegrityError`.
- Empty commander signature input raises `ValueError`.
- Bootstrap fails fast if a schema file is missing or invalid.

## Tests

- Database bootstraps all required tables.
- Foreign keys are enabled and enforced.
- Core card and commander repository paths work.
- Source raw payloads are preserved.
- Canonical event/source links work.
- Canonical deck cards and evidence counts work.
- Regional, simulation, and user repositories work.
- Curated registries and analysis sessions work.
- Required-field validation and commander signatures are deterministic.

## Architecture Compliance

- Providers are not implemented and therefore cannot write to the database.
- Persistence routes through repositories or schema bootstrap.
- Analytics tables are derived-record targets and do not read raw source data.
- `scryfall_id` remains the exact card primary key; `oracle_id` is indexed for analytics grouping.
- Raw provider payload fields are present in source tables.
- No strategy inference language or UI claims are implemented.
