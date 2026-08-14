from scm_ontology.claim_evidence import ClaimEvidenceRelationship


def test_claim_evidence_relationship_is_first_class():
    link = ClaimEvidenceRelationship("R1", "C1", "supported_by", "E1")
    assert link.relationship_id == "R1"
    assert link.claim_id == "C1"
    assert link.predicate == "supported_by"
    assert link.evidence_id == "E1"


def test_claim_evidence_predicate_is_open():
    link = ClaimEvidenceRelationship("R1", "C1", "corroborated_by", "E1")
    assert link.predicate == "corroborated_by"


def test_empty_endpoint_is_rejected():
    try:
        ClaimEvidenceRelationship("R1", "", "supported_by", "E1")
    except ValueError as exc:
        assert "claim_id" in str(exc)
    else:
        raise AssertionError("expected ValueError")
