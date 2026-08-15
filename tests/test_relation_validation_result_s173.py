from scm_ontology.relation_validation_result import ValidationStatus, validation_result


def test_validation_result_preserves_instance_types() -> None:
    result = validation_result(
        "fulfills",
        domain_ok=True,
        range_ok=True,
        subject_type="Supply",
        object_type="Demand",
    )
    assert result.status is ValidationStatus.PASS
    assert result.subject_type == "Supply"
    assert result.object_type == "Demand"
    assert result.domain_ok is True
    assert result.range_ok is True


def test_review_result_exposes_failed_side() -> None:
    result = validation_result(
        "fulfills",
        domain_ok=False,
        range_ok=True,
        subject_type="Location",
        object_type="Demand",
    )
    assert result.status is ValidationStatus.REVIEW
    assert result.domain_ok is False
    assert result.range_ok is True
