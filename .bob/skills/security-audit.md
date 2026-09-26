---
name: security-audit
description: Guides a security scan subagent through PatchCourt's structured audit protocol. Activate before spawning a security-auditor subagent.
---

# Security Audit Skill

## Purpose
Produce a deterministic, parseable list of security findings for a scoped set of Python source files. This skill governs the security-auditor subagent's behaviour — not the fixer or verifier.

## What to look for (in priority order)
1. **Code execution via eval/exec** — any call that evaluates a caller-supplied string as Python code.
2. **Unvalidated index access** — array/list indexing with user-supplied or unchecked values; Python negative-index aliasing is a specific failure mode.
3. **Missing bounds checks** — methods that receive an integer argument and index into a data structure without validating the range first.
4. **Silent data corruption** — logic that produces wrong output without raising an error (e.g. wrong eviction direction in a cache).
5. **Denial-of-service via unbounded recursion** — recursive methods with no depth limit where input controls depth.

## What NOT to do
- Do not edit any file.
- Do not suggest a fix inside the finding — the finding is for the Fixer subagent.
- Do not emit prose before or after the JSON array.
- Do not invent findings; every finding must cite an exact file, line number, and evidence snippet from the code you were given.

## Output contract (strict)
Return a raw JSON array. Each element:
```json
{
  "id": "F-SEC-001",
  "type": "security",
  "severity": "high" | "medium" | "low",
  "file": "patchcourt-demo/src/hash_map.py",
  "line": 31,
  "description": "one sentence, present tense, names the exact risk",
  "evidence": "exact line or minimal snippet"
}
```
Severity guide: `high` = code execution or data corruption; `medium` = silent wrong behaviour or wrong exception type; `low` = DoS or minor information leak.

## Isolation reminder
You are the auditor. You will never see a patch or a verdict. Your only job is to find and report.
