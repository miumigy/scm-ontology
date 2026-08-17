"""SCM Distribution Decision Application (Phase R5, S362).

R5 application that resolves a shipment requirement against available
transportation capacity into a distribution decision and, when shipment is
feasible, drives it through the governed loop to an authorized execution
command and an S353 dry run.

It reuses the S348 governed loop, the S351 rule-based provider, and the S353
execution runtime. It introduces no new canonical semantics and performs no
external side effect. Distribution routes physical movement of items via
origin/destination locations, reusing the canonical shipment concept.
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


class DistributionApplicationError(ValueError):
    """Raised when a distribution application input or invocation is invalid."""


_QUESTION_ID = "distribution-capacity"
_COMMAND_TYPE = "shipment"


def _shipment_is_feasible(observations) -> bool:
    """Pure predicate: required quantity does not exceed transportation capacity."""
    for observation in observations:
        if observation.question_id != _QUESTION_ID or not isinstance(observation.value, dict):
            continue
        required = observation.value.get("required_quantity")
        capacity = observation.value.get("capacity")
        if isinstance(required, (int, float)) and isinstance(capacity, (int, float)):
            return required <= capacity
    return False


@dataclass(frozen=True)
class DistributionObservation:
    """Canonical shipment requirement and available capacity for one route."""

    shipment_id: str
    item_id: str
    required_quantity: float
    capacity: float
    origin_location_id: str
    destination_location_id: str
    unit: str = "unit"
    evidence_ids: tuple[str, ...] = ()
    provenance_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.shipment_id, str) or not self.shipment_id.strip():
            raise DistributionApplicationError("shipment_id must be non-empty")
        if not isinstance(self.item_id, str) or not self.item_id.strip():
            raise DistributionApplicationError("item_id must be non-empty")
        if not isinstance(self.origin_location_id, str) or not self.origin_location_id.strip():
            raise DistributionApplicationError("origin_location_id must be non-empty")
        if not isinstance(self.destination_location_id, str) or not self.destination_location_id.strip():
            raise DistributionApplicationError("destination_location_id must be non-empty")
        if self.origin_location_id == self.destination_location_id:
            raise DistributionApplicationError("origin and destination must differ")
        if not isinstance(self.unit, str) or not self.unit.strip():
            raise DistributionApplicationError("unit must be non-empty")
        for name in ("required_quantity", "capacity"):
            value = getattr(self, name)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
                raise DistributionApplicationError(f"{name} must be a non-negative number")
        object.__setattr__(self, "evidence_ids", tuple(sorted(set(self.evidence_ids))))
        object.__setattr__(self, "provenance_ids", tuple(sorted(set(self.provenance_ids))))

    @property
    def headroom(self) -> float:
        return self.capacity - self.required_quantity

    def to_observation(self, context_id: str) -> GraphReasoningObservation:
        """Project this canonical input into an S339 graph reasoning observation."""
        if not isinstance(context_id, str) or not context_id.strip():
            raise DistributionApplicationError("context_id must be non-empty")
        return GraphReasoningObservation(
            question_id=_QUESTION_ID,
            value={
                "shipment_id": self.shipment_id,
                "item_id": self.item_id,
                "required_quantity": self.required_quantity,
                "capacity": self.capacity,
                "origin_location_id": self.origin_location_id,
                "destination_location_id": self.destination_location_id,
                "unit": self.unit,
            },
            evidence_ids=self.evidence_ids,
            provenance_ids=self.provenance_ids,
        )


def build_distribution_provider(
    observation: DistributionObservation,
) -> RuleReasoningProvider:
    """Build a deterministic rule provider that ships a feasible requirement."""
    if not isinstance(observation, DistributionObservation):
        raise DistributionApplicationError("observation must be a DistributionObservation")
    rule = ReasoningRule(
        rule_id="ship-within-capacity",
        proposal={
            "action": "ship",
            "shipment_id": observation.shipment_id,
            "item_id": observation.item_id,
            "quantity": observation.required_quantity,
            "origin_location_id": observation.origin_location_id,
            "destination_location_id": observation.destination_location_id,
            "unit": observation.unit,
        },
        rationale=(
            f"shipment {observation.shipment_id} of {observation.required_quantity} {observation.unit} "
            f"fits within capacity {observation.capacity} {observation.unit}"
        ),
        matches=_shipment_is_feasible,
        condition_description="distribution-observation.required_quantity <= capacity",
    )
    return RuleReasoningProvider(provider_id="distribution-rule", rules=(rule,))


@dataclass(frozen=True)
class DistributionDecision:
    """Immutable result of running the governed distribution application."""

    shipment_id: str
    action: str
    quantity: float
    unit: str
    rationale: str
    governed: GovernedExecutionResult | None = None

    @property
    def is_ship(self) -> bool:
        return self.action == "ship"

    def to_mapping(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "contract_version": "S362.1",
            "shipment_id": self.shipment_id,
            "action": self.action,
            "quantity": self.quantity,
            "unit": self.unit,
            "rationale": self.rationale,
        }
        if self.governed is not None:
            value["governed"] = self.governed.to_mapping()
        return value


def run_distribution_application(
    observation: DistributionObservation,
    *,
    context_id: str,
    actor_id: str,
    authority: str,
    authorized_at: str,
    command_id: str,
    dry_ran_at: str,
    adapter: ExecutionAdapter | None = None,
) -> DistributionDecision:
    """Run the governed distribution loop for one shipment route.

    When the shipment requirement exceeds transportation capacity (infeasible),
    the application returns an ``escalate`` decision without creating a
    command. When feasible (including exact fit), it drives the full governed
    loop (rule provider -> validation -> authorization -> command -> dry run).
    """
    if not isinstance(observation, DistributionObservation):
        raise DistributionApplicationError("observation must be a DistributionObservation")
    if not isinstance(context_id, str) or not context_id.strip():
        raise DistributionApplicationError("context_id must be non-empty")

    if observation.required_quantity > observation.capacity:
        return DistributionDecision(
            shipment_id=observation.shipment_id,
            action="escalate",
            quantity=0.0,
            unit=observation.unit,
            rationale=(
                f"shipment requirement {observation.required_quantity} exceeds capacity "
                f"{observation.capacity}; escalate for planning"
            ),
        )

    provider = build_distribution_provider(observation)
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
    return DistributionDecision(
        shipment_id=observation.shipment_id,
        action="ship",
        quantity=observation.required_quantity,
        unit=observation.unit,
        rationale="shipment requirement fits within capacity; shipping",
        governed=governed,
    )
