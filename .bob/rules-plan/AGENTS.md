# AGENTS.md — Plan mode rules

This file provides guidance to agents when working with code in this repository.

## PatchCourt architecture constraints

### Verifier isolation is the load-bearing constraint
The entire pitch depends on the Verifier subagent having **no access to the
Fixer's rationale**. In practice this means:
- Verifier is spawned as `subagent_type: explore`, `fork_context: false`.
- The orchestrator builds `verifier_input = {finding, diff, test_before, test_after}` —
  the `rationale` key is explicitly excluded before spawning.
- No "explain why this should work" text may appear anywhere in the verifier's
  description string.

### Parallelism boundary
The two auditors (security + coverage) run in parallel — they share no state and
their scopes do not overlap (security reads `src/` only; coverage reads `src/` +
`tests/`). The Fixer is sequential (one finding at a time). The Verifier is
sequential (one verdict at a time).

### Patch acceptance gate
```
Fixer emits Patch{diff, rationale}
  orchestrator applies diff to working copy
  orchestrator runs: python -m pytest -v
  orchestrator strips rationale → sends {finding, diff, test_before, test_after}
  Verifier returns Verdict{pass|fail, reasoning, confidence}
  if verdict == pass → ACQUITTED (bundle into PR)
  if verdict == fail → REJECTED (log reason, do not apply)
```

### Three findings, three different fix types
- `union_find.py`: logic fix (add bounds guard, raise ValueError)
- `lru_cache.py`: logic fix (change `head.next` → `tail.prev`)
- `hash_map.py`: security fix (remove eval(), replace with safe alternative)
  — has NO failing test, so the only signal is the security finding itself and
  the Verifier's diff analysis (not test-output delta).

### Results artifact
Every run writes `/results/run-<timestamp>.json` with:
`{run_id, wall_clock_seconds, findings_total, patches_proposed,
  verdicts:{pass, fail}, rejected_findings:[{finding_id, reason}],
  accepted_finding_ids:[], manual_review_estimate:{...}}`
