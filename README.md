# patchcourt-demo

A small, from-scratch data-structures library used as the demo target for
**PatchCourt** at the IBM Bob 2.0 hackathon. Three real implementations
(union-find, LRU cache, hash map), each with one intentionally seeded issue,
so the audit -> fix -> verify pipeline has real, reproducible findings to
work against.

## Seeded issues (for the team's reference — remove this section before final submission if you don't want it spoiling the "reveal")

1. **`src/union_find.py` — missing bounds check.** `find()` doesn't validate
   its input index. Negative indices silently alias to the wrong element;
   out-of-range positive indices raise a raw `IndexError` instead of a clear
   error. Caught by two failing tests in `tests/test_union_find.py`.
2. **`src/lru_cache.py` — wrong eviction order.** Under capacity pressure,
   `put()` evicts the node next to `head` (most-recently-used side) instead
   of the node next to `tail` (least-recently-used side). Caught by
   `test_eviction_removes_least_recently_used` in `tests/test_lru_cache.py`.
3. **`src/hash_map.py` — unsafe `eval()`.** `compute_key()` evaluates a
   caller-supplied string directly. No functional test catches this — it's
   a static/security finding, not a logic bug, which is exactly why the
   security-auditor exists as a separate track from the coverage-auditor.

## Setup

```bash
git init
git checkout -b patchcourt-demo
pip install -r requirements.txt
git add .
git commit -m "Seed patchcourt-demo with three known issues"
```

## Confirm the baseline before opening Bob

```bash
pytest -v
```

Expect: 2 failing tests in `test_union_find.py`, 1 failing test in
`test_lru_cache.py`, all `test_hash_map.py` tests passing (the eval() issue
has no failing test — that's the point). This failing-test output is your
"before" baseline to hand the Verifier later.

Once this matches, open this folder as the workspace in Bob IDE and proceed
with the PatchCourt pipeline.
