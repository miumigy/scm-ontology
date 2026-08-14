import pytest

from scm_ontology.state import CanonicalState, StateConceptError, is_state


def test_creates_canonical_state():
    state = CanonicalState(
        state_type="arrived",
        subject_id="SHP-001",
        effective_at="2026-09-01T14:10:00+09:00",
    )
    assert state.state_type == "arrived"
    assert is_state(state)


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"state_type": "", "subject_id": "S", "effective_at": "2026-09-01"}, "state_type"),
        ({"state_type": "arrived", "subject_id": "", "effective_at": "2026-09-01"}, "subject_id"),
        ({"state_type": "arrived", "subject_id": "S", "effective_at": ""}, "effective_at"),
    ],
)
def test_rejects_invalid_state(kwargs, message):
    with pytest.raises(StateConceptError, match=message):
        CanonicalState(**kwargs)
