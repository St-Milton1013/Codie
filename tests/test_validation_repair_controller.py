from __future__ import annotations

import os
import unittest

from codie.validation.local_gate import ValidationGateError
from codie.validation.repair_controller import (
    RepairControllerOptions,
    RepairExecutionResult,
    ValidationCycleResult,
    run_repair_controller,
    unauthorized_repair_paths,
)


SHA1 = "1" * 40
SHA2 = "2" * 40
SHA3 = "3" * 40


def options() -> RepairControllerOptions:
    return RepairControllerOptions(
        phase_id="Phase35A",
        phase_part="outside-validation",
        gate_scope="INTERMEDIATE_PACKET",
        pr_branch="codex/operational-local-validation-bootstrap",
        target_sha=SHA1,
    )


class RepairControllerTest(unittest.TestCase):
    def test_successful_first_repair(self) -> None:
        validations = {
            SHA1: ValidationCycleResult("REPAIR_REQUIRED", SHA1),
            SHA2: ValidationCycleResult("CLEAN_PASS", SHA2),
        }

        result = run_repair_controller(
            options(),
            validation_runner=lambda sha, _cycle: validations[sha],
            repair_runner=lambda _attempt, _sha: RepairExecutionResult(
                "COMMITTED",
                commit_sha=SHA2,
                changed_files=("codie/cards/example.py",),
            ),
        )

        self.assertEqual(result.final_result, "CLEAN_PASS")
        self.assertEqual(result.attempts_used, 1)

    def test_successful_second_repair(self) -> None:
        validations = {
            SHA1: ValidationCycleResult("REPAIR_REQUIRED", SHA1),
            SHA2: ValidationCycleResult("REPAIR_REQUIRED", SHA2),
            SHA3: ValidationCycleResult("CLEAN_PASS", SHA3),
        }
        commits = [SHA2, SHA3]

        result = run_repair_controller(
            options(),
            validation_runner=lambda sha, _cycle: validations[sha],
            repair_runner=lambda _attempt, _sha: RepairExecutionResult(
                "COMMITTED",
                commit_sha=commits.pop(0),
                changed_files=("tests/test_example.py",),
            ),
        )

        self.assertEqual(result.final_result, "CLEAN_PASS")
        self.assertEqual(result.attempts_used, 2)

    def test_exhausted_repair_attempts(self) -> None:
        validations = {
            SHA1: ValidationCycleResult("REPAIR_REQUIRED", SHA1),
            SHA2: ValidationCycleResult("REPAIR_REQUIRED", SHA2),
            SHA3: ValidationCycleResult("REPAIR_REQUIRED", SHA3),
        }
        commits = [SHA2, SHA3]

        result = run_repair_controller(
            options(),
            validation_runner=lambda sha, _cycle: validations[sha],
            repair_runner=lambda _attempt, _sha: RepairExecutionResult(
                "COMMITTED",
                commit_sha=commits.pop(0),
                changed_files=("codie/cards/example.py",),
            ),
        )

        self.assertEqual(result.final_result, "HUMAN_REVIEW_REQUIRED")
        self.assertEqual(result.attempts_used, 2)

    def test_stale_reports_after_repair_commit(self) -> None:
        result = run_repair_controller(
            options(),
            validation_runner=lambda sha, cycle: ValidationCycleResult(
                "REPAIR_REQUIRED" if cycle == 1 else "CLEAN_PASS",
                SHA1,
            ),
            repair_runner=lambda _attempt, _sha: RepairExecutionResult(
                "COMMITTED",
                commit_sha=SHA2,
                changed_files=("codie/cards/example.py",),
            ),
        )

        self.assertEqual(result.final_result, "STALE_RESULTS")

    def test_usage_limit_pause_does_not_consume_attempt(self) -> None:
        result = run_repair_controller(
            options(),
            validation_runner=lambda sha, _cycle: ValidationCycleResult("REPAIR_REQUIRED", sha),
            repair_runner=lambda _attempt, _sha: RepairExecutionResult("USAGE_LIMIT", message="usage limit"),
        )

        self.assertEqual(result.final_result, "CODEX_USAGE_LIMIT")
        self.assertEqual(result.attempts_used, 0)

    def test_unauthorized_file_changes(self) -> None:
        result = run_repair_controller(
            options(),
            validation_runner=lambda sha, _cycle: ValidationCycleResult("REPAIR_REQUIRED", sha),
            repair_runner=lambda _attempt, _sha: RepairExecutionResult(
                "COMMITTED",
                commit_sha=SHA2,
                changed_files=("docs/hidden_findings.md",),
            ),
        )

        self.assertEqual(result.final_result, "HUMAN_REVIEW_REQUIRED")

    def test_forbidden_validator_modification(self) -> None:
        offenders = unauthorized_repair_paths(("codie/validation/local_gate.py",))

        self.assertEqual(offenders, ("codie/validation/local_gate.py",))

    def test_forbidden_constitution_modification(self) -> None:
        offenders = unauthorized_repair_paths(("docs/CODIE_V1_CONSTITUTION.md",))

        self.assertEqual(offenders, ("docs/CODIE_V1_CONSTITUTION.md",))

    def test_no_api_key_fallback(self) -> None:
        original = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = "blocked"
        try:
            with self.assertRaises(ValidationGateError):
                run_repair_controller(
                    options(),
                    validation_runner=lambda sha, _cycle: ValidationCycleResult("REPAIR_REQUIRED", sha),
                    repair_runner=lambda _attempt, _sha: RepairExecutionResult("FAILED"),
                )
        finally:
            if original is None:
                os.environ.pop("OPENAI_API_KEY", None)
            else:
                os.environ["OPENAI_API_KEY"] = original


if __name__ == "__main__":
    unittest.main()
