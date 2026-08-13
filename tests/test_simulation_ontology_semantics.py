from scm_ontology.simulation import Event, SimulationKernel, State


def product_location_state():
    return State(
        state_id="S-PL-001",
        effective_at=0,
        entities={
            "PL-P001-F001": {
                "id": "PL-P001-F001",
                "entityType": "ProductLocation",
                "productId": "P-001",
                "siteId": "F-001",
            },
            "DEM-001": {
                "id": "DEM-001",
                "entityType": "Demand",
                "productLocationId": "PL-P001-F001",
                "quantity": 100,
            },
            "IP-001": {
                "id": "IP-001",
                "entityType": "InventoryPosition",
                "productLocationId": "PL-P001-F001",
                "available": 60,
                "inTransit": 20,
            },
            "SUP-A": {
                "id": "SUP-A",
                "entityType": "Party",
                "partyType": "SUPPLIER",
                "leadTimeDays": 5,
            },
        },
    )


def demand_supply_gap(state: State) -> int:
    demand = sum(
        entity.get("quantity", 0)
        for entity in state.entities.values()
        if entity.get("entityType") == "Demand"
        and entity.get("productLocationId") == "PL-P001-F001"
    )
    relevant_supply = sum(
        entity.get("available", 0) + entity.get("inTransit", 0)
        for entity in state.entities.values()
        if entity.get("entityType") == "InventoryPosition"
        and entity.get("productLocationId") == "PL-P001-F001"
    )
    return max(demand - relevant_supply, 0)


def test_simulation_state_matches_canonical_demand_supply_semantics():
    state = product_location_state()

    assert demand_supply_gap(state) == 20
    assert state.entities["DEM-001"]["quantity"] == 100
    assert state.entities["IP-001"]["available"] == 60
    assert state.entities["IP-001"]["inTransit"] == 20


def test_supplier_delay_does_not_mutate_unrelated_demand_supply_state():
    state = product_location_state()
    event = Event("E-001", "SUPPLIER_DELAY", 7, "SUP-A", {"magnitudeDays": 7})

    next_state, _ = SimulationKernel().apply_event(state, event)

    assert demand_supply_gap(state) == 20
    assert demand_supply_gap(next_state) == 20
    assert next_state.entities["SUP-A"]["leadTimeDays"] == 12
