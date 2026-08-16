import pytest
from scm_ontology.capability_negotiation import CapabilitySet
from scm_ontology.profile_bundle_builder import ProfileBundleConstructionError
from scm_ontology.semantic_contract_e2e import SemanticContractSession


def test_e2e_negotiation_profile_and_bundle_construction():
    session = SemanticContractSession.negotiate(
        CapabilitySet(frozenset({"1.0.0", "1.1.0"}), frozenset({"planning", "execution"})),
        CapabilitySet(frozenset({"1.0.0"}), frozenset({"planning"})),
    )
    assert session.profile.schema_version == "1.0.0"
    assert session.profile.shared_capabilities == ("planning",)
    assert session.build_bundle({"decision_trace": {"id": "d1"}}) == {"decision_trace": {"id": "d1"}}


def test_e2e_rejects_bundle_outside_negotiated_surface():
    session = SemanticContractSession.negotiate(
        CapabilitySet(frozenset({"1.0.0"}), frozenset({"planning"})),
        CapabilitySet(frozenset({"1.0.0"}), frozenset({"planning"})),
    )
    with pytest.raises(ProfileBundleConstructionError):
        session.build_bundle({"execution_event": {"id": "e1"}})
