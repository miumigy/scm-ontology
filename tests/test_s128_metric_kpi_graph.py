from pathlib import Path

import yaml


FIXTURE = Path(__file__).parents[1] / "examples" / "s128" / "metric-kpi-graph.yaml"


def test_metric_kpi_graph_preserves_semantic_chain() -> None:
    data = yaml.safe_load(FIXTURE.read_text())
    nodes = {node["id"]: node for node in data["nodes"]}
    edges = {(edge["from"], edge["predicate"], edge["to"]) for edge in data["edges"]}

    assert nodes["metric_value_001"]["actual"] is True
    assert nodes["target_otd"]["type"] == "Target"
    assert nodes["assessment_001"]["type"] == "PerformanceAssessment"
    assert ("assessment_001", "informs", "recommendation_001") in edges
    assert ("recommendation_001", "considered_by", "decision_001") in edges


def test_kpi_does_not_collapse_into_target_or_actual() -> None:
    data = yaml.safe_load(FIXTURE.read_text())
    nodes = {node["id"]: node for node in data["nodes"]}

    assert nodes["kpi_otd"]["type"] == "KPI"
    assert nodes["target_otd"]["type"] == "Target"
    assert nodes["metric_value_001"]["type"] == "MetricValue"
    assert nodes["metric_value_001"]["actual"] is True
    assert nodes["target_otd"]["value"] != nodes["metric_value_001"]["value"]
