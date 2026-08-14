from scm_ontology.claim import Claim


def test_claim_subject_is_an_opaque_reference():
    claim = Claim("C1", "Shipment-001", "has_status", "delivered")
    assert claim.subject_id == "Shipment-001"


def test_claim_subject_accepts_uri_like_reference_without_uri_semantics():
    claim = Claim("C2", "erp://shipment/001", "has_status", "delivered")
    assert claim.subject_id == "erp://shipment/001"


def test_claim_subject_accepts_domain_specific_reference():
    claim = Claim("C3", "enterprise-specific-subject", "has_status", "delivered")
    assert claim.subject_id == "enterprise-specific-subject"


def test_claim_subject_has_no_literal_value_form():
    claim = Claim("C4", "S4", "quantity", 100)
    assert isinstance(claim.subject_id, str)
    assert claim.subject_id != 100
