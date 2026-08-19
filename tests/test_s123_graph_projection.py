from pathlib import Path

import yaml


FIXTURE = Path(__file__).parents[1] / "examples" / "canonical-graph" / "canonical-scm-graph.yaml"


def test_graph_fixture_preserves_semantic_predicates() -> None:
    data = yaml.safe_load(FIXTURE.read_text())
    predicates = {edge["predicate"] for edge in data["graph"]["edges"]}
    assert "contains" in predicates
    assert "measured_by" in predicates
    assert "planned_for" in predicates


def test_scenario_is_distinct_from_actual_entities() -> None:
    data = yaml.safe_load(FIXTURE.read_text())
    nodes = data["graph"]["nodes"]
    scenario = next(node for node in nodes if node["kind"] == "scenario")
    assert scenario["scenario_type"] == "counterfactual"


def test_temporal_and_observation_metadata_are_preserved() -> None:
    data = yaml.safe_load(FIXTURE.read_text())
    inventory = next(node for node in data["graph"]["nodes"] if node["concept"] == "Inventory")
    assert "valid_from" in inventory
    assert "observed_at" in inventory
