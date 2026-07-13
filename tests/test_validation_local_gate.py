from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

from codie.validation.local_gate import (
    REPOSITORY,
    SCHEMA_VERSION,
    ValidationFinding,
    ValidationGateError,
    ValidationGateOptions,
    ValidatorReport,
    aggregate_validator_reports,
    parse_validator_json,
    run_ollama_validator,
    validate_report_payload,
)


SHA = "a" * 40


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
    data = {
        "phase_id": "Phase35A",
        "phase_part": "outside-validation",
        "gate_scope": "INTERMEDIATE_PACKET",
        "repository": REPOSITORY,
        "branch": "codex/operational-local-validation-bootstrap",
        "target_sha": SHA,
        "validator": "deterministic",
        "result": "CLEAN_PASS",
        "findings": (),
        "errors": (),
    }
    data.update(overrides)
    return ValidatorReport(**data)


def report_payload(**overrides):
    payload = {
        "schema_version": SCHEMA_VERSION,
        "phase_id": "Phase35A",
        "phase_part": "outside-validation",
        "gate_scope": "INTERMEDIATE_PACKET",
        "repository": REPOSITORY,
        "branch": "codex/operational-local-validation-bootstrap",
        "target_sha": SHA,
        "validator": "architecture",
        "result": "CLEAN_PASS",
        "model": "qwen2.5-coder:7b",
        "generated_at": "2026-07-13T00:00:00+00:00",
        "commands": [],
        "findings": [],
        "errors": [],
    }
    payload.update(overrides)
    return payload


class ValidationLocalGateTest(unittest.TestCase):
    def test_valid_clean_reports_aggregate_to_clean_pass(self) -> None:
        result = aggregate_validator_reports(
            (
                report(validator="deterministic"),
                report(validator="architecture", model="qwen2.5-coder:7b"),
                report(validator="adversarial", model="llama3.1:latest"),
            ),
            SHA,
        )

        self.assertEqual(result.result, "CLEAN_PASS")

    def test_malformed_json_fails(self) -> None:
        with self.assertRaises(ValidationGateError):
            parse_validator_json("{not-json")

    def test_schema_violations_fail(self) -> None:
        payload = report_payload()
        del payload["validator"]

        with self.assertRaises(ValidationGateError):
            validate_report_payload(payload)

    def test_stale_sha_is_rejected(self) -> None:
        result = aggregate_validator_reports((report(target_sha="b" * 40),), SHA)

        self.assertEqual(result.result, "STALE_RESULTS")

    def test_wrong_phase_is_constitution_conflict(self) -> None:
        result = aggregate_validator_reports((report(phase_id="Phase35B"),), SHA)

        self.assertEqual(result.result, "CONSTITUTION_CONFLICT")

    def test_duplicate_findings_fail(self) -> None:
        with self.assertRaises(ValidationGateError):
            report(findings=(finding(), finding()))

    def test_contradictory_findings_fail(self) -> None:
        with self.assertRaises(ValidationGateError):
            report(
                findings=(
                    finding(finding_id="finding:1", resolution_status="OPEN"),
                    finding(finding_id="finding:2", resolution_status="RESOLVED"),
                )
            )

    def test_intermediate_severity_policy_allows_medium_and_low_notes(self) -> None:
        result = aggregate_validator_reports(
            (
                report(
                    result="CLEAN_PASS",
                    findings=(
                        finding(finding_id="finding:medium", severity="MEDIUM"),
                        finding(finding_id="finding:low", severity="LOW"),
                    ),
                ),
            ),
            SHA,
        )

        self.assertEqual(result.result, "CLEAN_PASS")

    def test_final_clean_pass_policy_rejects_medium_and_low(self) -> None:
        result = aggregate_validator_reports(
            (
                report(
                    gate_scope="FINAL_PHASE",
                    result="CLEAN_PASS",
                    findings=(finding(finding_id="finding:medium", severity="MEDIUM"),),
                ),
            ),
            SHA,
        )

        self.assertEqual(result.result, "REPAIR_REQUIRED")

    def test_validator_failure_requires_repair(self) -> None:
        result = aggregate_validator_reports(
            (report(result="FAIL", findings=(finding(),)),),
            SHA,
        )

        self.assertEqual(result.result, "REPAIR_REQUIRED")

    def test_ollama_unavailable_is_validator_error(self) -> None:
        options = ValidationGateOptions(
            phase_id="Phase35A",
            phase_part="outside-validation",
            gate_scope="INTERMEDIATE_PACKET",
            target_sha=SHA,
            branch="codex/operational-local-validation-bootstrap",
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
            ),
            SHA,
        )

        self.assertEqual(result.result, "COST_POLICY_VIOLATION")

    def test_ollama_json_report_is_validated(self) -> None:
        options = ValidationGateOptions(
            phase_id="Phase35A",
            phase_part="outside-validation",
            gate_scope="INTERMEDIATE_PACKET",
            target_sha=SHA,
            branch="codex/operational-local-validation-bootstrap",
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
            phase_id="Phase35A",
            phase_part="outside-validation",
            gate_scope="INTERMEDIATE_PACKET",
            target_sha=SHA,
            branch="codex/operational-local-validation-bootstrap",
        )

        def failing_runner(_model: str, _prompt: str) -> str:
            raise subprocess.CalledProcessError(1, "ollama", stderr="model missing")

        output = run_ollama_validator("adversarial", options, Path.cwd(), ollama_runner=failing_runner)

        self.assertEqual(output.result, "ERROR")
        self.assertEqual(output.errors, ("model missing",))


if __name__ == "__main__":
    unittest.main()
