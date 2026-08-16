from scm_ontology.accountability_runtime import AccountabilityRuntime
from scm_ontology.end_to_end_accountability import EndToEndAccountability
from scm_ontology.decision_accountability import DecisionAccountability
from scm_ontology.evidence_accountability import EvidenceAccountability
from scm_ontology.provenance_accountability import ProvenanceAccountability
from scm_ontology.fact_provenance import FactProvenance, ProvenancedFact
from scm_ontology.snapshot_lineage import SnapshotTransition

def _result():
    transition = SnapshotTransition("s0", "fp0", "e1", "o1", "s1", "fp1", "2026-08-16T02:00:00Z")
    decision = DecisionAccountability("s1", (transition,), "d1", "fp0")
    fact = ProvenancedFact("f1", "stock", "sku-1", 30, FactProvenance("ERP", "record-42", observed_at="2026-08-16T01:00:00Z", valid_from="2026-08-16T00:00:00Z"))
    evidence = EvidenceAccountability("ev1", fact)
    provenance = ProvenanceAccountability("ev1", fact, "record-42", "2026-08-16T01:00:00Z", "2026-08-16T00:00:00Z", None)
    return EndToEndAccountability(decision, (evidence,), (provenance,))

def test_runtime_exposes_versioned_mapping():
    mapping = AccountabilityRuntime().mapping(_result())
    assert mapping["contract_version"] == "1.0.0"
    assert mapping["decision"]["decision_id"] == "d1"

def test_runtime_exposes_canonical_json():
    payload = AccountabilityRuntime().json(_result())
    assert payload == AccountabilityRuntime().json(_result())
    assert '"contract_version": "1.0.0"' in payload
