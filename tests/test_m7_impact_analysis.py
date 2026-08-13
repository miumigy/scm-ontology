from pathlib import Path

from scm_ontology.graph import load_yaml


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "examples" / "automotive" / "data.yaml"
QUERY = ROOT / "queries" / "impact_analysis.cypher"


def test_impact_analysis_query_exists_and_traverses_causal_chain():
    query = QUERY.read_text(encoding="utf-8")

    assert "CAUSES*0..5" in query
    assert "AFFECTS" in query
    assert "HAS_SUPPLY_GAP" in query
    assert "EXPOSES" in query
    assert "$event_id" in query


def test_automotive_supply_risk_fixture_contains_causal_trigger():
    dataset = load_yaml(DATASET)
    nodes = {node["id"]: node for node in dataset["nodes"]}
    edges = dataset["edges"]

    assert nodes["EVT-001"]["properties"]["eventType"] == "SUPPLIER_DELAY"
    assert nodes["EVT-002"]["properties"]["eventType"] == "MATERIAL_SHORTAGE_RISK"
    assert any(
        edge["type"] == "CAUSES"
        and edge["from"] == "EVT-001"
        and edge["to"] == "EVT-002"
        for edge in edges
    )
