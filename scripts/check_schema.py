"""Validate that Codie's SQLite schema files bootstrap cleanly."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = REPO_ROOT / "codie" / "db" / "schema"
EXPECTED_SCHEMA_ORDER = (
    "core.sql",
    "source.sql",
    "canonical.sql",
    "curated.sql",
    "analytics.sql",
    "regional.sql",
    "simulation.sql",
    "user.sql",
    "indexes.sql",
)


def main() -> int:
    sys.path.insert(0, str(REPO_ROOT))

    from codie.db.bootstrap import SCHEMA_ORDER, bootstrap  # noqa: PLC0415

    schema_files = tuple(sorted(path.name for path in SCHEMA_DIR.glob("*.sql")))
    ordered_files = tuple(SCHEMA_ORDER)

    missing_from_order = sorted(set(schema_files) - set(ordered_files))
    missing_from_disk = sorted(set(ordered_files) - set(schema_files))
    if missing_from_order or missing_from_disk:
        print("Schema order drift detected.")
        if missing_from_order:
            print(f"SQL files not listed in SCHEMA_ORDER: {missing_from_order}")
        if missing_from_disk:
            print(f"SCHEMA_ORDER entries missing from disk: {missing_from_disk}")
        return 1

    if ordered_files != EXPECTED_SCHEMA_ORDER:
        print("SCHEMA_ORDER changed. Update scripts/check_schema.py and document the schema change.")
        print(f"Actual:   {ordered_files}")
        print(f"Expected: {EXPECTED_SCHEMA_ORDER}")
        return 1

    connection = sqlite3.connect(":memory:")
    try:
        bootstrap(connection)
        connection.execute("PRAGMA foreign_key_check")
    finally:
        connection.close()

    print("Schema bootstrap check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
