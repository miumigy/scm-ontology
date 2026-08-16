from scm_ontology.fact_provenance import FactProvenance, ProvenancedFact
from scm_ontology.fact_temporal import is_valid_at, select_valid_facts

def test_fact_temporal_validity_uses_half_open_interval():
    fact = ProvenancedFact("f1", "stock", "sku-1", 10, FactProvenance("ERP", "r1", valid_from="2026-01-01T00:00:00Z", valid_to="2026-02-01T00:00:00Z"))
    assert is_valid_at(fact, "2026-01-31T23:59:59Z")
    assert not is_valid_at(fact, "2026-02-01T00:00:00Z")

def test_select_valid_facts_filters_temporally_invalid_evidence():
    active = ProvenancedFact("f1", "stock", "sku-1", 10, FactProvenance("ERP", "r1", valid_from="2026-01-01T00:00:00Z"))
    expired = ProvenancedFact("f2", "stock", "sku-1", 20, FactProvenance("ERP", "r2", valid_from="2025-01-01T00:00:00Z", valid_to="2026-01-01T00:00:00Z"))
    assert select_valid_facts((active, expired), at="2026-08-16T00:00:00Z") == (active,)
