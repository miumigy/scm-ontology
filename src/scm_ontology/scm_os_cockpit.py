"""SCM OS Cockpit v0 (Phase 6, P6-A).

A minimal, read-only web control plane that *composes* the existing governed
SCM OS runtime contracts into one browsable surface. It exposes the governed
state, exceptions, decisions, simulation, execution, and governance produced by
the prior phases (R5 applications S358-S362, demand/supply gap, governed
simulation S363, operational workflow S366) without re-deriving any decision
and without mutating Canonical Truth.

The cockpit is a bounded, in-memory reference capability:

  - ``CockpitFixture`` wraps the existing governed artifacts to compose;
  - ``build_cockpit_state`` folds them into an immutable, content-addressed
    ``CockpitState`` snapshot with domain projections and an overview;
  - ``run_cockpit_reference_path`` is the deterministic reference path that
    composes the existing governed applications end to end;
  - a stdlib ``BaseHTTPRequestHandler`` adapter serves the snapshot read-only.

Design rules honored: compose existing contracts, do not duplicate semantics,
protect Canonical Truth, fail closed, deterministic reference path first, and
side effects are explicit (GET-only, no writes).
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from threading import Thread
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
import urllib.parse

from .command_lifecycle import CommandState
from .demand_supply_gap import (
    DemandSupplyGap,
    DemandSupplyRecord,
    resolve_demand_supply_gap,
)
from .distribution_application import (
    DistributionDecision,
    DistributionObservation,
    run_distribution_application,
)
from .governed_simulation import (
    GovernedSimulationResult,
    SimulationApplication,
    SimulationStep,
    run_governed_simulation,
)
from .operational_workflow import (
    OperationalStep,
    OperationalWorkflowResult,
    run_operational_workflow,
)
from .procurement_application import ProcurementDecision
from .production_application import (
    ProductionDecision,
    ProductionObservation,
    run_production_application,
)
from .replenishment_application import (
    ReplenishmentDecision,
    ReplenishmentObservation,
    run_replenishment_application,
)


class CockpitError(ValueError):
    """Raised when the cockpit input or invocation is invalid."""


_DECISION_TYPES: dict[str, type] = {
    "replenishment": ReplenishmentDecision,
    "procurement": ProcurementDecision,
    "production": ProductionDecision,
    "distribution": DistributionDecision,
}

_SUPPORTED_DECISIONS = tuple(_DECISION_TYPES.values())


@dataclass(frozen=True)
class CockpitFixture:
    """Immutable bundle of governed artifacts the cockpit composes.

    The cockpit never re-derives or mutates these artifacts; it only projects
    them into a browsable, deterministic snapshot.
    """

    context_id: str
    recorded_at: str
    actor_id: str
    decisions: tuple[Any, ...] = ()
    gaps: tuple[DemandSupplyGap, ...] = ()
    simulation: GovernedSimulationResult | None = None
    workflow: OperationalWorkflowResult | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.context_id, str) or not self.context_id.strip():
            raise CockpitError("context_id must be non-empty")
        if not isinstance(self.recorded_at, str) or not self.recorded_at.strip():
            raise CockpitError("recorded_at must be non-empty")
        if not isinstance(self.actor_id, str) or not self.actor_id.strip():
            raise CockpitError("actor_id must be non-empty")
        for decision in self.decisions:
            if not isinstance(decision, _SUPPORTED_DECISIONS):
                raise CockpitError(
                    f"unsupported decision artifact: {type(decision).__name__}"
                )
        for gap in self.gaps:
            if not isinstance(gap, DemandSupplyGap):
                raise CockpitError("gaps must contain DemandSupplyGap values")
        if self.simulation is not None and not isinstance(
            self.simulation, GovernedSimulationResult
        ):
            raise CockpitError("simulation must be a GovernedSimulationResult")
        if self.workflow is not None and not isinstance(
            self.workflow, OperationalWorkflowResult
        ):
            raise CockpitError("workflow must be an OperationalWorkflowResult")


@dataclass(frozen=True)
class CockpitOverview:
    """Deterministic aggregate counts across the cockpit domains."""

    decision_count: int
    actionable_decisions: int
    no_action_decisions: int
    exception_count: int
    simulation_steps: int
    workflow_steps: int
    execution_dry_runs: int
    governance_audits: int
    governance_in_dry_run: int

    def to_mapping(self) -> dict[str, Any]:
        return {
            "decision_count": self.decision_count,
            "actionable_decisions": self.actionable_decisions,
            "no_action_decisions": self.no_action_decisions,
            "exception_count": self.exception_count,
            "simulation_steps": self.simulation_steps,
            "workflow_steps": self.workflow_steps,
            "execution_dry_runs": self.execution_dry_runs,
            "governance_audits": self.governance_audits,
            "governance_in_dry_run": self.governance_in_dry_run,
        }


def _decision_domain(decision: Any) -> dict[str, Any]:
    """Project one R5 decision into a read-only cockpit record."""
    mapping = decision.to_mapping()
    return {
        "type": type(decision).__name__,
        "action": getattr(decision, "action", ""),
        "has_governed_result": getattr(decision, "governed", None) is not None,
        "payload": mapping,
    }


def _exception_domain(gaps: tuple[DemandSupplyGap, ...]) -> list[dict[str, Any]]:
    return [gap.to_mapping() for gap in gaps]


def _simulation_domain(simulation: GovernedSimulationResult | None) -> list[dict[str, Any]]:
    if simulation is None:
        return []
    return [
        {
            "step_id": step.step_id,
            "application": step.application.value
            if isinstance(step.application, SimulationApplication)
            else step.application,
            "action": step.action,
            "command_id": step.command_id or None,
        }
        for step in simulation.steps
    ]


def _execution_domain(
    decisions: tuple[Any, ...], workflow: OperationalWorkflowResult | None
) -> list[dict[str, Any]]:
    """Expose dry-run results for governed decisions and workflow command states."""
    dry_runs: list[dict[str, Any]] = []
    for decision in decisions:
        governed = getattr(decision, "governed", None)
        if governed is None:
            continue
        dry_runs.append(
            {
                "result_id": governed.dry_run.result_id,
                "status": governed.dry_run.status,
                "command_id": governed.dry_run.command.command_id,
                "execution_target": governed.dry_run.plan.execution_target,
                "action": governed.dry_run.plan.action,
                "detail": governed.dry_run.plan.detail,
            }
        )
    if workflow is not None:
        for step in workflow.steps:
            dry_runs.append(
                {
                    "workflow_step_id": step.step_id,
                    "application": step.application,
                    "command_id": step.command_id or None,
                    "state": step.state,
                }
            )
    return dry_runs


def _governance_domain(workflow: OperationalWorkflowResult | None) -> list[dict[str, Any]]:
    if workflow is None:
        return []
    return [
        {
            "step_id": step.step_id,
            "application": step.application,
            "command_id": step.command_id or None,
            "audit_id": step.audit_id,
            "command_state": step.state,
        }
        for step in workflow.steps
    ]


@dataclass(frozen=True)
class CockpitState:
    """Immutable, content-addressed snapshot of the governed SCM OS runtime."""

    snapshot_id: str
    context_id: str
    recorded_at: str
    actor_id: str
    decisions: tuple[dict[str, Any], ...]
    exceptions: tuple[dict[str, Any], ...]
    simulation: tuple[dict[str, Any], ...]
    execution: tuple[dict[str, Any], ...]
    governance: tuple[dict[str, Any], ...]
    overview: CockpitOverview

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P6A.1",
            "is_operational_tool": True,
            "snapshot_id": self.snapshot_id,
            "context_id": self.context_id,
            "recorded_at": self.recorded_at,
            "actor_id": self.actor_id,
            "overview": self.overview.to_mapping(),
            "domains": {
                "decisions": list(self.decisions),
                "exceptions": list(self.exceptions),
                "simulation": list(self.simulation),
                "execution": list(self.execution),
                "governance": list(self.governance),
            },
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

    def domain_json(self, domain: str) -> str:
        key = {"decisions": "decisions", "exceptions": "exceptions",
               "simulation": "simulation", "execution": "execution",
               "governance": "governance"}.get(domain)
        if key is None:
            raise CockpitError(f"unknown domain: {domain}")
        return json.dumps(
            list(self.to_mapping()["domains"][key]),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def build_cockpit_state(fixture: CockpitFixture) -> CockpitState:
    """Fold a CockpitFixture into an immutable, deterministic snapshot.

    Composition only: the cockpit never re-derives a decision, never mutates
    Canonical Truth, and never performs an external side effect.
    """
    if not isinstance(fixture, CockpitFixture):
        raise CockpitError("fixture must be a CockpitFixture")

    decisions = tuple(_decision_domain(decision) for decision in fixture.decisions)
    exceptions = tuple(_exception_domain(fixture.gaps))
    simulation = tuple(_simulation_domain(fixture.simulation))
    execution = tuple(_execution_domain(fixture.decisions, fixture.workflow))
    governance = tuple(_governance_domain(fixture.workflow))

    actionable = sum(1 for d in fixture.decisions if getattr(d, "governed", None) is not None)
    overview = CockpitOverview(
        decision_count=len(fixture.decisions),
        actionable_decisions=actionable,
        no_action_decisions=len(fixture.decisions) - actionable,
        exception_count=len(fixture.gaps),
        simulation_steps=len(simulation),
        workflow_steps=0 if fixture.workflow is None else len(fixture.workflow.steps),
        execution_dry_runs=sum(1 for e in execution if "result_id" in e),
        governance_audits=sum(1 for g in governance if g.get("audit_id") is not None),
        governance_in_dry_run=sum(
            1 for g in governance if g.get("command_state") == CommandState.DRY_RUN.value
        ),
    )

    payload = {
        "context_id": fixture.context_id,
        "recorded_at": fixture.recorded_at,
        "actor_id": fixture.actor_id,
        "decisions": list(decisions),
        "exceptions": list(exceptions),
        "simulation": list(simulation),
        "execution": list(execution),
        "governance": list(governance),
    }
    snapshot_id = sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return CockpitState(
        snapshot_id=snapshot_id,
        context_id=fixture.context_id,
        recorded_at=fixture.recorded_at,
        actor_id=fixture.actor_id,
        decisions=decisions,
        exceptions=exceptions,
        simulation=simulation,
        execution=execution,
        governance=governance,
        overview=overview,
    )


def run_cockpit_reference_path(
    *,
    context_id: str = "ctx-cockpit",
    recorded_at: str = "2026-08-18T12:00:00Z",
    actor_id: str = "planner-1",
) -> CockpitState:
    """Deterministic reference path that composes the governed SCM OS runtime.

    Reuses the existing R5 applications (replenishment, production), the
    demand/supply gap business question, the governed simulation, and the
    operational workflow to populate every cockpit domain. No new canonical
    semantics and no external side effect.
    """
    authority = "supply-chain-manager"
    authorized_at = recorded_at
    dry_ran_at = recorded_at

    # State / exceptions: an explicit shortfall across item/period/unit scope.
    gaps = resolve_demand_supply_gap(
        (
            DemandSupplyRecord(
                item_id="A-100", quantity=120.0, kind="demand", unit="unit",
                period_start="2026-08-18", period_end="2026-08-18",
                evidence_id="e1", provenance_id="p1",
            ),
            DemandSupplyRecord(
                item_id="A-100", quantity=90.0, kind="supply", unit="unit",
                period_start="2026-08-18", period_end="2026-08-18",
                evidence_id="e2", provenance_id="p2",
            ),
        )
    )

    # Decisions via the existing governed applications.
    decision_r = run_replenishment_application(
        ReplenishmentObservation(
            product_id="P-1", location_id="WH-1", on_hand=5.0,
            reorder_point=10.0, reorder_quantity=25.0,
            evidence_ids=("e1",), provenance_ids=("p1",),
        ),
        context_id=context_id, actor_id=actor_id, authority=authority,
        authorized_at=authorized_at, command_id="cmd-r", dry_ran_at=dry_ran_at,
    )

    decision_p = run_production_application(
        ProductionObservation(
            resource_id="LINE-1", required=80.0, capacity=100.0,
            evidence_ids=("e2",), provenance_ids=("p2",),
        ),
        context_id=context_id, actor_id=actor_id, authority=authority,
        authorized_at=authorized_at, command_id="cmd-p", dry_ran_at=dry_ran_at,
    )

    # Simulation via the existing governed simulation.
    simulation = run_governed_simulation(
        (
            SimulationStep(
                step_id="sim-1", application=SimulationApplication.REPLENISHMENT,
                observation=ReplenishmentObservation(
                    product_id="P-1", location_id="WH-1", on_hand=5.0,
                    reorder_point=10.0, reorder_quantity=25.0,
                    evidence_ids=("e1",), provenance_ids=("p1",),
                ),
                command_id="cmd-sr",
            ),
            SimulationStep(
                step_id="sim-2", application=SimulationApplication.DISTRIBUTION,
                observation=DistributionObservation(
                    shipment_id="S", item_id="I", required_quantity=80.0,
                    capacity=100.0, origin_location_id="WH",
                    destination_location_id="DC",
                    evidence_ids=("e3",), provenance_ids=("p3",),
                ),
                command_id="cmd-sd",
            ),
        ),
        context_id=context_id, actor_id=actor_id, authority=authority,
        authorized_at=authorized_at, dry_ran_at=dry_ran_at,
    )

    # Operational workflow: audits + command lifecycle into dry-run state.
    workflow = run_operational_workflow(
        (
            OperationalStep(step_id="w1", application="replenishment", command_id="cmd-r", decision=decision_r),
            OperationalStep(step_id="w2", application="production", command_id="cmd-p", decision=decision_p),
        ),
        workflow_id="wf-cockpit", recorded_at=recorded_at, actor_id=actor_id,
    )

    fixture = CockpitFixture(
        context_id=context_id,
        recorded_at=recorded_at,
        actor_id=actor_id,
        decisions=(decision_r, decision_p),
        gaps=gaps,
        simulation=simulation,
        workflow=workflow,
    )
    return build_cockpit_state(fixture)


# ---------------------------------------------------------------------------
# Read-only HTTP adapter (stdlib)
# ---------------------------------------------------------------------------

_JSON_DOMAINS = ("decisions", "exceptions", "simulation", "execution", "governance")

_HTML_TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>SCM OS Cockpit (P6-A)</title></head>
<body>
<h1>SCM OS Cockpit v0</h1>
<p>contract_version: {version} &middot; snapshot_id: <code>{snapshot_id}</code></p>
<pre>{overview_json}</pre>
<ul>
<li><a href="/api/state">/api/state</a></li>
<li><a href="/api/decisions">/api/decisions</a></li>
<li><a href="/api/exceptions">/api/exceptions</a></li>
<li><a href="/api/simulation">/api/simulation</a></li>
<li><a href="/api/execution">/api/execution</a></li>
<li><a href="/api/governance">/api/governance</a></li>
</ul>
</body></html>
"""


def make_cockpit_handler(state: CockpitState) -> type[BaseHTTPRequestHandler]:
    """Build a read-only GET handler bound to an immutable cockpit snapshot."""

    if not isinstance(state, CockpitState):
        raise CockpitError("state must be a CockpitState")

    mapping = state.to_mapping()

    def _reply(handler: BaseHTTPRequestHandler, code: int, body: bytes, ctype: str) -> None:
        handler.send_response(code)
        handler.send_header("Content-Type", ctype)
        handler.send_header("Content-Length", str(len(body)))
        handler.end_headers()
        handler.wfile.write(body)

    class _CockpitHandler(BaseHTTPRequestHandler):
        def log_message(self, *args: Any) -> None:
            return  # deterministic, side-effect-free logging

        def _route(self) -> None:
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path
            if path == "/" or path == "":
                body = _HTML_TEMPLATE.format(
                    version=mapping["contract_version"],
                    snapshot_id=mapping["snapshot_id"],
                    overview_json=json.dumps(
                        mapping["overview"], ensure_ascii=False, sort_keys=True,
                        separators=(",", ":"),
                    ),
                ).encode("utf-8")
                _reply(self, 200, body, "text/html; charset=utf-8")
                return
            if path == "/api/state":
                body = state.to_json().encode("utf-8")
                _reply(self, 200, body, "application/json; charset=utf-8")
                return
            if path.startswith("/api/"):
                domain = path[len("/api/"):]
                if domain in _JSON_DOMAINS:
                    body = state.domain_json(domain).encode("utf-8")
                    _reply(self, 200, body, "application/json; charset=utf-8")
                    return
            _reply(self, 404, b'{"error": "not found"}', "application/json; charset=utf-8")

        def do_GET(self) -> None:  # noqa: N802 (http.server naming)
            self._route()

        def do_POST(self) -> None:  # noqa: N802
            _reply(self, 405, b'{"error": "method not allowed"}', "application/json; charset=utf-8")

        def do_PUT(self) -> None:  # noqa: N802
            _reply(self, 405, b'{"error": "method not allowed"}', "application/json; charset=utf-8")

        def do_DELETE(self) -> None:  # noqa: N802
            _reply(self, 405, b'{"error": "method not allowed"}', "application/json; charset=utf-8")

    return _CockpitHandler


def create_cockpit_server(
    state: CockpitState, *, host: str = "127.0.0.1", port: int = 8000
) -> ThreadingHTTPServer:
    """Create a thread-per-request HTTP server serving the cockpit read-only.

    Callers are responsible for lifecycle (serve_forever / shutdown / close).
    """
    handler = make_cockpit_handler(state)
    return ThreadingHTTPServer((host, port), handler)


def run_cockpit_server(
    state: CockpitState, *, host: str = "127.0.0.1", port: int = 8000
) -> None:
    """Run the cockpit HTTP server in the current thread (blocking)."""
    server = create_cockpit_server(state, host=host, port=port)
    try:
        server.serve_forever()
    finally:
        server.server_close()


class CockpitServerThread:
    """Small convenience wrapper to run the cockpit server on a background thread."""

    def __init__(self, state: CockpitState, *, host: str = "127.0.0.1", port: int = 0) -> None:
        self._server = create_cockpit_server(state, host=host, port=port)
        self._thread: Thread | None = None

    def start(self) -> None:
        if self._thread is not None:
            raise CockpitError("server already started")
        self._thread = Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()

    @property
    def port(self) -> int:
        return self._server.server_address[1]

    def stop(self) -> None:
        self._server.shutdown()
        self._server.server_close()
        self._thread = None
