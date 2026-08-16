from scm_ontology.capability_negotiation import CapabilitySet
from scm_ontology.contract_runtime import ContractRuntime
from scm_ontology.decision_learning import learn_from_feedback
from scm_ontology.runtime_feedback import record_execution_feedback
from scm_ontology.semantic_contract_e2e import SemanticContractSession
from scm_ontology.semantic_runtime import DecisionTrace

def _feedback():
    session = SemanticContractSession.negotiate(CapabilitySet(frozenset({"1.0.0"}), frozenset({"planning"})), CapabilitySet(frozenset({"1.0.0"}), frozenset({"planning"})))
    pipeline = ContractRuntime(session).build_pipeline(DecisionTrace("d1", {"action": "expedite"}), rationale="late", request_id="d1")
    return pipeline.trace, record_execution_feedback(pipeline.request, event_id="e1", outcome={"status": "done"}, valid=False, findings=("late",))

def test_feedback_evaluates_and_can_create_a_revised_decision():
    trace, feedback = _feedback()
    outcome = learn_from_feedback(trace, feedback, revision_id="d2", revised_decision={"action": "expedite_earlier"}, reason="prior action was too late")
    assert outcome.evaluation.decision_id == "d1"
    assert outcome.evaluation.successful is False
    assert outcome.revision.source_decision_id == "d1"
    assert outcome.revision.revised_decision["action"] == "expedite_earlier"
