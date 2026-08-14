import pytest

from scm_ontology.s132_what_if import (
    Intervention,
    ScenarioEpistemicStatus,
    WhatIfScenario,
    build_what_if_result,
)


def scenario():
    return WhatIfScenario(
        ref="whatif:1",
        baseline_ref="state:actual",
        intervention_ref="intervention:1",
        scenario_ref="scenario:counterfactual-1",
    )


def test_intervention_is_not_execution() -> None:
    intervention = Intervention(
        ref="intervention:1",
        kind="alternative_decision",
        description="Increase production capacity",
        alternative_decision_ref="decision:alternative-1",
    )
    assert intervention.kind == "alternative_decision"
    assert intervention.alternative_decision_ref != "action:executed"


def test_scenario_cannot_replace_baseline() -> None:
    with pytest.raises(ValueError):
        WhatIfScenario(
            ref="whatif:bad",
            baseline_ref="same",
            intervention_ref="intervention:1",
            scenario_ref="same",
        )


def test_result_remains_hypothetical() -> None:
    result = build_what_if_result(
        scenario(),
        outcome_ref="outcome:hypothetical",
        epistemic_status=ScenarioEpistemicStatus.SIMULATED,
        constraint_evaluation_refs=("evaluation:c1",),
        causal_assessment_refs=("assessment:c1",),
        provenance_refs=("provenance:p1",),
    )
    assert result.epistemic_status is ScenarioEpistemicStatus.SIMULATED
    assert result.is_actual_outcome is False
    assert result.is_executed_action is False


def test_unknown_remains_unknown() -> None:
    result = build_what_if_result(
        scenario(),
        outcome_ref="outcome:unknown",
        epistemic_status=ScenarioEpistemicStatus.UNKNOWN,
    )
    assert result.epistemic_status is ScenarioEpistemicStatus.UNKNOWN
