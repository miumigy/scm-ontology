from pathlib import Path

import yaml


FIXTURE = Path(__file__).parents[1] / "examples" / "scenario-counterfactual" / "scenario-counterfactual.yaml"


def test_scenario_has_explicit_reference_world() -> None:
    data = yaml.safe_load(FIXTURE.read_text())
    scenario = data["scenario"]
    assert scenario["type"] == "scenario"
    assert scenario["reference_world"] == "actual-world"


def test_counterfactual_does_not_overwrite_actual() -> None:
    data = yaml.safe_load(FIXTURE.read_text())
    actual = data["actual"]["service_level"]["value"]
    hypothetical = data["counterfactual"]["outcome"]["value"]
    assert actual != hypothetical


def test_counterfactual_keeps_reference_world() -> None:
    data = yaml.safe_load(FIXTURE.read_text())
    cf = data["counterfactual"]
    assert cf["reference_world"] == "actual-world"
    assert cf["outcome"]["epistemic_status"] == "counterfactual"
