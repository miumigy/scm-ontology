from scm_ontology.capability_negotiation import CapabilitySet
from scm_ontology.closed_loop_runtime import ClosedLoopRuntime
from scm_ontology.contract_runtime import ContractRuntime
from scm_ontology.semantic_contract_e2e import SemanticContractSession
from scm_ontology.semantic_runtime import DecisionTrace

def test_closed_loop_runtime_completes_decision_execution_feedback_revision():
    session = SemanticContractSession.negotiate(CapabilitySet(frozenset({"1.0.0"}), frozenset({"planning"})), CapabilitySet(frozenset({"1.0.0"}), frozenset({"planning"})))
    result = ClosedLoopRuntime(ContractRuntime(session)).run(DecisionTrace("d1", {"action": "expedite"}), rationale="late supplier", request_id="r1", event_id="e1", outcome={"status": "late"}, valid=False, findings=("late",), revision_id="d2", revised_decision={"action": "expedite_earlier"}, revision_reason="improve lead-time response")
    assert result.pipeline.request.request_id == "r1"
    assert result.feedback.event.event_id == "e1"
    assert result.learning.revision.source_decision_id == "d1"
    assert result.learning.revision.revised_decision["action"] == "expedite_earlier"
