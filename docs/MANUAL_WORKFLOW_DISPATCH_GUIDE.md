# Manual Workflow Dispatch Guide

Workflow:

```text
Codie Local Validation Gate
```

Use manual dispatch only from `St-Milton1013/Codie`.

Inputs:

```text
phase_id: Phase35A
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET or FINAL_PHASE
pull_request_number: optional PR number
target_sha: exact commit SHA, optional but recommended
```

The workflow runs on the self-hosted Windows runner only. It does not use
GitHub-hosted runners and does not call paid APIs.
