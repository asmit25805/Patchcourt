## PR: fix(patchcourt): verified patches for 3 seeded issues — all ACQUITTED

### Summary

This PR contains patches for three issues found and independently verified by the PatchCourt
pipeline (IBM Bob 2.0 hackathon). Each patch was authored by an isolated Fixer subagent and
independently verified by a Verifier subagent with no access to the Fixer's reasoning.

Pipeline: `auditor (×2, parallel) → fixer → verifier (isolated context) → PR`

---

### Accepted findings (ACQUITTED)

**F-SEC-002-COV-002** — `src/union_find.py` — Security / Medium  
`find()` had no bounds check. Negative indices silently aliased to valid elements via Python's
negative-index semantics; out-of-range positive indices raised `IndexError` instead of `ValueError`.  
Fix: added `if not (0 <= x < len(self.parent)): raise ValueError(...)` as the first statement in `find()`.  
Verifier verdict: **PASS** (confidence 0.98) — both previously-failing tests now pass, no regressions,
recursive path-compression call protected by same guard.

**F-COV-001** — `src/lru_cache.py` — Test-Coverage / High  
`put()` evicted `self.head.next` (the MRU node) instead of `self.tail.prev` (the LRU node),
silently evicting the wrong cache entry under capacity pressure.  
Fix: changed `evict = self.head.next` → `evict = self.tail.prev`.  
Verifier verdict: **PASS** (confidence 0.99) — `test_eviction_removes_least_recently_used` now passes,
no regressions.

**F-SEC-001** — `src/hash_map.py` — Security / High  
`compute_key()` called `eval()` on a caller-supplied string — arbitrary code execution for any
external input (config file, request body, CLI arg).  
Fix: replaced `eval(expression)` with `raise TypeError(...)`. No existing test called this method.  
Verifier verdict: **PASS** (confidence 0.98) — eval() call eliminated entirely, no regressions,
no test calls compute_key() so unconditional raise is the correct security tradeoff.

---

### Rejected findings (REJECTED)

None in this run. All three proposed patches were independently verified as correct.

> Note: The rejection log is a first-class output of the PatchCourt pipeline — a Verifier
> rejection with evidence is the expected demo moment, not a failure case. See
> `results/run-2025-01-15T14-32-00.json` for the full machine-readable run record.

---

### Test delta

| State | Passed | Failed |
|---|---|---|
| Before (seeded HEAD) | 7 | 3 |
| After (all patches applied) | 10 | 0 |

### Files changed
- `src/union_find.py` — bounds check in `find()`
- `src/lru_cache.py` — eviction direction in `put()`
- `src/hash_map.py` — remove `eval()` from `compute_key()`

### Pipeline artifacts
- `results/run-2025-01-15T14-32-00.json` — full findings, patches, verdicts, timing
- `AGENTS.md` — repo governance + PatchCourt isolation rule
- `.bob/custom_modes.yaml` — 4 custom modes (security-auditor, coverage-auditor, fixer, verifier)
- `.bob/rules.md` — global behavioral rules (10 rules, non-overridable)
- `.bob/skills/security-audit.md` — reusable security audit skill
- `.bob/skills/verify-patch.md` — reusable verify patch skill
