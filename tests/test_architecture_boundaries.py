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
            "codie.canonical",
            "codie.combos",
            "codie.db",
            "codie.ingestion",
            "codie.primers",
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

    def test_analytics_do_not_import_provider_or_source_layers(self) -> None:
        offenders = []
        forbidden_prefixes = (
            "codie.providers",
            "codie.ingestion",
            "codie.db.repositories.source",
        )
        for path in sorted((ROOT / "codie" / "analytics").rglob("*.py")):
            imports = imports_for(path)
            offenders.extend(
                f"{path.relative_to(ROOT)} imports {module}"
                for module in imports
                if module.startswith(forbidden_prefixes)
            )
        self.assertEqual(offenders, [])

    def test_analytics_repository_does_not_query_source_tables(self) -> None:
        repository = ROOT / "codie" / "db" / "repositories" / "analytics.py"
        text = repository.read_text(encoding="utf-8")
        forbidden_fragments = (
            "FROM source_events",
            "JOIN source_events",
            "FROM source_decks",
            "JOIN source_decks",
            "FROM source_deck_cards",
            "JOIN source_deck_cards",
            "FROM provider_objects",
            "JOIN provider_objects",
        )
        offenders = [fragment for fragment in forbidden_fragments if fragment in text]
        self.assertEqual(offenders, [])

    def test_combo_sync_does_not_import_providers_or_recommendations(self) -> None:
        offenders = []
        forbidden_prefixes = (
            "codie.providers",
            "codie.recommendations",
        )
        for path in sorted((ROOT / "codie" / "combos").rglob("*.py")):
            imports = imports_for(path)
            offenders.extend(
                f"{path.relative_to(ROOT)} imports {module}"
                for module in imports
                if module.startswith(forbidden_prefixes)
            )
        self.assertEqual(offenders, [])

    def test_primer_sync_does_not_import_providers_or_recommendations(self) -> None:
        offenders = []
        forbidden_prefixes = (
            "codie.providers",
            "codie.recommendations",
        )
        for path in sorted((ROOT / "codie" / "primers").rglob("*.py")):
            imports = imports_for(path)
            offenders.extend(
                f"{path.relative_to(ROOT)} imports {module}"
                for module in imports
                if module.startswith(forbidden_prefixes)
            )
        self.assertEqual(offenders, [])

    def test_recommendations_cannot_read_source_or_provider_layers(self) -> None:
        recommendation_root = ROOT / "codie" / "recommendations"
        if not recommendation_root.exists():
            return
        forbidden_exact_imports = {"sqlite3"}
        forbidden_import_prefixes = (
            "codie.providers",
            "codie.ingestion",
            "codie.db.repositories.source",
        )
        forbidden_text = (
            "source_events",
            "source_decks",
            "source_deck_cards",
            "source_primers",
            "source_combos",
            "provider_objects",
            "Moxfield",
            "Spellbook",
            "moxfield",
            "spellbook",
            "recommendation_runs",
            "recommendation_candidates",
        )
        forbidden_sql_fragments = (
            "execute(",
            "executescript(",
        )
        offenders = []
        for path in sorted(recommendation_root.rglob("*.py")):
            imports = imports_for(path)
            offenders.extend(
                f"{path.relative_to(ROOT)} imports {module}"
                for module in imports
                if module in forbidden_exact_imports
            )
            offenders.extend(
                f"{path.relative_to(ROOT)} imports {module}"
                for module in imports
                if module.startswith(forbidden_import_prefixes)
            )
            text = path.read_text(encoding="utf-8")
            offenders.extend(
                f"{path.relative_to(ROOT)} references {fragment}"
                for fragment in forbidden_text
                if fragment in text
            )
            offenders.extend(
                f"{path.relative_to(ROOT)} uses raw SQL fragment {fragment}"
                for fragment in forbidden_sql_fragments
                if fragment in text
            )
        self.assertEqual(offenders, [])
