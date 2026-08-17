"""SCM Governed Simulation Application (Phase 5, S363).

Composes the existing Phase R5 governed applications (replenishment S358,
procurement S360, production S361, distribution S362) into a multi-period,
multi-decision simulation that runs each decision through the S348 governed
loop.

A simulation is a bounded sequence of governed decisions executed against a
shared context. Each R5 observation produces an authorized ExecutionCommand and
an S353 dry run, recorded in an immutable, deterministic, side-effect-free run.

S363 introduces no new canonical semantics and performs no external side
effect. It reuses the S348 governed loop, the S351 rule-based provider, and the
S353 execution runtime, and preserves the M8 boundary between derived
decisions and Canonical Truth.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Any, Callable, Iterable

from .distribution_application import (
    DistributionDecision,
    DistributionObservation,
    run_distribution_application,
)
from .execution_runtime import ExecutionAdapter
from .procurement_application import (
    ProcurementDecision,
    ProcurementObservation,
    run_procurement_application,
)
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


class GovernedSimulationError(ValueError):
    """Raised when a governed simulation input or invocation is invalid."""


class SimulationApplication(str, Enum):
    """The supported R5 decision applications in a governed simulation."""

    REPLENISHMENT = "replenishment"
    PROCUREMENT = "procurement"
    PRODUCTION = "production"
    DISTRIBUTION = "distribution"


# Dispatch table: application -> runner callable + decision verifier.
_RUNNERS: dict[str, Callable[..., Any]] = {
    SimulationApplication.REPLENISHMENT.value: run_replenishment_application,
    SimulationApplication.PROCUREMENT.value: run_procurement_application,
    SimulationApplication.PRODUCTION.value: run_production_application,
    SimulationApplication.DISTRIBUTION.value: run_distribution_application,
}

_DECISION_TYPES: dict[str, type] = {
    SimulationApplication.REPLENISHMENT.value: ReplenishmentDecision,
    SimulationApplication.PROCUREMENT.value: ProcurementDecision,
    SimulationApplication.PRODUCTION.value: ProductionDecision,
    SimulationApplication.DISTRIBUTION.value: DistributionDecision,
}


@dataclass(frozen=True)
class SimulationStep:
    """One governed R5 decision bound to its observation and command id."""

    step_id: str
    application: SimulationApplication
    observation: Any
    command_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.step_id, str) or not self.step_id.strip():
            raise GovernedSimulationError("step_id must be non-empty")
        if not isinstance(self.application, SimulationApplication):
            raise GovernedSimulationError("application must be a SimulationApplication")
        if self.application.value not in _RUNNERS:
            raise GovernedSimulationError(f"unsupported application: {self.application}")
        if not isinstance(self.command_id, str) or not self.command_id.strip():
            raise GovernedSimulationError("command_id must be non-empty")


@dataclass(frozen=True)
class SimulationStepResult:
    """Immutable outcome of one governed simulation step."""

    step_id: str
    application: str
    action: str
    decision: Any
    command_id: str = ""

    def to_mapping(self) -> dict[str, Any]:
        return {
            "step_id": self.step_id,
            "application": self.application,
            "action": self.action,
            "command_id": self.command_id,
        }


@dataclass(frozen=True)
class GovernedSimulationResult:
    """Immutable bundle of every governed step in one simulation run."""

    simulation_run_id: str
    context_id: str
    steps: tuple[SimulationStep, ...]

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "S363.1",
            "simulation_run_id": self.simulation_run_id,
            "context_id": self.context_id,
            "steps": [step.to_mapping() for step in self.steps],
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def _simulation_run_id(steps: tuple[SimulationStep, ...], context_id: str) -> str:
    """Stable content-addressed id for a deterministic simulation run."""
    payload = {
        "context_id": context_id,
        "steps": [
            {
                "step_id": step.step_id,
                "application": step.application.value,
                "command_id": step.command_id,
            }
            for step in steps
        ],
    }
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def run_governed_simulation(
    steps: Iterable[SimulationStep],
    *,
    context_id: str,
    actor_id: str,
    authority: str,
    authorized_at: str,
    dry_ran_at: str,
    adapter: ExecutionAdapter | None = None,
) -> GovernedSimulationResult:
    """Run a bounded sequence of governed R5 decisions as one simulation.

    Each step dispatches to the matching R5 application runner. Steps that
    require no action (no reorder, no shortage, infeasible capacity) are
    recorded as ``no_action`` decisions with no command. Every governed
    decision runs through the S348 loop with an S353 dry run.
    """
    if not isinstance(context_id, str) or not context_id.strip():
        raise GovernedSimulationError("context_id must be non-empty")
    if not isinstance(actor_id, str) or not actor_id.strip():
        raise GovernedSimulationError("actor_id must be non-empty")
    if not isinstance(authority, str) or not authority.strip():
        raise GovernedSimulationError("authority must be non-empty")
    if not isinstance(authorized_at, str) or not authorized_at.strip():
        raise GovernedSimulationError("authorized_at must be non-empty")
    if not isinstance(dry_ran_at, str) or not dry_ran_at.strip():
        raise GovernedSimulationError("dry_ran_at must be non-empty")

    steps_tuple = tuple(steps)
    if not steps_tuple:
        raise GovernedSimulationError("steps must not be empty")

    step_ids = [step.step_id for step in steps_tuple]
    if len(step_ids) != len(set(step_ids)):
        raise GovernedSimulationError("step ids must be unique within the simulation")

    results: list[SimulationStepResult] = []
    for step in steps_tuple:
        runner = _RUNNERS[step.application.value]
        decision = runner(
            step.observation,
            context_id=context_id,
            actor_id=actor_id,
            authority=authority,
            authorized_at=authorized_at,
            command_id=step.command_id,
            dry_ran_at=dry_ran_at,
            adapter=adapter,
        )
        results.append(
            SimulationStepResult(
                step_id=step.step_id,
                application=step.application,
                action=decision.action,
                decision=decision,
                command_id=step.command_id,
            )
        )

    run_id = _simulation_run_id(steps_tuple, context_id)
    return GovernedSimulationResult(
        simulation_run_id=run_id,
        context_id=context_id,
        steps=tuple(results),
    )
