import pytest
from scm_ontology.capability_aware_negotiation import negotiate_semantic_surface
from scm_ontology.capability_negotiation import CapabilitySet
from scm_ontology.semantic_surface_profile import profile_from_negotiation

def test_profile_materializes_negotiated_semantic_surface():
    result = negotiate_semantic_surface(CapabilitySet(frozenset({"1.0.0", "1.1.0"}), frozenset({"planning", "execution"})), CapabilitySet(frozenset({"1.0.0"}), frozenset({"planning"})))
    profile = profile_from_negotiation(result)
    assert profile.schema_version == "1.0.0"
    assert profile.shared_capabilities == ("planning",)
    assert profile.semantic_elements == ("decision_trace", "execution_request")
    assert profile.usable is True

def test_profile_rejects_unnegotiated_preferred_version():
    result = negotiate_semantic_surface(CapabilitySet(frozenset({"1.0.0"}), frozenset({"planning"})), CapabilitySet(frozenset({"1.0.0"}), frozenset({"planning"})))
    with pytest.raises(ValueError):
        profile_from_negotiation(result, preferred_schema_version="2.0.0")

def test_profile_rejects_no_compatible_version():
    result = negotiate_semantic_surface(CapabilitySet(frozenset({"2.0.0"}), frozenset({"planning"})), CapabilitySet(frozenset({"1.0.0"}), frozenset({"planning"})))
    with pytest.raises(ValueError):
        profile_from_negotiation(result)
