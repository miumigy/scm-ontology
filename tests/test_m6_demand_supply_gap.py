from pathlib import Path

from scm_ontology.graph import load_yaml

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "examples" / "automotive" / "data.yaml"
QUERY = ROOT / "queries" / "demand_supply_gap.cypher"


def test_automotive_fixture_supports_expected_demand_supply_gap():
    dataset = load_yaml(DATASET)
    nodes = {node["id"]: node for node in dataset["nodes"]}

    demand = nodes["DEM-001"]["properties"]["quantity"]
    available = nodes["INV-VEHICLE-PLANT"]["properties"]["available"]
    inbound = nodes["INV-VEHICLE-PLANT"]["properties"]["inTransit"]

    assert demand == 100
    assert available == 60
    assert inbound == 20
    assert demand - available - inbound == 20


def test_demand_supply_gap_query_exposes_canonical_supply_gap_fields():
    query = QUERY.read_text(encoding="utf-8")

    for field in (
        "demandQuantity",
        "availableQuantity",
        "inboundQuantity",
        "relevantSupplyQuantity",
        "gapQuantity",
    ):
        assert field in query

    assert "demand - relevantSupply" in query
    assert "ORDER BY gapQuantity DESC" in query
