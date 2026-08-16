from scm_ontology.fact_evidence import CanonicalFact, bind_fact_evidence, trace_with_fact_evidence

def test_canonical_fact_is_preserved_as_decision_evidence():
    fact = CanonicalFact("f1", "supplier_lead_time_days", "supplier-1", 7, "2026-08-16T00:00:00Z")
    binding = bind_fact_evidence(fact, evidence_id="ev1")
    trace = trace_with_fact_evidence("d1", {"action": "expedite"}, (binding,))
    assert binding.fact_id == "f1"
    assert binding.fact is fact
    assert trace.evidence == (binding,)
    assert trace.evidence[0].fact.predicate == "supplier_lead_time_days"
