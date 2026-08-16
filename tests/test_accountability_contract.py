from scm_ontology.accountability_contract import accountability_to_json, accountability_to_mapping
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

def test_mapping_has_stable_contract_version_and_json_safe_values():
    mapping = accountability_to_mapping(_result())
    assert mapping["contract_version"] == "1.0.0"
    assert mapping["decision"]["decision_id"] == "d1"
    assert mapping["provenance"][0]["source_record"] == "record-42"

def test_json_is_deterministic_and_utf8_safe():
    result = _result()
    assert accountability_to_json(result) == accountability_to_json(result)
    assert "contract_version" in accountability_to_json(result)
