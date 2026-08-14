from scm_ontology.claim import Claim


def test_reference_valued_claim_can_correspond_to_relationship_proposition() -> None:
    claim = Claim(
        claim_id="C1",
        subject_id="Order-001",
        predicate="supplied_by",
        object_value="Supplier-A",
    )

    assert (claim.subject_id, claim.predicate, claim.object_value) == (
        "Order-001",
        "supplied_by",
        "Supplier-A",
    )


def test_literal_valued_claim_does_not_imply_relationship() -> None:
    claim = Claim(
        claim_id="C2",
        subject_id="Shipment-001",
        predicate="has_status",
        object_value="delivered",
    )

    assert claim.object_value == "delivered"


def test_claim_correspondence_does_not_create_relationship_identity() -> None:
    claim = Claim(
        claim_id="C3",
        subject_id="Order-001",
        predicate="supplied_by",
        object_value="Supplier-A",
    )

    assert claim.claim_id == "C3"
    assert not hasattr(claim, "relationship_id")
