import pytest
from scm_ontology.evidence_accountability import EvidenceAccountabilityNotFound, trace_evidence_accountability
from scm_ontology.semantic_runtime import DecisionTrace

def test_decision_evidence_is_resolved_in_declared_order():
    decision = DecisionTrace("d1", {"action": "expedite"}, ("ev2", "ev1"))
    result = trace_evidence_accountability(decision, evidence_by_id={"ev1": {"fact": "f1"}, "ev2": {"fact": "f2"}})
    assert result.decision_id == "d1"
    assert result.evidence == ({"fact": "f2"}, {"fact": "f1"})

def test_missing_evidence_is_not_silently_dropped():
    decision = DecisionTrace("d1", {"action": "expedite"}, ("ev1", "missing"))
    with pytest.raises(EvidenceAccountabilityNotFound):
        trace_evidence_accountability(decision, evidence_by_id={"ev1": {"fact": "f1"}})
