from scm_ontology.fact_provenance import FactProvenance, ProvenancedFact
from scm_ontology.snapshot_identity import snapshot_fingerprint
from scm_ontology.temporal_snapshot import build_snapshot

def _fact(fact_id: str, value: object) -> ProvenancedFact:
    return ProvenancedFact(fact_id, "stock", "sku-1", value, FactProvenance("ERP", fact_id, valid_from="2026-01-01T00:00:00Z"))

def test_snapshot_fingerprint_is_deterministic_and_order_independent():
    a = build_snapshot("a", (_fact("f2", 20), _fact("f1", 10)), at="2026-08-16T00:00:00Z")
    b = build_snapshot("b", (_fact("f1", 10), _fact("f2", 20)), at="2026-08-16T00:00:00Z")
    assert snapshot_fingerprint(a) == snapshot_fingerprint(b)

def test_snapshot_fingerprint_changes_when_semantic_content_changes():
    a = build_snapshot("a", (_fact("f1", 10),), at="2026-08-16T00:00:00Z")
    b = build_snapshot("b", (_fact("f1", 11),), at="2026-08-16T00:00:00Z")
    assert snapshot_fingerprint(a) != snapshot_fingerprint(b)
