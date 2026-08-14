import pytest

from scm_ontology.canonical_state import CanonicalState, CanonicalStateError, is_state


def test_state_represents_entity_condition():
    state = CanonicalState("SITE-A", "availability", {"status": "available"})
    assert state.entity_id == "SITE-A"
    assert state.state_type == "availability"
    assert is_state(state)


def test_state_requires_entity_and_type():
    with pytest.raises(CanonicalStateError, match="entity_id must be non-empty"):
        CanonicalState("", "availability", {})
    with pytest.raises(CanonicalStateError, match="state_type must be non-empty"):
        CanonicalState("SITE-A", "", {})


def test_state_attributes_are_explicit():
    with pytest.raises(CanonicalStateError, match="attributes must be provided"):
        CanonicalState("SITE-A", "availability", None)
