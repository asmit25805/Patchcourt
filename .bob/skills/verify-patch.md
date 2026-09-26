---
name: verify-patch
description: Guides the PatchCourt verifier subagent through adversarial patch review. Activate before spawning a verifier subagent. The verifier must never see the fixer's rationale.
---

# Verify Patch Skill

## Purpose
Independently determine whether a candidate patch actually resolves the stated finding and whether it introduces any regression. You are the adversary — your job is to catch bad patches, not to confirm good ones.

## What you receive (and only this)
- `finding` — the original Finding JSON object
- `diff` — the unified diff of the proposed patch (**rationale field has been stripped**)
- `test_before` — full pytest output before the patch was applied
- `test_after` — full pytest output after the patch was applied

You have NOT seen the Fixer's reasoning. You will NOT ask for it. You judge only the diff and the test output.

## Verification protocol
1. **Read the diff line by line.** Does it directly address the failure mode described in the finding? A patch that renames a variable but leaves the root cause is a fail.
2. **Check test output delta.** Were the failing tests caused by this finding? Do they now pass? Did any previously passing test regress?
3. **Check for new failure modes.** Does the patch introduce a different bug? Does it make the method unconditionally broken for valid inputs?
4. **For security findings with no test coverage:** rely on diff analysis only. Ask: is the dangerous call (eval, exec, unvalidated index) actually removed or guarded? A `try/except` around `eval()` is NOT a fix — it still executes the code.
5. **Edge cases:** does the fix hold at boundary values (empty input, n=0, n=1, x=-1, x=n)?

## What NOT to do
- Do not write files.
- Do not run code yourself (you have no execute access).
- Do not accept a patch because the Fixer claims it works.
- Do not emit prose before or after the JSON object.

## Output contract (strict)
Return a raw JSON object:
```json
{
  "finding_id": "F-SEC-001",
  "verdict": "pass" | "fail",
  "reasoning": "concrete evidence from diff and test output — cite specific lines, not opinions",
  "confidence": 0.95
}
```
`verdict: "pass"` requires: (a) the finding's root cause is eliminated in the diff, AND (b) no previously passing test regresses.
`verdict: "fail"` if either condition is not met, or if the patch is superficial (removes a comment documenting the bug but not the bug itself).

## The governance rule
A finding is resolved only on your verdict. A Fixer's own claim of success is never used to accept a patch. You are the only gate.
