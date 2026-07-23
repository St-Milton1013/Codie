import json
from pathlib import Path
import unittest

from codie.cockatrice import (
    COCKATRICE_INTEROPERABILITY_VERSION,
    CockatriceDeckCard,
    CockatriceExportOptions,
    CockatriceInteropBuildError,
    build_cockatrice_export_packet,
    build_cockatrice_import_request,
    cockatrice_export_packet_to_dict,
    cockatrice_imported_deck_to_dict,
    parse_cockatrice_deck_payload,
)


FIXTURES = Path(__file__).parent / "fixtures" / "cockatrice"


def _fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


class CockatriceInteroperabilityTests(unittest.TestCase):
    def test_valid_commander_deck_parses_deterministically(self):
        deck = parse_cockatrice_deck_payload(_fixture("valid_commander_deck.cod"), source_file_label="valid.cod")

        first = cockatrice_imported_deck_to_dict(deck)
        second = cockatrice_imported_deck_to_dict(parse_cockatrice_deck_payload(_fixture("valid_commander_deck.cod"), source_file_label="valid.cod"))

        self.assertEqual(first, second)
        self.assertEqual(first["interoperability_version"], COCKATRICE_INTEROPERABILITY_VERSION)
        self.assertEqual(first["deck_name"], "Codie Fixture Deck")
        self.assertTrue(first["user_local"])
        self.assertTrue(first["deck_metadata"]["not_tournament_evidence"])
        self.assertEqual(first["failures"], [])
        self.assertEqual([zone["section_name"] for zone in first["zones"]], ["commander", "mainboard"])

    def test_partner_commander_deck_preserves_partner_ordering(self):
        deck = parse_cockatrice_deck_payload(_fixture("partner_commander_deck.cod"))
        data = cockatrice_imported_deck_to_dict(deck)
        commander_zone = next(zone for zone in data["zones"] if zone["section_name"] == "commander")

        self.assertEqual(
            [card["card_name"] for card in commander_zone["cards"]],
            ["Tymna the Weaver", "Kraum, Ludevic's Opus"],
        )

    def test_mainboard_and_sideboard_remain_distinct(self):
        deck = parse_cockatrice_deck_payload(_fixture("mainboard_sideboard.cod"))
        data = cockatrice_imported_deck_to_dict(deck)

        sections = {zone["section_name"]: zone for zone in data["zones"]}
        self.assertIn("mainboard", sections)
        self.assertIn("sideboard", sections)
        self.assertEqual(sections["mainboard"]["cards"][0]["card_name"], "Brainstorm")
        self.assertEqual(sections["sideboard"]["cards"][0]["card_name"], "Pyroblast")

    def test_custom_zone_creates_visible_unsupported_record(self):
        deck = parse_cockatrice_deck_payload(_fixture("custom_zone.cod"))
        data = cockatrice_imported_deck_to_dict(deck)

        self.assertTrue(data["zones"][0]["unsupported"])
        self.assertEqual(data["zones"][0]["section_name"], "unsupported:maybeboard")
        self.assertEqual(data["unsupported_items"][0]["warning_code"], "COCKATRICE_UNKNOWN_ZONE")

    def test_malformed_xml_creates_visible_failure(self):
        deck = parse_cockatrice_deck_payload(_fixture("malformed_xml.cod"))
        data = cockatrice_imported_deck_to_dict(deck)

        self.assertEqual(data["failures"][0]["failure_code"], "COCKATRICE_XML_MALFORMED")

    def test_unsafe_xml_external_entity_is_rejected(self):
        deck = parse_cockatrice_deck_payload(_fixture("unsafe_xml_external_entity.cod"))
        data = cockatrice_imported_deck_to_dict(deck)

        self.assertEqual(data["failures"][0]["failure_code"], "COCKATRICE_XML_UNSAFE")

    def test_unsupported_format_is_rejected(self):
        deck = parse_cockatrice_deck_payload(_fixture("unsupported_format.txt"))
        data = cockatrice_imported_deck_to_dict(deck)

        self.assertEqual(data["failures"][0]["failure_code"], "COCKATRICE_XML_MALFORMED")

    def test_empty_deck_creates_visible_failure(self):
        deck = parse_cockatrice_deck_payload(_fixture("empty_deck.cod"))
        data = cockatrice_imported_deck_to_dict(deck)

        self.assertEqual(data["failures"][0]["failure_code"], "COCKATRICE_EMPTY_DECK")

    def test_unresolved_card_rows_remain_visible(self):
        deck = parse_cockatrice_deck_payload(_fixture("unresolved_card_row.cod"))
        data = cockatrice_imported_deck_to_dict(deck)
        card = data["zones"][0]["cards"][0]

        self.assertTrue(card["unresolved"])
        self.assertEqual(data["warnings"][0]["warning_code"], "COCKATRICE_CARD_UNRESOLVED")

    def test_duplicate_card_rows_remain_visible_with_caveat(self):
        deck = parse_cockatrice_deck_payload(_fixture("duplicate_card_row.cod"))
        data = cockatrice_imported_deck_to_dict(deck)

        self.assertEqual(len(data["zones"][0]["cards"]), 2)
        self.assertEqual(data["warnings"][0]["warning_code"], "COCKATRICE_DUPLICATE_CARD_ROW")

    def test_privacy_metadata_is_rejected_recursively(self):
        deck = parse_cockatrice_deck_payload(_fixture("privacy_metadata_failure.cod"))
        data = cockatrice_imported_deck_to_dict(deck)

        self.assertEqual(data["failures"][0]["failure_code"], "COCKATRICE_PRIVACY_METADATA_REJECTED")

        with self.assertRaises(CockatriceInteropBuildError):
            build_cockatrice_export_packet(
                export_id="private",
                deck_name="Private",
                cards=[
                    CockatriceDeckCard(
                        card_name="Sol Ring",
                        quantity=1,
                        zone_name="main",
                        section_name="mainboard",
                        metadata={"nested": {"private_notes": "secret"}},
                    )
                ],
            )

    def test_import_request_does_not_preserve_raw_payload_text(self):
        request = build_cockatrice_import_request(
            source_file_label="valid.cod",
            payload_text=_fixture("valid_commander_deck.cod"),
        )
        data = request.to_dict()

        self.assertEqual(data["source_format"], "cockatrice_cod_xml")
        self.assertEqual(data["source_file_label"], "valid.cod")
        self.assertNotIn("payload_text", data)

    def test_export_packet_serializes_deterministically_and_preserves_failures(self):
        cards = [
            CockatriceDeckCard(card_name="Side Card", quantity=1, zone_name="sideboard", section_name="sideboard"),
            CockatriceDeckCard(card_name="Commander", quantity=1, zone_name="commander", section_name="commander"),
            CockatriceDeckCard(card_name="Unknown", quantity=1, zone_name="weird", section_name="unsupported:weird"),
            CockatriceDeckCard(card_name="Mystery", quantity=1, zone_name="main", section_name="mainboard", unresolved=True),
        ]
        packet = build_cockatrice_export_packet(export_id="export-1", deck_name="Export Fixture", cards=cards)
        first = cockatrice_export_packet_to_dict(packet)
        second = cockatrice_export_packet_to_dict(build_cockatrice_export_packet(export_id="export-1", deck_name="Export Fixture", cards=cards))

        self.assertEqual(first, second)
        self.assertEqual([zone["section_name"] for zone in first["zones"]], ["commander", "mainboard", "sideboard"])
        self.assertEqual(first["warnings"][0]["warning_code"], "COCKATRICE_EXPORT_UNSUPPORTED_CARD")
        self.assertEqual(first["failures"][0]["failure_code"], "COCKATRICE_UNKNOWN_ZONE")

    def test_export_packet_can_reject_unresolved_rows(self):
        packet = build_cockatrice_export_packet(
            export_id="export-unresolved",
            deck_name="Export Fixture",
            cards=[
                CockatriceDeckCard(
                    card_name="Mystery",
                    quantity=1,
                    zone_name="main",
                    section_name="mainboard",
                    unresolved=True,
                )
            ],
            options=CockatriceExportOptions(preserve_unresolved_rows=False),
        )
        data = cockatrice_export_packet_to_dict(packet)

        self.assertEqual(data["zones"], [])
        self.assertEqual(data["failures"][0]["failure_code"], "COCKATRICE_EXPORT_UNSUPPORTED_CARD")

    def test_dictionary_round_trip_preserves_all_fields(self):
        payload = json.loads((FIXTURES / "round_trip_import_export.json").read_text(encoding="utf-8"))
        cards = [CockatriceDeckCard.from_mapping(item) for item in payload["cards"]]
        packet = build_cockatrice_export_packet(export_id="round-trip", deck_name="Round Trip", cards=cards)
        data = cockatrice_export_packet_to_dict(packet)

        rebuilt = type(packet).from_mapping(data)

        self.assertEqual(cockatrice_export_packet_to_dict(rebuilt), data)

    def test_unknown_unavailable_unsupported_zero_states_remain_distinct(self):
        deck = parse_cockatrice_deck_payload(_fixture("custom_zone.cod"))
        data = cockatrice_imported_deck_to_dict(deck)
        unresolved_deck = parse_cockatrice_deck_payload(_fixture("unresolved_card_row.cod"))
        unresolved_data = cockatrice_imported_deck_to_dict(unresolved_deck)

        self.assertEqual(data["zones"][0]["section_name"], "unsupported:maybeboard")
        self.assertEqual(data["failures"], [])
        self.assertEqual(data["zones"][0]["metadata"]["card_count"], 1)
        self.assertIsNone(unresolved_data["zones"][0]["cards"][0]["scryfall_id"])
        self.assertTrue(unresolved_data["zones"][0]["cards"][0]["unresolved"])

    def test_forbidden_recommendation_language_is_rejected(self):
        with self.assertRaises(CockatriceInteropBuildError):
            build_cockatrice_export_packet(
                export_id="bad-language",
                deck_name="Bad",
                cards=[
                    CockatriceDeckCard(
                        card_name="Sol Ring",
                        quantity=1,
                        zone_name="main",
                        section_name="mainboard",
                        metadata={"note": "this should include card"},
                    )
                ],
            )

    def test_no_forbidden_imports_or_runtime_coupling(self):
        module_text = Path("codie/cockatrice/interoperability.py").read_text(encoding="utf-8")
        forbidden = (
            "requests",
            "httpx",
            "sqlite3",
            "codie.db",
            "codie.providers",
            "codie.analytics",
            "codie.recommendations",
            "codie.decision_intelligence",
            "codie.evidence_fusion",
            "openai",
            "anthropic",
            "fastapi",
            "flask",
            "uvicorn",
        )

        for needle in forbidden:
            self.assertNotIn(needle, module_text)
        self.assertNotIn("open(", module_text)
        self.assertNotIn(".write_text", module_text)


if __name__ == "__main__":
    unittest.main()
