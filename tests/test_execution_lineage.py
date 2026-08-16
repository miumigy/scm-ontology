import pytest
from scm_ontology.execution_lineage import record_execution, record_outcome
from scm_ontology.semantic_runtime import ExecutionRequest, ReasoningProvenance

def _request() -> ExecutionRequest:
    provenance = ReasoningProvenance("d1", "inventory policy", (), "fp1")
    return ExecutionRequest("r1", "d1", {"action": "replenish"}, provenance)

def test_execution_lineage_links_request_to_completed_outcome():
    lineage = record_execution(_request(), event_id="e1", status="completed", observed_at="2026-08-16T01:00:00Z")
    lineage = record_outcome(lineage, outcome_id="o1", observed_at="2026-08-16T02:00:00Z", result={"stock": 30})
    assert lineage.event.request_id == "r1"
    assert lineage.outcome.event_id == "e1"
    assert lineage.request.provenance.snapshot_fingerprint == "fp1"

def test_outcome_requires_completed_execution():
    lineage = record_execution(_request(), event_id="e1", status="failed", observed_at="2026-08-16T01:00:00Z")
    with pytest.raises(ValueError):
        record_outcome(lineage, outcome_id="o1", observed_at="2026-08-16T02:00:00Z", result={})
