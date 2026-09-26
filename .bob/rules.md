# PatchCourt — Global Rules
# These rules apply to every Bob session in this project, regardless of mode.
# Bob must never deviate from these rules mid-session.

## Pipeline governance

1. **Verifier isolation is non-negotiable.**
   The Verifier subagent's context must contain only: the Finding JSON, the diff (rationale
   field stripped), and the test output (before + after). No fixer chain-of-thought, no
   "here's why this should work" prose, no parent conversation history.
   Enforcement: spawn Verifier as `subagent_type: explore`, `fork_context: false`.
   Construct the description string to contain ONLY `{finding, diff, test_before, test_after}`.

2. **A finding is resolved only on a Verifier verdict.**
   A Fixer subagent's own claims of success (e.g. "tests should now pass", "this fixes the
   issue") are never used to accept a patch. The only gate is a Verifier `verdict: "pass"`.

3. **Every Fixer patch must include a rationale field.**
   Even though the Verifier never sees it, the rationale must be present in the Patch JSON
   for the dashboard and human review. A Patch without a rationale is malformed.

4. **Fixer writes only the file named in the finding.**
   No other source file, no test file, no config file may be touched in the same patch.
   If a fix requires two files, split into two findings and two patches.

## Commit and PR discipline

5. **Conventional commit messages.**
   Format: `fix(<scope>): <description>` for patches, `feat(patchcourt): <description>` for
   pipeline code. Scope is the filename without extension (e.g. `fix(union_find): add bounds
   check in find()`).

6. **PR descriptions must list findings by verdict.**
   Include two sections: "Accepted findings (ACQUITTED)" and "Rejected findings (REJECTED
   with reason)". Do not include only the accepted diff — the rejection log is a first-class
   output and must appear in the PR body.

## Agent safety

7. **Auto-approve read actions for auditor subagents.**
   Require manual approval for any Fixer write and any command execution.
   This prevents runaway loops from burning Bobcoin budget and is a deliberate,
   safety-aware design choice worth stating in the Bob Usage Statement.

8. **Use Bob's Rollback for any Fixer write that turns out wrong.**
   Do not use manual `git checkout` to undo a bad patch — use Bob Rollback for
   faster iteration and a cleaner session history.

## Context discipline

9. **Point subagents at specific files with @-mentions.**
   Never give an auditor or fixer access to the full repo. Vague scope is how context
   leaks between "isolated" agents in practice. Always scope by file list.

10. **Strip the rationale before building the Verifier description string.**
    The orchestrator must explicitly project `{finding_id, diff}` from the Patch object —
    do not pass the full Patch object to the Verifier. This is the single implementation
    detail that makes isolation real rather than theatrical.
