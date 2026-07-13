"""Automated local repair controller for Codie validation failures."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from codie.validation.local_gate import (
    AGGREGATOR_RESULTS,
    REPOSITORY,
    ValidationGateError,
    ValidationGateOptions,
    aggregate_validator_reports,
    aggregated_result_to_dict,
    run_validation_gate,
)


MAX_REPAIR_ATTEMPTS = 2
REPAIR_STATUSES = frozenset({"COMMITTED", "FAILED", "USAGE_LIMIT"})
FORBIDDEN_REPAIR_PATHS = frozenset({"docs/CODIE_V1_CONSTITUTION.md"})
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
CODEX_BIN_ROOT = Path(r"C:\Users\Main\AppData\Local\OpenAI\Codex\bin")


@dataclass(frozen=True)
class PullRequestMetadata:
    number: int
    repository: str
    state: str
    head_branch: str
    base_branch: str
    head_sha: str
    is_fork: bool

    @classmethod
    def from_gh_json(cls, payload: str) -> "PullRequestMetadata":
        data = json.loads(payload)
        head_repo = data.get("headRepository") or {}
        return cls(
            number=int(data["number"]),
            repository=REPOSITORY,
            state=str(data["state"]),
            head_branch=str(data["headRefName"]),
            base_branch=str(data["baseRefName"]),
            head_sha=str(data["headRefOid"]),
            is_fork=bool(head_repo.get("isFork")) or bool(data.get("isCrossRepository")),
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
    pull_request_number: int
    repository: str = REPOSITORY
    base_branch: str = "main"
    max_attempts: int = MAX_REPAIR_ATTEMPTS
    python_executable: str = r"C:\Users\Main\.venvs\codie-py312\Scripts\python.exe"

    def __post_init__(self) -> None:
        if not self.pr_branch or self.pr_branch in {"main", "master"}:
            raise ValidationGateError("repair controller requires an active PR branch")
        if self.pull_request_number < 1:
            raise ValidationGateError("pull_request_number must be positive")
        if self.max_attempts != MAX_REPAIR_ATTEMPTS:
            raise ValidationGateError("repair controller maximum attempts is fixed at two")
        if self.repository != REPOSITORY:
            raise ValidationGateError("repository mismatch")


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
CommandRunner = Callable[[tuple[str, ...], Path], subprocess.CompletedProcess[str]]


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


def run_real_repair_controller(
    options: RepairControllerOptions,
    root: Path,
    command_runner: CommandRunner | None = None,
) -> RepairControllerResult:
    runner = command_runner or _run_command
    pr = verify_pull_request(options, root, runner)
    codex_path = discover_codex_executable()

    def validate(sha: str, cycle: int) -> ValidationCycleResult:
        gate_options = ValidationGateOptions(
            phase_id=options.phase_id,
            phase_part=options.phase_part,
            gate_scope=options.gate_scope,
            target_sha=sha,
            pull_request_number=options.pull_request_number,
            repository=options.repository,
            branch=options.pr_branch,
            base_branch=pr.base_branch,
            python_executable=options.python_executable,
        )
        aggregate = run_validation_gate(gate_options, root=root)
        return ValidationCycleResult(
            aggregate.result,
            aggregate.target_sha,
            json.dumps(aggregated_result_to_dict(aggregate), sort_keys=True),
        )

    def repair(attempt: int, sha: str) -> RepairExecutionResult:
        prompt = _repair_prompt(options, attempt, sha)
        return codex_exec_repair_attempt(
            attempt,
            sha,
            root,
            options.pr_branch,
            prompt,
            codex_path=codex_path,
            command_runner=runner,
        )

    return run_repair_controller(options, validation_runner=validate, repair_runner=repair)


def verify_pull_request(
    options: RepairControllerOptions,
    root: Path,
    command_runner: CommandRunner | None = None,
) -> PullRequestMetadata:
    runner = command_runner or _run_command
    command = (
        "gh",
        "pr",
        "view",
        str(options.pull_request_number),
        "--repo",
        options.repository,
        "--json",
        "number,state,headRefName,baseRefName,headRefOid,headRepository,isCrossRepository",
    )
    completed = _checked(runner, command, root, "fetch pull request metadata")
    metadata = PullRequestMetadata.from_gh_json(completed.stdout)
    if metadata.number != options.pull_request_number:
        raise ValidationGateError("pull_request_number mismatch")
    if metadata.repository != options.repository:
        raise ValidationGateError("pull request repository mismatch")
    if metadata.state != "OPEN":
        raise ValidationGateError("pull request is not open")
    if metadata.head_branch != options.pr_branch:
        raise ValidationGateError("pull request head branch mismatch")
    if metadata.base_branch != options.base_branch:
        raise ValidationGateError("pull request base branch mismatch")
    if metadata.head_sha != options.target_sha:
        raise ValidationGateError("pull request head SHA mismatch")
    if metadata.is_fork:
        raise ValidationGateError("fork pull requests are not eligible for automated repair")
    return metadata


def unauthorized_repair_paths(paths: tuple[str, ...]) -> tuple[str, ...]:
    offenders = []
    for path in paths:
        normalized = _normalize_path(path)
        if normalized in FORBIDDEN_REPAIR_PATHS:
            offenders.append(normalized)
        elif any(normalized.startswith(prefix) for prefix in FORBIDDEN_REPAIR_PREFIXES):
            offenders.append(normalized)
    return tuple(sorted(set(offenders)))


def discover_codex_executable(root: Path = CODEX_BIN_ROOT) -> Path:
    candidates = sorted(root.glob("**/codex.exe")) + sorted(root.glob("**/codex.cmd")) + sorted(root.glob("**/codex"))
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise ValidationGateError(f"Codex executable not found under {root}")


def codex_exec_repair_attempt(
    attempt_number: int,
    current_sha: str,
    root: Path,
    pr_branch: str,
    prompt: str,
    codex_path: Path | None = None,
    command_runner: CommandRunner | None = None,
) -> RepairExecutionResult:
    _reject_api_key_fallback()
    runner = command_runner or _run_command
    codex = codex_path or discover_codex_executable()
    worktree_dir = root / ".repair-worktrees" / f"attempt-{attempt_number}"
    repair_branch = f"codex-repair-{attempt_number}-{current_sha[:12]}"
    try:
        _checked(runner, ("git", "worktree", "add", "-b", repair_branch, str(worktree_dir), current_sha), root, "create repair worktree")
        completed = runner((str(codex), "exec", "--full-auto", prompt), worktree_dir)
        if completed.returncode != 0:
            combined = f"{completed.stdout}\n{completed.stderr}".lower()
            if "usage limit" in combined or "rate limit" in combined:
                return RepairExecutionResult(status="USAGE_LIMIT", message=combined.strip())
            return RepairExecutionResult(status="FAILED", message=combined.strip())
        changed_files = _changed_files(runner, worktree_dir)
        unauthorized = unauthorized_repair_paths(changed_files)
        if unauthorized:
            return RepairExecutionResult(status="FAILED", changed_files=unauthorized, message="unauthorized file changes")
        if not changed_files:
            return RepairExecutionResult(status="FAILED", message="codex produced no changes")
        _checked(runner, ("git", "add", "--", *changed_files), worktree_dir, "stage repair changes")
        _checked(runner, ("git", "commit", "-m", f"Apply validation repair attempt {attempt_number}"), worktree_dir, "commit repair")
        commit_sha = _checked(runner, ("git", "rev-parse", "HEAD"), worktree_dir, "read repair SHA").stdout.strip()
        if commit_sha == current_sha:
            return RepairExecutionResult(status="FAILED", changed_files=changed_files, message="repair did not advance SHA")
        _checked(runner, ("git", "push", "origin", f"HEAD:{pr_branch}"), worktree_dir, "push repair commit")
        remote_sha = _checked(runner, ("git", "ls-remote", "origin", f"refs/heads/{pr_branch}"), worktree_dir, "verify remote PR head").stdout.split()[0]
        if remote_sha != commit_sha:
            return RepairExecutionResult(status="FAILED", changed_files=changed_files, message="remote PR head SHA mismatch after push")
        return RepairExecutionResult(status="COMMITTED", commit_sha=commit_sha, changed_files=changed_files)
    finally:
        runner(("git", "worktree", "remove", "--force", str(worktree_dir)), root)
        runner(("git", "worktree", "prune"), root)


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


def _changed_files(runner: CommandRunner, worktree_dir: Path) -> tuple[str, ...]:
    tracked = _checked(runner, ("git", "diff", "--name-only"), worktree_dir, "detect tracked changes")
    staged = _checked(runner, ("git", "diff", "--cached", "--name-only"), worktree_dir, "detect staged changes")
    untracked = _checked(runner, ("git", "ls-files", "--others", "--exclude-standard"), worktree_dir, "detect untracked changes")
    files = {
        _normalize_path(line)
        for output in (tracked.stdout, staged.stdout, untracked.stdout)
        for line in output.splitlines()
        if line.strip()
    }
    return tuple(sorted(files))


def _checked(runner: CommandRunner, command: tuple[str, ...], root: Path, action: str) -> subprocess.CompletedProcess[str]:
    completed = runner(command, root)
    if completed.returncode != 0:
        raise ValidationGateError(f"failed to {action}: {(completed.stderr or completed.stdout).strip()}")
    return completed


def _repair_prompt(options: RepairControllerOptions, attempt: int, sha: str) -> str:
    return (
        f"Repair Codie PR #{options.pull_request_number} attempt {attempt} at SHA {sha}. "
        "Make the smallest code/test changes needed for the local validation gate. "
        "Do not modify docs/CODIE_V1_CONSTITUTION.md, do not merge, and do not implement Phase 35B."
    )


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
