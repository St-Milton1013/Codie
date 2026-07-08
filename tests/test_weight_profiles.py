from __future__ import annotations

import json
import unittest
from pathlib import Path

from codie.weight_profiles import (
    WeightComponent,
    WeightProfileBuildError,
    analysis_profile_to_dict,
    build_analysis_profile,
    build_default_weight_profiles,
    build_weight_profile,
    compare_weight_profile_versions,
    compatibility_report_to_dict,
    weight_profile_to_dict,
)


GENERATED_AT = "2026-07-08T00:00:00+00:00"


def component(**overrides) -> WeightComponent:
    data = {
        "component_id": "measured-metric",
        "component_name": "Measured Metrics",
        "component_type": "measured_metric",
        "weight": 1.0,
        "enabled": True,
        "minimum_threshold": 0.0,
        "maximum_threshold": 1.0,
        "applies_to_decision_types": ("all",),
        "description": "Measured evidence is the primary weighted signal.",
        "metadata": {"visible": True},
    }
    data.update(overrides)
    return WeightComponent(**data)


def profile(**overrides):
    data = {
        "profile_id": "competitive-default",
        "profile_name": "competitive-default",
        "profile_version": "1.0.0",
        "profile_label": "Competitive Default",
        "profile_description": "Balanced competitive evidence profile.",
        "components": (
            component(component_id="authority", component_type="authority", component_name="Authority"),
            component(),
            component(
                component_id="source-agreement",
                component_type="source_agreement",
                component_name="Source Agreement",
            ),
            component(
                component_id="simulator-comparison",
                component_type="simulator_comparison",
                component_name="Simulator Comparison",
                weight=0.5,
                metadata={"simulator_only": True, "visible": True},
            ),
            component(
                component_id="primer-context",
                component_type="primer_context",
                component_name="Primer Context",
                weight=0.2,
                minimum_threshold=None,
                maximum_threshold=None,
                metadata={"explanatory_only": True, "visible": True},
            ),
            component(
                component_id="caveat-penalty",
                component_type="caveat_penalty",
                component_name="Caveat Penalty",
                weight=-0.5,
                minimum_threshold=None,
                maximum_threshold=None,
            ),
            component(
                component_id="conflict-penalty",
                component_type="conflict_penalty",
                component_name="Conflict Penalty",
                weight=-0.75,
                minimum_threshold=None,
                maximum_threshold=None,
            ),
        ),
        "normalization_rule": "none",
        "minimum_confidence": 0.25,
        "minimum_coverage_ratio": 0.1,
        "minimum_sample_size": 1,
        "generated_at": GENERATED_AT,
        "analysis_version": "phase27b-weight-profile",
        "metadata": {"source": "fixture"},
    }
    data.update(overrides)
    return build_weight_profile(**data)


def analysis_profile(**overrides):
    data = {
        "analysis_profile_id": "analysis-profile:competitive-default",
        "analysis_profile_name": "Competitive Default Analysis",
        "analysis_profile_version": "1.0.0",
        "weight_profile_id": "competitive-default",
        "weight_profile_version": "1.0.0",
        "decision_version": "phase26b-boundary",
        "evidence_version": "phase25a-contract",
        "analysis_scope": "deck_analysis",
        "default_filters": {"minimum_sample_size": 1, "region": None},
        "generated_at": GENERATED_AT,
        "metadata": {"source": "fixture"},
    }
    data.update(overrides)
    return build_analysis_profile(**data)


class WeightProfileTest(unittest.TestCase):
    def test_weight_profile_serializes_deterministically(self) -> None:
        payload = weight_profile_to_dict(profile(metadata={"z": 2, "a": 1}))

        json.dumps(payload, sort_keys=True)
        self.assertEqual(payload["profile_id"], "competitive-default")
        self.assertEqual(list(payload["metadata"].keys()), ["a", "z"])
        self.assertEqual(
            [item["component_id"] for item in payload["components"]],
            [
                "authority",
                "caveat-penalty",
                "conflict-penalty",
                "measured-metric",
                "primer-context",
                "simulator-comparison",
                "source-agreement",
            ],
        )

    def test_analysis_profile_serializes_versions(self) -> None:
        payload = analysis_profile_to_dict(analysis_profile())

        self.assertEqual(payload["weight_profile_id"], "competitive-default")
        self.assertEqual(payload["weight_profile_version"], "1.0.0")
        self.assertEqual(payload["decision_version"], "phase26b-boundary")
        self.assertEqual(payload["evidence_version"], "phase25a-contract")

    def test_profile_ids_and_versions_are_required(self) -> None:
        with self.assertRaises(WeightProfileBuildError):
            profile(profile_id="")
        with self.assertRaises(WeightProfileBuildError):
            profile(profile_version="")
        with self.assertRaises(WeightProfileBuildError):
            analysis_profile(weight_profile_version="")

    def test_component_ids_are_unique(self) -> None:
        with self.assertRaises(WeightProfileBuildError):
            profile(components=(component(), component()))

    def test_component_weights_are_numeric_and_bounded(self) -> None:
        with self.assertRaises(WeightProfileBuildError):
            component(weight=11.0)
        with self.assertRaises(WeightProfileBuildError):
            component(weight="heavy")

    def test_disabled_components_remain_visible(self) -> None:
        payload = weight_profile_to_dict(
            profile(
                components=(
                    component(component_id="measured-metric"),
                    component(
                        component_id="disabled-user-context",
                        component_type="user_context",
                        component_name="Disabled User Context",
                        weight=0.0,
                        enabled=False,
                        minimum_threshold=None,
                        maximum_threshold=None,
                        metadata={"visible": True},
                    ),
                    component(
                        component_id="caveat-penalty",
                        component_type="caveat_penalty",
                        component_name="Caveat Penalty",
                        weight=-0.5,
                        minimum_threshold=None,
                        maximum_threshold=None,
                    ),
                    component(
                        component_id="conflict-penalty",
                        component_type="conflict_penalty",
                        component_name="Conflict Penalty",
                        weight=-0.75,
                        minimum_threshold=None,
                        maximum_threshold=None,
                    ),
                )
            )
        )

        disabled = [item for item in payload["components"] if item["component_id"] == "disabled-user-context"][0]
        self.assertFalse(disabled["enabled"])
        self.assertEqual(disabled["metadata"]["visible"], True)

    def test_default_profiles_exist_and_are_generic(self) -> None:
        profiles = build_default_weight_profiles()
        labels = {item.profile_label for item in profiles}

        self.assertEqual(
            labels,
            {
                "Competitive Default",
                "Tournament Heavy",
                "Simulation Heavy",
                "Primer Aware",
                "Budget Aware",
            },
        )
        budget = [item for item in profiles if item.profile_label == "Budget Aware"][0]
        payload = weight_profile_to_dict(budget)
        self.assertIn("Generic price-sensitivity", payload["profile_description"])
        self.assertNotIn("user_budget_limit", json.dumps(payload, sort_keys=True))

    def test_old_profile_version_replay_is_distinguishable(self) -> None:
        old = profile(profile_version="1.0.0")
        new = profile(
            profile_version="1.1.0",
            components=(
                component(component_id="authority", component_type="authority", component_name="Authority"),
                component(weight=1.2),
                component(
                    component_id="caveat-penalty",
                    component_type="caveat_penalty",
                    component_name="Caveat Penalty",
                    weight=-0.5,
                    minimum_threshold=None,
                    maximum_threshold=None,
                ),
                component(
                    component_id="conflict-penalty",
                    component_type="conflict_penalty",
                    component_name="Conflict Penalty",
                    weight=-0.75,
                    minimum_threshold=None,
                    maximum_threshold=None,
                ),
            ),
        )
        report = compare_weight_profile_versions(old, new, generated_at=GENERATED_AT)
        payload = compatibility_report_to_dict(report)

        self.assertEqual(payload["base_profile_version"], "1.0.0")
        self.assertEqual(payload["candidate_profile_version"], "1.1.0")
        self.assertFalse(payload["compatible"])
        self.assertTrue(payload["informational_only"])
        self.assertIn("measured-metric", payload["changed_component_ids"])

    def test_no_hidden_weights_all_components_serialize_visibly(self) -> None:
        payload = weight_profile_to_dict(profile())

        for item in payload["components"]:
            self.assertIn("weight", item)
            self.assertIn("enabled", item)
            self.assertIn("component_type", item)
            self.assertEqual(item["metadata"].get("visible"), True)

    def test_primer_context_cannot_replace_measured_metric(self) -> None:
        with self.assertRaises(WeightProfileBuildError):
            profile(
                components=(
                    component(
                        component_id="primer-context",
                        component_type="primer_context",
                        component_name="Primer Context",
                    ),
                    component(
                        component_id="caveat-penalty",
                        component_type="caveat_penalty",
                        component_name="Caveat Penalty",
                        weight=-0.5,
                        minimum_threshold=None,
                        maximum_threshold=None,
                    ),
                    component(
                        component_id="conflict-penalty",
                        component_type="conflict_penalty",
                        component_name="Conflict Penalty",
                        weight=-0.75,
                        minimum_threshold=None,
                        maximum_threshold=None,
                    ),
                )
            )

    def test_simulator_component_remains_simulator_only(self) -> None:
        with self.assertRaises(WeightProfileBuildError):
            profile(
                components=(
                    component(),
                    component(
                        component_id="simulator-comparison",
                        component_type="simulator_comparison",
                        component_name="Simulator Comparison",
                    ),
                    component(
                        component_id="caveat-penalty",
                        component_type="caveat_penalty",
                        component_name="Caveat Penalty",
                        weight=-0.5,
                        minimum_threshold=None,
                        maximum_threshold=None,
                    ),
                    component(
                        component_id="conflict-penalty",
                        component_type="conflict_penalty",
                        component_name="Conflict Penalty",
                        weight=-0.75,
                        minimum_threshold=None,
                        maximum_threshold=None,
                    ),
                )
            )

    def test_caveat_and_conflict_penalties_remain_visible(self) -> None:
        with self.assertRaises(WeightProfileBuildError):
            profile(
                components=(
                    component(),
                    component(
                        component_id="caveat-penalty",
                        component_type="caveat_penalty",
                        component_name="Caveat Penalty",
                        weight=-0.5,
                        enabled=False,
                        minimum_threshold=None,
                        maximum_threshold=None,
                    ),
                    component(
                        component_id="conflict-penalty",
                        component_type="conflict_penalty",
                        component_name="Conflict Penalty",
                        weight=-0.75,
                        minimum_threshold=None,
                        maximum_threshold=None,
                    ),
                )
            )

    def test_private_metadata_rejected(self) -> None:
        with self.assertRaises(WeightProfileBuildError):
            component(metadata={"raw_" + "provider_payload": {"secret": True}})
        with self.assertRaises(WeightProfileBuildError):
            profile(metadata={"safe": [{"private-deck-text": "hidden"}]})

    def test_unsupported_strategic_language_rejected(self) -> None:
        bad = "this is a strict " + "upgrade"

        with self.assertRaises(WeightProfileBuildError):
            component(description=bad)

    def test_module_has_no_forbidden_imports_raw_sql_file_writes_server_or_llm_calls(self) -> None:
        import codie.weight_profiles.models as models_module

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
