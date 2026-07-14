from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from codie.validation.repair_controller import (
    RepairControllerOptions,
    repair_controller_result_to_dict,
    run_real_repair_controller,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Codie local validation and automated repair controller.")
    parser.add_argument("--phase-id", required=True)
    parser.add_argument("--phase-part", required=True)
    parser.add_argument("--gate-scope", required=True)
    parser.add_argument("--pull-request-number", type=int, required=True)
    parser.add_argument("--pr-branch", required=True)
    parser.add_argument("--base-branch", default="main")
    parser.add_argument("--target-sha", required=True)
    parser.add_argument("--python-executable", default=r"C:\Users\Main\.venvs\codie-py312\Scripts\python.exe")
    parser.add_argument("--output-dir", default="validation_artifacts")
    parser.add_argument("--expected-validation-result", default="REPAIR_REQUIRED")
    args = parser.parse_args()
    options = RepairControllerOptions(
        phase_id=args.phase_id,
        phase_part=args.phase_part,
        gate_scope=args.gate_scope,
        pull_request_number=args.pull_request_number,
        pr_branch=args.pr_branch,
        base_branch=args.base_branch,
        target_sha=args.target_sha,
        python_executable=args.python_executable,
        output_dir=Path(args.output_dir),
        expected_validation_result=args.expected_validation_result,
    )
    result = run_real_repair_controller(options, Path.cwd())
    print(json.dumps(repair_controller_result_to_dict(result), indent=2, sort_keys=True))
    return 0 if result.final_result == "CLEAN_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
