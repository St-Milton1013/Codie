from __future__ import annotations

import json
import unittest
from pathlib import Path

from codie.decision_intelligence import (
    DecisionIntelligenceBuildError,
    DecisionIntelligenceOptions,
    build_decision_packet,
    build_decision_packet_bundle,
    decision_packet_bundle_to_dict,
    decision_packet_to_dict,
)
from codie.evidence_fusion import (
    EvidenceAuthorityRef,
    EvidenceCaveat,
    EvidenceConflict,
    EvidenceMetricRef,
    EvidenceObservationRef,
    EvidencePrimerContextRef,
    EvidenceSimulatorRef,
    EvidenceSourceAgreement,
    UnifiedEvidenceSubject,
    build_unified_evidence_object,
)


GENERATED_AT = "2026-07-08T00:00:00+00:00"


def subject(**overrides) -> UnifiedEvidenceSubject:
    data = {
        "subject_id": "subject:card:rhystic-study",
        "subject_type": "card",
        "subject_key": "oracle:rhystic-study",
        "display_name": "Rhystic Study",
        "oracle_id": "oracle-rhystic-study",
        "scryfall_id": "scryfall-rhystic-study",
        "generated_at": GENERATED_AT,
        "metadata": {"source": "fixture"},
    }
    data.update(overrides)
    return UnifiedEvidenceSubject(**data)


def source_agreement(**overrides) -> EvidenceSourceAgreement:
    data = {
        "agreement_id": "agreement:1",
        "agreement_label": "strong",
        "supporting_ref_ids": ("metric:inclusion:rhystic-study",),
        "conflicting_ref_ids": (),
        "coverage_ratio": 0.84,
        "sample_size": 50,
        "generated_at": GENERATED_AT,
        "metadata": {"sources": 2},
    }
    data.update(overrides)
    return EvidenceSourceAgreement(**data)


def caveat(**overrides) -> EvidenceCaveat:
    data = {
        "caveat_id": "caveat:coverage",
        "caveat_type": "low_coverage",
        "severity": "warning",
        "message": "Coverage is below the preferred threshold.",
        "related_ref_ids": ("metric:inclusion:rhystic-study",),
        "generated_at": GENERATED_AT,
        "metadata": {"coverage_ratio": 0.84},
    }
    data.update(overrides)
    return EvidenceCaveat(**data)


def conflict(**overrides) -> EvidenceConflict:
    data = {
        "conflict_id": "conflict:source:1",
        "conflict_type": "source_disagreement",
        "summary": "One source reports a different card count.",
        "ref_ids": ("observation:deck:1",),
        "requires_manual_review": True,
        "generated_at": GENERATED_AT,
        "metadata": {"visible": True},
    }
    data.update(overrides)
    return EvidenceConflict(**data)


def evidence_object(**overrides):
    item_subject = overrides.pop("subject", subject())
    data = {
        "evidence_object_id": "evidence:rhystic-study",
        "subject": item_subject,
        "source_agreement": source_agreement(),
        "generated_at": GENERATED_AT,
        "authority_refs": (
            EvidenceAuthorityRef(
                authority_ref_id="authority:scryfall:rhystic-study",
                authority_type="scryfall_card",
                authority_source="scryfall",
                authority_key="scryfall-rhystic-study",
                authority_label="Rhystic Study",
                authority_url="https://scryfall.example/cards/rhystic-study",
                authority_version="fixture",
                generated_at=GENERATED_AT,
                metadata={"oracle_id": "oracle-rhystic-study"},
            ),
        ),
        "observation_refs": (
            EvidenceObservationRef(
                observation_ref_id="observation:deck:1",
                observation_type="canonical_deck_card",
                source_system="canonical",
                source_record_id="canonical_deck_card:1",
                canonical_record_id="canonical_deck:1",
                source_label="Fixture Top 16 Deck",
                source_url="https://example.test/deck/1",
                observed_at="2026-07-01",
                generated_at=GENERATED_AT,
                metadata={"placement": "top_16"},
            ),
        ),
        "metric_refs": (
            EvidenceMetricRef(
                metric_ref_id="metric:inclusion:rhystic-study",
                metric_type="inclusion_rate",
                metric_name="Top 16 inclusion rate",
                metric_value=0.42,
                metric_unit="ratio",
                scope_type="commander",
                scope_key="commander:fixture",
                window_start="2026-06-01",
                window_end="2026-07-01",
                sample_size=50,
                coverage_ratio=0.84,
                generated_at=GENERATED_AT,
                metadata={"window_days": 30},
            ),
        ),
        "primer_context_refs": (
            EvidencePrimerContextRef(
                primer_context_ref_id="primer-context:1",
                primer_ref_id="primer:1",
                context_type="strategy_summary",
                context_label="Primer context only.",
                commander_signature="Tymna the Weaver|Kraum, Ludevic's Opus",
                source_url="https://moxfield.example/primer/1",
                generated_at=GENERATED_AT,
                metadata={"body_stripped": True},
            ),
        ),
        "simulator_refs": (
            EvidenceSimulatorRef(
                simulator_ref_id="simulator:1",
                simulation_type="target_access",
                result_id="result:1",
                deck_hash="deck-hash-fixture",
                target_label="Cast Rhystic Study by turn 2",
                success_rate=0.18,
                sample_size=1000,
                unsupported_cards_count=2,
                review_status="unreviewed",
                generated_at=GENERATED_AT,
                metadata={"seed": "fixture-seed"},
            ),
        ),
        "caveats": (caveat(),),
        "conflicts": (conflict(),),
        "evidence_level": "high",
        "speculation_level": "low",
        "coverage_ratio": 0.84,
        "sample_size": 50,
        "metadata": {"source": "fixture"},
    }
    data.update(overrides)
    return build_unified_evidence_object(**data)


def decision_packet(**overrides):
    item_subject = overrides.pop("subject", subject())
    item_evidence = overrides.pop("evidence_objects", (evidence_object(subject=item_subject),))
    data = {
        "decision_id": "decision:rhystic-study:signal",
        "decision_type": "candidate_signal",
        "subject": item_subject,
        "summary": "Evidence signal for Rhystic Study.",
        "confidence": 0.72,
        "expected_impact": "medium",
        "source_agreement": source_agreement(),
        "evidence_objects": item_evidence,
        "generated_at": GENERATED_AT,
        "speculation_level": "low",
        "metadata": {"source": "fixture"},
    }
    data.update(overrides)
    return build_decision_packet(**data)


class DecisionIntelligenceBoundaryTest(unittest.TestCase):
    def test_decision_packet_requires_unified_evidence_object(self) -> None:
        with self.assertRaises(DecisionIntelligenceBuildError):
            decision_packet(evidence_objects=())

    def test_decision_packet_exposes_required_fields(self) -> None:
        payload = decision_packet_to_dict(decision_packet())

        self.assertEqual(payload["decision_id"], "decision:rhystic-study:signal")
        self.assertEqual(payload["confidence"], 0.72)
        self.assertEqual(payload["expected_impact"], "medium")
        self.assertEqual(payload["source_agreement"]["agreement_label"], "strong")
        self.assertEqual(payload["evidence_object_ids"], ["evidence:rhystic-study"])
        self.assertEqual(payload["caveat_ids"], ["caveat:coverage"])
        self.assertEqual(payload["speculation_level"], "low")

    def test_decision_packet_preserves_contradiction_visibility(self) -> None:
        payload = decision_packet_to_dict(
            decision_packet(contradicting_ref_ids=("conflict:source:1",))
        )

        self.assertEqual(payload["contradicting_ref_ids"], ["conflict:source:1"])
        self.assertEqual(payload["evidence_breakdown"]["conflict_ids"], ["conflict:source:1"])

    def test_decision_packet_distinguishes_simulator_from_tournament_evidence(self) -> None:
        payload = decision_packet_to_dict(decision_packet())
        breakdown = payload["evidence_breakdown"]

        self.assertEqual(breakdown["tournament_observation_ref_ids"], ["observation:deck:1"])
        self.assertEqual(breakdown["simulator_ref_ids"], ["simulator:1"])

    def test_decision_packet_distinguishes_primer_context_from_measured_evidence(self) -> None:
        payload = decision_packet_to_dict(decision_packet())
        breakdown = payload["evidence_breakdown"]

        self.assertEqual(breakdown["primer_context_ref_ids"], ["primer-context:1"])
        self.assertEqual(breakdown["measured_metric_ref_ids"], ["metric:inclusion:rhystic-study"])
        self.assertEqual(breakdown["authority_ref_ids"], ["authority:scryfall:rhystic-study"])

    def test_private_metadata_rejected(self) -> None:
        with self.assertRaises(DecisionIntelligenceBuildError):
            decision_packet(metadata={"raw_" + "provider_payload": {"secret": True}})
        with self.assertRaises(DecisionIntelligenceBuildError):
            decision_packet(metadata={"safe": [{"private-deck-text": "hidden"}]})

    def test_unsupported_strategic_language_rejected(self) -> None:
        bad = "you " + "should " + "play this card"

        with self.assertRaises(DecisionIntelligenceBuildError):
            decision_packet(summary=bad)

    def test_high_confidence_requires_sufficient_source_agreement(self) -> None:
        with self.assertRaises(DecisionIntelligenceBuildError):
            decision_packet(confidence=0.9, source_agreement=source_agreement(agreement_label="weak"))

    def test_high_speculation_cannot_pair_with_medium_or_high_confidence(self) -> None:
        with self.assertRaises(DecisionIntelligenceBuildError):
            decision_packet(confidence=0.5, speculation_level="high")

    def test_options_reject_invalid_limits(self) -> None:
        with self.assertRaises(DecisionIntelligenceBuildError):
            DecisionIntelligenceOptions(maximum_evidence_objects_per_packet=0)
        with self.assertRaises(DecisionIntelligenceBuildError):
            DecisionIntelligenceOptions(maximum_packets_per_bundle=0)

    def test_bundle_serializes_deterministically(self) -> None:
        item = decision_packet(metadata={"z": 2, "a": 1})
        bundle = build_decision_packet_bundle(
            bundle_id="bundle:decision:1",
            bundle_type="deck_analysis",
            subject=subject(),
            decision_packets=(item,),
            caveats=(caveat(),),
            conflicts=(conflict(),),
            generated_at=GENERATED_AT,
            metadata={"z": 2, "a": 1},
        )

        payload = decision_packet_bundle_to_dict(bundle)

        json.dumps(payload, sort_keys=True)
        self.assertEqual(payload["bundle_type"], "deck_analysis")
        self.assertEqual(list(payload["metadata"].keys()), ["a", "z"])
        self.assertEqual(payload["decision_packets"][0]["decision_id"], "decision:rhystic-study:signal")

    def test_bundle_rejects_duplicate_decision_ids(self) -> None:
        first = decision_packet()
        second = decision_packet()

        with self.assertRaises(DecisionIntelligenceBuildError):
            build_decision_packet_bundle(
                bundle_id="bundle:duplicate",
                bundle_type="deck_analysis",
                subject=subject(),
                decision_packets=(first, second),
                generated_at=GENERATED_AT,
            )

    def test_bundle_rejects_mismatched_subjects(self) -> None:
        other_subject = subject(
            subject_id="subject:card:other",
            subject_key="oracle:other",
            display_name="Other Card",
        )
        other = decision_packet(
            decision_id="decision:other",
            subject=other_subject,
            evidence_objects=(evidence_object(subject=other_subject, evidence_object_id="evidence:other"),),
        )

        with self.assertRaises(DecisionIntelligenceBuildError):
            build_decision_packet_bundle(
                bundle_id="bundle:mismatch",
                bundle_type="deck_analysis",
                subject=subject(),
                decision_packets=(other,),
                generated_at=GENERATED_AT,
            )

    def test_module_has_no_forbidden_imports_raw_sql_file_writes_server_or_llm_calls(self) -> None:
        import codie.decision_intelligence.models as models_module

        source = Path(models_module.__file__).read_text(encoding="utf-8")
        forbidden = (
            "codie." + "db",
            "codie." + "providers",
            "codie." + "repositories",
            "codie." + "ingestion",
            "codie." + "canonical",
            "codie." + "analytics",
            "codie." + "cards",
            "codie." + "probability_engine",
            "req" + "uests",
            "ht" + "tpx",
            "sqlite" + "3",
            "open" + "ai",
            "anth" + "ropic",
            "fl" + "ask",
            "fast" + "api",
            "uvi" + "corn",
            "star" + "lette",
            "SEL" + "ECT ",
            "INS" + "ERT ",
            "UPD" + "ATE ",
            "DEL" + "ETE ",
            "exec" + "ute(",
            "execute" + "script(",
            "open(",
            "write_text(",
            "write_bytes(",
            "Path(",
            "mkdir(",
            "touch(",
            "unlink(",
        )
        for pattern in forbidden:
            self.assertNotIn(pattern, source)


if __name__ == "__main__":
    unittest.main()
