from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "examples" / "automotive" / "data.yaml"


def test_automotive_demand_supply_gap():
    data = yaml.safe_load(DATASET.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in data["nodes"]}
    edges = data["edges"]

    demand_by_location = {}
    inventory_by_location = {}

    for edge in edges:
        if edge["type"] == "DEMANDS":
            demand_by_location.setdefault(edge["from"], []).append(nodes[edge["to"]])
        elif edge["type"] == "HAS_INVENTORY_POSITION":
            inventory_by_location[edge["from"]] = nodes[edge["to"]]

    location = "PL-VEHICLE-PLANT"
    demand = sum(d["properties"]["quantity"] for d in demand_by_location[location])
    inventory = inventory_by_location[location]["properties"]
    available = inventory["available"]
    inbound = inventory["inTransit"]

    gap = max(demand - available - inbound, 0)

    assert demand == 100
    assert available == 60
    assert inbound == 20
    assert gap == 20
