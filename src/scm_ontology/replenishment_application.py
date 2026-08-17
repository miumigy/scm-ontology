"""SCM Replenishment Decision Application (Phase R5, S358).

R5 puts the governed decision loop to work for a concrete SCM business
application. This application resolves on-hand inventory to a replenishment
decision and, when a reorder is needed, drives it through the S348 governed
loop to an authorized execution command and an S353 dry run.

It reuses: S326 inventory observation semantics, the S351 rule-based provider,
the S348 decision runtime, and the S353 execution runtime. It introduces no new
canonical semantics and performs no external side effect.
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
from .rule_reasoning_provider import (
    ReasoningRule,
    RuleReasoningProvider,
    when_measurement_below,
)


class ReplenishmentApplicationError(ValueError):
    """Raised when a replenishment application input or invocation is invalid."""


_QUESTION_ID = "inventory-position"
_COMMAND_TYPE = "replenishment"


@dataclass(frozen=True)
class ReplenishmentObservation:
    """Canonical on-hand inventory and reorder parameters for one product/location."""

    product_id: str
    location_id: str
    on_hand: float
    reorder_point: float
    reorder_quantity: float
    unit: str = "unit"
    evidence_ids: tuple[str, ...] = ()
    provenance_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.product_id, str) or not self.product_id.strip():
            raise ReplenishmentApplicationError("product_id must be non-empty")
        if not isinstance(self.location_id, str) or not self.location_id.strip():
            raise ReplenishmentApplicationError("location_id must be non-empty")
        if not isinstance(self.unit, str) or not self.unit.strip():
            raise ReplenishmentApplicationError("unit must be non-empty")
        for name in ("on_hand", "reorder_point", "reorder_quantity"):
            value = getattr(self, name)
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise ReplenishmentApplicationError(f"{name} must be numeric")
        object.__setattr__(self, "evidence_ids", tuple(sorted(set(self.evidence_ids))))
        object.__setattr__(self, "provenance_ids", tuple(sorted(set(self.provenance_ids))))

    def to_observation(self, context_id: str) -> GraphReasoningObservation:
        """Project this canonical input into an S339 graph reasoning observation."""
        if not isinstance(context_id, str) or not context_id.strip():
            raise ReplenishmentApplicationError("context_id must be non-empty")
        return GraphReasoningObservation(
            question_id=_QUESTION_ID,
            value={
                "product_id": self.product_id,
                "location_id": self.location_id,
                "on_hand": self.on_hand,
                "reorder_point": self.reorder_point,
                "reorder_quantity": self.reorder_quantity,
                "unit": self.unit,
            },
            evidence_ids=self.evidence_ids,
            provenance_ids=self.provenance_ids,
        )


def build_replenishment_provider(
    observation: ReplenishmentObservation,
) -> RuleReasoningProvider:
    """Build a deterministic rule provider that replenishes below reorder point."""
    if not isinstance(observation, ReplenishmentObservation):
        raise ReplenishmentApplicationError("observation must be a ReplenishmentObservation")
    desc, matches = when_measurement_below(_QUESTION_ID, "on_hand", observation.reorder_point)
    rule = ReasoningRule(
        rule_id="replenish-below-reorder-point",
        proposal={
            "action": "replenish",
            "quantity": observation.reorder_quantity,
            "unit": observation.unit,
        },
        rationale=f"on-hand inventory below reorder point {observation.reorder_point}",
        matches=matches,
        condition_description=desc,
    )
    return RuleReasoningProvider(provider_id="replenishment-rule", rules=(rule,))


@dataclass(frozen=True)
class ReplenishmentDecision:
    """Immutable result of running the governed replenishment application."""

    product_id: str
    location_id: str
    action: str
    quantity: float
    unit: str
    rationale: str
    governed: GovernedExecutionResult | None = None

    @property
    def is_replenish(self) -> bool:
        return self.action == "replenish"

    def to_mapping(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "contract_version": "S358.1",
            "product_id": self.product_id,
            "location_id": self.location_id,
            "action": self.action,
            "quantity": self.quantity,
            "unit": self.unit,
            "rationale": self.rationale,
        }
        if self.governed is not None:
            value["governed"] = self.governed.to_mapping()
        return value


def run_replenishment_application(
    observation: ReplenishmentObservation,
    *,
    context_id: str,
    actor_id: str,
    authority: str,
    authorized_at: str,
    command_id: str,
    dry_ran_at: str,
    adapter: ExecutionAdapter | None = None,
) -> ReplenishmentDecision:
    """Run the governed replenishment loop for one product/location.

    When on-hand is at or above the reorder point, no rule fires and the
    application returns a ``no_replenishment`` decision without creating a
    command or dry run. When a reorder is needed, the application drives the
    full governed loop (rule provider -> validation -> authorization -> command
    -> dry run) and returns the result.
    """
    if not isinstance(observation, ReplenishmentObservation):
        raise ReplenishmentApplicationError("observation must be a ReplenishmentObservation")
    if not isinstance(context_id, str) or not context_id.strip():
        raise ReplenishmentApplicationError("context_id must be non-empty")

    reason = f"on-hand {observation.on_hand} >= reorder point {observation.reorder_point}"
    if observation.on_hand >= observation.reorder_point:
        return ReplenishmentDecision(
            product_id=observation.product_id,
            location_id=observation.location_id,
            action="no_replenishment",
            quantity=0.0,
            unit=observation.unit,
            rationale=reason,
        )

    provider = build_replenishment_provider(observation)
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
    return ReplenishmentDecision(
        product_id=observation.product_id,
        location_id=observation.location_id,
        action="replenish",
        quantity=observation.reorder_quantity,
        unit=observation.unit,
        rationale="on-hand inventory below reorder point",
        governed=governed,
    )
