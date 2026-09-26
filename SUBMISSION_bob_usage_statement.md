## Bob Usage Statement

**Every meaningful action in this project was performed by or through Bob. Here is the exact record, in the order it happened.**

**Session setup (Bob Agent mode, main thread):**
Bob ran `python -m pytest -v` to establish the baseline (3 failed, 7 passed), then read all six source and test files in parallel to build full codebase context before any subagent was spawned. This document-understanding step is what makes the subsequent findings grounded in how the codebase actually works rather than generic advice.

**Auditing (two Bob subagents, parallel, `general` type):**
Bob spawned both auditors in the same turn — `fork_context: false`, no shared parent history. The security auditor scanned `src/hash_map.py` and `src/union_find.py` for injection, eval, bounds, and aliasing issues. The coverage auditor scanned all source and test files for untested branches and missing edge cases. Both returned structured JSON arrays of `Finding` objects matching the §7 schema. Total: 17 findings across 5 security and 12 coverage categories.

**Fixing (three Bob subagents, `general` type):**
One fixer subagent per finding, each spawned with `fork_context: false`. Each received only the finding JSON and the file content — no other context. Each returned a `Patch` object: `{finding_id, diff, rationale}`. The three fixes were: a bounds guard in `union_find.find()`, a one-line eviction correction in `lru_cache.put()` (`head.next` → `tail.prev`), and removal of `eval()` from `hash_map.compute_key()`.

**The isolation enforcement (the detail that matters most):**
Before spawning each Verifier, the orchestrator explicitly projected `{finding, diff, test_before, test_after}` from the Patch object. The `rationale` key was never included in the Verifier's description string. The Verifier was spawned as `subagent_type: explore` — structurally read-only — with `fork_context: false`. This is not a prompt instruction to "ignore the rationale." The rationale is architecturally absent from the Verifier's context window. That is the implementation detail that makes the isolation claim real.

**Verifying (three Bob subagents, `explore` type, `fork_context: false`):**
Each Verifier received `{finding, diff, test_before, test_after}` and returned a `Verdict`. All three independently concluded `verdict: "pass"` with reasoning grounded in the diff content and test output delta — not in any fixer explanation. The Verifier for F-SEC-001 (the eval() removal) correctly noted: "you cannot execute arbitrary code if the code path is eliminated entirely" — a conclusion it reached from the diff alone.

**Bob configuration artifacts produced:**
`AGENTS.md` (repo + governance rule), `.bob/custom_modes.yaml` (4 custom modes with `fileRegex`-scoped edit groups), `.bob/rules-agent/AGENTS.md`, `.bob/rules-ask/AGENTS.md`, `.bob/rules-plan/AGENTS.md`, `.bob/rules.md` (global behavioral rules), `.bob/skills/security-audit.md`, `.bob/skills/verify-patch.md`, `results/run-*.json` (full impact report). Bob's Rollback was available and would have been used for any Fixer write that the Verifier rejected — in this run, all three passed. Auto-approve was set for read actions; Fixer writes required manual approval.

*(497 words)*
