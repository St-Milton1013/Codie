from __future__ import annotations

import ast
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def imports_for(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    return imports


class ArchitectureBoundaryTest(unittest.TestCase):
    def test_providers_do_not_import_database_or_repositories(self) -> None:
        provider_files = sorted((ROOT / "codie" / "providers").rglob("*.py"))
        forbidden_exact = {"sqlite3"}
        forbidden_prefixes = (
            "codie.analytics",
            "codie.cards",
            "codie.db",
            "codie.ingestion",
            "codie.recommendations",
        )
        for path in provider_files:
            imports = imports_for(path)
            offenders = [
                module
                for module in imports
                if module in forbidden_exact or module.startswith(forbidden_prefixes)
            ]
            self.assertEqual(offenders, [], f"{path} imports forbidden modules: {offenders}")

    def test_sqlite_imports_stay_inside_db_package_or_tests(self) -> None:
        offenders = []
        for path in sorted((ROOT / "codie").rglob("*.py")):
            if ROOT / "codie" / "db" in path.parents:
                continue
            if "sqlite3" in imports_for(path):
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [])

    def test_no_live_network_dependency_in_scryfall_layer(self) -> None:
        offenders = []
        forbidden_imports = {"requests", "urllib.request", "http.client"}
        for path in sorted((ROOT / "codie" / "providers" / "scryfall").rglob("*.py")):
            imports = imports_for(path)
            if imports.intersection(forbidden_imports):
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [])
