import sqlite3
import unittest

from codie.db.bootstrap import SCHEMA_DIR, SCHEMA_ORDER, bootstrap


class SchemaBootstrapGuardrailTests(unittest.TestCase):
    def test_schema_order_lists_every_schema_file(self):
        schema_files = {path.name for path in SCHEMA_DIR.glob("*.sql")}

        self.assertEqual(schema_files, set(SCHEMA_ORDER))

    def test_schema_bootstraps_in_memory_database(self):
        connection = sqlite3.connect(":memory:")
        try:
            bootstrap(connection)
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                ).fetchall()
            }
        finally:
            connection.close()

        self.assertIn("cards", tables)
        self.assertIn("source_events", tables)
        self.assertIn("canonical_decks", tables)
        self.assertIn("simulation_batches", tables)
        self.assertIn("simulation_traces", tables)
        self.assertIn("user_decks", tables)


if __name__ == "__main__":
    unittest.main()
