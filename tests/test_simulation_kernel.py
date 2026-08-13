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


def delay_event(event_id="E-001", occurred_at=7, magnitude=7):
    return Event(event_id, "SUPPLIER_DELAY", occurred_at, "SUP-A", {"magnitudeDays": magnitude})


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


def test_multiple_events_form_a_connected_transition_chain():
    events = (
        delay_event("E-002", occurred_at=14, magnitude=2),
        delay_event("E-001", occurred_at=7, magnitude=7),
    )
    run = SimulationKernel().run(Scenario("SCN-chain", supplier_state(), events, seed=42))

    assert [event.event_id for event in run.events] == ["E-001", "E-002"]
    assert len(run.transitions) == 2
    assert run.transitions[0].from_state_id == "S-000"
    assert run.transitions[0].to_state_id == run.transitions[1].from_state_id
    assert run.transitions[1].to_state_id == run.final_state.state_id
    assert run.final_state.entities["SUP-A"]["leadTimeDays"] == 14
    run.validate_transition_chain()


def test_events_are_processed_deterministically_by_time_then_id():
    first = delay_event("E-002", occurred_at=7, magnitude=2)
    second = delay_event("E-001", occurred_at=7, magnitude=7)
    scenario = Scenario("SCN-order", supplier_state(), (first, second), seed=1)

    run = SimulationKernel().run(scenario)

    assert [event.event_id for event in run.events] == ["E-001", "E-002"]
    assert run.final_state.entities["SUP-A"]["leadTimeDays"] == 14


def test_duplicate_event_ids_are_rejected():
    scenario = Scenario(
        "SCN-duplicate",
        supplier_state(),
        (delay_event("E-001"), delay_event("E-001", occurred_at=14, magnitude=2)),
    )
    try:
        SimulationKernel().run(scenario)
    except SimulationError as exc:
        assert "event ids must be unique" in str(exc)
    else:
        raise AssertionError("duplicate event ids were accepted")


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
