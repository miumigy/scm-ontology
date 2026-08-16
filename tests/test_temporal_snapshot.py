from scm_ontology.fact_provenance import FactProvenance, ProvenancedFact
from scm_ontology.temporal_snapshot import build_snapshot, trace_from_snapshot

def test_snapshot_contains_only_facts_valid_at_snapshot_time():
    facts = (
        ProvenancedFact("f1", "stock", "sku-1", 10, FactProvenance("ERP", "r1", valid_from="2026-01-01T00:00:00Z")),
        ProvenancedFact("f2", "shipment_status", "s1", "delayed", FactProvenance("TMS", "r2", valid_from="2025-01-01T00:00:00Z", valid_to="2026-01-01T00:00:00Z")),
    )
    snapshot = build_snapshot("snap-1", facts, at="2026-08-16T00:00:00Z")
    assert snapshot.fact("f1") is facts[0]
    assert snapshot.fact("f2") is None

def test_snapshot_can_become_decision_evidence():
    fact = ProvenancedFact("f1", "stock", "sku-1", 10, FactProvenance("ERP", "r1", valid_from="2026-01-01T00:00:00Z"))
    trace = trace_from_snapshot("d1", {"action": "replenish"}, build_snapshot("snap-1", (fact,), at="2026-08-16T00:00:00Z"))
    assert trace.evidence[0].fact.fact_id == "f1"
