from __future__ import annotations

from dataclasses import FrozenInstanceError
import json
from pathlib import Path
import unittest

from codie.user_decks.immutable_snapshots import (
    IMMUTABLE_DECK_SNAPSHOT_VERSION,
    DeckSnapshotAnalysisRef,
    DeckSnapshotCard,
    DeckSnapshotReplayMetadata,
    DeckSnapshotSourceRef,
    DeckSnapshotWarning,
    ImmutableDeckSnapshotError,
    ImmutableDeckSnapshotOptions,
    build_immutable_deck_snapshot,
    immutable_deck_snapshot_to_dict,
    validate_immutable_deck_snapshot,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "user_deck_snapshots"


class UserDeckImmutableSnapshotsTest(unittest.TestCase):
    def test_redacted_snapshot_builds_by_default_and_omits_cards(self) -> None:
        snapshot = _build_snapshot(cards=_sample_cards())
        serialized = immutable_deck_snapshot_to_dict(snapshot)

        self.assertEqual(snapshot.snapshot_version, IMMUTABLE_DECK_SNAPSHOT_VERSION)
        self.assertEqual(serialized["snapshot_id"], "snapshot-001")
        self.assertEqual(serialized["deck_hash"], "deckhash-001")
        self.assertEqual(serialized["commander_signature"], "tymna-kraum")
        self.assertEqual(serialized["privacy_policy"]["redaction_policy"], "redacted")
        self.assertIn("card entries omitted", serialized["privacy_policy"]["privacy_caveats"][0])
        self.assertNotIn("cards", serialized)

    def test_full_card_list_requires_explicit_option_and_preserves_card_fields(self) -> None:
        snapshot = _build_snapshot(
            cards=_sample_cards(),
            options=ImmutableDeckSnapshotOptions(include_card_entries=True),
        )
        serialized = immutable_deck_snapshot_to_dict(snapshot)

        self.assertEqual(serialized["privacy_policy"]["redaction_policy"], "full_card_list")
        self.assertIn("explicit snapshot option", serialized["privacy_policy"]["privacy_caveats"][0])
        self.assertEqual([card["name"] for card in serialized["cards"]], ["Command Tower", "Thassa's Oracle"])
        self.assertEqual(serialized["cards"][0]["quantity"], 1)
        self.assertEqual(serialized["cards"][0]["zone"], "main")
        self.assertEqual(serialized["cards"][0]["source_order"], 0)
        self.assertEqual(serialized["cards"][0]["scryfall_id"], "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
        self.assertEqual(serialized["cards"][1]["oracle_id"], "22222222-2222-2222-2222-222222222222")

    def test_source_analysis_profile_replay_warning_and_manual_refs_remain_visible(self) -> None:
        snapshot = _build_snapshot()
        serialized = immutable_deck_snapshot_to_dict(snapshot)

        self.assertEqual(serialized["source_refs"][0]["source_id"], "user-deck-001")
        self.assertEqual(serialized["analysis_refs"][0]["analysis_id"], "analysis-001")
        self.assertEqual(serialized["analysis_profile_refs"], ["analysis-profile-competitive-default@1"])
        self.assertEqual(serialized["replay_metadata"]["analysis_profile_id"], "analysis-profile-competitive-default")
        self.assertEqual(serialized["validation_warnings"][0]["warning_id"], "user-local-only")
        self.assertEqual(serialized["manual_review_items"][0]["item_id"], "review-001")

    def test_serialization_is_deterministic_and_dictionary_compatible(self) -> None:
        snapshot = _build_snapshot(metadata={"z": {"b": 2, "a": 1}, "a": ["kept"]})
        first = immutable_deck_snapshot_to_dict(snapshot)
        second = immutable_deck_snapshot_to_dict(snapshot)

        self.assertEqual(first, second)
        decoded = json.loads(json.dumps(first, sort_keys=True))
        self.assertEqual(decoded, first)
        self.assertEqual(first["metadata"], {"a": ["kept"], "z": {"a": 1, "b": 2}})

    def test_snapshot_values_are_frozen_and_input_payloads_are_not_mutated(self) -> None:
        metadata = {"nested": {"kept": True}}
        replay_metadata = {"nested": {"kept": True}}
        snapshot = _build_snapshot(
            metadata=metadata,
            replay_metadata=DeckSnapshotReplayMetadata(metadata=replay_metadata),
        )
        metadata["nested"]["kept"] = False
        replay_metadata["nested"]["kept"] = False

        with self.assertRaises(FrozenInstanceError):
            snapshot.deck_hash = "changed"  # type: ignore[misc]
        self.assertEqual(immutable_deck_snapshot_to_dict(snapshot)["metadata"]["nested"]["kept"], True)
        self.assertEqual(
            immutable_deck_snapshot_to_dict(snapshot)["replay_metadata"]["metadata"]["nested"]["kept"],
            True,
        )

    def test_malformed_snapshot_failures_are_clean(self) -> None:
        with self.assertRaises(ImmutableDeckSnapshotError):
            _build_snapshot(snapshot_id="")
        with self.assertRaises(ImmutableDeckSnapshotError):
            _build_snapshot(cards=[DeckSnapshotCard(name="Bad", quantity=0, zone="main", source_order=0)])

    def test_redacted_snapshot_with_cards_is_invalid(self) -> None:
        snapshot = _build_snapshot(cards=())
        object.__setattr__(snapshot, "cards", _sample_cards())

        with self.assertRaises(ImmutableDeckSnapshotError):
            validate_immutable_deck_snapshot(snapshot)

    def test_blocked_private_keys_are_rejected_recursively_across_all_inputs(self) -> None:
        cases = [
            {"privacy_metadata": {"nested": {"raw_input": "secret"}}},
            {"metadata": {"nested": {"original_import_text": "secret"}}},
            {"source_refs": [DeckSnapshotSourceRef("user_deck", "deck", metadata={"raw_provider_payload": {}})]},
            {"analysis_refs": [DeckSnapshotAnalysisRef("analysis", "comparison", metadata={"provider_payload": {}})]},
            {
                "replay_metadata": DeckSnapshotReplayMetadata(
                    generated_by_phase="Phase 36C",
                    metadata={"nested": {"private_deck_text": "secret"}},
                )
            },
            {
                "validation_warnings": [
                    DeckSnapshotWarning(
                        warning_id="warning",
                        message="privacy warning",
                        severity="informational",
                        metadata={"private_notes": "secret"},
                    )
                ]
            },
            {"manual_review_items": [{"nested": {"private_user_notes": "secret"}}]},
            {"metadata": {"nested": [{"full_primer_body": "secret"}]}},
            {"privacy_metadata": {"nested": {"primer_body": "secret"}}},
        ]

        for kwargs in cases:
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ImmutableDeckSnapshotError):
                    _build_snapshot(**kwargs)

    def test_fixture_shapes_match_redacted_and_full_outputs(self) -> None:
        redacted_fixture = json.loads((FIXTURE_DIR / "user_deck_snapshot_redacted.json").read_text(encoding="utf-8"))
        full_fixture = json.loads((FIXTURE_DIR / "user_deck_snapshot_full.json").read_text(encoding="utf-8"))

        redacted = immutable_deck_snapshot_to_dict(_build_snapshot())
        full = immutable_deck_snapshot_to_dict(
            _build_snapshot(
                snapshot_id="snapshot-full-001",
                deck_hash="deckhash-full-001",
                cards=_sample_cards(),
                options=ImmutableDeckSnapshotOptions(include_card_entries=True),
                replay_metadata=None,
                source_refs=[],
                analysis_refs=[],
                analysis_profile_refs=[],
                validation_warnings=[],
                manual_review_items=[],
                privacy_metadata={"privacy_mode": "full_card_list"},
            )
        )

        self.assertEqual(redacted_fixture["privacy_policy"], redacted["privacy_policy"])
        self.assertNotIn("cards", redacted_fixture)
        self.assertEqual(full_fixture["privacy_policy"], full["privacy_policy"])
        self.assertEqual(full_fixture["cards"], full["cards"])

    def test_invalid_fixture_contains_blocked_private_key_shape(self) -> None:
        invalid_fixture = json.loads((FIXTURE_DIR / "user_deck_snapshot_invalid.json").read_text(encoding="utf-8"))

        with self.assertRaises(ImmutableDeckSnapshotError):
            _build_snapshot(privacy_metadata=invalid_fixture["privacy_metadata"])

    def test_user_snapshots_do_not_use_forbidden_dependencies_or_recommendation_language(self) -> None:
        module_text = (Path(__file__).parents[1] / "codie" / "user_decks" / "immutable_snapshots.py").read_text(
            encoding="utf-8"
        )
        for forbidden in (
            "codie.db",
            "sqlite3",
            "codie.providers",
            "codie.analytics",
            "codie.recommendations",
            "codie.evidence_fusion",
            "codie.decision_intelligence",
            "requests",
            "httpx",
            "openai",
            "anthropic",
            "flask",
            "fastapi",
        ):
            self.assertNotIn(forbidden, module_text)
        for forbidden_phrase in (
            "should play",
            "must include",
            "strict upgrade",
            "auto-include",
            "recommended cut",
            "recommended include",
        ):
            self.assertNotIn(forbidden_phrase, module_text)


def _build_snapshot(**overrides):
    kwargs = {
        "snapshot_id": "snapshot-001",
        "snapshot_scope": "user_deck",
        "deck_hash": "deckhash-001",
        "commander_signature": "tymna-kraum",
        "created_at": "2026-07-14T00:00:00+00:00",
        "commander_names": ["Tymna the Weaver", "Kraum, Ludevic's Opus"],
        "partner_names": ["Kraum, Ludevic's Opus"],
        "source_refs": [
            DeckSnapshotSourceRef(
                source_type="user_deck",
                source_id="user-deck-001",
                metadata={"source_layer": "user-local"},
            )
        ],
        "user_deck_ref": "user-deck-001",
        "analysis_refs": [
            DeckSnapshotAnalysisRef(
                analysis_id="analysis-001",
                analysis_type="comparison",
                analysis_profile_id="analysis-profile-competitive-default",
                analysis_profile_version="1",
                metadata={"scope": "local-user"},
            )
        ],
        "analysis_profile_refs": ["analysis-profile-competitive-default@1"],
        "cards": (),
        "privacy_metadata": {"privacy_mode": "redacted"},
        "replay_metadata": DeckSnapshotReplayMetadata(
            analysis_profile_id="analysis-profile-competitive-default",
            analysis_profile_version="1",
            weight_profile_id="competitive-default",
            weight_profile_version="1",
            evidence_version="evidence-v1",
            decision_version="decision-v1",
            source_snapshot_ids=("source-snapshot-001",),
            generated_by_phase="Phase 36C",
            metadata={"replay_scope": "local"},
        ),
        "validation_warnings": [
            DeckSnapshotWarning(
                warning_id="user-local-only",
                message="user deck snapshots are local replay packets",
                severity="informational",
                metadata={"evidence_scope": "not_tournament_evidence"},
            )
        ],
        "manual_review_items": [{"item_id": "review-001", "message": "local snapshot caveat acknowledged"}],
        "metadata": {"fixture": True},
    }
    kwargs.update(overrides)
    return build_immutable_deck_snapshot(**kwargs)


def _sample_cards() -> tuple[DeckSnapshotCard, ...]:
    return (
        DeckSnapshotCard(
            name="Command Tower",
            quantity=1,
            zone="main",
            source_order=0,
            scryfall_id="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            oracle_id="11111111-1111-1111-1111-111111111111",
        ),
        DeckSnapshotCard(
            name="Thassa's Oracle",
            quantity=1,
            zone="main",
            source_order=1,
            scryfall_id="bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
            oracle_id="22222222-2222-2222-2222-222222222222",
        ),
    )


if __name__ == "__main__":
    unittest.main()
