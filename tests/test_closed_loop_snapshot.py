from scm_ontology.closed_loop_snapshot import rebuild_snapshot
from scm_ontology.fact_provenance import FactProvenance, ProvenancedFact
from scm_ontology.feedback_loop import outcome_to_fact
from scm_ontology.execution_lineage import record_execution, record_outcome
from scm_ontology.semantic_runtime import ExecutionRequest, ReasoningProvenance

def test_feedback_rebuilds_next_snapshot_with_observed_actual_state():
    prior = ProvenancedFact("f1", "stock", "sku-1", 10, FactProvenance("ERP", "r1", valid_from="2026-01-01T00:00:00Z"))
    request = ExecutionRequest("r1", "d1", {"action": "replenish"}, ReasoningProvenance("d1", "policy"))
    lineage = record_outcome(record_execution(request, event_id="e1", status="completed", observed_at="2026-08-16T01:00:00Z"), outcome_id="o1", observed_at="2026-08-16T02:00:00Z", result={"stock": 30})
    feedback = outcome_to_fact(lineage, fact_id="f2", predicate="stock", subject_id="sku-1", value=30)
    snapshot = rebuild_snapshot("s2", (prior,), (feedback,), at="2026-08-16T03:00:00Z")
    assert snapshot.fact("f2").value == 30
    assert snapshot.fact("f2").provenance.source_record == "o1"
