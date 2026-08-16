from scm_ontology.accountability_query import AccountabilityQueryRequest, execute_accountability_query, query_response_to_mapping
from scm_ontology.semantic_runtime import DecisionTrace
from scm_ontology.snapshot_lineage import SnapshotTransition
from scm_ontology.fact_provenance import FactProvenance, ProvenancedFact

def _inputs():
    transition = SnapshotTransition("s0", "fp0", "e1", "o1", "s1", "fp1", "2026-08-16T02:00:00Z")
    decision = DecisionTrace("d1", {"action": "expedite"}, ("ev1",), "fp0")
    fact = ProvenancedFact("f1", "stock", "sku-1", 30, FactProvenance("ERP", "record-42", observed_at="2026-08-16T01:00:00Z", valid_from="2026-08-16T00:00:00Z"))
    return (transition,), (decision,), {"ev1": fact}, {"ev1": fact}

def test_query_resolves_to_versioned_response():
    response = execute_accountability_query(AccountabilityQueryRequest("s1"), transitions=_inputs()[0], decisions=_inputs()[1], evidence_by_id=_inputs()[2], facts_by_evidence_id=_inputs()[3])
    assert response.status == "resolved"
    assert response.contract_version == "1.0.0"
    assert response.accountability["decision"]["decision_id"] == "d1"
    assert response.accountability["evidence"][0]["evidence_id"] == "ev1"

def test_query_unknown_snapshot_is_protocol_not_found():
    inputs = _inputs()
    response = execute_accountability_query(AccountabilityQueryRequest("missing"), transitions=(), decisions=(), evidence_by_id={}, facts_by_evidence_id={})
    assert response.status == "not_found"
    assert response.error == "missing"

def test_query_rejects_unknown_contract_version():
    inputs = _inputs()
    response = execute_accountability_query(AccountabilityQueryRequest("s1", "9.9.9"), transitions=inputs[0], decisions=inputs[1], evidence_by_id=inputs[2], facts_by_evidence_id=inputs[3])
    assert response.status == "contract_version_mismatch"
    assert query_response_to_mapping(response)["error"] == "9.9.9"
