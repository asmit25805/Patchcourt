## Problem & Solution Statement

**The problem: AI auto-fix tools are untrustworthy because the model that writes a patch also grades its own homework.**

When an LLM proposes a code fix, it has already reasoned its way to a conclusion. Its chain-of-thought is invested in the solution being correct. Asking the same model — with the same context, the same reasoning history — to then verify the fix is not verification. It is confirmation bias with an API. This is why engineering teams who pilot AI code review tools almost always add a rule: "someone still has to read every AI-authored change before it merges." The time savings disappear.

This isn't a new problem. Security researchers solved the equivalent issue in human review decades ago: the person who writes the code cannot be the person who approves it. The same structural separation is what makes AI auto-fix trustworthy — and it is almost universally absent from the tools available today. Most competing approaches (single-pass LLM reviewers, "chat with your codebase" tools, inline copilot suggestions) are variations of the same self-grading loop. The fix gets proposed and accepted in the same context window.

**PatchCourt breaks that loop at the architecture level.**

The pipeline separates every job into an isolated Bob subagent with a scoped context:

1. **Two Auditor subagents** scan the repo in parallel — one for security weaknesses (eval injection, missing bounds checks, silent aliasing), one for test-coverage gaps — and return structured `Finding` objects. Neither auditor can write files; they can only read.

2. **A Fixer subagent** receives exactly one finding and produces a minimal patch (`diff` + private `rationale`). It writes only the specific file named in the finding — nothing else.

3. **A Verifier subagent** runs in a completely fresh context (`fork_context: false`, `subagent_type: explore`). It receives the finding and the diff. The rationale is stripped by the orchestrator before the Verifier is spawned — it is architecturally unreachable, not just omitted by convention. The Verifier reads the diff, reads the test output (before and after), and returns a structured `Verdict` with concrete evidence. It cannot write files.

4. Only patches with `verdict: "pass"` are accepted and bundled into a PR. Rejected patches are logged with the Verifier's reason. The rejection log is a first-class output — a Verifier catching a bad patch is the demonstration, not a failure mode.

This run found 17 issues across three source files, patched three of them, and had all three independently verified as correct. Test results moved from 7/10 passing to 10/10 passing. Estimated manual review time for the same three findings: 45 minutes. Actual pipeline time: ~5 minutes.

The architectural claim is simple and falsifiable: if the Verifier's context ever included the Fixer's rationale, the isolation collapses and the tool becomes another self-grading loop. The implementation enforces this at the API call level, not just in the prompt.

*(497 words)*
