"""SCM OS Phase 6 Acceptance (P6-F).

Closes Phase 6 (SCM OS Control Plane) with a deterministic acceptance contract:
the major existing runtime capabilities are *discoverable* and *operable* from
one coherent SCM OS surface.

P6-F defines an explicit Phase 6 capability inventory (the P6-A..P6-E
control-plane surfaces plus the underlying governed R5 application), probes each
capability deterministically, and folds the results into an immutable,
content-addressed ``Phase6AcceptanceReport`` with an overall ``accepted`` flag.

P6-F composes the existing P6-A..P6-E entry points. It re-derives no decision,
mutates no Canonical Truth, and performs no external side effect.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Callable

from .decision_inbox import InboxDecision, build_decision_inbox
from .execution_workspace import launch_execution_workflow
from .replenishment_application import (
    ReplenishmentObservation,
    run_replenishment_application,
)
from .scm_os_cockpit import run_cockpit_reference_path
from .sim_optim_workspace import launch_reference_workspace
from .control_plane_e2e import ControlPlaneRequest, run_control_plane_flow


class Phase6AcceptanceError(ValueError):
    """Raised when an acceptance input or invocation is invalid."""


_CAPABILITIES: tuple[tuple[str, str, Callable[[], Any]], ...] = (
    (
        "cockpit",
        "SCM OS Cockpit v0 (P6-A)",
        lambda: run_cockpit_reference_path().to_mapping(),
    ),
    (
        "governed_application",
        "Governed replenishment application (S358)",
        lambda: run_replenishment_application(
            ReplenishmentObservation(
                product_id="P-1", location_id="WH-1", on_hand=5.0,
                reorder_point=10.0, reorder_quantity=25.0,
                evidence_ids=("e1",), provenance_ids=("p1",),
            ),
            context_id="ctx-accept", actor_id="planner-1",
            authority="supply-chain-manager", authorized_at="2026-08-18T16:00:00Z",
            command_id="cmd-a", dry_ran_at="2026-08-18T16:00:01Z",
        ).governed is not None,
    ),
    (
        "decision_inbox",
        "Decision Inbox (P6-B)",
        lambda: build_decision_inbox(
            (
                InboxDecision(
                    run_replenishment_application(
                        ReplenishmentObservation(
                            product_id="P-1", location_id="WH-1", on_hand=5.0,
                            reorder_point=10.0, reorder_quantity=25.0,
                            evidence_ids=("e1",), provenance_ids=("p1",),
                        ),
                        context_id="ctx-accept", actor_id="planner-1",
                        authority="supply-chain-manager",
                        authorized_at="2026-08-18T16:00:00Z",
                        command_id="cmd-b", dry_ran_at="2026-08-18T16:00:01Z",
                    ),
                    "dec-accept",
                ),
            ),
            viewed_at="2026-08-18T16:00:02Z",
            viewer_actor_id="operator-1",
        ).to_mapping(),
    ),
    (
        "simulation_optimization_workspace",
        "Simulation/Optimization Workspace (P6-C)",
        lambda: launch_reference_workspace().to_mapping(),
    ),
    (
        "execution_workspace",
        "Execution Workflow Workspace (P6-D)",
        lambda: launch_execution_workflow(
            governed_runs=(
                run_replenishment_application(
                    ReplenishmentObservation(
                        product_id="P-1", location_id="WH-1", on_hand=5.0,
                        reorder_point=10.0, reorder_quantity=25.0,
                        evidence_ids=("e1",), provenance_ids=("p1",),
                    ),
                    context_id="ctx-accept", actor_id="planner-1",
                    authority="supply-chain-manager",
                    authorized_at="2026-08-18T16:00:00Z",
                    command_id="cmd-c", dry_ran_at="2026-08-18T16:00:01Z",
                ).governed,
            ),
            actor_id="planner-1",
            recorded_at="2026-08-18T16:00:02Z",
        ).to_mapping(),
    ),
    (
        "control_plane_e2e",
        "Control Plane E2E (P6-E)",
        lambda: run_control_plane_flow(
            ControlPlaneRequest(
                context_id="ctx-accept", operator_id="operator-1",
                authority="supply-chain-manager", observed_at="2026-08-18T16:00:00Z",
            )
        ).to_mapping(),
    ),
)


@dataclass(frozen=True)
class CapabilityResult:
    """Deterministic probe result for one Phase 6 capability."""

    key: str
    name: str
    operable: bool
    evidence_id: str
    error: str | None = None

    def to_mapping(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "key": self.key,
            "name": self.name,
            "operable": self.operable,
            "evidence_id": self.evidence_id,
        }
        if self.error is not None:
            value["error"] = self.error
        return value


@dataclass(frozen=True)
class AcceptanceSummary:
    """Deterministic aggregate counts across the capability probes."""

    capability_count: int
    operable_count: int
    failed_count: int

    def to_mapping(self) -> dict[str, Any]:
        return {
            "capability_count": self.capability_count,
            "operable_count": self.operable_count,
            "failed_count": self.failed_count,
        }


@dataclass(frozen=True)
class Phase6AcceptanceReport:
    """Immutable, content-addressed Phase 6 acceptance report."""

    report_id: str
    accepted: bool
    accepted_at: str
    capabilities: tuple[CapabilityResult, ...]
    summary: AcceptanceSummary

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P6F.1",
            "is_phase6_acceptance": True,
            "report_id": self.report_id,
            "accepted": self.accepted,
            "accepted_at": self.accepted_at,
            "summary": self.summary.to_mapping(),
            "capabilities": [cap.to_mapping() for cap in self.capabilities],
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def _evidence_id(output: Any) -> str:
    payload = json.dumps(
        output, ensure_ascii=False, sort_keys=True,
        separators=(",", ":"), default=str,
    )
    return sha256(payload.encode()).hexdigest()


def _probe(key: str, name: str, fn: Callable[[], Any]) -> CapabilityResult:
    try:
        output = fn()
    except Exception as exc:  # noqa: BLE001 - acceptance probe must fail closed
        return CapabilityResult(
            key=key, name=name, operable=False,
            evidence_id="", error=f"{type(exc).__name__}: {exc}",
        )
    if output is None or output is False:
        return CapabilityResult(
            key=key, name=name, operable=False,
            evidence_id="", error="probe produced no usable output",
        )
    return CapabilityResult(
        key=key, name=name, operable=True, evidence_id=_evidence_id(output),
    )


def run_phase6_acceptance(*, accepted_at: str) -> Phase6AcceptanceReport:
    """Run the Phase 6 capability probes and produce an acceptance report.

    A capability is operable when its deterministic probe returns a usable
    result without error. The phase is accepted when every capability is
    operable.
    """
    if not isinstance(accepted_at, str) or not accepted_at.strip():
        raise Phase6AcceptanceError("accepted_at must be non-empty")

    capabilities = tuple(
        _probe(key, name, fn) for key, name, fn in _CAPABILITIES
    )
    operable = sum(1 for cap in capabilities if cap.operable)
    summary = AcceptanceSummary(
        capability_count=len(capabilities),
        operable_count=operable,
        failed_count=len(capabilities) - operable,
    )
    accepted = operable == len(capabilities)

    payload = {
        "accepted_at": accepted_at,
        "capabilities": [cap.to_mapping() for cap in capabilities],
    }
    report_id = sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return Phase6AcceptanceReport(
        report_id=report_id,
        accepted=accepted,
        accepted_at=accepted_at,
        capabilities=capabilities,
        summary=summary,
    )
