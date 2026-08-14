from pathlib import Path

import yaml


FIXTURE = Path(__file__).parents[1] / "examples" / "s121" / "planning-sop-psi-mapping.yaml"


def test_planning_fixture_is_readable() -> None:
    data = yaml.safe_load(FIXTURE.read_text())
    assert data["scenario"] == "baseline"
    assert len(data["mappings"]) == 5


def test_forecast_keeps_prediction_semantics() -> None:
    data = yaml.safe_load(FIXTURE.read_text())
    forecast = data["mappings"][0]
    assert forecast["source"]["concept"] == "Forecast"
    assert forecast["target"]["concept"] == "Demand"
    assert forecast["epistemic"]["status"] == "prediction"


def test_sop_decision_maps_to_plan_not_recommendation() -> None:
    data = yaml.safe_load(FIXTURE.read_text())
    decision = data["mappings"][2]
    assert decision["source"]["concept"] == "Decision"
    assert decision["target"]["concept"] == "Plan"
    assert decision["status"] == "approved"


def test_actual_production_is_observation() -> None:
    data = yaml.safe_load(FIXTURE.read_text())
    actual = data["mappings"][3]
    assert actual["source"]["concept"] == "ActualProduction"
    assert actual["epistemic"]["status"] == "observation"


def test_kpi_remains_metric_layer() -> None:
    data = yaml.safe_load(FIXTURE.read_text())
    metric = data["mappings"][4]
    assert metric["target"]["concept"] == "Metric"
