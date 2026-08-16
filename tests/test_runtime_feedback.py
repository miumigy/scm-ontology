from scm_ontology.capability_negotiation import CapabilitySet
from scm_ontology.contract_runtime import ContractRuntime
from scm_ontology.runtime_feedback import record_execution_feedback
from scm_ontology.semantic_contract_e2e import SemanticContractSession
from scm_ontology.semantic_runtime import DecisionTrace


def test_execution_feedback_preserves_request_to_outcome_lineage():
    session = SemanticContractSession.negotiate(
        CapabilitySet(frozenset({"1.0.0"}), frozenset({"planning"})),
        CapabilitySet(frozenset({"1.0.0"}), frozenset({"planning"})),
    )
    pipeline = ContractRuntime(session).build_pipeline(
        DecisionTrace("d1", {"action": "expedite"}), rationale="late", request_id="r1"
    )
    feedback = record_execution_feedback(pipeline.request, event_id="e1", outcome={"status": "done"}, valid=True)
    assert feedback.event.request_id == "r1"
    assert feedback.validation.event_id == "e1"
    assert feedback.validation.valid is True
