from pathlib import Path

import yaml

from scm_ontology.simulation import Event, Scenario, SimulationKernel, State

FIXTURE = Path(__file__).parents[1] / "examples" / "automotive" / "data.yaml"


def load_automotive_fixture():
    return yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))


def test_automotive_fixture_projects_into_simulation_state():
    data = load_automotive_fixture()
    nodes = {node["id"]: node for node in data["nodes"]}
    supplies = next(edge for edge in data["edges"] if edge["type"] == "SUPPLIES" and edge["from"] == "SUP-001")
    supplier = dict(nodes["SUP-001"]["properties"])
    supplier["leadTimeDays"] = supplies["properties"]["leadTimeDays"]
    state = State(
        state_id="AUTO-DEMO-001:t0", effective_at=0,
        entities={
            "SUP-001": {"entityType": "Party", **supplier},
            "PL-VEHICLE-PLANT": {"entityType": "ProductLocation", **nodes["PL-VEHICLE-PLANT"]["properties"]},
            "INV-VEHICLE-PLANT": {"entityType": "InventoryPosition", **nodes["INV-VEHICLE-PLANT"]["properties"]},
            "DEM-001": {"entityType": "Demand", **nodes["DEM-001"]["properties"]},
        },
    )
    assert state.entities["SUP-001"]["leadTimeDays"] == 7
    assert state.entities["PL-VEHICLE-PLANT"]["available"] == 60
    assert state.entities["INV-VEHICLE-PLANT"]["inTransit"] == 20
    assert state.entities["DEM-001"]["quantity"] == 100


def test_automotive_supplier_delay_is_deterministic_and_preserves_gap_semantics():
    data = load_automotive_fixture()
    nodes = {node["id"]: node for node in data["nodes"]}
    supplies = next(edge for edge in data["edges"] if edge["type"] == "SUPPLIES" and edge["from"] == "SUP-001")
    supplier = dict(nodes["SUP-001"]["properties"])
    supplier["leadTimeDays"] = supplies["properties"]["leadTimeDays"]
    state = State(
        state_id="AUTO-DEMO-001:t0", effective_at=0,
        entities={
            "SUP-001": {"entityType": "Party", **supplier},
            "PL-VEHICLE-PLANT": {"entityType": "ProductLocation", **nodes["PL-VEHICLE-PLANT"]["properties"]},
            "INV-VEHICLE-PLANT": {"entityType": "InventoryPosition", **nodes["INV-VEHICLE-PLANT"]["properties"]},
            "DEM-001": {"entityType": "Demand", **nodes["DEM-001"]["properties"]},
        },
    )
    event = Event("AUTO-EVT-SUPPLIER-DELAY", "SUPPLIER_DELAY", 7, "SUP-001", {"magnitudeDays": 7})
    scenario = Scenario("AUTO-S2-SUPPLIER-DELAY", state, (event,), seed=42)
    kernel = SimulationKernel()
    run_a = kernel.run(scenario)
    run_b = kernel.run(scenario)
    assert run_a.to_dict() == run_b.to_dict()
    assert run_a.final_state.entities["SUP-001"]["leadTimeDays"] == 14
    final = run_a.final_state.entities
    gap = max(final["DEM-001"]["quantity"] - final["INV-VEHICLE-PLANT"]["available"] - final["INV-VEHICLE-PLANT"]["inTransit"], 0)
    assert gap == 20
    assert run_a.transitions[0].changes["leadTimeDays"] == {"before": 7, "after": 14}
