from scm_ontology.fact_evidence import CanonicalFact, bind_fact_evidence, provenanced_fact_from_canonical
from scm_ontology.fact_provenance import FactProvenance

def test_provenanced_canonical_fact_can_become_runtime_evidence():
    fact = CanonicalFact("f1", "shipment_status", "shipment-1", "delayed")
    provenance = FactProvenance("WMS", "shipment-1", observed_at="2026-08-16T01:00:00Z", confidence=0.99)
    provenanced = provenanced_fact_from_canonical(fact, provenance)
    evidence = bind_fact_evidence(provenanced, evidence_id="ev1")
    assert evidence.fact.fact_id == "f1"
    assert evidence.fact.provenance.source == "WMS"
    assert evidence.fact.provenance.confidence == 0.99
