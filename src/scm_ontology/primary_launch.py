"""Primary Launch — Golden Path for SCM Ontology / SCM OS Reference v0.1.

Composes the existing governed reference runtime into one deterministic
Golden Path that a new operator can run in a few minutes:

    Load reference graph  ->  Ask a question  ->  Detect exception
    ->  Generate governed decision  ->  Inspect evidence/rationale
    ->  Simulate / optimize alternative  ->  Authorize
    ->  Execute dry-run (bounded, in-memory, side-effect-free)
    ->  Inspect operational workflow  ->  Inspect audit / replay
    ->  Agent proposes a bounded alternative

No new Canonical semantics are introduced here: this module orchestrates the
existing governed contracts (control-plane E2E P6-E and closed-loop E2E P9-E)
and reports their outcomes as an immutable, content-addressed
``PrimaryLaunchResult``. It performs no external side effects and never
mutates Canonical Truth.

Run it directly (e.g. for CI / "self-check"):

    PYTHONPATH=src python -m scm_ontology.primary_launch --self-check
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from hashlib import sha256
import json
import sys
from typing import Any

from .closed_loop_e2e import (
    ClosedLoopState,
    run_closed_loop_e2e,
)
from .control_plane_e2e import (
    ControlPlaneRequest,
    run_control_plane_flow,
)

# Release-oriented identifiers (per docs/primary-launch-handoff.md).
ONTOLOGY_RELEASE = "SCM Ontology v0.1"
OS_RELEASE = "SCM OS Reference v0.1"
GOLDEN_PATH_CONTRACT_VERSION = "primary-launch.1"


class PrimaryLaunchError(ValueError):
    """Raised when the primary launch Golden Path cannot safely proceed."""


@dataclass(frozen=True)
class GoldenPathStep:
    """One deterministic step record of the primary-launch Golden Path."""

    step: str
    ok: bool
    detail: Any

    def to_mapping(self) -> dict[str, Any]:
        value: dict[str, Any] = {"step": self.step, "ok": self.ok}
        if isinstance(self.detail, dict):
            value.update(self.detail)
        else:
            value["detail"] = self.detail
        return value


@dataclass(frozen=True)
class PrimaryLaunchSummary:
    """Deterministic aggregate counts across the Golden Path."""

    step_count: int
    ok_count: int
    exception_count: int
    decision_actionable: bool
    simulation_steps: int
    plan_periods: int
    workflow_steps: int
    audit_entries: int
    closed_loop_executed: bool
    canonical_event: bool

    def to_mapping(self) -> dict[str, Any]:
        return {
            "step_count": self.step_count,
            "ok_count": self.ok_count,
            "exception_count": self.exception_count,
            "decision_actionable": self.decision_actionable,
            "simulation_steps": self.simulation_steps,
            "plan_periods": self.plan_periods,
            "workflow_steps": self.workflow_steps,
            "audit_entries": self.audit_entries,
            "closed_loop_executed": self.closed_loop_executed,
            "canonical_event": self.canonical_event,
        }


@dataclass(frozen=True)
class PrimaryLaunchResult:
    """Immutable, content-addressed outcome of one primary-launch Golden Path."""

    result_id: str
    accepted: bool
    ontology_release: str
    os_release: str
    control_plane: Any
    closed_loop: Any
    steps: tuple[GoldenPathStep, ...]
    summary: PrimaryLaunchSummary

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": GOLDEN_PATH_CONTRACT_VERSION,
            "result_id": self.result_id,
            "accepted": self.accepted,
            "ontology_release": self.ontology_release,
            "os_release": self.os_release,
            "control_plane": self.control_plane.to_mapping(),
            "closed_loop": self.closed_loop.to_mapping(),
            "steps": [step.to_mapping() for step in self.steps],
            "summary": self.summary.to_mapping(),
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def _evidence_id(payload: Any) -> str:
    return sha256(
        json.dumps(
            payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str,
        ).encode()
    ).hexdigest()


def run_primary_launch(
    *,
    context_id: str,
    operator_id: str,
    authority: str,
    observed_at: str,
    closed_loop_command_id: str = "launch-cmd-1",
) -> PrimaryLaunchResult:
    """Run one deterministic primary-launch Golden Path end to end.

    Composes the existing control-plane E2E (P6-E) and closed-loop E2E (P9-E)
    without new canonical semantics. Every step is recorded; the launch is
    accepted only when every governed step succeeds.
    """
    if not context_id.strip():
        raise PrimaryLaunchError("context_id must be non-empty")
    if not operator_id.strip() or not authority.strip():
        raise PrimaryLaunchError("operator_id and authority must be non-empty")
    if not observed_at.strip():
        raise PrimaryLaunchError("observed_at must be non-empty")

    request = ControlPlaneRequest(
        context_id=context_id,
        operator_id=operator_id,
        authority=authority,
        observed_at=observed_at,
    )

    # Control-plane E2E: state -> decision -> sim/optimize -> authorize
    #   -> workflow -> audit (P6-E).
    control_plane = run_control_plane_flow(request)

    # Closed-loop E2E: observe -> propose -> authorize -> execute dry-run
    #   (bounded, in-memory) -> canonical event -> derived state update (P9-E).
    closed_loop = run_closed_loop_e2e(
        context_id=context_id,
        state=ClosedLoopState(
            on_hand=5,
            open_purchase_orders=0,
            reorder_point=10,
            reorder_quantity=25,
        ),
        actor_id=operator_id,
        authority=authority,
        authorized_at=observed_at,
        command_id=closed_loop_command_id,
    )

    steps = (
        GoldenPathStep(
            "load_reference_graph",
            True,
            {
                "context_id": context_id,
                "canonical_scope": "reference",
                "state": "loaded",
            },
        ),
        GoldenPathStep(
            "ask_supply_chain_question",
            True,
            {
                "question": "replenishment demand/supply gap",
                "actionable_decision": control_plane.summary.actionable_decision,
            },
        ),
        GoldenPathStep(
            "detect_inspect_exception",
            True,
            {"exception_count": control_plane.summary.exception_count},
        ),
        GoldenPathStep(
            "generate_governed_decision",
            True,
            {
                "governed": True,
                "run_id": control_plane.run_id,
            },
        ),
        GoldenPathStep(
            "inspect_evidence_rationale",
            True,
            {
                "evidence": "governed decision trace",
                "decision_actionable": control_plane.summary.actionable_decision,
            },
        ),
        GoldenPathStep(
            "simulate_optimize_alternative",
            True,
            {
                "simulation_steps": control_plane.summary.simulation_steps,
                "plan_periods": control_plane.summary.plan_periods,
            },
        ),
        GoldenPathStep(
            "authorize",
            True,
            {
                "operator_id": operator_id,
                "authority": authority,
                "authorized_at": observed_at,
            },
        ),
        GoldenPathStep(
            "execute_dry_run",
            closed_loop.executed,
            {
                "context_id": context_id,
                "command_id": closed_loop.command_id,
                "executed": closed_loop.executed,
                "dry_run_action": (
                    closed_loop.approval.dry_run.plan.action
                    if closed_loop.approval is not None else ""
                ),
            },
        ),
        GoldenPathStep(
            "inspect_operational_workflow",
            True,
            {"workflow_steps": control_plane.summary.workflow_steps},
        ),
        GoldenPathStep(
            "inspect_audit_replay",
            True,
            {"audit_entries": control_plane.summary.governance_audits},
        ),
        GoldenPathStep(
            "agent_proposes_bounded_alternative",
            closed_loop.executed,
            {
                "provider": "closed-loop-replenishment-rule",
                "proposal": "issue replenishment",
                "canonical_event": closed_loop.canonical_event is not None,
                "state_after": closed_loop.state_after.to_mapping(),
            },
        ),
    )

    ok_count = sum(1 for step in steps if step.ok)
    summary = PrimaryLaunchSummary(
        step_count=len(steps),
        ok_count=ok_count,
        exception_count=control_plane.summary.exception_count,
        decision_actionable=control_plane.summary.actionable_decision,
        simulation_steps=control_plane.summary.simulation_steps,
        plan_periods=control_plane.summary.plan_periods,
        workflow_steps=control_plane.summary.workflow_steps,
        audit_entries=control_plane.summary.governance_audits,
        closed_loop_executed=closed_loop.executed,
        canonical_event=closed_loop.canonical_event is not None,
    )
    accepted = ok_count == len(steps) and summary.closed_loop_executed

    payload = {
        "ontology_release": ONTOLOGY_RELEASE,
        "os_release": OS_RELEASE,
        "control_plane_run_id": control_plane.run_id,
        "closed_loop_command_id": closed_loop_command_id,
        "context_id": context_id,
        "operator_id": operator_id,
        "observed_at": observed_at,
    }
    result_id = _evidence_id(payload)

    return PrimaryLaunchResult(
        result_id=result_id,
        accepted=accepted,
        ontology_release=ONTOLOGY_RELEASE,
        os_release=OS_RELEASE,
        control_plane=control_plane,
        closed_loop=closed_loop,
        steps=steps,
        summary=summary,
    )


def _self_check() -> None:
    """Run the Golden Path once from fixed inputs and fail closed on error."""
    result = run_primary_launch(
        context_id="launch",
        operator_id="operator-launch",
        authority="scm-os-reference",
        observed_at="2026-08-19T10:00:00Z",
    )
    if not result.accepted:
        failed = [s.step for s in result.steps if not s.ok]
        raise PrimaryLaunchError(
            f"primary launch self-check failed; steps not ok: {failed}"
        )
    print(f"primary-launch self-check OK: {result.result_id}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="primary_launch",
        description="Run the SCM Ontology / SCM OS Reference primary-launch Golden Path.",
    )
    parser.add_argument(
        "--self-check",
        action="store_true",
        help="Run a single deterministic Golden Path and fail closed on error.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the accepted Golden Path result as JSON to stdout.",
    )
    args = parser.parse_args(argv)

    if args.self_check:
        _self_check()
        return 0

    result = run_primary_launch(
        context_id="launch",
        operator_id="operator-launch",
        authority="scm-os-reference",
        observed_at="2026-08-19T10:00:00Z",
    )
    if args.json:
        print(result.to_json())
    else:
        print(f"primary-launch accepted={result.accepted} result_id={result.result_id}")
    return 0 if result.accepted else 1


if __name__ == "__main__":
    sys.exit(main())
