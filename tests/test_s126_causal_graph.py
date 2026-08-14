from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_counterfactual_is_separate_from_actual_world():
    data = yaml.safe_load((ROOT / "examples/s126/causal-graph.yaml").read_text())
    worlds = {w["id"]: w for w in data["worlds"]}
    assert worlds["actual-world"]["type"] == "actual"
    assert worlds["scenario-delay"]["type"] == "counterfactual"
    assert worlds["scenario-delay"]["parent"] == "actual-world"


def test_causal_claim_retains_uncertainty_and_provenance():
    data = yaml.safe_load((ROOT / "examples/s126/causal-graph.yaml").read_text())
    causal = next(e for e in data["edges"] if e["type"] == "causes")
    assert causal["properties"]["causal_status"] == "asserted"
    assert causal["properties"]["uncertainty"] == "medium"
    assert causal["properties"]["provenance_ref"] == "evidence-port-001"


def test_counterfactual_result_does_not_become_actual_history():
    data = yaml.safe_load((ROOT / "examples/s126/causal-graph.yaml").read_text())
    hypothetical = next(e for e in data["edges"] if e["type"] == "results_in")
    assert hypothetical["properties"]["causal_status"] == "hypothetical"
    assert hypothetical["properties"]["scenario_ref"] == "scenario-delay"
