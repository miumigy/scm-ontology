from scm_ontology.claim_evidence import ClaimEvidenceRelationship


def test_supports_is_an_evidence_role_predicate() -> None:
    relationship = ClaimEvidenceRelationship("R1", "C1", "supports", "E1")

    assert relationship.predicate == "supports"


def test_contradicts_is_an_evidence_role_predicate() -> None:
    relationship = ClaimEvidenceRelationship("R2", "C1", "contradicts", "E2")

    assert relationship.predicate == "contradicts"


def test_evidence_role_vocabulary_remains_open() -> None:
    relationship = ClaimEvidenceRelationship(
        "R3", "C1", "enterprise_specific_evidence_role", "E3"
    )

    assert relationship.predicate == "enterprise_specific_evidence_role"
