from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
import sys
from pathlib import Path
from unittest import mock

from codie.validation.local_gate import (
    ACTIVE_VALIDATION_SCOPE_SCHEMA_VERSION,
    ACTIVE_VALIDATION_SCOPE_PATH,
    ActiveValidationScope,
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
    authoritative_active_validation_scope,
    model_response_json_schema,
    parse_model_validator_json,
    parse_validator_json,
    report_json_schema,
    resolve_active_phase,
    resolve_active_validation_scope,
    _run_ollama,
    _portable_python_executable,
    run_ollama_validator,
    run_validation_gate,
    validate_report_payload,
    validator_report_from_model_response,
    validator_report_to_dict,
    _changed_files_for_scan,
    _content_scan_text,
    _phase_ledger_findings,
)


SHA = "a" * 40
BRANCH = "codex/operational-local-validation-bootstrap"
PR_NUMBER = 1


def write_scope(root: Path, *, phase_id: str = "Phase35B", phase_part: str = "outside-validation", gate_scope: str = "INTERMEDIATE_PACKET") -> None:
    path = root / ACTIVE_VALIDATION_SCOPE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "schema_version": ACTIVE_VALIDATION_SCOPE_SCHEMA_VERSION,
                "phase_id": phase_id,
                "phase_part": phase_part,
                "gate_scope": gate_scope,
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


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


def model_payload(**overrides):
    payload = {
        "result": "FAIL",
        "findings": [
            {
                "severity": "HIGH",
                "title": "Architecture boundary leak",
                "description": "The changed file imports a forbidden module.",
                "affected_files": ["codie/validation/local_gate.py"],
                "governing_rule": "Architecture Boundary",
                "required_correction": "Remove the forbidden import.",
            }
        ],
    }
    payload.update(overrides)
    return payload


class ValidationLocalGateTest(unittest.TestCase):
    def test_valid_clean_reports_aggregate_to_clean_pass(self) -> None:
        result = aggregate_validator_reports(three_reports(), SHA)

        self.assertEqual(result.result, "CLEAN_PASS")

    def test_aggregate_records_manual_snapshot_metadata_and_skipped_validators(self) -> None:
        result = aggregate_validator_reports(
            three_reports(),
            SHA,
            target_ref="main",
            validation_scope="full_project",
            validator_profile="deterministic",
            skipped_validators=("architecture", "adversarial"),
        )
        payload = validator_report_to_dict(result.reports[0])
        aggregate_payload = {
            "target_ref": result.target_ref,
            "validation_scope": result.validation_scope,
            "validator_profile": result.validator_profile,
            "skipped_validators": result.skipped_validators,
        }

        self.assertEqual(result.result, "CLEAN_PASS")
        self.assertEqual(payload["target_sha"], SHA)
        self.assertEqual(aggregate_payload["target_ref"], "main")
        self.assertEqual(aggregate_payload["validation_scope"], "full_project")
        self.assertEqual(aggregate_payload["validator_profile"], "deterministic")
        self.assertEqual(aggregate_payload["skipped_validators"], ("adversarial", "architecture"))

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

    def test_preflight_stale_sha_not_overwritten_by_missing_validators(self) -> None:
        result = aggregate_validator_reports(
            (
                report(
                    validator="deterministic",
                    result="FAIL",
                    findings=(
                        finding(
                            finding_id="security:stale-sha",
                            severity="BLOCKER",
                            governing_rule="Exact SHA validation",
                            required_correction="Dispatch validation for the current pull request head SHA.",
                        ),
                    ),
                ),
            ),
            SHA,
        )

        self.assertEqual(result.result, "STALE_RESULTS")
        self.assertIn("missing validators: adversarial, architecture", result.errors)

    def test_preflight_cost_policy_not_overwritten_by_missing_validators(self) -> None:
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
                            required_correction="Remove paid/cloud API usage and rerun validation.",
                        ),
                    ),
                ),
            ),
            SHA,
        )

        self.assertEqual(result.result, "COST_POLICY_VIOLATION")
        self.assertIn("missing validators: adversarial, architecture", result.errors)

    def test_preflight_constitution_conflict_not_overwritten_by_missing_validators(self) -> None:
        result = aggregate_validator_reports(
            (
                report(
                    validator="deterministic",
                    result="FAIL",
                    findings=(
                        finding(
                            finding_id="security:phase",
                            severity="BLOCKER",
                            governing_rule="CONSTITUTION_CONFLICT",
                            required_correction="Use the authoritative repository validation scope.",
                        ),
                    ),
                ),
            ),
            SHA,
        )

        self.assertEqual(result.result, "CONSTITUTION_CONFLICT")
        self.assertIn("missing validators: adversarial, architecture", result.errors)

    def test_validator_rule_text_is_excluded_from_static_content_scan(self) -> None:
        rule_phrase = "recommended " + "include"
        text = '\n'.join(
            (
                f'    "{rule_phrase}",',
                '    finding="Placeholder or TODO language is present in changed PR content.",',
                '    finding="Real TODO remains in production logic.",',
            )
        )

        scan_text = _content_scan_text("codie/validation/local_gate.py", text)

        self.assertNotIn(rule_phrase, scan_text)
        self.assertNotIn("Placeholder or TODO language", scan_text)
        self.assertIn("Real TODO remains", scan_text)
        self.assertNotIn(rule_phrase, _content_scan_text("tests/test_validation_local_gate.py", text))

    def test_guardrail_literal_blocks_are_excluded_from_static_content_scan(self) -> None:
        guarded_phrase = "must " + "include"
        visible_phrase = "you " + "should " + "play this card"
        text = '\n'.join(
            (
                "FORBIDDEN_COMPARISON_FRAGMENTS = (",
                '    "' + "should " + 'play",',
                f'    "{guarded_phrase}",',
                ")",
                f'USER_VISIBLE_TEXT = "{visible_phrase}"',
            )
        )

        scan_text = _content_scan_text("codie/user_decks/evidence_comparison.py", text)

        self.assertNotIn(guarded_phrase, scan_text)
        self.assertIn(visible_phrase, scan_text)

    def test_phase35b_can_become_active_without_source_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_scope(root, phase_id="Phase35B")

            self.assertEqual(resolve_active_phase(root), "Phase35B")

    def test_active_scope_resolves_phase_part_and_gate_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_scope(root, phase_id="Phase35B", gate_scope="INTERMEDIATE_PACKET")

            scope = resolve_active_validation_scope(root)

            self.assertEqual(scope.phase_id, "Phase35B")
            self.assertEqual(scope.phase_part, "outside-validation")
            self.assertEqual(scope.gate_scope, "INTERMEDIATE_PACKET")

    def test_historical_final_phase_prose_cannot_alter_active_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            write_scope(root, phase_id="Phase35B", gate_scope="INTERMEDIATE_PACKET")
            (root / "docs" / "ACTIVE_ROADMAP_INDEX.md").write_text(
                "Current action: send Phase 35Z final phase outside validation packet\n",
                encoding="utf-8",
            )
            (root / "docs" / "NEXT_PHASE_CONTRACT.md").write_text(
                "Phase 35Z is the final phase outside validation gate.\n",
                encoding="utf-8",
            )

            scope = resolve_active_validation_scope(root)

            self.assertEqual(scope.phase_id, "Phase35B")
            self.assertEqual(scope.phase_part, "outside-validation")
            self.assertEqual(scope.gate_scope, "INTERMEDIATE_PACKET")

    def test_phase_ledger_allows_distinct_historical_token_sets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_scope(root, phase_id="Phase37A", gate_scope="INTERMEDIATE_PACKET")
            (root / "docs" / "ACTIVE_ROADMAP_INDEX.md").write_text(
                "Phase 31R accepted. Current action: Phase 37A outside validation.\n",
                encoding="utf-8",
            )
            (root / "docs" / "VALIDATION_STATUS_INDEX.md").write_text(
                "Phase 0 through Phase 36C accepted. Phase37A internal pass.\n",
                encoding="utf-8",
            )
            (root / "docs" / "NEXT_PHASE_CONTRACT.md").write_text(
                "Historical note: Phase 22C. Current gate: Phase 37A.\n",
                encoding="utf-8",
            )
            (root / "docs" / "CODEX_CONTINUITY_HANDOFF.md").write_text(
                "Long-form continuity mentions Phase 12C, Phase 13Z, and Phase 37A.\n",
                encoding="utf-8",
            )

            findings = _phase_ledger_findings(root)

            self.assertEqual(findings, ())

    def test_phase_ledger_rejects_missing_active_phase_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_scope(root, phase_id="Phase37A", gate_scope="INTERMEDIATE_PACKET")
            for relative in (
                "docs/ACTIVE_ROADMAP_INDEX.md",
                "docs/VALIDATION_STATUS_INDEX.md",
                "docs/CODEX_CONTINUITY_HANDOFF.md",
            ):
                path = root / relative
                path.write_text("Current gate: Phase 37A.\n", encoding="utf-8")
            (root / "docs" / "NEXT_PHASE_CONTRACT.md").write_text(
                "Historical note only: Phase 22C.\n",
                encoding="utf-8",
            )

            findings = _phase_ledger_findings(root)

            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0].finding_id, "phase-ledger:active-phase-missing")
            self.assertEqual(findings[0].affected_files, ("docs/NEXT_PHASE_CONTRACT.md",))

    def test_phase_ledger_invalid_active_phase_id_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_scope(root, phase_id="not-a-phase", gate_scope="INTERMEDIATE_PACKET")

            findings = _phase_ledger_findings(root)

            self.assertEqual(len(findings), 5)
            self.assertTrue(any(finding.finding_id == "phase-ledger:active-scope-invalid" for finding in findings))

    def test_missing_active_scope_declaration_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValidationGateError):
                resolve_active_validation_scope(Path(tmp))

    def test_duplicate_active_scope_declaration_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / ACTIVE_VALIDATION_SCOPE_PATH
            path.parent.mkdir(parents=True)
            path.write_text(
                '{"schema_version":"codie.active_validation_scope.v1","phase_id":"Phase35B","phase_id":"Phase35C","phase_part":"outside-validation","gate_scope":"INTERMEDIATE_PACKET"}',
                encoding="utf-8",
            )

            with self.assertRaises(ValidationGateError):
                resolve_active_validation_scope(root)

    def test_invalid_active_scope_declaration_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_scope(root, gate_scope="BAD_SCOPE")

            with self.assertRaises(ValidationGateError):
                resolve_active_validation_scope(root)

    def test_pr_head_scope_change_cannot_weaken_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_scope(root, phase_id="Phase35B", gate_scope="INTERMEDIATE_PACKET")
            base_text = json.dumps(
                {
                    "schema_version": ACTIVE_VALIDATION_SCOPE_SCHEMA_VERSION,
                    "phase_id": "Phase35B",
                    "phase_part": "outside-validation",
                    "gate_scope": "FINAL_PHASE",
                },
                sort_keys=True,
            )
            with mock.patch("codie.validation.local_gate._git_show_text", return_value=base_text):
                scope, conflict = authoritative_active_validation_scope(root, "main")

            self.assertEqual(scope.gate_scope, "FINAL_PHASE")
            self.assertIn("modified active validation scope", conflict)

    def test_base_branch_scope_is_authoritative(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base_text = json.dumps(
                {
                    "schema_version": ACTIVE_VALIDATION_SCOPE_SCHEMA_VERSION,
                    "phase_id": "Phase35B",
                    "phase_part": "outside-validation",
                    "gate_scope": "INTERMEDIATE_PACKET",
                },
                sort_keys=True,
            ) + "\n"
            (root / ACTIVE_VALIDATION_SCOPE_PATH).parent.mkdir(parents=True, exist_ok=True)
            (root / ACTIVE_VALIDATION_SCOPE_PATH).write_text(base_text, encoding="utf-8")
            with mock.patch("codie.validation.local_gate._git_show_text", return_value=base_text):
                scope, conflict = authoritative_active_validation_scope(root, "main")

            self.assertEqual(scope.phase_id, "Phase35B")
            self.assertEqual(scope.gate_scope, "INTERMEDIATE_PACKET")
            self.assertEqual(conflict, "")

    def test_full_project_scope_uses_tracked_production_and_harness_files(self) -> None:
        options = ValidationGateOptions(
            phase_id=CURRENT_EXPECTED_PHASE_ID,
            phase_part="outside-validation",
            gate_scope="INTERMEDIATE_PACKET",
            target_sha=SHA,
            pull_request_number=PR_NUMBER,
            branch=BRANCH,
            validation_scope="full_project",
        )

        with mock.patch(
            "codie.validation.local_gate._run_command",
            return_value=subprocess.CompletedProcess(
                ("git", "ls-files"),
                0,
                stdout="\n".join(
                    (
                        "codie/validation/local_gate.py",
                        "scripts/check_schema.py",
                        ".github/workflows/codie-local-validation.yml",
                        "tests/test_validation_local_gate.py",
                        "docs/CODIE_V1_CONSTITUTION.md",
                    )
                ),
                stderr="",
            ),
        ):
            files = _changed_files_for_scan(options, Path.cwd())

        self.assertIn("codie/validation/local_gate.py", files)
        self.assertIn("scripts/check_schema.py", files)
        self.assertIn(".github/workflows/codie-local-validation.yml", files)
        self.assertNotIn("tests/test_validation_local_gate.py", files)
        self.assertNotIn("docs/CODIE_V1_CONSTITUTION.md", files)

    def test_wrong_phase_part_rejected_against_authoritative_scope(self) -> None:
        result = self._run_security_only_gate(
            active_scope=ActiveValidationScope("Phase35B", "outside-validation", "INTERMEDIATE_PACKET"),
            options=ValidationGateOptions(
                phase_id="Phase35B",
                phase_part="wrong-part",
                gate_scope="INTERMEDIATE_PACKET",
                target_sha=SHA,
                pull_request_number=PR_NUMBER,
                branch=BRANCH,
            ),
        )

        self.assertEqual(result.result, "CONSTITUTION_CONFLICT")

    def test_wrong_gate_scope_rejected_against_authoritative_scope(self) -> None:
        result = self._run_security_only_gate(
            active_scope=ActiveValidationScope("Phase35B", "outside-validation", "FINAL_PHASE"),
            options=ValidationGateOptions(
                phase_id="Phase35B",
                phase_part="outside-validation",
                gate_scope="INTERMEDIATE_PACKET",
                target_sha=SHA,
                pull_request_number=PR_NUMBER,
                branch=BRANCH,
            ),
        )

        self.assertEqual(result.result, "CONSTITUTION_CONFLICT")

    def test_manual_weaker_gate_rejected(self) -> None:
        result = self._run_security_only_gate(
            active_scope=ActiveValidationScope("Phase35B", "outside-validation", "FINAL_PHASE"),
            options=ValidationGateOptions(
                phase_id="Phase35B",
                phase_part="outside-validation",
                gate_scope="INTERMEDIATE_PACKET",
                target_sha=SHA,
                pull_request_number=PR_NUMBER,
                branch=BRANCH,
            ),
        )

        self.assertEqual(result.result, "CONSTITUTION_CONFLICT")

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

    def test_trusted_report_duplicate_finding_ids_still_fail(self) -> None:
        duplicate = finding(finding_id="finding:duplicate")

        with self.assertRaises(ValidationGateError):
            report(
                validator="architecture",
                model="qwen2.5-coder:7b",
                findings=(duplicate, duplicate),
                severity_totals=SeverityTotals(HIGH=2),
            )

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

    def test_intermediate_medium_only_fail_report_does_not_block(self) -> None:
        result = aggregate_validator_reports(
            (
                report(validator="deterministic", result="FAIL", findings=(finding(finding_id="finding:medium", severity="MEDIUM"),)),
                report(validator="architecture", model="qwen2.5-coder:7b"),
                report(validator="adversarial", model="llama3.1:latest"),
            ),
            SHA,
        )

        self.assertEqual(result.result, "CLEAN_PASS")

    def test_intermediate_low_only_fail_report_does_not_block(self) -> None:
        result = aggregate_validator_reports(
            (
                report(validator="deterministic", result="FAIL", findings=(finding(finding_id="finding:low", severity="LOW"),)),
                report(validator="architecture", model="qwen2.5-coder:7b"),
                report(validator="adversarial", model="llama3.1:latest"),
            ),
            SHA,
        )

        self.assertEqual(result.result, "CLEAN_PASS")

    def test_intermediate_high_finding_blocks(self) -> None:
        result = aggregate_validator_reports(
            (
                report(validator="deterministic", result="FAIL", findings=(finding(finding_id="finding:high", severity="HIGH"),)),
                report(validator="architecture", model="qwen2.5-coder:7b"),
                report(validator="adversarial", model="llama3.1:latest"),
            ),
            SHA,
        )

        self.assertEqual(result.result, "REPAIR_REQUIRED")

    def test_final_clean_pass_policy_rejects_medium_and_low(self) -> None:
        result = aggregate_validator_reports(
            three_reports(gate_scope="FINAL_PHASE", result="CLEAN_PASS", findings=(finding(severity="MEDIUM"),)),
            SHA,
        )

        self.assertEqual(result.result, "REPAIR_REQUIRED")

    def test_final_phase_any_open_finding_blocks(self) -> None:
        result = aggregate_validator_reports(
            three_reports(gate_scope="FINAL_PHASE", result="CLEAN_PASS", findings=(finding(severity="INFORMATIONAL"),)),
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

    def test_model_findings_only_response_is_wrapped_as_trusted_report(self) -> None:
        options = ValidationGateOptions(
            phase_id=CURRENT_EXPECTED_PHASE_ID,
            phase_part="outside-validation",
            gate_scope="INTERMEDIATE_PACKET",
            target_sha=SHA,
            pull_request_number=PR_NUMBER,
            branch=BRANCH,
        )

        output = validator_report_from_model_response(
            validator="architecture",
            model="qwen2.5-coder:7b",
            options=options,
            payload=model_payload(),
            started_at="2026-07-13T00:00:00+00:00",
            completed_at="2026-07-13T00:01:00+00:00",
        )

        self.assertEqual(output.validator, "architecture")
        self.assertEqual(output.branch, BRANCH)
        self.assertEqual(output.target_sha, SHA)
        self.assertEqual(output.pull_request_number, PR_NUMBER)
        self.assertEqual(output.result, "FAIL")
        self.assertEqual(output.severity_totals.HIGH, 1)
        self.assertTrue(output.findings[0].finding_id.startswith("architecture:"))

    def test_duplicate_model_findings_are_collapsed_before_trusted_id_assignment(self) -> None:
        options = ValidationGateOptions(
            phase_id=CURRENT_EXPECTED_PHASE_ID,
            phase_part="outside-validation",
            gate_scope="INTERMEDIATE_PACKET",
            target_sha=SHA,
            pull_request_number=PR_NUMBER,
            branch=BRANCH,
        )
        duplicate_finding = model_payload()["findings"][0]

        output = validator_report_from_model_response(
            validator="adversarial",
            model="llama3.1:latest",
            options=options,
            payload=model_payload(findings=[duplicate_finding, dict(duplicate_finding)]),
            started_at="2026-07-13T00:00:00+00:00",
            completed_at="2026-07-13T00:01:00+00:00",
        )

        self.assertEqual(output.result, "FAIL")
        self.assertEqual(len(output.findings), 1)
        self.assertEqual(output.severity_totals.HIGH, 1)

    def test_model_findings_are_limited_to_changed_pr_files(self) -> None:
        options = ValidationGateOptions(
            phase_id=CURRENT_EXPECTED_PHASE_ID,
            phase_part="outside-validation",
            gate_scope="INTERMEDIATE_PACKET",
            target_sha=SHA,
            pull_request_number=PR_NUMBER,
            branch=BRANCH,
        )

        output = validator_report_from_model_response(
            validator="architecture",
            model="qwen2.5-coder:7b",
            options=options,
            payload=model_payload(),
            started_at="2026-07-13T00:00:00+00:00",
            completed_at="2026-07-13T00:01:00+00:00",
            allowed_affected_files=frozenset({"codie/validation/repair_controller.py"}),
        )

        self.assertEqual(output.result, "CLEAN_PASS")
        self.assertEqual(output.findings, ())

    def test_model_cannot_contribute_reserved_preflight_or_deterministic_findings(self) -> None:
        options = ValidationGateOptions(
            phase_id=CURRENT_EXPECTED_PHASE_ID,
            phase_part="outside-validation",
            gate_scope="INTERMEDIATE_PACKET",
            target_sha=SHA,
            pull_request_number=PR_NUMBER,
            branch=BRANCH,
        )
        payload = model_payload(
            findings=[
                {
                    "severity": "BLOCKER",
                    "title": "Stale SHA",
                    "description": "Target SHA does not match the checked-out HEAD.",
                    "affected_files": [],
                    "governing_rule": "Exact SHA validation",
                    "required_correction": "Check out the requested commit and rerun validation.",
                },
                {
                    "severity": "HIGH",
                    "title": "Potential Strategy-Inference Language Present",
                    "description": "Potential strategy-inference language is present in changed PR content.",
                    "affected_files": ["path/to/file.py"],
                    "governing_rule": "Evidence First Rule",
                    "required_correction": "Use evidence-only phrasing.",
                },
                {
                    "severity": "HIGH",
                    "title": "Valid architecture issue",
                    "description": "Changed code imports through the wrong boundary.",
                    "affected_files": ["codie/validation/local_gate.py"],
                    "governing_rule": "Architecture Boundary",
                    "required_correction": "Use the approved local boundary.",
                },
            ],
        )

        output = validator_report_from_model_response(
            validator="architecture",
            model="qwen2.5-coder:7b",
            options=options,
            payload=payload,
            started_at="2026-07-13T00:00:00+00:00",
            completed_at="2026-07-13T00:01:00+00:00",
            allowed_affected_files=frozenset({"codie/validation/local_gate.py"}),
        )

        self.assertEqual(output.result, "FAIL")
        self.assertEqual(len(output.findings), 1)
        self.assertEqual(output.findings[0].governing_rule, "Architecture Boundary")

    def test_model_cannot_override_trusted_report_fields(self) -> None:
        payload = model_payload(branch="wrong", target_sha="b" * 40, severity_totals={"HIGH": 99})

        with self.assertRaises(ValidationGateError):
            parse_model_validator_json(json.dumps(payload))

    def test_ollama_findings_only_json_is_validated(self) -> None:
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
            ollama_runner=lambda _model, _prompt: json.dumps({"result": "CLEAN_PASS", "findings": []}),
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
        self.assertIn("expected exactly one JSON object", output.errors[0])

    def test_malformed_json_recovery_from_wrapped_prose(self) -> None:
        payload = parse_model_validator_json(f"Here is the result:\n{json.dumps(model_payload())}\nDone.")

        self.assertEqual(payload["result"], "FAIL")

    def test_multiple_json_objects_are_rejected(self) -> None:
        text = f"{json.dumps({'result': 'CLEAN_PASS', 'findings': []})}\n{json.dumps({'result': 'CLEAN_PASS', 'findings': []})}"

        with self.assertRaises(ValidationGateError):
            parse_model_validator_json(text)

    def test_run_ollama_requests_json_format_and_sends_prompt_on_stdin(self) -> None:
        calls = []

        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self):
                return b'{"response": "{\\"result\\": \\"CLEAN_PASS\\", \\"findings\\": []}"}'

        def fake_urlopen(request, timeout):
            calls.append((request, timeout))
            return FakeResponse()

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            output = _run_ollama("llama3.1:latest", "validator prompt")

        self.assertEqual(output, '{"result": "CLEAN_PASS", "findings": []}')
        request, timeout = calls[0]
        body = json.loads(request.data.decode("utf-8"))
        self.assertEqual(timeout, 300)
        self.assertEqual(body["model"], "llama3.1:latest")
        self.assertEqual(body["prompt"], "validator prompt")
        self.assertFalse(body["stream"])
        self.assertEqual(body["options"]["temperature"], 0)
        self.assertEqual(body["format"], model_response_json_schema())

    def test_linux_python312_regression_uses_current_interpreter_when_windows_venv_missing(self) -> None:
        self.assertEqual(_portable_python_executable("Z:/definitely/missing/python.exe"), sys.executable)

    def _run_security_only_gate(self, *, active_scope: ActiveValidationScope, options: ValidationGateOptions):
        with mock.patch("codie.validation.local_gate.authoritative_active_validation_scope", return_value=(active_scope, "")), mock.patch(
            "codie.validation.local_gate._git_output",
            return_value=SHA,
        ):
            return run_validation_gate(options, root=Path.cwd())


if __name__ == "__main__":
    unittest.main()
