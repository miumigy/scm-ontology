from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Optional


class CausalRelationKind(StrEnum):
    CAUSES = "causes"
    CONTRIBUTES_TO = "contributes_to"
    PREVENTS = "prevents"
    MODIFIES = "modifies"


class ScenarioKind(StrEnum):
    ACTUAL = "actual"
    ALTERNATIVE = "alternative"
    HYPOTHETICAL = "hypothetical"
    COUNTERFACTUAL = "counterfactual"


@dataclass(frozen=True)
class CausalRelationship:
    ref: str
    cause_ref: str
    effect_ref: str
    kind: CausalRelationKind
    evidence_refs: tuple[str, ...] = ()
    uncertainty_ref: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.ref or not self.cause_ref or not self.effect_ref:
            raise ValueError("ref, cause_ref, and effect_ref are required")
        if self.cause_ref == self.effect_ref:
            raise ValueError("cause and effect must be distinct")


@dataclass(frozen=True)
class Scenario:
    ref: str
    kind: ScenarioKind
    parent_world_ref: str
    description: str
    assumptions_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.ref or not self.parent_world_ref or not self.description:
            raise ValueError("ref, parent_world_ref, and description are required")
        if self.kind is ScenarioKind.ACTUAL:
            raise ValueError("actual world is not represented as a scenario")


@dataclass(frozen=True)
class ScenarioChange:
    ref: str
    scenario_ref: str
    subject_ref: str
    attribute_ref: str
    baseline_value_ref: str
    alternative_value_ref: str

    def __post_init__(self) -> None:
        if not all((self.ref, self.scenario_ref, self.subject_ref, self.attribute_ref,
                    self.baseline_value_ref, self.alternative_value_ref)):
            raise ValueError("all scenario change references are required")
        if self.baseline_value_ref == self.alternative_value_ref:
            raise ValueError("scenario change requires a different alternative value")


@dataclass(frozen=True)
class Counterfactual:
    ref: str
    scenario_ref: str
    intervention_ref: str
    observed_outcome_ref: str
    counterfactual_outcome_ref: str
    causal_basis_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not all((self.ref, self.scenario_ref, self.intervention_ref,
                    self.observed_outcome_ref, self.counterfactual_outcome_ref)):
            raise ValueError("counterfactual references are required")
        if self.observed_outcome_ref == self.counterfactual_outcome_ref:
            raise ValueError("observed and counterfactual outcomes must be distinct")
