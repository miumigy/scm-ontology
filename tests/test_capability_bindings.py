import pytest
from scm_ontology.capability_bindings import CAPABILITY_BINDINGS, get_capability_binding
from scm_ontology.canonical_capabilities import CANONICAL_CAPABILITIES

def test_every_canonical_capability_has_a_trace_binding():
    assert set(CAPABILITY_BINDINGS) == set(CANONICAL_CAPABILITIES)
    assert all(CAPABILITY_BINDINGS.values())

def test_planning_binding_exposes_decision_and_request_semantics():
    binding = get_capability_binding("planning")
    assert binding.bundle_elements == frozenset({"decision_trace", "execution_request"})

def test_unknown_capability_binding_is_rejected():
    with pytest.raises(ValueError):
        get_capability_binding("unknown")
