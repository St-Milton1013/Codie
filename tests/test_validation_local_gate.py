from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from codie.validation.local_gate import (
    CONSTITUTION_VERSION,
    CURRENT_EXPECTED_PHASE_ID,
    REPOSITORY,
    SCHEMA_VERSION,
    SeverityTotals,
    ValidationFinding,
    ValidationGateError,
    ValidationGateOptions,
    ValidatorReport,
    aggregate_validator_reports,
    parse_validator_json,
    report_json_schema,
    resolve_active_phase,
    _run_ollama,
    run_ollama_validator,
    validate_report_payload,
    validator_report_to_dict,
)


SHA = "a" * 40
BRANCH = "codex/operational-local-validation-bootstrap"
PR_NUMBER = 1


def finding(**overrides) -> ValidationFinding:
    data = {
        "finding_id": "finding:1",
        "severity": "HIGH",
        "finding": "A high-severity validation issue remains.",
        "affected_files": ("codie/example.py",),
        "governing_rule": "Implementation Quality Gate",
        "required_correction": "Repair the high-severity issue.",
        "resolution_status": "OPEN",
    }
    data.update(overrides)
    return ValidationFinding(**data)


def report(**overrides) -> ValidatorReport:
    findings = tuple(overrides.pop("findings", ()))
    data = {
        "phase_id": CURRENT_EXPECTED_PHASE_ID,
        "phase_part": "outside-validation",
        "gate_scope": "INTERMEDIATE_PACKET",
        "repository": REPOSITORY,
        "branch": BRANCH,
        "target_sha": SHA,
        "pull_request_number": PR_NUMBER,
        "validator": "deterministic",
        "result": "CLEAN_PASS",
        "constitution_path": "docs/CODIE_V1_CONSTITUTION.md",
        "constitution_version": CONSTITUTION_VERSION,
        "started_at": "2026-07-13T00:00:00+00:00",
        "completed_at": "2026-07-13T00:01:00+00:00",
        "severity_totals": SeverityTotals.from_findings(findings),
        "findings": findings,
        "errors": (),
    }
    data.update(overrides)
    return ValidatorReport(**data)


def three_reports(**overrides):
    return (
        report(validator="deterministic", **overrides),
        report(validator="architecture", model="qwen2.5-coder:7b", **overrides),
        report(validator="adversarial", model="llama3.1:latest", **overrides),
    )


def report_payload(**overrides):
    payload = validator_report_to_dict(report(validator="architecture", model="qwen2.5-coder:7b"))
    payload.update(overrides)
    return payload


class ValidationLocalGateTest(unittest.TestCase):
    def test_valid_clean_reports_aggregate_to_clean_pass(self) -> None:
        result = aggregate_validator_reports(three_reports(), SHA)

        self.assertEqual(result.result, "CLEAN_PASS")

    def test_missing_validator_is_rejected(self) -> None:
        result = aggregate_validator_reports(
            (report(validator="deterministic"), report(validator="architecture", model="qwen2.5-coder:7b")),
            SHA,
        )

        self.assertEqual(result.result, "VALIDATOR_ERROR")
        self.assertIn("missing validators: adversarial", result.errors)

    def test_duplicate_validator_is_rejected(self) -> None:
        result = aggregate_validator_reports(
            (
                report(validator="deterministic"),
                report(validator="deterministic"),
                report(validator="adversarial", model="llama3.1:latest"),
            ),
            SHA,
        )

        self.assertEqual(result.result, "VALIDATOR_ERROR")
        self.assertIn("duplicate validators: deterministic", result.errors)

    def test_cross_validator_contradiction_requires_human_review(self) -> None:
        result = aggregate_validator_reports(
            (
                report(validator="deterministic", result="FAIL", findings=(finding(resolution_status="OPEN"),)),
                report(
                    validator="architecture",
                    model="qwen2.5-coder:7b",
                    findings=(finding(finding_id="finding:2", resolution_status="RESOLVED"),),
                ),
                report(validator="adversarial", model="llama3.1:latest"),
            ),
            SHA,
        )

        self.assertEqual(result.result, "HUMAN_REVIEW_REQUIRED")

    def test_mismatched_phase_part_is_rejected(self) -> None:
        result = aggregate_validator_reports(
            (
                report(validator="deterministic"),
                report(validator="architecture", model="qwen2.5-coder:7b", phase_part="wrong"),
                report(validator="adversarial", model="llama3.1:latest"),
            ),
            SHA,
        )

        self.assertEqual(result.result, "VALIDATOR_ERROR")

    def test_mismatched_gate_scope_is_rejected(self) -> None:
        result = aggregate_validator_reports(
            (
                report(validator="deterministic"),
                report(validator="architecture", model="qwen2.5-coder:7b", gate_scope="FINAL_PHASE"),
                report(validator="adversarial", model="llama3.1:latest"),
            ),
            SHA,
        )

        self.assertEqual(result.result, "VALIDATOR_ERROR")

    def test_mismatched_branch_is_rejected(self) -> None:
        result = aggregate_validator_reports(
            (
                report(validator="deterministic"),
                report(validator="architecture", model="qwen2.5-coder:7b", branch="wrong"),
                report(validator="adversarial", model="llama3.1:latest"),
            ),
            SHA,
        )

        self.assertEqual(result.result, "VALIDATOR_ERROR")

    def test_stale_sha_is_rejected(self) -> None:
        result = aggregate_validator_reports(
            (
                report(validator="deterministic"),
                report(validator="architecture", model="qwen2.5-coder:7b", target_sha="b" * 40),
                report(validator="adversarial", model="llama3.1:latest"),
            ),
            SHA,
        )

        self.assertEqual(result.result, "STALE_RESULTS")

    def test_phase35b_can_become_active_without_source_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs" / "ACTIVE_ROADMAP_INDEX.md").write_text(
                "## Current Phase 35B Outside Validation Packet\n",
                encoding="utf-8",
            )

            self.assertEqual(resolve_active_phase(root), "Phase35B")

    def test_malformed_json_fails(self) -> None:
        with self.assertRaises(ValidationGateError):
            parse_validator_json("{not-json")

    def test_schema_violations_fail(self) -> None:
        payload = report_payload()
        del payload["validator"]

        with self.assertRaises(ValidationGateError):
            validate_report_payload(payload)

    def test_invalid_pr_number_fails_schema(self) -> None:
        payload = report_payload(pull_request_number=0)

        with self.assertRaises(ValidationGateError):
            validate_report_payload(payload)

    def test_schema_runtime_drift_prevention(self) -> None:
        schema = report_json_schema()

        self.assertIn("pull_request_number", schema["required"])
        self.assertIn("severity_totals", schema["required"])

    def test_intermediate_severity_policy_allows_medium_and_low_notes(self) -> None:
        result = aggregate_validator_reports(
            (
                report(validator="deterministic", findings=(finding(finding_id="finding:medium", severity="MEDIUM"),)),
                report(validator="architecture", model="qwen2.5-coder:7b"),
                report(validator="adversarial", model="llama3.1:latest"),
            ),
            SHA,
        )

        self.assertEqual(result.result, "CLEAN_PASS")

    def test_final_clean_pass_policy_rejects_medium_and_low(self) -> None:
        result = aggregate_validator_reports(
            three_reports(gate_scope="FINAL_PHASE", result="CLEAN_PASS", findings=(finding(severity="MEDIUM"),)),
            SHA,
        )

        self.assertEqual(result.result, "REPAIR_REQUIRED")

    def test_validator_failure_requires_repair(self) -> None:
        result = aggregate_validator_reports(
            (
                report(validator="deterministic", result="FAIL", findings=(finding(),)),
                report(validator="architecture", model="qwen2.5-coder:7b"),
                report(validator="adversarial", model="llama3.1:latest"),
            ),
            SHA,
        )

        self.assertEqual(result.result, "REPAIR_REQUIRED")

    def test_ollama_unavailable_is_validator_error(self) -> None:
        options = ValidationGateOptions(
            phase_id=CURRENT_EXPECTED_PHASE_ID,
            phase_part="outside-validation",
            gate_scope="INTERMEDIATE_PACKET",
            target_sha=SHA,
            pull_request_number=PR_NUMBER,
            branch=BRANCH,
        )

        report_result = run_ollama_validator(
            "architecture",
            options,
            Path.cwd(),
            ollama_runner=lambda _model, _prompt: (_ for _ in ()).throw(FileNotFoundError()),
        )

        self.assertEqual(report_result.result, "ERROR")
        self.assertIn("Ollama executable is unavailable.", report_result.errors)

    def test_cost_policy_violation_is_reported(self) -> None:
        result = aggregate_validator_reports(
            (
                report(
                    validator="deterministic",
                    result="FAIL",
                    findings=(
                        finding(
                            finding_id="cost-policy:environment",
                            severity="BLOCKER",
                            governing_rule="Zero Cost Requirement",
                            finding="Forbidden paid API key environment variable is set.",
                        ),
                    ),
                ),
                report(validator="architecture", model="qwen2.5-coder:7b"),
                report(validator="adversarial", model="llama3.1:latest"),
            ),
            SHA,
        )

        self.assertEqual(result.result, "COST_POLICY_VIOLATION")

    def test_ollama_json_report_is_validated(self) -> None:
        options = ValidationGateOptions(
            phase_id=CURRENT_EXPECTED_PHASE_ID,
            phase_part="outside-validation",
            gate_scope="INTERMEDIATE_PACKET",
            target_sha=SHA,
            pull_request_number=PR_NUMBER,
            branch=BRANCH,
        )
        payload = report_payload()

        output = run_ollama_validator(
            "architecture",
            options,
            Path.cwd(),
            ollama_runner=lambda _model, _prompt: json.dumps(payload),
        )

        self.assertEqual(output.result, "CLEAN_PASS")

    def test_ollama_called_process_error_becomes_error_report(self) -> None:
        options = ValidationGateOptions(
            phase_id=CURRENT_EXPECTED_PHASE_ID,
            phase_part="outside-validation",
            gate_scope="INTERMEDIATE_PACKET",
            target_sha=SHA,
            pull_request_number=PR_NUMBER,
            branch=BRANCH,
        )

        def failing_runner(_model: str, _prompt: str) -> str:
            raise subprocess.CalledProcessError(1, "ollama", stderr="model missing")

        output = run_ollama_validator("adversarial", options, Path.cwd(), ollama_runner=failing_runner)

        self.assertEqual(output.result, "ERROR")
        self.assertEqual(output.errors, ("model missing",))

    def test_ollama_malformed_json_becomes_error_report(self) -> None:
        options = ValidationGateOptions(
            phase_id=CURRENT_EXPECTED_PHASE_ID,
            phase_part="outside-validation",
            gate_scope="INTERMEDIATE_PACKET",
            target_sha=SHA,
            pull_request_number=PR_NUMBER,
            branch=BRANCH,
        )

        output = run_ollama_validator(
            "architecture",
            options,
            Path.cwd(),
            ollama_runner=lambda _model, _prompt: "not-json",
        )

        self.assertEqual(output.result, "ERROR")
        self.assertIn("malformed validator JSON", output.errors[0])

    def test_run_ollama_requests_json_format_and_sends_prompt_on_stdin(self) -> None:
        calls = []

        def fake_run(command, **kwargs):
            calls.append((command, kwargs))
            return subprocess.CompletedProcess(command, 0, stdout='{"ok": true}', stderr="")

        original_run = subprocess.run
        try:
            subprocess.run = fake_run
            output = _run_ollama("llama3.1:latest", "validator prompt")
        finally:
            subprocess.run = original_run

        self.assertEqual(output, '{"ok": true}')
        command, kwargs = calls[0]
        self.assertEqual(command, ("ollama", "run", "llama3.1:latest", "--format", "json"))
        self.assertEqual(kwargs["input"], "validator prompt")
        self.assertTrue(kwargs["capture_output"])
        self.assertTrue(kwargs["check"])


if __name__ == "__main__":
    unittest.main()
