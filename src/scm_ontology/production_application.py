"""SCM Production Decision Application (Phase R5, S361).

R5 application that resolves a production requirement against resource capacity
into a scheduling decision and, when production is feasible, drives it through
the governed loop to an authorized execution command and an S353 dry run.

It reuses the S348 governed loop, the S351 rule-based provider, and the S353
execution runtime. It introduces no new canonical semantics and performs no
external side effect.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .execution_runtime import (
    ExecutionAdapter,
    GovernedExecutionResult,
    run_governed_loop_and_dry_run,
)
from .graph_reasoning_projection import GraphReasoningObservation
from .rule_reasoning_provider import ReasoningRule, RuleReasoningProvider


class ProductionApplicationError(ValueError):
    """Raised when a production application input or invocation is invalid."""


_QUESTION_ID = "capacity-requirement"
_COMMAND_TYPE = "production-order"


def _requirement_is_feasible(observations) -> bool:
    """Pure predicate: required quantity does not exceed available capacity."""
    for observation in observations:
        if observation.question_id != _QUESTION_ID or not isinstance(observation.value, dict):
            continue
        required = observation.value.get("required")
        capacity = observation.value.get("capacity")
        if isinstance(required, (int, float)) and isinstance(capacity, (int, float)):
            return required <= capacity
    return False


@dataclass(frozen=True)
class ProductionObservation:
    """Canonical production requirement and available capacity for one resource."""

    resource_id: str
    required: float
    capacity: float
    unit: str = "unit"
    evidence_ids: tuple[str, ...] = ()
    provenance_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.resource_id, str) or not self.resource_id.strip():
            raise ProductionApplicationError("resource_id must be non-empty")
        if not isinstance(self.unit, str) or not self.unit.strip():
            raise ProductionApplicationError("unit must be non-empty")
        for name in ("required", "capacity"):
            value = getattr(self, name)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
                raise ProductionApplicationError(f"{name} must be a non-negative number")
        object.__setattr__(self, "evidence_ids", tuple(sorted(set(self.evidence_ids))))
        object.__setattr__(self, "provenance_ids", tuple(sorted(set(self.provenance_ids))))

    @property
    def headroom(self) -> float:
        return self.capacity - self.required

    def to_observation(self, context_id: str) -> GraphReasoningObservation:
        """Project this canonical input into an S339 graph reasoning observation."""
        if not isinstance(context_id, str) or not context_id.strip():
            raise ProductionApplicationError("context_id must be non-empty")
        return GraphReasoningObservation(
            question_id=_QUESTION_ID,
            value={
                "resource_id": self.resource_id,
                "required": self.required,
                "capacity": self.capacity,
                "unit": self.unit,
            },
            evidence_ids=self.evidence_ids,
            provenance_ids=self.provenance_ids,
        )


def build_production_provider(
    observation: ProductionObservation,
) -> RuleReasoningProvider:
    """Build a deterministic rule provider that schedules feasible production."""
    if not isinstance(observation, ProductionObservation):
        raise ProductionApplicationError("observation must be a ProductionObservation")
    rule = ReasoningRule(
        rule_id="schedule-feasible-production",
        proposal={
            "action": "schedule",
            "resource_id": observation.resource_id,
            "quantity": observation.required,
            "unit": observation.unit,
        },
        rationale=(
            f"production requirement {observation.required} {observation.unit} "
            f"is within capacity {observation.capacity} {observation.unit}"
        ),
        matches=_requirement_is_feasible,
        condition_description="capacity-observation.required <= capacity",
    )
    return RuleReasoningProvider(provider_id="production-rule", rules=(rule,))


@dataclass(frozen=True)
class ProductionDecision:
    """Immutable result of running the governed production application."""

    resource_id: str
    action: str
    quantity: float
    unit: str
    rationale: str
    governed: GovernedExecutionResult | None = None

    @property
    def is_schedule(self) -> bool:
        return self.action == "schedule"

    def to_mapping(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "contract_version": "S361.1",
            "resource_id": self.resource_id,
            "action": self.action,
            "quantity": self.quantity,
            "unit": self.unit,
            "rationale": self.rationale,
        }
        if self.governed is not None:
            value["governed"] = self.governed.to_mapping()
        return value


def run_production_application(
    observation: ProductionObservation,
    *,
    context_id: str,
    actor_id: str,
    authority: str,
    authorized_at: str,
    command_id: str,
    dry_ran_at: str,
    adapter: ExecutionAdapter | None = None,
) -> ProductionDecision:
    """Run the governed production loop for one resource.

    When the requirement exceeds capacity (infeasible), the application returns
    an ``escalate`` decision without creating a command. When feasible, it
    schedules production through the full governed loop (rule provider ->
    validation -> authorization -> command -> dry run).
    """
    if not isinstance(observation, ProductionObservation):
        raise ProductionApplicationError("observation must be a ProductionObservation")
    if not isinstance(context_id, str) or not context_id.strip():
        raise ProductionApplicationError("context_id must be non-empty")

    if observation.required > observation.capacity:
        return ProductionDecision(
            resource_id=observation.resource_id,
            action="escalate",
            quantity=0.0,
            unit=observation.unit,
            rationale=(
                f"requirement {observation.required} exceeds capacity "
                f"{observation.capacity}; escalate for planning"
            ),
        )

    provider = build_production_provider(observation)
    governed = run_governed_loop_and_dry_run(
        context_id=context_id,
        observations=(observation.to_observation(context_id),),
        provider=provider,
        actor_id=actor_id,
        authority=authority,
        authorized_at=authorized_at,
        command_type=_COMMAND_TYPE,
        command_id=command_id,
        dry_ran_at=dry_ran_at,
        adapter=adapter,
    )
    return ProductionDecision(
        resource_id=observation.resource_id,
        action="schedule",
        quantity=observation.required,
        unit=observation.unit,
        rationale="production requirement is within capacity; scheduling",
        governed=governed,
    )
