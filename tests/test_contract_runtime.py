import pytest
from scm_ontology.capability_negotiation import CapabilitySet
from scm_ontology.contract_runtime import ContractRuntime
from scm_ontology.semantic_contract_e2e import SemanticContractSession
from scm_ontology.semantic_runtime import DecisionTrace
from scm_ontology.profile_enforcement import SemanticBoundaryError

def test_contract_runtime_enforces_negotiated_capability_before_execution():
    session = SemanticContractSession.negotiate(CapabilitySet(frozenset({"1.0.0"}), frozenset({"planning"})), CapabilitySet(frozenset({"1.0.0"}), frozenset({"planning"})))
    pipeline = ContractRuntime(session).build_pipeline(DecisionTrace("d1", {"action": "expedite"}), rationale="late", request_id="r1")
    assert pipeline.request.request_id == "r1"
    assert pipeline.request.provenance.decision_id == "d1"

def test_contract_runtime_rejects_unsupported_capability():
    session = SemanticContractSession.negotiate(CapabilitySet(frozenset({"1.0.0"}), frozenset({"planning"})), CapabilitySet(frozenset({"1.0.0"}), frozenset({"planning"})))
    with pytest.raises(SemanticBoundaryError):
        ContractRuntime(session).build_pipeline(DecisionTrace("d1", "act"), rationale="r", request_id="r1", capability="execution")
