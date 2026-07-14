# Repair Loop Behavior Guide

The repair controller runs only on an active PR branch.

Rules:

```text
maximum two automated repair attempts
one isolated Git worktree per repair
repair writes restricted to the active PR branch
full validator rerun after each repair commit
previous reports invalidated by SHA mismatch
usage-limit interruption does not consume an attempt
no API-key fallback
no automatic merge
two failed repairs stop with HUMAN_REVIEW_REQUIRED
```

Automated repair must never modify:

```text
docs/CODIE_V1_CONSTITUTION.md
validator rules
aggregator gates
acceptance criteria
meaningful tests by deletion
documentation to hide findings
unrelated project scope
```
