from scm_ontology.evidence import EvidenceReference


def test_evidence_reference_is_canonical_source_reference():
    evidence = EvidenceReference("E1", "erp_record", "record://erp/order/1")
    assert evidence.evidence_id == "E1"
    assert evidence.evidence_type == "erp_record"
    assert evidence.reference == "record://erp/order/1"


def test_empty_fields_are_rejected():
    for kwargs in (
        {"evidence_id": "", "evidence_type": "record", "reference": "r"},
        {"evidence_id": "E1", "evidence_type": "", "reference": "r"},
        {"evidence_id": "E1", "evidence_type": "record", "reference": ""},
    ):
        try:
            EvidenceReference(**kwargs)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")


def test_evidence_reference_has_no_quality_or_trust_semantics():
    evidence = EvidenceReference("E1", "document", "doc://1")
    assert not hasattr(evidence, "confidence")
    assert not hasattr(evidence, "trust_score")
