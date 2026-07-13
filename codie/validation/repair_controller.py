"""Automated local repair controller for Codie validation failures."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from codie.validation.local_gate import (
    AGGREGATOR_RESULTS,
    ACTIVE_PHASE_ID,
    ValidationGateError,
    ValidationGateOptions,
    aggregate_validator_reports,
)


MAX_REPAIR_ATTEMPTS = 2
REPAIR_STATUSES = frozenset({"COMMITTED", "FAILED", "USAGE_LIMIT"})
FORBIDDEN_REPAIR_PATHS = frozenset(
    {
        "docs/CODIE_V1_CONSTITUTION.md",
        "codie/validation/local_gate.py",
        "codie/validation/repair_controller.py",
        "schemas/codie_validator_report_v1.schema.json",
    }
)
FORBIDDEN_REPAIR_PREFIXES = (
    ".github/workflows/",
    "docs/CODIE_LOCAL_VALIDATION_AUTOMATION_CONTRACT.md",
)
FORBIDDEN_COST_KEYS = frozenset(
    {
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "GOOGLE_API_KEY",
        "GEMINI_API_KEY",
    }
)


@dataclass(frozen=True)
class ValidationCycleResult:
    result: str
    target_sha: str
    summary: str = ""

    def __post_init__(self) -> None:
        if self.result not in AGGREGATOR_RESULTS:
            raise ValidationGateError(f"unsupported validation result: {self.result}")


@dataclass(frozen=True)
class RepairExecutionResult:
    status: str
    commit_sha: str = ""
    changed_files: tuple[str, ...] = ()
    message: str = ""

    def __post_init__(self) -> None:
        if self.status not in REPAIR_STATUSES:
            raise ValidationGateError(f"unsupported repair status: {self.status}")
        object.__setattr__(self, "changed_files", tuple(sorted(_normalize_path(path) for path in self.changed_files)))


@dataclass(frozen=True)
class RepairControllerOptions:
    phase_id: str
    phase_part: str
    gate_scope: str
    pr_branch: str
    target_sha: str
    pull_request_number: int | None = None
    max_attempts: int = MAX_REPAIR_ATTEMPTS
    python_executable: str = r"C:\Users\Main\.venvs\codie-py312\Scripts\python.exe"

    def __post_init__(self) -> None:
        if self.phase_id != ACTIVE_PHASE_ID:
            raise ValidationGateError("repair controller may only run for the active Phase 35A gate")
        if not self.pr_branch or self.pr_branch in {"main", "master"}:
            raise ValidationGateError("repair controller requires an active PR branch")
        if self.max_attempts != MAX_REPAIR_ATTEMPTS:
            raise ValidationGateError("repair controller maximum attempts is fixed at two")


@dataclass(frozen=True)
class RepairControllerResult:
    final_result: str
    attempts_used: int
    validation_cycles: tuple[ValidationCycleResult, ...]
    repair_results: tuple[RepairExecutionResult, ...]
    current_sha: str
    message: str = ""


ValidationRunner = Callable[[str, int], ValidationCycleResult]
RepairRunner = Callable[[int, str], RepairExecutionResult]


def run_repair_controller(
    options: RepairControllerOptions,
    validation_runner: ValidationRunner,
    repair_runner: RepairRunner,
) -> RepairControllerResult:
    _reject_api_key_fallback()
    cycles: list[ValidationCycleResult] = []
    repairs: list[RepairExecutionResult] = []
    current_sha = options.target_sha
    initial = validation_runner(current_sha, 1)
    cycles.append(initial)
    if initial.target_sha != current_sha:
        return _finish("STALE_RESULTS", 0, cycles, repairs, current_sha, "initial report was stale")
    if initial.result == "CLEAN_PASS":
        return _finish("CLEAN_PASS", 0, cycles, repairs, current_sha, "initial validation passed")
    attempts_used = 0
    while attempts_used < options.max_attempts:
        repair = repair_runner(attempts_used + 1, current_sha)
        repairs.append(repair)
        if repair.status == "USAGE_LIMIT":
            return _finish(
                "CODEX_USAGE_LIMIT",
                attempts_used,
                cycles,
                repairs,
                current_sha,
                "codex usage limit interrupted repair without consuming an attempt",
            )
        if repair.status != "COMMITTED":
            return _finish("HUMAN_REVIEW_REQUIRED", attempts_used, cycles, repairs, current_sha, repair.message)
        unauthorized = unauthorized_repair_paths(repair.changed_files)
        if unauthorized:
            return _finish(
                "HUMAN_REVIEW_REQUIRED",
                attempts_used,
                cycles,
                repairs,
                current_sha,
                f"unauthorized repair paths: {', '.join(unauthorized)}",
            )
        attempts_used += 1
        current_sha = repair.commit_sha
        cycle = validation_runner(current_sha, attempts_used + 1)
        cycles.append(cycle)
        if cycle.target_sha != current_sha:
            return _finish("STALE_RESULTS", attempts_used, cycles, repairs, current_sha, "repair report was stale")
        if cycle.result == "CLEAN_PASS":
            return _finish("CLEAN_PASS", attempts_used, cycles, repairs, current_sha, "repair validation passed")
    return _finish(
        "HUMAN_REVIEW_REQUIRED",
        attempts_used,
        cycles,
        repairs,
        current_sha,
        "maximum automated repair attempts exhausted",
    )


def unauthorized_repair_paths(paths: tuple[str, ...]) -> tuple[str, ...]:
    offenders = []
    for path in paths:
        normalized = _normalize_path(path)
        if normalized in FORBIDDEN_REPAIR_PATHS:
            offenders.append(normalized)
        elif any(normalized.startswith(prefix) for prefix in FORBIDDEN_REPAIR_PREFIXES):
            offenders.append(normalized)
        elif normalized.startswith("codie/validation/") or normalized.startswith("schemas/"):
            offenders.append(normalized)
        elif normalized.startswith("docs/") and "finding" in normalized.lower():
            offenders.append(normalized)
    return tuple(sorted(set(offenders)))


def codex_exec_repair_attempt(
    attempt_number: int,
    current_sha: str,
    root: Path,
    pr_branch: str,
    prompt: str,
    command_runner: Callable[[tuple[str, ...], Path], subprocess.CompletedProcess[str]] | None = None,
) -> RepairExecutionResult:
    _reject_api_key_fallback()
    runner = command_runner or _run_command
    worktree_dir = root / ".repair-worktrees" / f"attempt-{attempt_number}"
    runner(("git", "worktree", "add", str(worktree_dir), pr_branch), root)
    codex = runner(("codex", "exec", "--full-auto", prompt), worktree_dir)
    if codex.returncode != 0:
        combined = f"{codex.stdout}\n{codex.stderr}".lower()
        if "usage limit" in combined or "rate limit" in combined:
            return RepairExecutionResult(status="USAGE_LIMIT", message=combined.strip())
        return RepairExecutionResult(status="FAILED", message=combined.strip())
    changed = runner(("git", "diff", "--name-only"), worktree_dir)
    changed_files = tuple(line.strip() for line in changed.stdout.splitlines() if line.strip())
    unauthorized = unauthorized_repair_paths(changed_files)
    if unauthorized:
        return RepairExecutionResult(status="FAILED", changed_files=unauthorized, message="unauthorized file changes")
    if not changed_files:
        return RepairExecutionResult(status="FAILED", message="codex produced no changes")
    runner(("git", "add", "--", *changed_files), worktree_dir)
    commit = runner(("git", "commit", "-m", f"Apply validation repair attempt {attempt_number}"), worktree_dir)
    if commit.returncode != 0:
        return RepairExecutionResult(status="FAILED", changed_files=changed_files, message=commit.stderr)
    commit_sha = runner(("git", "rev-parse", "HEAD"), worktree_dir).stdout.strip()
    if commit_sha == current_sha:
        return RepairExecutionResult(status="FAILED", changed_files=changed_files, message="repair did not advance SHA")
    return RepairExecutionResult(status="COMMITTED", commit_sha=commit_sha, changed_files=changed_files)


def validation_cycle_from_reports(
    options: ValidationGateOptions,
    reports,
    validation_cycle: int,
    repair_attempt: int,
) -> ValidationCycleResult:
    aggregate = aggregate_validator_reports(
        tuple(reports),
        options.target_sha,
        validation_cycle=validation_cycle,
        repair_attempt=repair_attempt,
    )
    return ValidationCycleResult(result=aggregate.result, target_sha=aggregate.target_sha)


def _finish(
    result: str,
    attempts_used: int,
    cycles: list[ValidationCycleResult],
    repairs: list[RepairExecutionResult],
    current_sha: str,
    message: str,
) -> RepairControllerResult:
    return RepairControllerResult(
        final_result=result,
        attempts_used=attempts_used,
        validation_cycles=tuple(cycles),
        repair_results=tuple(repairs),
        current_sha=current_sha,
        message=message,
    )


def _reject_api_key_fallback() -> None:
    present = sorted(key for key in FORBIDDEN_COST_KEYS if os.environ.get(key))
    if present:
        raise ValidationGateError(f"paid API key fallback is forbidden: {', '.join(present)}")


def _normalize_path(path: str) -> str:
    return path.replace("\\", "/").strip().lstrip("./")


def _run_command(command: tuple[str, ...], root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
