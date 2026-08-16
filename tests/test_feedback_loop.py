import pytest
from scm_ontology.execution_lineage import record_execution, record_outcome
from scm_ontology.feedback_loop import outcome_to_fact
from scm_ontology.semantic_runtime import ExecutionRequest, ReasoningProvenance

def _lineage(completed=True):
    request = ExecutionRequest("r1", "d1", {"action": "replenish"}, ReasoningProvenance("d1", "policy", (), "fp1"))
    return record_execution(request, event_id="e1", status="completed" if completed else "failed", observed_at="2026-08-16T01:00:00Z")

def test_completed_outcome_becomes_canonical_fact_with_provenance():
    lineage = record_outcome(_lineage(), outcome_id="o1", observed_at="2026-08-16T02:00:00Z", result={"stock": 30})
    feedback = outcome_to_fact(lineage, fact_id="f3", predicate="stock", subject_id="sku-1", value=30)
    assert feedback.fact.value == 30
    assert feedback.fact.provenance.source_record == "o1"
    assert feedback.outcome_id == "o1"

def test_feedback_requires_observed_outcome():
    with pytest.raises(ValueError):
        outcome_to_fact(_lineage(), fact_id="f3", predicate="stock", subject_id="sku-1", value=30)
