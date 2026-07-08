from __future__ import annotations

import json
import unittest
from pathlib import Path

from codie.evidence_fusion import (
    EvidenceAuthorityRef,
    EvidenceCaveat,
    EvidenceConflict,
    EvidenceFusionBuildError,
    EvidenceFusionOptions,
    EvidenceMetricRef,
    EvidenceObservationRef,
    EvidencePrimerContextRef,
    EvidenceSimulatorRef,
    EvidenceSourceAgreement,
    UnifiedEvidenceSubject,
    build_unified_evidence_bundle,
    build_unified_evidence_object,
    unified_evidence_bundle_to_dict,
    unified_evidence_object_to_dict,
)


GENERATED_AT = "2026-07-08T00:00:00+00:00"


def subject(**overrides) -> UnifiedEvidenceSubject:
    data = {
        "subject_id": "subject:card:rhystic-study",
        "subject_type": "card",
        "subject_key": "oracle:rhystic-study",
        "display_name": "Rhystic Study",
        "commander_signature": None,
        "oracle_id": "oracle-rhystic-study",
        "scryfall_id": "scryfall-rhystic-study",
        "region_code": None,
        "generated_at": GENERATED_AT,
        "metadata": {"source": "fixture"},
    }
    data.update(overrides)
    return UnifiedEvidenceSubject(**data)


def authority_ref(**overrides) -> EvidenceAuthorityRef:
    data = {
        "authority_ref_id": "authority:scryfall:rhystic-study",
        "authority_type": "scryfall_card",
        "authority_source": "scryfall",
        "authority_key": "scryfall-rhystic-study",
        "authority_label": "Rhystic Study",
        "authority_url": "https://scryfall.example/cards/rhystic-study",
        "authority_version": "fixture",
        "generated_at": GENERATED_AT,
        "metadata": {"oracle_id": "oracle-rhystic-study"},
    }
    data.update(overrides)
    return EvidenceAuthorityRef(**data)


def observation_ref(**overrides) -> EvidenceObservationRef:
    data = {
        "observation_ref_id": "observation:deck:1",
        "observation_type": "canonical_deck_card",
        "source_system": "canonical",
        "source_record_id": "canonical_deck_card:1",
        "canonical_record_id": "canonical_deck:1",
        "source_label": "Fixture Top 16 Deck",
        "source_url": "https://example.test/deck/1",
        "observed_at": "2026-07-01",
        "generated_at": GENERATED_AT,
        "metadata": {"placement": "top_16"},
    }
    data.update(overrides)
    return EvidenceObservationRef(**data)


def metric_ref(**overrides) -> EvidenceMetricRef:
    data = {
        "metric_ref_id": "metric:inclusion:rhystic-study",
        "metric_type": "inclusion_rate",
        "metric_name": "Top 16 inclusion rate",
        "metric_value": 0.42,
        "metric_unit": "ratio",
        "scope_type": "commander",
        "scope_key": "commander:fixture",
        "window_start": "2026-06-01",
        "window_end": "2026-07-01",
        "sample_size": 50,
        "coverage_ratio": 0.84,
        "generated_at": GENERATED_AT,
        "metadata": {"window_days": 30},
    }
    data.update(overrides)
    return EvidenceMetricRef(**data)


def primer_context_ref(**overrides) -> EvidencePrimerContextRef:
    data = {
        "primer_context_ref_id": "primer-context:1",
        "primer_ref_id": "primer:1",
        "context_type": "strategy_summary",
        "context_label": "Primer mentions draw density context.",
        "commander_signature": "Tymna the Weaver|Kraum, Ludevic's Opus",
        "source_url": "https://moxfield.example/primer/1",
        "generated_at": GENERATED_AT,
        "metadata": {"body_stripped": True},
    }
    data.update(overrides)
    return EvidencePrimerContextRef(**data)


def simulator_ref(**overrides) -> EvidenceSimulatorRef:
    data = {
        "simulator_ref_id": "simulator:1",
        "simulation_type": "target_access",
        "result_id": "result:1",
        "deck_hash": "deck-hash-fixture",
        "target_label": "Cast Rhystic Study by turn 2",
        "success_rate": 0.18,
        "sample_size": 1000,
        "unsupported_cards_count": 2,
        "review_status": "unreviewed",
        "generated_at": GENERATED_AT,
        "metadata": {"seed": "fixture-seed"},
    }
    data.update(overrides)
    return EvidenceSimulatorRef(**data)


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


def source_agreement(**overrides) -> EvidenceSourceAgreement:
    data = {
        "agreement_id": "agreement:1",
        "agreement_label": "strong",
        "supporting_ref_ids": ("metric:inclusion:rhystic-study", "observation:deck:1"),
        "conflicting_ref_ids": (),
        "coverage_ratio": 0.84,
        "sample_size": 50,
        "generated_at": GENERATED_AT,
        "metadata": {"sources": 2},
    }
    data.update(overrides)
    return EvidenceSourceAgreement(**data)


def evidence_object(**overrides):
    data = {
        "evidence_object_id": "evidence:rhystic-study",
        "subject": subject(),
        "source_agreement": source_agreement(),
        "generated_at": GENERATED_AT,
        "authority_refs": (authority_ref(),),
        "observation_refs": (observation_ref(),),
        "metric_refs": (metric_ref(),),
        "primer_context_refs": (primer_context_ref(),),
        "simulator_refs": (simulator_ref(),),
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


class EvidenceFusionModelTest(unittest.TestCase):
    def test_authority_ref_serializes_deterministically(self) -> None:
        payload = unified_evidence_object_to_dict(evidence_object())

        json.dumps(payload, sort_keys=True)
        self.assertEqual(payload["authority_refs"][0]["authority_source"], "scryfall")

    def test_authority_and_observation_refs_remain_visible(self) -> None:
        payload = unified_evidence_object_to_dict(evidence_object())

        self.assertEqual(
            payload["authority_refs"][0]["authority_ref_id"],
            "authority:scryfall:rhystic-study",
        )
        self.assertEqual(payload["authority_refs"][0]["authority_type"], "scryfall_card")
        self.assertEqual(payload["observation_refs"][0]["observation_ref_id"], "observation:deck:1")
        self.assertEqual(payload["observation_refs"][0]["observation_type"], "canonical_deck_card")

    def test_observation_ref_rejects_raw_provider_payload_metadata(self) -> None:
        with self.assertRaises(EvidenceFusionBuildError):
            observation_ref(metadata={"raw_" + "provider_payload": {"secret": True}})

    def test_metric_ref_preserves_sample_and_coverage(self) -> None:
        payload = unified_evidence_object_to_dict(evidence_object())

        metric = payload["metric_refs"][0]
        self.assertEqual(metric["sample_size"], 50)
        self.assertEqual(metric["coverage_ratio"], 0.84)

    def test_primer_context_rejects_full_body_metadata(self) -> None:
        with self.assertRaises(EvidenceFusionBuildError):
            primer_context_ref(metadata={"full_" + "primer_body": "not allowed"})

    def test_primer_context_remains_explanatory_and_cannot_replace_metrics(self) -> None:
        with self.assertRaises(EvidenceFusionBuildError):
            evidence_object(
                metric_refs=(),
                primer_context_refs=(primer_context_ref(),),
                evidence_level="high",
            )

    def test_primer_context_does_not_override_authority_refs(self) -> None:
        payload = unified_evidence_object_to_dict(
            evidence_object(
                authority_refs=(authority_ref(authority_label="Official card identity"),),
                primer_context_refs=(primer_context_ref(context_label="Primer context only."),),
            )
        )

        self.assertEqual(payload["authority_refs"][0]["authority_label"], "Official card identity")
        self.assertEqual(payload["authority_refs"][0]["authority_type"], "scryfall_card")
        self.assertEqual(payload["primer_context_refs"][0]["context_label"], "Primer context only.")
        self.assertEqual(payload["primer_context_refs"][0]["context_type"], "strategy_summary")

    def test_primer_context_cannot_override_source_agreement(self) -> None:
        with self.assertRaises(EvidenceFusionBuildError):
            evidence_object(
                source_agreement=source_agreement(agreement_label="weak"),
                primer_context_refs=(primer_context_ref(),),
                evidence_level="high",
            )

    def test_simulator_ref_preserves_unsupported_card_count(self) -> None:
        payload = unified_evidence_object_to_dict(evidence_object())

        self.assertEqual(payload["simulator_refs"][0]["unsupported_cards_count"], 2)

    def test_simulator_refs_remain_simulator_evidence_only(self) -> None:
        payload = unified_evidence_object_to_dict(evidence_object())

        self.assertEqual(payload["simulator_refs"][0]["simulator_ref_id"], "simulator:1")
        self.assertEqual(payload["simulator_refs"][0]["simulation_type"], "target_access")
        self.assertNotIn("simulator_ref_id", payload["observation_refs"][0])
        self.assertNotEqual(payload["observation_refs"][0]["observation_type"], "simulator_statistic")

    def test_caveats_conflicts_and_agreement_remain_visible(self) -> None:
        payload = unified_evidence_object_to_dict(evidence_object())

        self.assertEqual(payload["caveats"][0]["caveat_type"], "low_coverage")
        self.assertEqual(payload["conflicts"][0]["conflict_type"], "source_disagreement")
        self.assertEqual(payload["source_agreement"]["agreement_label"], "strong")

    def test_unified_evidence_bundle_serializes_deterministically(self) -> None:
        bundle = build_unified_evidence_bundle(
            bundle_id="bundle:deck-analysis",
            bundle_type="deck_analysis",
            subject=subject(),
            evidence_objects=(evidence_object(),),
            caveats=(caveat(),),
            conflicts=(conflict(),),
            generated_at=GENERATED_AT,
            metadata={"z": 2, "a": 1},
        )

        payload = unified_evidence_bundle_to_dict(bundle)

        json.dumps(payload, sort_keys=True)
        self.assertEqual(payload["bundle_type"], "deck_analysis")
        self.assertEqual(list(payload["metadata"].keys()), ["a", "z"])

    def test_high_evidence_requires_metric_ref(self) -> None:
        with self.assertRaises(EvidenceFusionBuildError):
            evidence_object(metric_refs=(), evidence_level="high")

    def test_high_evidence_requires_sufficient_source_agreement(self) -> None:
        with self.assertRaises(EvidenceFusionBuildError):
            evidence_object(source_agreement=source_agreement(agreement_label="weak"))

    def test_high_speculation_cannot_pair_with_medium_evidence(self) -> None:
        with self.assertRaises(EvidenceFusionBuildError):
            evidence_object(evidence_level="medium", speculation_level="high")

    def test_speculation_level_remains_visible_in_object_and_bundle_serialization(self) -> None:
        item = evidence_object(evidence_level="low", speculation_level="medium")
        bundle = build_unified_evidence_bundle(
            bundle_id="bundle:speculation",
            bundle_type="deck_analysis",
            subject=subject(),
            evidence_objects=(item,),
            generated_at=GENERATED_AT,
        )

        object_payload = unified_evidence_object_to_dict(item)
        bundle_payload = unified_evidence_bundle_to_dict(bundle)

        self.assertEqual(object_payload["speculation_level"], "medium")
        self.assertEqual(
            bundle_payload["evidence_objects"][0]["speculation_level"],
            "medium",
        )

    def test_options_reject_invalid_limits(self) -> None:
        with self.assertRaises(EvidenceFusionBuildError):
            EvidenceFusionOptions(maximum_refs_per_object=0)

    def test_options_can_disable_primer_context_simulator_and_conflicts(self) -> None:
        with self.assertRaises(EvidenceFusionBuildError):
            evidence_object(options=EvidenceFusionOptions(allow_primer_context=False))
        with self.assertRaises(EvidenceFusionBuildError):
            evidence_object(options=EvidenceFusionOptions(allow_simulator_refs=False))
        with self.assertRaises(EvidenceFusionBuildError):
            evidence_object(options=EvidenceFusionOptions(allow_conflicts=False))

    def test_bundle_rejects_duplicate_object_ids(self) -> None:
        first = evidence_object()
        second = evidence_object()

        with self.assertRaises(EvidenceFusionBuildError):
            build_unified_evidence_bundle(
                bundle_id="bundle:duplicates",
                bundle_type="deck_analysis",
                subject=subject(),
                evidence_objects=(first, second),
                generated_at=GENERATED_AT,
            )

    def test_bundle_rejects_mismatched_subjects(self) -> None:
        other_subject = subject(subject_id="subject:card:other", subject_key="oracle:other", display_name="Other Card")
        other = evidence_object(evidence_object_id="evidence:other", subject=other_subject)

        with self.assertRaises(EvidenceFusionBuildError):
            build_unified_evidence_bundle(
                bundle_id="bundle:mismatch",
                bundle_type="deck_analysis",
                subject=subject(),
                evidence_objects=(other,),
                generated_at=GENERATED_AT,
            )

    def test_nested_private_metadata_keys_fail_cleanly(self) -> None:
        with self.assertRaises(EvidenceFusionBuildError):
            evidence_object(metadata={"safe": [{"private-deck-text": "hidden"}]})

    def test_forbidden_strategic_language_fails_cleanly(self) -> None:
        bad = "you " + "should " + "play this card"

        with self.assertRaises(EvidenceFusionBuildError):
            caveat(message=bad)

    def test_module_has_no_forbidden_imports_raw_sql_file_writes_server_or_llm_calls(self) -> None:
        import codie.evidence_fusion.models as models_module

        source = Path(models_module.__file__).read_text(encoding="utf-8")
        forbidden = (
            "codie." + "db",
            "codie." + "providers",
            "codie." + "analytics",
            "codie." + "recommendations",
            "codie." + "ingestion",
            "codie." + "cards",
            "codie." + "probability_engine",
            "codie." + "canonical",
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
