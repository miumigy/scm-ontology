# S356 — Authorization Policy, Approval & Override

## Purpose

S356 is a Governance milestone (Phase R4). It provides the fail-closed
authorization policy, human-approval, and senior-override gates for the
governed decision loop, deciding whether an already-validated proposal may be
authorized through the S345 boundary.

## Contract

`DefaultAuthorizationPolicy` allows authorization only for enumerated
authorities and may require explicit human approval for high-value command
types. `evaluate_authorization_policy(...)` returns an immutable
`AuthorizationDecision` (`allowed`, `policy_id`, `requires_approval`, `reason`).

`ApprovalRecord` records an explicit human approval for a context and command
type. `DecisionOverride` records an explicit senior override that permits a
routinely-denied decision for a context/actor/authority. Both are immutable and
reference the governed context by `context_id`.

`authorize_under_policy(...)` authorizes a validated proposal only when all
required gates pass, returning the S345 `AuthorizedDecision`.

## Fail-closed behavior

`authorize_under_policy` MUST raise unless:

- the policy allows the authority; and
- when the policy requires approval, a matching `ApprovalRecord` is present
  (`context_id` + `command_type`); or
- when the policy denies, a matching `DecisionOverride` is present
  (`context_id` + `actor_id` + `authority`).

## Non-goals

S356 does not:

- mutate Canonical Truth or external systems;
- execute the command;
- invent approvals or overrides;
- bypass the S345 authorization boundary.
