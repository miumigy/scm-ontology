import pytest
from scm_ontology.execution_lineage import record_execution, record_outcome
from scm_ontology.fact_provenance import FactProvenance, ProvenancedFact
from scm_ontology.semantic_runtime import ExecutionRequest, ReasoningProvenance
from scm_ontology.snapshot_lineage import link_snapshot_transition
from scm_ontology.temporal_snapshot import build_snapshot

def _request():
    return ExecutionRequest("r1", "d1", {"action": "replenish"}, ReasoningProvenance("d1", "policy", (), "fp0"))

def test_snapshot_transition_links_prior_and_next_state_through_outcome():
    fact1 = ProvenancedFact("f1", "stock", "sku-1", 10, FactProvenance("ERP", "r1", valid_from="2026-01-01T00:00:00Z"))
    fact2 = ProvenancedFact("f2", "stock", "sku-1", 30, FactProvenance("execution", "o1", valid_from="2026-08-16T02:00:00Z"))
    previous = build_snapshot("s1", (fact1,), at="2026-08-16T00:00:00Z")
    next_snapshot = build_snapshot("s2", (fact1, fact2), at="2026-08-16T03:00:00Z")
    lineage = record_outcome(record_execution(_request(), event_id="e1", status="completed", observed_at="2026-08-16T01:00:00Z"), outcome_id="o1", observed_at="2026-08-16T02:00:00Z", result={"stock": 30})
    transition = link_snapshot_transition(previous, lineage, next_snapshot)
    assert transition.from_snapshot_id == "s1"
    assert transition.to_snapshot_id == "s2"
    assert transition.execution_event_id == "e1"
    assert transition.outcome_id == "o1"
    assert transition.from_fingerprint != transition.to_fingerprint

def test_snapshot_transition_requires_next_state_after_outcome():
    fact = ProvenancedFact("f1", "stock", "sku-1", 10, FactProvenance("ERP", "r1", valid_from="2026-01-01T00:00:00Z"))
    previous = build_snapshot("s1", (fact,), at="2026-08-16T00:00:00Z")
    next_snapshot = build_snapshot("s2", (fact,), at="2026-08-16T01:00:00Z")
    lineage = record_outcome(record_execution(_request(), event_id="e1", status="completed", observed_at="2026-08-16T01:00:00Z"), outcome_id="o1", observed_at="2026-08-16T02:00:00Z", result={})
    with pytest.raises(ValueError):
        link_snapshot_transition(previous, lineage, next_snapshot)
