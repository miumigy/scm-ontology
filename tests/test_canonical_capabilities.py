import pytest
from scm_ontology.canonical_capabilities import CANONICAL_CAPABILITIES, get_canonical_capability

def test_canonical_capability_vocabulary_is_stable_and_nonempty():
    assert {"planning", "execution", "provenance", "learning", "reasoning", "temporal"} <= set(CANONICAL_CAPABILITIES)
    assert all(CANONICAL_CAPABILITIES.values())

def test_canonical_capability_returns_structured_definition():
    capability = get_canonical_capability("planning")
    assert capability.key == "planning"
    assert capability.description

def test_unknown_capability_is_rejected():
    with pytest.raises(ValueError):
        get_canonical_capability("made_up_capability")
