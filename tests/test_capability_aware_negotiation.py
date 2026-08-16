from scm_ontology.capability_aware_negotiation import negotiate_semantic_surface
from scm_ontology.capability_negotiation import CapabilitySet

def test_negotiation_derives_shared_semantic_surface():
    producer = CapabilitySet(frozenset({"1.0.0"}), frozenset({"planning", "provenance", "learning"}))
    consumer = CapabilitySet(frozenset({"1.0.0"}), frozenset({"planning", "execution"}))
    result = negotiate_semantic_surface(producer, consumer)
    assert result.compatible is True
    assert result.shared_capabilities == ("planning",)
    assert result.shared_semantic_elements == ("decision_trace", "execution_request")

def test_no_shared_capability_still_reports_version_compatibility_but_empty_surface():
    producer = CapabilitySet(frozenset({"1.0.0"}), frozenset({"planning"}))
    consumer = CapabilitySet(frozenset({"1.0.0"}), frozenset({"execution"}))
    result = negotiate_semantic_surface(producer, consumer)
    assert result.compatible is True
    assert result.shared_capabilities == ()
    assert result.shared_semantic_elements == ()
