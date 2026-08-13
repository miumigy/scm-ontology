from pathlib import Path

import pytest
import yaml

from scm_ontology.ontology_adapter import (
    OntologyAdapterError,
    find_relationship_state,
    project_canonical_state,
    relationship_state_id,
)

FIXTURE = Path(__file__).parents[1] / "examples" / "automotive" / "data.yaml"


def load_fixture():
    return yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))


def test_canonical_nodes_and_relationship_properties_project_separately():
    state = project_canonical_state(load_fixture(), state_id="AUTO-S3:t0")
    assert state.entities["SUP-001"]["partyType"] == "SUPPLIER"
    assert "leadTimeDays" not in state.entities["SUP-001"]
    supply = find_relationship_state(state, "SUPPLIES", "SUP-001", "MAT-001")
    assert supply["leadTimeDays"] == 7
    assert supply["moq"] == 100
    assert supply["unitCost"] == 120
    assert relationship_state_id("SUPPLIES", "SUP-001", "MAT-001") in state.relationship_states


def test_relationship_projection_preserves_scope_for_multiple_supply_links():
    dataset = load_fixture()
    dataset["edges"].append({"type": "SUPPLIES", "from": "SUP-001", "to": "SEAT-001", "properties": {"leadTimeDays": 12}})
    state = project_canonical_state(dataset, state_id="AUTO-S3-MULTI:t0")
    first = find_relationship_state(state, "SUPPLIES", "SUP-001", "MAT-001")
    second = find_relationship_state(state, "SUPPLIES", "SUP-001", "SEAT-001")
    assert first["leadTimeDays"] == 7
    assert second["leadTimeDays"] == 12


def test_projection_is_deterministic():
    dataset = load_fixture()
    state_a = project_canonical_state(dataset, state_id="AUTO-S3:t0")
    state_b = project_canonical_state(dataset, state_id="AUTO-S3:t0")
    assert state_a.snapshot() == state_b.snapshot()


def test_duplicate_node_id_is_rejected():
    dataset = load_fixture()
    dataset["nodes"].append({"id": "SUP-001", "type": "Party", "properties": {}})
    with pytest.raises(OntologyAdapterError, match="duplicate canonical node id"):
        project_canonical_state(dataset, state_id="AUTO-S3-DUP-NODE:t0")


def test_missing_relationship_endpoint_is_rejected():
    dataset = load_fixture()
    dataset["edges"].append(
        {"type": "SUPPLIES", "from": "SUP-001", "to": "UNKNOWN", "properties": {"leadTimeDays": 3}}
    )
    with pytest.raises(OntologyAdapterError, match="relationship endpoint not found"):
        project_canonical_state(dataset, state_id="AUTO-S3-MISSING-ENDPOINT:t0")


def test_duplicate_relationship_projection_is_rejected():
    dataset = load_fixture()
    dataset["edges"].append(
        {"type": "SUPPLIES", "from": "SUP-001", "to": "MAT-001", "properties": {"leadTimeDays": 9}}
    )
    with pytest.raises(OntologyAdapterError, match="duplicate relationship projection"):
        project_canonical_state(dataset, state_id="AUTO-S3-DUP-REL:t0")
