from __future__ import annotations

import argparse
import json

from codie.validation.repair_controller import RepairControllerOptions


def main() -> int:
    parser = argparse.ArgumentParser(description="Describe Codie local repair controller policy.")
    parser.add_argument("--phase-id", required=True)
    parser.add_argument("--phase-part", required=True)
    parser.add_argument("--gate-scope", required=True)
    parser.add_argument("--pr-branch", required=True)
    parser.add_argument("--target-sha", required=True)
    args = parser.parse_args()
    options = RepairControllerOptions(
        phase_id=args.phase_id,
        phase_part=args.phase_part,
        gate_scope=args.gate_scope,
        pr_branch=args.pr_branch,
        target_sha=args.target_sha,
    )
    print(
        json.dumps(
            {
                "phase_id": options.phase_id,
                "phase_part": options.phase_part,
                "gate_scope": options.gate_scope,
                "pr_branch": options.pr_branch,
                "target_sha": options.target_sha,
                "max_attempts": options.max_attempts,
                "mode": "local-codex-exec-repair-policy",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
