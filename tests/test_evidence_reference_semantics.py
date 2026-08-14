"""Tests for S70 EvidenceReference reference semantics."""

from scm_ontology.evidence import EvidenceReference


def test_reference_may_point_to_a_canonical_observation_id():
    evidence = EvidenceReference("E1", "observation", "O1")
    assert evidence.reference == "O1"


def test_reference_may_be_an_external_opaque_reference():
    evidence = EvidenceReference("E2", "erp_record", "record://erp/order/1")
    assert evidence.reference == "record://erp/order/1"


def test_reference_is_not_interpreted_by_evidence_reference():
    evidence = EvidenceReference("E3", "document", "https://example.invalid/doc/123")
    assert evidence.reference == "https://example.invalid/doc/123"
    assert not hasattr(evidence, "uri")
    assert not hasattr(evidence, "target_type")


def test_reference_semantics_do_not_close_evidence_types():
    evidence = EvidenceReference("E4", "custom_enterprise_source", "source-42")
    assert evidence.evidence_type == "custom_enterprise_source"
    assert evidence.reference == "source-42"
