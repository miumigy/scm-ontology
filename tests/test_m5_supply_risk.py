from pathlib import Path

from scm_ontology.graph import load_yaml
from scm_ontology.neo4j_loader import build_statements

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "examples" / "automotive" / "supply_risk.yaml"


def test_supply_risk_dataset_loads_and_builds_causal_graph():
    dataset = load_yaml(DATASET)
    statements = build_statements(dataset)

    assert statements
    assert {node["id"] for node in dataset["nodes"]} >= {
        "EVT-001",
        "EVT-002",
        "RISK-001",
    }
    assert next(
        node["properties"]["eventType"]
        for node in dataset["nodes"]
        if node["id"] == "EVT-001"
    ) == "SUPPLIER_DELAY"
    assert next(
        node["properties"]["eventType"]
        for node in dataset["nodes"]
        if node["id"] == "EVT-002"
    ) == "MATERIAL_SHORTAGE_RISK"
    assert any("MERGE (a)-[r:CAUSES]->(b)" in statement for statement in statements)


def test_supply_risk_preserves_stable_ids():
    dataset = load_yaml(DATASET)
    statements = build_statements(dataset)

    assert any("{id: $node_id}" in statement for statement in statements)
