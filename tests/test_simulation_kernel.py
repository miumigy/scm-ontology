from scm_ontology.simulation import Event, Scenario, SimulationError, SimulationKernel, State


def supplier_state():
    return State(
        state_id="S-000",
        effective_at=0,
        entities={
            "SUP-A": {
                "id": "SUP-A",
                "entityType": "Party",
                "partyType": "SUPPLIER",
                "name": "Supplier A",
                "leadTimeDays": 5,
            },
            "MAT-M001": {"id": "MAT-M001", "entityType": "Material", "available": 60},
            "DEM-001": {"id": "DEM-001", "entityType": "Demand", "quantity": 100},
        },
    )


def delay_event():
    return Event("E-001", "SUPPLIER_DELAY", 7, "SUP-A", {"magnitudeDays": 7})


def test_supplier_delay_is_explicit_state_transition():
    initial = supplier_state()
    next_state, transition = SimulationKernel().apply_event(initial, delay_event())

    assert initial.entities["SUP-A"]["leadTimeDays"] == 5
    assert next_state.entities["SUP-A"]["leadTimeDays"] == 12
    assert transition.changes["leadTimeDays"] == {"before": 5, "after": 12}
    assert transition.event_id == "E-001"


def test_event_does_not_mutate_input_state():
    initial = supplier_state()
    original = initial.snapshot()
    SimulationKernel().apply_event(initial, delay_event())
    assert initial.snapshot() == original


def test_same_scenario_and_seed_are_reproducible():
    scenario = Scenario("SCN-delay", supplier_state(), (delay_event(),), seed=42)
    kernel = SimulationKernel()

    run_a = kernel.run(scenario)
    run_b = kernel.run(scenario)

    assert run_a.to_dict() == run_b.to_dict()
    assert run_a.simulation_run_id == run_b.simulation_run_id


def test_events_are_processed_deterministically_by_time_then_id():
    first = Event("E-002", "SUPPLIER_DELAY", 7, "SUP-A", {"magnitudeDays": 2})
    second = Event("E-001", "SUPPLIER_DELAY", 7, "SUP-A", {"magnitudeDays": 7})
    scenario = Scenario("SCN-order", supplier_state(), (first, second), seed=1)

    run = SimulationKernel().run(scenario)

    assert [event.event_id for event in run.events] == ["E-001", "E-002"]
    assert run.final_state.entities["SUP-A"]["leadTimeDays"] == 14


def test_invalid_supplier_delay_is_rejected():
    event = Event("E-bad", "SUPPLIER_DELAY", 1, "MAT-M001", {"magnitudeDays": 7})
    try:
        SimulationKernel().apply_event(supplier_state(), event)
    except SimulationError as exc:
        assert "supplier Party" in str(exc)
    else:
        raise AssertionError("invalid supplier delay was accepted")


def test_canonical_payload_is_machine_readable():
    scenario = Scenario("SCN-delay", supplier_state(), (delay_event(),), seed=42)
    payload = SimulationKernel().run(scenario).canonical_payload()

    assert payload["simulationRun"]["scenarioId"] == "SCN-delay"
    assert payload["events"][0]["eventType"] == "SUPPLIER_DELAY"
    assert payload["transitions"][0]["entityId"] == "SUP-A"
