from scm_ontology.fact_provenance import FactProvenance, ProvenancedFact
from scm_ontology.temporal_evidence import select_evidence_at, trace_with_temporal_evidence

def test_temporal_evidence_only_binds_facts_valid_at_decision_time():
    facts = (
        ProvenancedFact("f1", "stock", "sku-1", 10, FactProvenance("ERP", "r1", valid_from="2026-01-01T00:00:00Z")),
        ProvenancedFact("f2", "stock", "sku-1", 20, FactProvenance("ERP", "r2", valid_from="2025-01-01T00:00:00Z", valid_to="2026-01-01T00:00:00Z")),
    )
    evidence = select_evidence_at(facts, at="2026-08-16T00:00:00Z")
    assert tuple(item.fact_id for item in evidence) == ("f1",)
    trace = trace_with_temporal_evidence("d1", {"action": "replenish"}, facts, at="2026-08-16T00:00:00Z")
    assert trace.evidence[0].fact.fact_id == "f1"
