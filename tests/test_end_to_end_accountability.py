import pytest
from scm_ontology.decision_accountability import DecisionAccountabilityNotFound
from scm_ontology.end_to_end_accountability import trace_end_to_end_accountability
from scm_ontology.fact_provenance import FactProvenance, ProvenancedFact
from scm_ontology.semantic_runtime import DecisionTrace
from scm_ontology.snapshot_lineage import SnapshotTransition

def test_end_to_end_accountability_resolves_decision_evidence_and_provenance():
    transition = SnapshotTransition("s0", "fp0", "e1", "o1", "s1", "fp1", "2026-08-16T02:00:00Z")
    decision = DecisionTrace("d1", {"action": "expedite"}, ("ev1",), "fp0")
    fact = ProvenancedFact("f1", "stock", "sku-1", 30, FactProvenance("ERP", "record-42", observed_at="2026-08-16T01:00:00Z", valid_from="2026-08-16T00:00:00Z"))
    result = trace_end_to_end_accountability((transition,), (decision,), snapshot_id="s1", evidence_by_id={"ev1": fact}, facts_by_evidence_id={"ev1": fact})
    assert result.decision.decision_id == "d1"
    assert result.evidence[0].evidence_id == "ev1"
    assert result.provenance[0].source_record == "record-42"

def test_unknown_snapshot_stays_an_accountability_failure():
    with pytest.raises(DecisionAccountabilityNotFound):
        trace_end_to_end_accountability((), (), snapshot_id="missing", evidence_by_id={}, facts_by_evidence_id={})
