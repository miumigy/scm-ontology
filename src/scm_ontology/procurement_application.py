"""SCM Procurement Decision Application (Phase R5, S360).

R5 application that resolves a demand/supply shortage into a procurement
decision and, when a purchase is needed, drives it through the governed loop
to an authorized execution command and an S353 dry run.

It reuses the S357/S348 governed loop, the S351 rule-based provider, and the
S353 execution runtime. It introduces no new canonical semantics and performs
no external side effect.
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


class ProcurementApplicationError(ValueError):
    """Raised when a procurement application input or invocation is invalid."""


_QUESTION_ID = "demand-supply-shortage"
_COMMAND_TYPE = "procurement-order"


@dataclass(frozen=True)
class ProcurementObservation:
    """Canonical item shortage and procurement parameters for one item/period."""

    item_id: str
    shortage: float
    unit: str = "unit"
    supplier_id: str = ""
    evidence_ids: tuple[str, ...] = ()
    provenance_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.item_id, str) or not self.item_id.strip():
            raise ProcurementApplicationError("item_id must be non-empty")
        if not isinstance(self.unit, str) or not self.unit.strip():
            raise ProcurementApplicationError("unit must be non-empty")
        if not isinstance(self.shortage, (int, float)) or isinstance(self.shortage, bool):
            raise ProcurementApplicationError("shortage must be numeric")
        if self.shortage < 0:
            raise ProcurementApplicationError("shortage must be non-negative")
        if not isinstance(self.supplier_id, str):
            raise ProcurementApplicationError("supplier_id must be a string")
        object.__setattr__(self, "evidence_ids", tuple(sorted(set(self.evidence_ids))))
        object.__setattr__(self, "provenance_ids", tuple(sorted(set(self.provenance_ids))))

    def to_observation(self, context_id: str) -> GraphReasoningObservation:
        """Project this canonical input into an S339 graph reasoning observation."""
        if not isinstance(context_id, str) or not context_id.strip():
            raise ProcurementApplicationError("context_id must be non-empty")
        return GraphReasoningObservation(
            question_id=_QUESTION_ID,
            value={
                "item_id": self.item_id,
                "shortage": self.shortage,
                "supplier_id": self.supplier_id,
                "unit": self.unit,
            },
            evidence_ids=self.evidence_ids,
            provenance_ids=self.provenance_ids,
        )


def _shortage_is_positive(observations) -> bool:
    """Pure predicate: any demand-supply-shortage observation has a positive shortage."""
    for observation in observations:
        if observation.question_id == _QUESTION_ID and isinstance(observation.value, dict):
            shortage = observation.value.get("shortage")
            if isinstance(shortage, (int, float)) and shortage > 0:
                return True
    return False


def build_procurement_provider(
    observation: ProcurementObservation,
) -> RuleReasoningProvider:
    """Build a deterministic rule provider that issues a purchase for a shortage."""
    if not isinstance(observation, ProcurementObservation):
        raise ProcurementApplicationError("observation must be a ProcurementObservation")
    # A positive shortage triggers a purchase order.
    rule = ReasoningRule(
        rule_id="procure-on-shortage",
        proposal={
            "action": "procure",
            "item_id": observation.item_id,
            "quantity": observation.shortage,
            "unit": observation.unit,
            "supplier_id": observation.supplier_id,
        },
        rationale=f"demand exceeds supply by {observation.shortage} {observation.unit}",
        matches=_shortage_is_positive,
        condition_description="demand-supply-shortage.shortage > 0",
    )
    return RuleReasoningProvider(provider_id="procurement-rule", rules=(rule,))


@dataclass(frozen=True)
class ProcurementDecision:
    """Immutable result of running the governed procurement application."""

    item_id: str
    action: str
    quantity: float
    unit: str
    rationale: str
    governed: GovernedExecutionResult | None = None

    @property
    def is_procure(self) -> bool:
        return self.action == "procure"

    def to_mapping(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "contract_version": "S360.1",
            "item_id": self.item_id,
            "action": self.action,
            "quantity": self.quantity,
            "unit": self.unit,
            "rationale": self.rationale,
        }
        if self.governed is not None:
            value["governed"] = self.governed.to_mapping()
        return value


def run_procurement_application(
    observation: ProcurementObservation,
    *,
    context_id: str,
    actor_id: str,
    authority: str,
    authorized_at: str,
    command_id: str,
    dry_ran_at: str,
    adapter: ExecutionAdapter | None = None,
) -> ProcurementDecision:
    """Run the governed procurement loop for one item/period.

    When there is no positive shortage, the application returns a
    ``no_procurement`` decision without creating a command or dry run. When a
    shortage exists, it drives the full governed loop (rule provider ->
    validation -> authorization -> command -> dry run).
    """
    if not isinstance(observation, ProcurementObservation):
        raise ProcurementApplicationError("observation must be a ProcurementObservation")
    if not isinstance(context_id, str) or not context_id.strip():
        raise ProcurementApplicationError("context_id must be non-empty")

    if observation.shortage <= 0.0:
        return ProcurementDecision(
            item_id=observation.item_id,
            action="no_procurement",
            quantity=0.0,
            unit=observation.unit,
            rationale=f"no shortage for item {observation.item_id}",
        )

    provider = build_procurement_provider(observation)
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
    return ProcurementDecision(
        item_id=observation.item_id,
        action="procure",
        quantity=observation.shortage,
        unit=observation.unit,
        rationale="demand exceeds supply; issuing a purchase order",
        governed=governed,
    )
