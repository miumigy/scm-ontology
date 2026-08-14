from scm_ontology.claim import Claim


def test_claim_uses_canonical_predicate_semantics() -> None:
    claim = Claim(
        claim_id="C1",
        subject_id="Order-001",
        predicate="supplies",
        object_value="Supplier-A",
    )

    assert claim.predicate == "supplies"


def test_claim_predicate_remains_open_vocabulary() -> None:
    claim = Claim(
        claim_id="C2",
        subject_id="Shipment-001",
        predicate="enterprise_specific_status",
        object_value="delivered",
    )

    assert claim.predicate == "enterprise_specific_status"


def test_claim_predicate_does_not_determine_object_form() -> None:
    reference_claim = Claim(
        claim_id="C3",
        subject_id="Order-001",
        predicate="supplied_by",
        object_value="Supplier-A",
    )
    value_claim = Claim(
        claim_id="C4",
        subject_id="Shipment-001",
        predicate="has_status",
        object_value="delivered",
    )

    assert reference_claim.predicate == "supplied_by"
    assert value_claim.predicate == "has_status"
