# Outside Validation Prompt — Phase51M Two-Lane Safety Amendment

Review this packet independently. Do not trust its summary, change files,
push, open or update a PR, rerun a workflow, merge, or grant acceptance.

## Verify First

1. Confirm the amendment is documentation-only and no held Phase51M source
   edits are included in its diff.
2. Read Phase51L and the amendment together. Prove whether Phase51L's
   per-finding `record_assertions` shape can suppress an ordinary finding.
3. Confirm the amendment replaces that attachment with separate top-level
   `findings` and `documentation_record_assertions` lanes.
4. Confirm no assertion can modify or suppress ordinary findings, and an
   ordinary record claim remains blocking when it is in the wrong lane.
5. Confirm malformed, mismatched, duplicate, contradictory, or unresolved
   assertions fail closed as deterministic blocking findings.
6. Confirm the Phase51K-to-Phase51N handoff and all constitutional hard
   boundaries remain intact.
7. Run `git diff --check`, `scripts/check_schema.py`, and the full unittest
   suite from the configured Codie Python environment.

## Required Verdict

Return PASS, PASS WITH REQUIRED CHANGES, or FAIL. Tie every claim to the exact
diff and command output. Do not treat a passing local suite as merge authority.
