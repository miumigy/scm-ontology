from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ScenarioEpistemicStatus(str, Enum):
    SIMULATED = "simulated"
    ESTIMATED = "estimated"
    INFERRED = "inferred"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Intervention:
    ref: str
    kind: str
    description: str
    alternative_decision_ref: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.ref or not self.description:
            raise ValueError("ref and description are required")


@dataclass(frozen=True)
class WhatIfScenario:
    ref: str
    baseline_ref: str
    intervention_ref: str
    scenario_ref: str
    temporal_context: Optional[str] = None

    def __post_init__(self) -> None:
        refs = (self.ref, self.baseline_ref, self.intervention_ref, self.scenario_ref)
        if any(not ref for ref in refs):
            raise ValueError("scenario references are required")
        if self.baseline_ref == self.scenario_ref:
            raise ValueError("scenario must not replace the baseline world")


@dataclass(frozen=True)
class WhatIfResult:
    scenario_ref: str
    outcome_ref: str
    epistemic_status: ScenarioEpistemicStatus
    constraint_evaluation_refs: tuple[str, ...] = ()
    causal_assessment_refs: tuple[str, ...] = ()
    provenance_refs: tuple[str, ...] = ()
    explanation: Optional[str] = None

    @property
    def is_actual_outcome(self) -> bool:
        return False

    @property
    def is_executed_action(self) -> bool:
        return False


def build_what_if_result(
    scenario: WhatIfScenario,
    *,
    outcome_ref: str,
    epistemic_status: ScenarioEpistemicStatus,
    constraint_evaluation_refs: tuple[str, ...] = (),
    causal_assessment_refs: tuple[str, ...] = (),
    provenance_refs: tuple[str, ...] = (),
) -> WhatIfResult:
    if not outcome_ref:
        raise ValueError("outcome_ref is required")
    return WhatIfResult(
        scenario_ref=scenario.scenario_ref,
        outcome_ref=outcome_ref,
        epistemic_status=epistemic_status,
        constraint_evaluation_refs=constraint_evaluation_refs,
        causal_assessment_refs=causal_assessment_refs,
        provenance_refs=provenance_refs,
    )
