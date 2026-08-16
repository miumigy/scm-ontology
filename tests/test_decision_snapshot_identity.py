from scm_ontology.fact_provenance import FactProvenance, ProvenancedFact
from scm_ontology.reasoning_gate import build_reasoning_context
from scm_ontology.snapshot_identity import snapshot_fingerprint
from scm_ontology.temporal_snapshot import build_snapshot
from scm_ontology.semantic_runtime import build_runtime_pipeline

def test_decision_trace_records_snapshot_fingerprint():
    fact = ProvenancedFact("f1", "stock", "sku-1", 10, FactProvenance("ERP", "r1", valid_from="2026-01-01T00:00:00Z"))
    snapshot = build_snapshot("s1", (fact,), at="2026-08-16T00:00:00Z")
    context = build_reasoning_context("d1", {"action": "replenish"}, snapshot)
    assert context.trace.snapshot_fingerprint == snapshot_fingerprint(snapshot)

def test_snapshot_fingerprint_survives_runtime_provenance():
    fact = ProvenancedFact("f1", "stock", "sku-1", 10, FactProvenance("ERP", "r1", valid_from="2026-01-01T00:00:00Z"))
    snapshot = build_snapshot("s1", (fact,), at="2026-08-16T00:00:00Z")
    context = build_reasoning_context("d1", {"action": "replenish"}, snapshot)
    pipeline = build_runtime_pipeline(context.trace, rationale="inventory policy", request_id="r1")
    assert pipeline.provenance.snapshot_fingerprint == context.trace.snapshot_fingerprint
    assert pipeline.request.provenance.snapshot_fingerprint == snapshot_fingerprint(snapshot)
