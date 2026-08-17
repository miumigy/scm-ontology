# SCM OS — New Session Handoff Prompt

Continue the user's `miumigy/scm-ontology` project as the implementation AI.

S371 is the first closed governed decision loop:

Canonical Graph -> Query/Projection -> ReasoningInput -> ReasoningProvider -> ReasoningOutput -> Proposal Validation -> AuthorizedDecision -> ExecutionCommand.

Existing contracts: `graph_query.py`, `graph_projection.py`, `graph_reasoning_projection.py`, `reasoning_assembly.py`, `reasoning_provider.py`, `reasoning_output.py`, `proposal_validation.py`, `decision_authorization.py`, `execution_command.py`.

Core principle: **AI may propose; governance authorizes; execution adapters perform side effects.**

Before any new Sxxx work, inspect current `main` and CI. Historical branches may be stale. Prefer additive changes and preserve immutable/fail-closed contracts.

Next phase should be runtime integration, not more contract proliferation: real graph/query adapters, real reasoning providers, authorization policy evaluation, execution adapters with idempotency/dry-run/audit semantics, persistent audit trail, operational API/UI, and end-to-end acceptance smoke tests.

At session start: inspect latest main, verify CI, inspect open PRs, then choose the smallest runtime milestone.
