import pytest

from scm_ontology.claim import Claim


def test_claim_represents_a_semantic_statement():
    claim = Claim(
        claim_id="C1",
        subject_id="SHP-001",
        predicate="has_status",
        object_value="delivered",
    )
    assert claim.claim_id == "C1"
    assert claim.subject_id == "SHP-001"
    assert claim.predicate == "has_status"
    assert claim.object_value == "delivered"


def test_claim_can_reference_an_entity_as_object():
    claim = Claim("C2", "ORD-001", "supplied_by", "SUP-001")
    assert claim.object_value == "SUP-001"


@pytest.mark.parametrize("kwargs, field", [
    ({"claim_id": "", "subject_id": "S", "predicate": "p", "object_value": "o"}, "claim_id"),
    ({"claim_id": "C", "subject_id": "", "predicate": "p", "object_value": "o"}, "subject_id"),
    ({"claim_id": "C", "subject_id": "S", "predicate": "", "object_value": "o"}, "predicate"),
])
def test_claim_rejects_missing_identity_or_statement_parts(kwargs, field):
    with pytest.raises(ValueError, match=field):
        Claim(**kwargs)


def test_claim_does_not_become_fact_or_evaluator():
    claim = Claim("C1", "S1", "p", "o")
    assert not hasattr(claim, "evaluate")
    assert not hasattr(claim, "derive")
    assert not hasattr(claim, "confidence")
