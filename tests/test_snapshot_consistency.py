import pytest
from scm_ontology.fact_provenance import FactProvenance, ProvenancedFact
from scm_ontology.snapshot_consistency import SnapshotConsistencyError, find_conflicts, require_consistent_snapshot
from scm_ontology.temporal_snapshot import build_snapshot

def _fact(fact_id: str, value: object) -> ProvenancedFact:
    return ProvenancedFact(fact_id, "stock", "sku-1", value, FactProvenance("ERP", fact_id, valid_from="2026-01-01T00:00:00Z"))

def test_snapshot_detects_conflicting_values_for_same_semantic_slot():
    snapshot = build_snapshot("s1", (_fact("f1", 10), _fact("f2", 20)), at="2026-08-16T00:00:00Z")
    conflicts = find_conflicts(snapshot)
    assert len(conflicts) == 1
    assert conflicts[0].fact_ids == ("f1", "f2")

def test_consistency_gate_rejects_conflicting_snapshot():
    snapshot = build_snapshot("s1", (_fact("f1", 10), _fact("f2", 20)), at="2026-08-16T00:00:00Z")
    with pytest.raises(SnapshotConsistencyError):
        require_consistent_snapshot(snapshot)

def test_consistency_gate_accepts_snapshot_without_conflicts():
    snapshot = build_snapshot("s1", (_fact("f1", 10),), at="2026-08-16T00:00:00Z")
    assert require_consistent_snapshot(snapshot) is snapshot
