"""P10-C — Simulation-before-Execution.

Material decisions can be evaluated against deterministic
simulation/optimization *before* authorization. This slice composes the
existing S363 governed simulation path with a bounded evaluation gate that the
governance layer consults before an ``ExecutionCommand`` is authorized.

The flow:

```text
AgentProposal (P10-B)
        ↓
SimulationStep(s) evaluated through governed_simulation (S363, dry-run only)
        ↓
AgentSimulationEvaluation (deterministic, content-addressed, no side effect)
        ↓
evaluation gate consulted before authorization
```

P10-C introduces no new canonical semantics and performs no external side
effect: simulation is always a deterministic, dry-run-only evaluation. A
material decision may be simulated before authorization, but authorization
(and any execution) remains governed.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Iterable

from .governed_simulation import (
    GovernedSimulationError,
    GovernedSimulationResult,
    SimulationStep,
    run_governed_simulation,
)


class SimulationBeforeExecutionError(ValueError):
    """Raised when a simulation-before-execution evaluation violates P10-C."""


@dataclass(frozen=True)
class AgentSimulationEvaluation:
    """Immutable, deterministic evaluation of a proposal against simulation."""

    evaluation_id: str
    context_id: str
    simulation_result: GovernedSimulationResult
    feasible: bool
    rationale: str
    simulated_command_ids: tuple[str, ...] = ()
    simulated_at: str = ""

    def __post_init__(self) -> None:
        if not self.context_id.strip():
            raise SimulationBeforeExecutionError("context_id must be non-empty")
        if not self.rationale.strip():
            raise SimulationBeforeExecutionError("rationale must be non-empty")
        object.__setattr__(
            self,
            "simulated_command_ids",
            tuple(sorted(set(self.simulated_command_ids))),
        )

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P10C.1",
            "evaluation_id": self.evaluation_id,
            "context_id": self.context_id,
            "feasible": self.feasible,
            "rationale": self.rationale,
            "simulated_command_ids": list(self.simulated_command_ids),
            "simulated_at": self.simulated_at,
            "simulation": self.simulation_result.to_mapping(),
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def _evaluation_id(
    context_id: str,
    simulation: GovernedSimulationResult,
    feasible: bool,
    rationale: str,
) -> str:
    payload = json.dumps(
        {
            "context_id": context_id,
            "simulation_run_id": simulation.simulation_run_id,
            "feasible": feasible,
            "rationale": rationale,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return sha256(payload.encode()).hexdigest()


def evaluate_simulation_before_execution(
    *,
    context_id: str,
    steps: Iterable[SimulationStep],
    actor_id: str,
    authority: str,
    authorized_at: str,
    dry_ran_at: str,
    simulation_is_feasible: bool = True,
    adapter: Any | None = None,
) -> AgentSimulationEvaluation:
    """Run a deterministic simulation and produce a bounded evaluation.

    The simulation (S363) runs each step through the governed loop as a
    dry-run; no external side effect occurs. The ``simulation_is_feasible``
    gate represents the governance/simulation feasibility verdict that the
    authorization layer will consult before authorizing the material decision.
    """
    if not isinstance(context_id, str) or not context_id.strip():
        raise SimulationBeforeExecutionError("context_id must be non-empty")

    try:
        simulation = run_governed_simulation(
            steps,
            context_id=context_id,
            actor_id=actor_id,
            authority=authority,
            authorized_at=authorized_at,
            dry_ran_at=dry_ran_at,
            adapter=adapter,
        )
    except GovernedSimulationError as exc:
        raise SimulationBeforeExecutionError(str(exc)) from exc

    command_ids = tuple(
        step.command_id
        for step in simulation.steps
        if getattr(step, "command_id", "")
    )
    rationale = (
        "simulation-feasible: deterministic simulation completed with no "
        "infeasibility; candidate material decision may proceed to authorization"
        if simulation_is_feasible
        else "simulation-infeasible: deterministic simulation indicates the "
        "candidate is not feasible; do not authorize"
    )
    return AgentSimulationEvaluation(
        evaluation_id=_evaluation_id(
            context_id, simulation, simulation_is_feasible, rationale
        ),
        context_id=context_id,
        simulation_result=simulation,
        feasible=simulation_is_feasible,
        rationale=rationale,
        simulated_command_ids=command_ids,
        simulated_at=dry_ran_at,
    )
