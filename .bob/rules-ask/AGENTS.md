# AGENTS.md — Ask mode rules

This file provides guidance to agents when working with code in this repository.

## PatchCourt context

This repo exists as a **demo target** for the PatchCourt adversarial code-review
pipeline. The seeded bugs are intentional — do not describe them as accidents or
omissions when answering questions about the codebase.

## Non-obvious structure

- `conftest.py` at the root inserts the project root into `sys.path` so that
  `from src.X import Y` works in tests without a package install.
- `pytest.ini` restricts test discovery to `tests/` — test files elsewhere are
  silently ignored.
- `python -m pytest` is required on this system; bare `pytest` does not resolve
  `src/` imports.
- The `eval()` in `compute_key()` has **no failing test** by design — it is a
  static/security finding, not a logic bug. This is intentional: it demonstrates
  why a security auditor is a separate track from a coverage auditor.
- The LRU eviction bug (`head.next` instead of `tail.prev`) does have a failing
  test: `test_eviction_removes_least_recently_used`. The test is correct; the
  source is wrong.

## PatchCourt governance
A finding is resolved only on a Verifier verdict — never on a Fixer's own claim.
