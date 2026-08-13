from pathlib import Path

from scm_ontology.graph import load_yaml, build_statements

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "examples" / "automotive" / "supply_risk.yaml"


def test_supply_risk_dataset_loads_and_builds_causal_graph():
    dataset = load_yaml(DATASET)
    statements = build_statements(dataset)

    assert statements
    assert any("SUPPLIER_DELAY" in statement for statement in statements)
    assert any("MATERIAL_SHORTAGE_RISK" in statement for statement in statements)
    assert any("CAUSES" in statement for statement in statements)


def test_supply_risk_preserves_stable_ids():
    dataset = load_yaml(DATASET)
    statements = build_statements(dataset)

    assert any("{id: $node_id}" in statement for statement in statements)
