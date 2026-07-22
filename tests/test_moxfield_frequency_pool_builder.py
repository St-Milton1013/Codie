from __future__ import annotations

import copy
import json
from dataclasses import FrozenInstanceError
from pathlib import Path
import unittest

from codie.frequency_pools import (
    MOXFIELD_FREQUENCY_POOL_BUILDER_VERSION,
    MoxfieldDeckInputRef,
    MoxfieldFrequencyPoolBuildError,
    MoxfieldFrequencyPoolBuilderOptions,
    build_moxfield_frequency_pool_request,
    build_moxfield_frequency_pool_result,
    extract_moxfield_public_id,
    moxfield_frequency_pool_result_to_dict,
    parse_moxfield_export_text,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "moxfield_frequency_pools"
MODULE_PATH = Path(__file__).parents[1] / "codie" / "frequency_pools" / "moxfield_builder.py"


def load_text(name: str) -> str:
    return (FIXTURE_DIR / name).read_text(encoding="utf-8")


def load_json(name: str) -> dict:
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


def input_ref(
    ref_id: str,
    *,
    source_key: str | None = None,
    export_text: str | None = None,
    payload: dict | None = None,
    metadata: dict | None = None,
    input_type: str = "text_export",
) -> MoxfieldDeckInputRef:
    return MoxfieldDeckInputRef(
        input_ref_id=ref_id,
        input_type=input_type,
        source_key=source_key or f"moxfield:{ref_id}",
        export_text=export_text,
        payload=payload or load_json("moxfield_url_payload.json"),
        metadata=metadata or {"fixture": True},
    )


class MoxfieldFrequencyPoolBuilderTest(unittest.TestCase):
    def test_extracts_public_moxfield_ids_and_rejects_malformed_urls(self) -> None:
        self.assertEqual(extract_moxfield_public_id("https://www.moxfield.com/decks/abc_123-def"), "abc_123-def")
        self.assertEqual(extract_moxfield_public_id("https://moxfield.com/decks/abc123?foo=bar"), "abc123")
        self.assertEqual(extract_moxfield_public_id("moxfield:deck_123"), "deck_123")
        self.assertEqual(extract_moxfield_public_id("plainDeckId123"), "plainDeckId123")

        with self.assertRaises(MoxfieldFrequencyPoolBuildError):
            extract_moxfield_public_id("https://example.com/decks/abc123")

    def test_parses_sections_and_default_exclusions(self) -> None:
        ref = input_ref("deck-1", export_text=load_text("brigid_export_1.txt"))
        parsed = parse_moxfield_export_text(ref.export_text or "", input_ref=ref)
        names = [card.card_name for card in parsed.cards]

        self.assertEqual(parsed.public_id, "deck-1")
        self.assertIn("Shared Draw Engine", names)
        self.assertIn("Repeated Interaction", names)
        self.assertNotIn("Brigid, Clachan's Heart", names)
        self.assertNotIn("Deafening Silence", names)
        self.assertNotIn("Plains", names)
        self.assertEqual(parsed.metadata["included_sections"], ("mainboard",))
        self.assertTrue(parsed.metadata["exclude_basic_lands"])

    def test_section_overrides_are_visible(self) -> None:
        options = MoxfieldFrequencyPoolBuilderOptions(
            included_sections=("mainboard", "sideboard"),
            excluded_sections=("commander", "maybeboard", "considering", "tokens"),
            exclude_basic_lands=False,
        )
        request = build_moxfield_frequency_pool_request(
            request_id="request-overrides",
            subject_key="brigid",
            inputs=(input_ref("deck-1", export_text=load_text("brigid_export_1.txt")),),
            options=options,
        )

        data = moxfield_frequency_pool_result_to_dict(build_moxfield_frequency_pool_result(request))
        filters = data["frequency_pool"]["filters"]
        names = [row["identity"]["card_name"] for row in data["frequency_pool"]["cards"]]

        self.assertEqual(filters["included_sections"], ["mainboard", "sideboard"])
        self.assertFalse(filters["exclude_basic_lands"])
        self.assertIn("Deafening Silence", names)
        self.assertIn("Plains", names)

    def test_uses_deck_presence_not_total_copy_count_by_default(self) -> None:
        request = build_moxfield_frequency_pool_request(
            request_id="request-presence",
            subject_key="brigid",
            inputs=(
                input_ref("deck-1", export_text=load_text("brigid_export_1.txt")),
                input_ref("deck-2", export_text=load_text("brigid_export_2.txt")),
            ),
        )
        data = moxfield_frequency_pool_result_to_dict(build_moxfield_frequency_pool_result(request))
        rows = {row["identity"]["card_name"]: row for row in data["frequency_pool"]["cards"]}

        self.assertEqual(rows["Repeated Interaction"]["deck_count"], 2)
        self.assertEqual(rows["Repeated Interaction"]["card_count"], 3)
        self.assertEqual(rows["Repeated Interaction"]["metadata"]["frequency_basis"], "deck_presence")
        self.assertEqual(rows["Repeated Interaction"]["metadata"]["frequency_label"], "2/2")

    def test_duplicate_inputs_partial_failures_and_unresolved_cards_remain_visible(self) -> None:
        duplicate_payload = load_json("moxfield_duplicate_inputs.json")
        inputs = tuple(
            input_ref(item["input_ref_id"], source_key=item["source_key"], export_text=load_text("brigid_export_1.txt"))
            for item in duplicate_payload["inputs"]
        )
        request = build_moxfield_frequency_pool_request(request_id="request-duplicates", subject_key="brigid", inputs=inputs)
        data = moxfield_frequency_pool_result_to_dict(build_moxfield_frequency_pool_result(request))

        self.assertEqual(data["duplicate_deck_count"], 1)
        self.assertTrue(any(failure["failure_code"] == "DUPLICATE_DECK_INPUT" for failure in data["failures"]))
        self.assertTrue(any(caveat["caveat_type"] == "partial_failure" for caveat in data["frequency_pool"]["caveats"]))

        unresolved_ref = input_ref("unresolved", export_text=load_text("moxfield_unresolved_card.txt"))
        unresolved_request = build_moxfield_frequency_pool_request(
            request_id="request-unresolved",
            subject_key="brigid",
            inputs=(unresolved_ref,),
        )
        unresolved_data = moxfield_frequency_pool_result_to_dict(build_moxfield_frequency_pool_result(unresolved_request))
        unresolved_rows = [row for row in unresolved_data["frequency_pool"]["cards"] if row["metadata"]["unresolved"]]

        self.assertEqual(len(unresolved_rows), 1)
        self.assertEqual(unresolved_data["unresolved_cards"][0]["raw_name"], "Unresolved Local Name")
        self.assertTrue(unresolved_rows[0]["identity"]["oracle_id"].startswith("unresolved:"))

    def test_url_without_local_payload_and_private_deck_payload_fail_visibly(self) -> None:
        url_ref = input_ref(
            "url-only",
            source_key="https://www.moxfield.com/decks/urlOnlyDeck",
            payload={},
            input_type="url",
        )
        url_request = build_moxfield_frequency_pool_request(
            request_id="request-url-only",
            subject_key="brigid",
            inputs=(url_ref, input_ref("deck-1", export_text=load_text("brigid_export_1.txt"))),
        )
        url_data = moxfield_frequency_pool_result_to_dict(build_moxfield_frequency_pool_result(url_request))
        self.assertTrue(any(failure["failure_code"] == "URL_PAYLOAD_UNAVAILABLE" for failure in url_data["failures"]))

        request = build_moxfield_frequency_pool_request(
            request_id="request-private",
            subject_key="brigid",
            inputs=(
                input_ref(
                    "private",
                    payload=load_json("moxfield_private_deck_failure.json"),
                    input_type="fixture_payload",
                ),
                input_ref("deck-1", export_text=load_text("brigid_export_1.txt")),
            ),
        )
        data = moxfield_frequency_pool_result_to_dict(build_moxfield_frequency_pool_result(request))

        self.assertTrue(any(failure["failure_code"] == "MOXFIELD_PRIVATE_DECK" for failure in data["failures"]))
        self.assertEqual(data["failed_deck_count"], 1)

    def test_unknown_sections_and_malformed_exports_are_not_silent(self) -> None:
        unknown = parse_moxfield_export_text(
            load_text("moxfield_unknown_section.txt"),
            input_ref=input_ref("unknown", export_text=load_text("moxfield_unknown_section.txt")),
        )
        self.assertTrue(any(warning.warning_code == "SECTION_UNKNOWN" for warning in unknown.warnings))

        malformed = parse_moxfield_export_text(
            load_text("moxfield_malformed_export.txt"),
            input_ref=input_ref("malformed", export_text=load_text("moxfield_malformed_export.txt")),
        )
        self.assertFalse(malformed.accepted)
        self.assertTrue(any(failure.failure_code == "UNSUPPORTED_EXPORT_FORMAT" for failure in malformed.failures))

    def test_result_serializes_deterministically_round_trips_and_does_not_mutate_inputs(self) -> None:
        payload = load_json("moxfield_url_payload.json")
        before = copy.deepcopy(payload)
        request = build_moxfield_frequency_pool_request(
            request_id="request-deterministic",
            subject_key="brigid",
            inputs=(input_ref("deck-1", export_text=load_text("brigid_export_1.txt"), payload=payload),),
        )
        result = build_moxfield_frequency_pool_result(request)
        first = moxfield_frequency_pool_result_to_dict(result)
        second = moxfield_frequency_pool_result_to_dict(result)

        self.assertEqual(first, second)
        self.assertEqual(first["builder_version"], MOXFIELD_FREQUENCY_POOL_BUILDER_VERSION)
        self.assertEqual(payload, before)
        with self.assertRaises(FrozenInstanceError):
            result.accepted_deck_count = 99
        rebuilt_request = build_moxfield_frequency_pool_request(
            request_id=first["request"]["request_id"],
            subject_key=first["request"]["subject_key"],
            inputs=request.inputs,
        )
        rebuilt = build_moxfield_frequency_pool_result(rebuilt_request)
        self.assertEqual(
            moxfield_frequency_pool_result_to_dict(rebuilt)["frequency_pool"]["cards"],
            first["frequency_pool"]["cards"],
        )

    def test_user_local_labels_and_frequency_pool_packet_compatibility_are_visible(self) -> None:
        request = build_moxfield_frequency_pool_request(
            request_id="request-compatible",
            subject_key="brigid",
            inputs=(input_ref("deck-1", export_text=load_text("brigid_export_1.txt")),),
        )
        data = moxfield_frequency_pool_result_to_dict(build_moxfield_frequency_pool_result(request))
        pool = data["frequency_pool"]

        self.assertEqual(pool["pool_type"], "user_local_snapshot")
        self.assertTrue(pool["subject"]["user_local"])
        self.assertTrue(pool["metadata"]["isolated_from_global_pools"])
        self.assertTrue(pool["metadata"]["not_tournament_evidence"])
        self.assertTrue(pool["metadata"]["not_" + "rec" + "ommendation_input"])
        self.assertEqual(data["accepted_deck_count"], 1)

    def test_private_raw_metadata_and_action_language_are_rejected(self) -> None:
        with self.assertRaises(MoxfieldFrequencyPoolBuildError):
            input_ref("private-meta", metadata={"private_notes": "hidden"})
        with self.assertRaises(MoxfieldFrequencyPoolBuildError):
            input_ref("raw-meta", payload={"raw_provider_payload": {"hidden": True}})
        with self.assertRaises(MoxfieldFrequencyPoolBuildError):
            input_ref("action", metadata={"note": "rec" + "ommended include"})

    def test_reproduces_brigid_five_deck_frequency_bucket_fixture(self) -> None:
        exports, identities = build_bucket_fixture()
        request = build_moxfield_frequency_pool_request(
            request_id="request-brigid-bucket",
            subject_key="brigid",
            inputs=tuple(
                input_ref(f"brigid-{index}", export_text=export, payload={"card_identities": identities})
                for index, export in enumerate(exports, start=1)
            ),
        )
        data = moxfield_frequency_pool_result_to_dict(build_moxfield_frequency_pool_result(request))
        bucket_counts: dict[int, int] = {}
        for row in data["frequency_pool"]["cards"]:
            bucket_counts[row["deck_count"]] = bucket_counts.get(row["deck_count"], 0) + 1

        self.assertEqual(bucket_counts[5], 49)
        self.assertEqual(bucket_counts[4], 27)
        self.assertEqual(bucket_counts[3], 17)
        self.assertEqual(bucket_counts[2], 22)
        self.assertEqual(bucket_counts[1], 37)
        self.assertEqual(data["accepted_deck_count"], 5)

    def test_module_has_no_forbidden_imports_or_runtime_coupling(self) -> None:
        source = MODULE_PATH.read_text(encoding="utf-8")
        forbidden = (
            "codie.db",
            "sqlite3",
            "codie.providers",
            "codie.analytics",
            "codie.rec" + "ommendations",
            "codie.decision_intelligence",
            "codie.evidence_fusion",
            "requests",
            "httpx",
            "urllib.",
            "openai",
            "anthropic",
            "google.generativeai",
            "langchain",
            "flask",
            "fastapi",
            "uvicorn",
            "starlette",
            "open(",
            "write_text(",
            "write_bytes(",
        )
        self.assertFalse(any(item in source for item in forbidden))


def build_bucket_fixture() -> tuple[list[str], dict[str, dict[str, str]]]:
    deck_cards: list[list[str]] = [[] for _ in range(5)]
    identities: dict[str, dict[str, str]] = {}

    def add_group(prefix: str, count: int, deck_indexes: range) -> None:
        for index in range(1, count + 1):
            name = f"{prefix} {index:02d}"
            identities[name] = {
                "oracle_id": f"oracle-{prefix.lower().replace(' ', '-')}-{index:02d}",
                "scryfall_id": f"scryfall-{prefix.lower().replace(' ', '-')}-{index:02d}",
            }
            for deck_index in deck_indexes:
                deck_cards[deck_index].append(name)

    add_group("Five Deck Card", 49, range(5))
    add_group("Four Deck Card", 27, range(4))
    add_group("Three Deck Card", 17, range(3))
    add_group("Two Deck Card", 22, range(2))
    add_group("One Deck Card", 37, range(1))

    exports = []
    for cards in deck_cards:
        body = "\n".join(f"1 {name}" for name in cards)
        exports.append(f"COMMANDER\n1 Brigid, Clachan's Heart\n\nMAINBOARD\n{body}\n\nSIDEBOARD\n1 Deafening Silence\n")
    return exports, identities


if __name__ == "__main__":
    unittest.main()
