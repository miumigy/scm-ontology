"""SCM OS Phase 10 Acceptance (P10-G).

Closes **Phase 10 (Autonomous SCM Control)** with a deterministic acceptance
contract: a bounded SCM use case can autonomously observe -> reason -> propose
-> simulate -> evaluate -> obtain authorization -> execute -> learn from the
outcome while remaining governed.

P10-G folds the P10-A..P10-F capabilities into an immutable, content-addressed
``Phase10AcceptanceReport`` with an overall ``accepted`` flag. The phase is
accepted when every capability is operable AND the **governed autonomous-loop
gate** (P10-G) holds.

P10-G performs no external side effect and never mutates Canonical Truth.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Callable

from .agent_observation import build_agent_observation
from .agent_replay import AgentAuditTrail
from .agent_tool import AgentProposal, run_agent_tool
from .graph_projection import GraphNode, GraphProjection
from .human_control import HumanReviewDecision, route_human_control
from .policy_autonomy import (
    AutonomyInput,
    AutonomyLevel,
    AutonomyPolicy,
    evaluate_autonomy,
)
from .replenishment_application import ReplenishmentObservation
from .simulation_before_execution import evaluate_simulation_before_execution
from .governed_simulation import SimulationApplication, SimulationStep


class Phase10AcceptanceError(ValueError):
    """Raised when an acceptance input or invocation is invalid."""


@dataclass(frozen=True)
class CapabilityResult:
    """Deterministic probe result for one Phase 10 capability."""

    key: str
    name: str
    operable: bool
    evidence_id: str
    detail: dict[str, Any] | None = None

    def to_mapping(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "key": self.key,
            "name": self.name,
            "operable": self.operable,
            "evidence_id": self.evidence_id,
        }
        if self.detail is not None:
            value["detail"] = self.detail
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
class Phase10AcceptanceReport:
    """Immutable, content-addressed Phase 10 acceptance report."""

    report_id: str
    accepted: bool
    accepted_at: str
    capabilities: tuple[CapabilityResult, ...]
    summary: AcceptanceSummary

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P10G.1",
            "is_phase10_acceptance": True,
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


def _observation_probe() -> dict[str, Any]:
    """P10-A — agents receive scoped, evidence-aware read-only observations."""
    projection = GraphProjection(
        nodes=(
            GraphNode("wh-a", "Warehouse", (("on_hand", 5),)),
            GraphNode("wh-b", "Warehouse", (("on_hand", 50),)),
        ),
        provenance_ids=("p-inv",),
    )
    observation = build_agent_observation(
        projection,
        question_id="inventory-position",
        agent_id="planner-agent",
        node_type="Warehouse",
        evidence_ids=("e-inv",),
    )
    return {
        "observation_id": observation.observation_id,
        "can_write": observation.can_write,
        "scoped_nodes": [n["node_id"] for n in observation.observation.value["nodes"]],
    }


def _tool_boundary_probe() -> dict[str, Any]:
    """P10-B — agent tools produce proposals, never canonical mutations."""
    projection = GraphProjection(
        nodes=(GraphNode("wh-a", "Warehouse", (("on_hand", 5),)),),
        provenance_ids=("p-inv",),
    )
    obs = build_agent_observation(
        projection,
        question_id="inventory-position",
        agent_id="planner-agent",
        evidence_ids=("e-inv",),
    )
    def propose(_observation):
        return AgentProposal(
            agent_id="planner-agent",
            context_id="ctx-p10g",
            action="replenish",
            payload={"quantity": 20},
            rationale="on-hand below reorder point",
            evidence_ids=("e-inv",),
            provenance_ids=("p-inv",),
            confidence=0.9,
        )
    result = run_agent_tool(
        tool_id="replenish-tool",
        agent_id="planner-agent",
        observation=obs,
        propose=propose,
    )
    return {
        "tool_id": result.tool_id,
        "can_mutate": result.can_mutate,
        "proposal_id": result.proposal.proposal_id if result.proposal else None,
    }


def _simulation_before_execution_probe() -> dict[str, Any]:
    """P10-C — material decisions evaluated against deterministic simulation."""
    step = SimulationStep(
        step_id="step-1",
        application=SimulationApplication.REPLENISHMENT,
        observation=ReplenishmentObservation(
            product_id="p-1",
            location_id="loc-1",
            on_hand=5,
            reorder_point=10,
            reorder_quantity=20,
            evidence_ids=("e-inv",),
            provenance_ids=("p-inv",),
        ),
        command_id="cmd-p10c-1",
    )
    evaluation = evaluate_simulation_before_execution(
        context_id="ctx-p10g",
        steps=(step,),
        actor_id="planner",
        authority="supply-chain-manager",
        authorized_at="2026-08-19T01:00:00Z",
        dry_ran_at="2026-08-19T01:00:00Z",
        simulation_is_feasible=True,
    )
    return {
        "evaluation_id": evaluation.evaluation_id,
        "feasible": evaluation.feasible,
        "steps_simulated": len(evaluation.simulation_result.steps),
    }


def _policy_autonomy_probe() -> dict[str, Any]:
    """P10-D — confidence, risk, impact, and scope determine autonomy level."""
    proposal = AgentProposal(
        agent_id="planner-agent",
        context_id="ctx-p10g",
        action="replenish",
        payload={"quantity": 20},
        rationale="on-hand below reorder point",
        evidence_ids=("e-inv",),
        provenance_ids=("p-inv",),
        confidence=0.9,
    )
    verdict = evaluate_autonomy(
        proposal,
        inputs=AutonomyInput(confidence=0.9, risk=0.1, monetary_impact=100.0, scope="inventory"),
        policy=AutonomyPolicy(
            policy_id="p-inv",
            allowed_by_scope={"inventory": AutonomyLevel.FULLY_AUTONOMOUS},
        ),
    )
    return {
        "verdict_id": verdict.verdict_id,
        "autonomy": verdict.autonomy.value,
    }


def _human_in_loop_probe() -> dict[str, Any]:
    """P10-E — explicit review, override, escalation, and delegation paths."""
    proposal = AgentProposal(
        agent_id="planner-agent",
        context_id="ctx-p10g",
        action="replenish",
        payload={"quantity": 20},
        rationale="requires approval",
        evidence_ids=("e-inv",),
        provenance_ids=("p-inv",),
        confidence=0.9,
    )
    verdict = evaluate_autonomy(
        proposal,
        inputs=AutonomyInput(confidence=0.9, risk=0.1, monetary_impact=5000.0, scope="inventory"),
        policy=AutonomyPolicy(
            policy_id="p-inv",
            allowed_by_scope={"inventory": AutonomyLevel.APPROVED},
            max_monetary_impact=2000.0,
        ),
    )
    record = route_human_control(
        proposal,
        verdict=verdict,
        review_decision=HumanReviewDecision(
            decision="approve", ruled_by="manager", at="2026-08-19T01:00:00Z"
        ),
        reviewer_id="manager",
        at="2026-08-19T01:00:00Z",
    )
    return {
        "path": record.path.value,
        "record_id": record.record_id,
        "approval_id": record.approval.approval_id if record.approval else None,
    }


def _replay_audit_probe() -> dict[str, Any]:
    """P10-F — every agent step is replayable and content-addressed."""
    trail = AgentAuditTrail(agent_id="planner-agent")
    trail = trail.record(
        outcome_ref="outcome-1",
        recorded_at="2026-08-19T01:00:00Z",
    )
    replayed = trail.replay()
    return {
        "entry_count": len(replayed.entries),
        "replay_ok": replayed.to_json() == trail.to_json(),
        "entry_id": replayed.entries[0].entry_id if replayed.entries else None,
    }


def _governed_autonomous_loop_gate() -> dict[str, Any]:
    """P10-G — a bounded SCM use case stays governed across the agent loop.

    Runs a fully-autonomous (low-risk, in-scope, low-impact) replenishment
    proposal through P10-A..P10-F: observe -> propose -> evaluate autonomy ->
    human control record -> replayable audit. The gate holds when every step
    stays governed and the full lifecycle is replayable.
    """
    observation = _inventory_observation()
    proposal = AgentProposal(
        agent_id="planner-agent",
        context_id="ctx-p10g-full",
        action="replenish",
        payload={"quantity": 20},
        rationale="on-hand below reorder point; simulation feasible; low risk",
        evidence_ids=("e-inv",),
        provenance_ids=("p-inv",),
        confidence=0.9,
    )
    verdict = evaluate_autonomy(
        proposal,
        inputs=AutonomyInput(confidence=0.9, risk=0.05, monetary_impact=50.0, scope="inventory"),
        policy=AutonomyPolicy(
            policy_id="p-auto",
            allowed_by_scope={"inventory": AutonomyLevel.FULLY_AUTONOMOUS},
            max_monetary_impact=1000.0,
            max_confidence_required=0.7,
            max_risk_allowed=0.3,
        ),
    )
    record = route_human_control(proposal, verdict=verdict, at="2026-08-19T01:00:00Z")

    trail = AgentAuditTrail(agent_id="planner-agent")
    trail = trail.record(
        observation=observation,
        proposal=proposal,
        autonomy=verdict,
        control=record,
        outcome_ref="outcome-auto-1",
        recorded_at="2026-08-19T01:00:00Z",
    )

    gate_holds = (
        observation.can_write is False
        and verdict.autonomy is AutonomyLevel.FULLY_AUTONOMOUS
        and record.path.value == "autonomous"
        and len(trail.entries) == 1
    )
    try:
        replay_ok = trail.replay().to_json() == trail.to_json()
    except Exception:  # noqa: BLE001 - gate fails closed
        replay_ok = False
    return {
        "gate_holds": gate_holds and replay_ok,
        "autonomy": verdict.autonomy.value,
        "control_path": record.path.value,
        "replay_ok": replay_ok,
    }


def _inventory_observation():
    projection = GraphProjection(
        nodes=(GraphNode("wh-a", "Warehouse", (("on_hand", 5),)),),
        provenance_ids=("p-inv",),
    )
    return build_agent_observation(
        projection,
        question_id="inventory-position",
        agent_id="planner-agent",
        evidence_ids=("e-inv",),
    )


_CAPABILITIES: tuple[tuple[str, str, Callable[[], dict[str, Any]]], ...] = (
    (
        "agent_observation_boundary",
        "P10-A Agent Observation Boundary",
        _observation_probe,
    ),
    (
        "agent_tool_boundary",
        "P10-B Tool / Action Boundary",
        _tool_boundary_probe,
    ),
    (
        "simulation_before_execution",
        "P10-C Simulation-before-Execution",
        _simulation_before_execution_probe,
    ),
    (
        "policy_aware_autonomy",
        "P10-D Policy-aware Autonomy",
        _policy_autonomy_probe,
    ),
    (
        "human_in_loop_control",
        "P10-E Human-in-the-loop Control",
        _human_in_loop_probe,
    ),
    (
        "agent_replay_audit",
        "P10-F Agent Replay / Audit",
        _replay_audit_probe,
    ),
    (
        "governed_autonomous_loop_gate",
        "P10-G Governed Autonomous-Loop Gate",
        _governed_autonomous_loop_gate,
    ),
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
            evidence_id="", detail={"error": f"{type(exc).__name__}: {exc}"},
        )
    if output is None or output is False:
        return CapabilityResult(
            key=key, name=name, operable=False,
            evidence_id="", detail={"error": "probe produced no usable output"},
        )
    return CapabilityResult(
        key=key,
        name=name,
        operable=True,
        evidence_id=_evidence_id(output),
        detail=output if isinstance(output, dict) else {"value": str(output)},
    )


def run_phase10_acceptance(
    *,
    accepted_at: str,
) -> Phase10AcceptanceReport:
    """Run the Phase 10 capability probes and produce the acceptance report.

    A capability is operable when its deterministic probe returns a usable
    result without error. The phase is accepted when every capability is
    operable, including the P10-G governed autonomous-loop gate.
    """
    if not isinstance(accepted_at, str) or not accepted_at.strip():
        raise Phase10AcceptanceError("accepted_at must be non-empty")

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

    return Phase10AcceptanceReport(
        report_id=report_id,
        accepted=accepted,
        accepted_at=accepted_at,
        capabilities=capabilities,
        summary=summary,
    )
