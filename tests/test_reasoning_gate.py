import pytest
from scm_ontology.fact_provenance import FactProvenance, ProvenancedFact
from scm_ontology.reasoning_gate import build_reasoning_context
from scm_ontology.snapshot_consistency import SnapshotConsistencyError
from scm_ontology.temporal_snapshot import build_snapshot

def _fact(fact_id: str, value: object) -> ProvenancedFact:
    return ProvenancedFact(fact_id, "stock", "sku-1", value, FactProvenance("ERP", fact_id, valid_from="2026-01-01T00:00:00Z"))

def test_reasoning_gate_builds_context_from_consistent_temporal_snapshot():
    snapshot = build_snapshot("s1", (_fact("f1", 10),), at="2026-08-16T00:00:00Z")
    context = build_reasoning_context("d1", {"action": "replenish"}, snapshot)
    assert context.snapshot is snapshot
    assert context.trace.decision_id == "d1"
    assert context.trace.evidence[0].fact.fact_id == "f1"

def test_reasoning_gate_rejects_conflicting_snapshot():
    snapshot = build_snapshot("s1", (_fact("f1", 10), _fact("f2", 20)), at="2026-08-16T00:00:00Z")
    with pytest.raises(SnapshotConsistencyError):
        build_reasoning_context("d1", {"action": "replenish"}, snapshot)
