# AGENTS.md — Agent mode rules

This file provides guidance to agents when working with code in this repository.

## PatchCourt pipeline — agent coding rules

### File-write scope (non-negotiable)
- Fixer patches touch **only the file named in the finding**. No other source file,
  no test file, no config file may be modified in the same patch.
- If a fix genuinely requires touching a second file, emit two separate findings and
  two separate patches — do not bundle them.

### Diff format
- All patches must be valid unified diffs: `--- a/file`, `+++ b/file`, `@@ ... @@` hunks.
- Line numbers in the diff must match the current file exactly. Read the file first.

### Never self-accept
- A Fixer subagent must not assert its own patch is correct.
- Do not include "tests should now pass" or equivalent success claims in the diff or
  the JSON output. Put reasoning in `rationale` only — and `rationale` is stripped
  before the Verifier sees the patch.

### Bounds checks in this repo
- `union_find.py` `find()` must validate `x` as `0 <= x < n` and raise `ValueError`.
  Python negative indexing is the exact failure mode — a bare `IndexError` is not
  sufficient because the test asserts `ValueError`.

### LRU eviction direction
- The LRU tail sentinel is `self.tail`. The LRU node to evict is always `self.tail.prev`
  (not `self.head.next`). The head side is MRU; the tail side is LRU.

### eval() removal
- Replacing `eval()` in `compute_key()` with a lookup table or a `raise` is the
  correct fix. Do not add a `try/except` around `eval()` — that does not remove
  the code-execution risk.
