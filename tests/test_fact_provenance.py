import pytest
from scm_ontology.fact_provenance import FactProvenance, bind_provenance

def test_fact_provenance_preserves_source_and_temporal_lineage():
    provenance = FactProvenance("WMS", "shipment-123", "2026-08-16T01:00:00Z", "2026-08-16T00:00:00Z", None, 0.98)
    fact = bind_provenance("f1", "shipment_status", "shipment-123", "delayed", provenance)
    assert fact.provenance.source == "WMS"
    assert fact.provenance.source_record == "shipment-123"
    assert fact.provenance.valid_from == "2026-08-16T00:00:00Z"
    assert fact.provenance.confidence == 0.98

def test_fact_provenance_rejects_invalid_confidence():
    with pytest.raises(ValueError):
        FactProvenance("ERP", "x", confidence=1.1)
