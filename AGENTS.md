# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Repo

`patchcourt` — three from-scratch Python data structures used as the live
demo target for the PatchCourt pipeline (IBM Bob 2.0 hackathon).

| File | Structure | Known seeded issue |
|---|---|---|
| `src/union_find.py` | Disjoint-set, path compression + union-by-rank | `find()` has no bounds check — negative indices alias silently, out-of-range raises raw `IndexError` instead of `ValueError` |
| `src/lru_cache.py` | Doubly-linked-list + dict | `put()` evicts from the **wrong end** (head = MRU side, not tail = LRU side) |
| `src/hash_map.py` | Separate chaining | `compute_key()` calls `eval()` on caller-supplied input — security issue, no failing test catches it |

## Commands

```bash
# Run full suite (from patchcourt/)
python -m pytest -v

# Run a single test file
python -m pytest tests/test_union_find.py -v

# Run a single test by name
python -m pytest tests/test_lru_cache.py::test_eviction_removes_least_recently_used -v
```

`pytest` alone (without `python -m`) may not resolve `src/` imports on this
system — always use `python -m pytest`.

`conftest.py` inserts the repo root into `sys.path` so `from src.X import Y`
works in tests without installing the package.

## Code style (non-obvious)

- No type annotations anywhere in source — do not add them unless the finding
  explicitly requires it.
- Tests import directly from `src.*` (not a package install) — new test files
  must follow the same import pattern.
- `pytest.ini` sets `testpaths = tests` — test files outside `tests/` are not
  collected automatically.

## PatchCourt governance (DO NOT DEVIATE)

This repo is audited by the PatchCourt pipeline:

```
Auditor (security + coverage, parallel)
  → Fixer (one patch per finding)
    → Verifier (isolated context, no fixer rationale)
      → ACQUITTED or REJECTED
```

**A finding is resolved only when a Verifier subagent — given only the
finding JSON and the diff, never the Fixer's rationale — independently
confirms the issue is gone and no tests regressed.**

A Fixer's own claim of success is never used to accept a patch.

Verifier subagent type: `explore`, `fork_context: false`.
Verifier input contract: `{finding, diff, test_before, test_after}` — no
rationale field, no fixer conversation history.
