from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import scripts.codie_repair_controller as repair_cli
from codie.validation.local_gate import ValidationGateError
from codie.validation.repair_controller import (
    PullRequestMetadata,
    RepairControllerOptions,
    RepairControllerResult,
    RepairExecutionResult,
    ValidationCycleResult,
    codex_exec_repair_attempt,
    discover_codex_executable,
    run_validation_cycle_in_worktree,
    run_repair_controller,
    unauthorized_repair_paths,
    verify_pull_request,
)


SHA1 = "1" * 40
SHA2 = "2" * 40
SHA3 = "3" * 40
BRANCH = "codex/operational-local-validation-bootstrap"


def options(**overrides) -> RepairControllerOptions:
    data = {
        "phase_id": "Phase35A",
        "phase_part": "outside-validation",
        "gate_scope": "INTERMEDIATE_PACKET",
        "pull_request_number": 1,
        "pr_branch": BRANCH,
        "target_sha": SHA1,
    }
    data.update(overrides)
    return RepairControllerOptions(**data)


def completed(stdout: str = "", stderr: str = "", returncode: int = 0) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(("fake",), returncode, stdout, stderr)


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

    def test_post_repair_validation_uses_new_sha(self) -> None:
        seen: list[str] = []

        result = run_repair_controller(
            options(),
            validation_runner=lambda sha, _cycle: seen.append(sha) or ValidationCycleResult(
                "REPAIR_REQUIRED" if sha == SHA1 else "CLEAN_PASS",
                sha,
            ),
            repair_runner=lambda _attempt, _sha: RepairExecutionResult(
                "COMMITTED",
                commit_sha=SHA2,
                changed_files=("codie/cards/example.py",),
            ),
        )

        self.assertEqual(result.final_result, "CLEAN_PASS")
        self.assertEqual(seen, [SHA1, SHA2])

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
                changed_files=("docs/CODIE_V1_CONSTITUTION.md",),
            ),
        )

        self.assertEqual(result.final_result, "HUMAN_REVIEW_REQUIRED")

    def test_forbidden_constitution_modification(self) -> None:
        offenders = unauthorized_repair_paths(("docs/CODIE_V1_CONSTITUTION.md",))

        self.assertEqual(offenders, ("docs/CODIE_V1_CONSTITUTION.md",))

    def test_invalid_pr_number(self) -> None:
        with self.assertRaises(ValidationGateError):
            options(pull_request_number=0)

    def test_pr_head_sha_mismatch(self) -> None:
        payload = self._pr_payload(headRefOid=SHA2)

        with self.assertRaises(ValidationGateError):
            verify_pull_request(options(), Path.cwd(), lambda _cmd, _root: completed(stdout=payload))

    def test_fork_pr_rejection(self) -> None:
        payload = self._pr_payload(headRepository={"isFork": True})

        with self.assertRaises(ValidationGateError):
            verify_pull_request(options(), Path.cwd(), lambda _cmd, _root: completed(stdout=payload))

    def test_dynamic_codex_discovery(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "nested" / "codex.exe"
            path.parent.mkdir()
            path.write_text("", encoding="utf-8")

            self.assertEqual(discover_codex_executable(root), path)

    def test_untracked_repair_file_detection_and_push(self) -> None:
        calls: list[tuple[str, ...]] = []

        def runner(command: tuple[str, ...], _root: Path):
            calls.append(command)
            if command[:3] == ("git", "ls-files", "--others"):
                return completed(stdout="codie/new_file.py\n")
            if command[:2] == ("git", "rev-parse"):
                return completed(stdout=f"{SHA2}\n")
            if command[:2] == ("git", "ls-remote"):
                return completed(stdout=f"{SHA2}\trefs/heads/{BRANCH}\n")
            return completed()

        with tempfile.TemporaryDirectory() as tmp:
            result = codex_exec_repair_attempt(
                1,
                SHA1,
                Path(tmp),
                BRANCH,
                "repair",
                codex_path=Path("C:/Codex/codex.exe"),
                command_runner=runner,
            )

        self.assertEqual(result.status, "COMMITTED")
        self.assertIn(("git", "push", "origin", f"HEAD:{BRANCH}"), calls)
        self.assertIn("codie/new_file.py", result.changed_files)

    def test_worktree_command_failure(self) -> None:
        def runner(command: tuple[str, ...], _root: Path):
            if command[:3] == ("git", "worktree", "add"):
                return completed(stderr="boom", returncode=1)
            return completed()

        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValidationGateError):
                codex_exec_repair_attempt(
                    1,
                    SHA1,
                    Path(tmp),
                    BRANCH,
                    "repair",
                    codex_path=Path("C:/Codex/codex.exe"),
                    command_runner=runner,
                )

    def test_worktree_cleanup(self) -> None:
        calls: list[tuple[str, ...]] = []

        def runner(command: tuple[str, ...], _root: Path):
            calls.append(command)
            if command[:3] == ("git", "worktree", "add"):
                return completed()
            if "codex.exe" in command[0]:
                return completed(returncode=1, stderr="failed")
            return completed()

        with tempfile.TemporaryDirectory() as tmp:
            result = codex_exec_repair_attempt(
                1,
                SHA1,
                Path(tmp),
                BRANCH,
                "repair",
                codex_path=Path("C:/Codex/codex.exe"),
                command_runner=runner,
            )

        self.assertEqual(result.status, "FAILED")
        self.assertTrue(any(command[:3] == ("git", "worktree", "remove") for command in calls))
        self.assertTrue(any(command[:3] == ("git", "worktree", "prune") for command in calls))

    def test_validation_worktree_uses_exact_sha_and_cleans_up(self) -> None:
        calls: list[tuple[str, ...]] = []

        def runner(command: tuple[str, ...], _root: Path):
            calls.append(command)
            return completed()

        fake_aggregate = mock.Mock(result="CLEAN_PASS", target_sha=SHA1)
        with mock.patch("codie.validation.repair_controller.run_validation_gate", return_value=fake_aggregate), mock.patch(
            "codie.validation.repair_controller.aggregated_result_to_dict",
            return_value={"final_result": "CLEAN_PASS"},
        ):
            result = run_validation_cycle_in_worktree(
                options=options(),
                base_branch="main",
                sha=SHA1,
                validation_cycle=1,
                root=Path("C:/repo"),
                command_runner=runner,
            )

        self.assertEqual(result.result, "CLEAN_PASS")
        add_commands = [command for command in calls if command[:4] == ("git", "worktree", "add", "--detach")]
        self.assertEqual(len(add_commands), 1)
        self.assertIn("cycle-1-111111111111", add_commands[0][4])
        self.assertEqual(add_commands[0][-1], SHA1)
        self.assertTrue(any(command[:3] == ("git", "worktree", "remove") for command in calls))
        self.assertTrue(any(command[:3] == ("git", "worktree", "prune") for command in calls))

    def test_real_repair_cli_execution(self) -> None:
        with mock.patch.object(repair_cli, "run_real_repair_controller") as mocked:
            mocked.return_value = RepairControllerResult("CLEAN_PASS", 0, (), (), SHA1, "")
            with mock.patch(
                "sys.argv",
                [
                    "codie_repair_controller.py",
                    "--phase-id",
                    "Phase35A",
                    "--phase-part",
                    "outside-validation",
                    "--gate-scope",
                    "INTERMEDIATE_PACKET",
                    "--pull-request-number",
                    "1",
                    "--pr-branch",
                    BRANCH,
                    "--target-sha",
                    SHA1,
                ],
            ):
                exit_code = repair_cli.main()

        self.assertEqual(exit_code, 0)
        mocked.assert_called_once()

    def test_pull_request_workflow_mode_never_invokes_repair(self) -> None:
        workflow = Path(".github/workflows/codie-local-validation.yml").read_text(encoding="utf-8")
        pr_section = workflow.split("manual-validation:")[0]

        self.assertIn("pull_request:", workflow)
        self.assertIn("scripts/codie_validation_gate.py", pr_section)
        self.assertNotIn("scripts/codie_repair_controller.py", pr_section)
        self.assertIn("persist-credentials: false", pr_section)

    def test_workflow_dispatch_repair_mode_can_invoke_repair(self) -> None:
        workflow = Path(".github/workflows/codie-local-validation.yml").read_text(encoding="utf-8")
        repair_section = workflow.split("manual-repair:")[1]

        self.assertIn("contents: write", repair_section)
        self.assertIn("scripts/codie_repair_controller.py", repair_section)
        self.assertIn("persist-credentials: true", repair_section)

    def test_workflow_requires_same_repository_pr(self) -> None:
        workflow = Path(".github/workflows/codie-local-validation.yml").read_text(encoding="utf-8")

        self.assertIn("github.event.pull_request.head.repo.full_name == github.event.repository.full_name", workflow)

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

    def _pr_payload(self, **overrides) -> str:
        data = {
            "number": 1,
            "state": "OPEN",
            "headRefName": BRANCH,
            "baseRefName": "main",
            "headRefOid": SHA1,
            "headRepository": {"isFork": False},
            "baseRepository": {"nameWithOwner": "St-Milton1013/Codie"},
        }
        data.update(overrides)
        return json.dumps(data)


if __name__ == "__main__":
    unittest.main()
