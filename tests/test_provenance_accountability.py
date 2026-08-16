import pytest
from scm_ontology.fact_provenance import FactProvenance, ProvenancedFact
from scm_ontology.provenance_accountability import ProvenanceAccountabilityNotFound, trace_provenance_accountability

def test_evidence_resolves_to_source_and_temporal_provenance():
    fact = ProvenancedFact("f1", "stock", "sku-1", 30, FactProvenance("ERP", "record-42", observed_at="2026-08-16T02:00:00Z", valid_from="2026-08-16T00:00:00Z", valid_to=None))
    result = trace_provenance_accountability("ev1", facts_by_evidence_id={"ev1": fact})
    assert result.source_record == "record-42"
    assert result.observed_at == "2026-08-16T02:00:00Z"
    assert result.valid_from == "2026-08-16T00:00:00Z"
    assert result.valid_to is None

def test_unknown_evidence_has_no_provenance_accountability():
    with pytest.raises(ProvenanceAccountabilityNotFound):
        trace_provenance_accountability("missing", facts_by_evidence_id={})
