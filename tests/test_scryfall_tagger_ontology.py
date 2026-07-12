from __future__ import annotations

from dataclasses import FrozenInstanceError
import json
from pathlib import Path
import unittest

from codie.cards.scryfall_tagger_ontology import (
    SCRYFALL_TAGGER_ONTOLOGY_VERSION,
    ScryfallTaggerOntologyError,
    ScryfallTaggerOntologyOptions,
    build_scryfall_tagger_coverage_report,
    build_scryfall_tagger_ontology,
    scryfall_tagger_coverage_report_to_dict,
    scryfall_tagger_ontology_to_dict,
    validate_scryfall_tagger_ontology,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "scryfall_tagger"


class ScryfallTaggerOntologyTest(unittest.TestCase):
    def _payload(self, name: str) -> dict:
        return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))

    def test_functional_tags_map_to_oracle_id_and_preserve_scryfall_provenance(self) -> None:
        ontology = build_scryfall_tagger_ontology(self._payload("tagger_functional_tags.json"))
        tag = ontology.tags[0]

        self.assertEqual(ontology.ontology_version, SCRYFALL_TAGGER_ONTOLOGY_VERSION)
        self.assertEqual(tag.oracle_id, "oracle-force")
        self.assertEqual(tag.scryfall_id, "sf-003")
        self.assertTrue(tag.is_functional)
        self.assertFalse(tag.is_excluded)
        self.assertEqual(tag.provenance["source"], "scryfall_tagger")
        self.assertEqual(tag.provenance["source_snapshot_id"], "tagger-fixture-2026-07-11")

    def test_ontology_serializes_deterministically_and_round_trips_through_json(self) -> None:
        ontology = build_scryfall_tagger_ontology(self._payload("tagger_functional_tags.json"))
        first = scryfall_tagger_ontology_to_dict(ontology)
        second = scryfall_tagger_ontology_to_dict(ontology)
        decoded = json.loads(json.dumps(first, sort_keys=True))

        self.assertEqual(first, second)
        self.assertEqual(decoded, first)
        self.assertEqual(decoded["ontology_version"], SCRYFALL_TAGGER_ONTOLOGY_VERSION)

    def test_artwork_and_cosmetic_tags_are_excluded_by_default(self) -> None:
        ontology = build_scryfall_tagger_ontology(self._payload("tagger_artwork_tags.json"))
        tags_by_name = {tag.normalized_tag: tag for tag in ontology.tags}

        self.assertTrue(tags_by_name["fish"].is_excluded)
        self.assertFalse(tags_by_name["fish"].is_functional)
        self.assertEqual(tags_by_name["fish"].exclusion_reason, "non-functional tag namespace")
        self.assertTrue(tags_by_name["draw engine"].is_functional)

    def test_unknown_namespaces_are_reported_not_silently_mapped(self) -> None:
        ontology = build_scryfall_tagger_ontology(self._payload("tagger_unknown_namespace.json"))

        self.assertFalse(ontology.tags[0].is_functional)
        self.assertIn("unknown tag namespace: future_namespace", ontology.validation_warnings)
        self.assertIn("unknown tag namespace: future_namespace", ontology.manual_review_items)

    def test_duplicate_tags_are_deduplicated_deterministically_and_coverage_reports_count(self) -> None:
        ontology = build_scryfall_tagger_ontology(self._payload("tagger_duplicate_tags.json"))
        coverage = build_scryfall_tagger_coverage_report(ontology, duplicate_tag_count=1)

        self.assertEqual(len(ontology.tags), 1)
        self.assertIn("duplicate tag ignored: oracle-remora/card_advantage/draw engine/scryfall_tagger", ontology.validation_warnings)
        self.assertEqual(coverage.duplicate_tag_count, 1)

    def test_confidence_values_remain_visible_and_bounded(self) -> None:
        ontology = build_scryfall_tagger_ontology(self._payload("tagger_functional_tags.json"))

        self.assertEqual(scryfall_tagger_ontology_to_dict(ontology)["tags"][0]["confidence"], 0.9)
        payload = self._payload("tagger_functional_tags.json")
        payload["tags"][0]["confidence"] = 1.5
        with self.assertRaises(ScryfallTaggerOntologyError):
            build_scryfall_tagger_ontology(payload)

    def test_manual_corrections_annotate_without_rewriting_source_tags(self) -> None:
        payload = self._payload("tagger_aliases_deprecated_conflicts.json")
        original_tag_text = payload["tags"][0]["tag"]
        ontology = build_scryfall_tagger_ontology(payload)

        self.assertEqual(payload["tags"][0]["tag"], original_tag_text)
        self.assertEqual(ontology.corrections[0].correction_source, "user_correction")
        self.assertEqual(ontology.corrections[0].review_status, "reviewed")

    def test_aliases_preserve_original_tags_and_normalize_deterministically(self) -> None:
        ontology = build_scryfall_tagger_ontology(self._payload("tagger_aliases_deprecated_conflicts.json"))
        alias = ontology.aliases[0]

        self.assertEqual(alias.alias_tag, "card draw")
        self.assertEqual(alias.canonical_tag, "draw engine")
        self.assertEqual(alias.source, "curated_functional_registry")

    def test_deprecated_tags_and_replacement_chains_remain_visible(self) -> None:
        ontology = build_scryfall_tagger_ontology(self._payload("tagger_aliases_deprecated_conflicts.json"))
        deprecated = {item.deprecated_tag for item in ontology.deprecated_tags}
        chains = {chain.original_tag: chain for chain in ontology.replacement_chains}

        self.assertIn("mana rock", deprecated)
        self.assertEqual(chains["mana rock"].replacement_tags, ("fast mana",))
        self.assertIn("deprecated tag remains visible: mana rock", ontology.manual_review_items)

    def test_cyclic_replacement_chains_fail_cleanly_as_visible_review_items(self) -> None:
        ontology = build_scryfall_tagger_ontology(self._payload("tagger_aliases_deprecated_conflicts.json"))
        cyclic = [chain for chain in ontology.replacement_chains if chain.original_tag == "old loop a"][0]

        self.assertTrue(cyclic.has_cycle)
        self.assertIn("cyclic replacement chain detected for tag old loop a", ontology.manual_review_items)

    def test_tag_conflicts_remain_visible_and_do_not_choose_winner(self) -> None:
        ontology = build_scryfall_tagger_ontology(self._payload("tagger_aliases_deprecated_conflicts.json"))
        conflict_types = {conflict.conflict_type for conflict in ontology.conflicts}

        self.assertIn("namespace_conflict", conflict_types)
        self.assertIn("manual_correction_conflict", conflict_types)
        self.assertTrue(any(conflict.tag == "fast mana" for conflict in ontology.conflicts))

    def test_coverage_ratio_is_deterministic_and_low_coverage_warns(self) -> None:
        ontology = build_scryfall_tagger_ontology(
            self._payload("tagger_functional_tags.json"),
            options=ScryfallTaggerOntologyOptions(low_coverage_threshold=0.9),
        )
        report = build_scryfall_tagger_coverage_report(
            ontology,
            total_cards_seen=10,
            cards_with_functional_tags=3,
            low_coverage_threshold=0.9,
        )
        first = scryfall_tagger_coverage_report_to_dict(report)
        second = scryfall_tagger_coverage_report_to_dict(report)

        self.assertEqual(first, second)
        self.assertEqual(report.coverage_ratio, 0.3)
        self.assertIn("low functional tag coverage", report.warnings)

    def test_raw_source_payloads_are_not_mutated_and_values_are_frozen(self) -> None:
        payload = self._payload("tagger_functional_tags.json")
        before = json.loads(json.dumps(payload, sort_keys=True))
        ontology = build_scryfall_tagger_ontology(payload)

        with self.assertRaises(FrozenInstanceError):
            ontology.tags[0].tag = "Changed"  # type: ignore[misc]
        self.assertEqual(payload, before)

    def test_malformed_fixtures_fail_cleanly(self) -> None:
        with self.assertRaises(ScryfallTaggerOntologyError):
            build_scryfall_tagger_ontology({"tags": "not-list"})
        with self.assertRaises(ScryfallTaggerOntologyError):
            build_scryfall_tagger_ontology({"tags": [{"tag": "Missing Oracle"}]})
        with self.assertRaises(ScryfallTaggerOntologyError):
            validate_scryfall_tagger_ontology(object())  # type: ignore[arg-type]

    def test_no_live_network_sqlite_or_recommendation_imports(self) -> None:
        module_text = (Path(__file__).parents[1] / "codie" / "cards" / "scryfall_tagger_ontology.py").read_text(
            encoding="utf-8"
        )
        for forbidden in (
            "import req" + "uests",
            "import ht" + "tpx",
            "import sql" + "ite3",
            "from codie" + ".db",
            "import codie" + ".db",
            "from codie" + ".prov" + "iders",
            "from codie" + ".analytics",
            "from codie" + ".recommendations",
            "import op" + "enai",
            "import anth" + "ropic",
        ):
            self.assertNotIn(forbidden, module_text)


if __name__ == "__main__":
    unittest.main()
