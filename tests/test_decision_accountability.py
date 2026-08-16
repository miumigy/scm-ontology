import pytest
from scm_ontology.decision_accountability import DecisionAccountabilityNotFound, trace_decision_accountability
from scm_ontology.execution_lineage import record_execution, record_outcome
from scm_ontology.fact_provenance import FactProvenance, ProvenancedFact
from scm_ontology.semantic_runtime import ExecutionRequest, ReasoningProvenance, DecisionTrace
from scm_ontology.snapshot_lineage import link_snapshot_transition
from scm_ontology.temporal_snapshot import build_snapshot

def test_current_snapshot_can_be_traced_back_to_decision():
    fact1 = ProvenancedFact("f1", "stock", "sku-1", 10, FactProvenance("ERP", "r1", valid_from="2026-01-01T00:00:00Z"))
    fact2 = ProvenancedFact("f2", "stock", "sku-1", 30, FactProvenance("execution", "o1", valid_from="2026-08-16T02:00:00Z"))
    s1 = build_snapshot("s1", (fact1,), at="2026-08-16T00:00:00Z")
    s2 = build_snapshot("s2", (fact1, fact2), at="2026-08-16T03:00:00Z")
    req = ExecutionRequest("r1", "d1", {"action": "replenish"}, ReasoningProvenance("d1", "policy", (), None))
    lineage = record_outcome(record_execution(req, event_id="e1", status="completed", observed_at="2026-08-16T01:00:00Z"), outcome_id="o1", observed_at="2026-08-16T02:00:00Z", result={"stock": 30})
    transition = link_snapshot_transition(s1, lineage, s2)
    decision = DecisionTrace("d1", {"action": "replenish"}, (), transition.from_fingerprint)
    result = trace_decision_accountability((transition,), (decision,), snapshot_id="s2")
    assert result.decision_id == "d1"
    assert result.snapshot_fingerprint == transition.from_fingerprint

def test_unknown_snapshot_has_no_accountability():
    with pytest.raises(DecisionAccountabilityNotFound):
        trace_decision_accountability((), (), snapshot_id="missing")
