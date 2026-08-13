from pathlib import Path

from scm_ontology.graph import load_yaml, build_statements


DATASET = Path("examples/automotive/data.yaml")
QUERY = Path("queries/impact_analysis.cypher")


def test_impact_analysis_query_exists_and_traverses_causal_chain():
    query = QUERY.read_text(encoding="utf-8")

    assert "CAUSES*0..5" in query
    assert "AFFECTS" in query
    assert "HAS_SUPPLY_GAP" in query
    assert "EXPOSES" in query
    assert "$event_id" in query


def test_automotive_supply_risk_fixture_contains_causal_trigger():
    dataset = load_yaml(DATASET)
    statements = build_statements(dataset)

    assert any("EVT-001" in statement and "SUPPLIER_DELAY" in statement for statement in statements)
    assert any("EVT-001" in statement and "EVT-002" in statement and "CAUSES" in statement for statement in statements)
