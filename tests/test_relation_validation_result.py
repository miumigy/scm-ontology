from scm_ontology.relation_validation_result import ValidationStatus, validation_result


def test_valid_relation_passes() -> None:
    result = validation_result("fulfills", domain_ok=True, range_ok=True)
    assert result.status is ValidationStatus.PASS
    assert result.valid


def test_type_mismatch_requires_review() -> None:
    result = validation_result("fulfills", domain_ok=False, range_ok=True)
    assert result.status is ValidationStatus.REVIEW
    assert not result.valid


def test_unknown_predicate_is_extension_not_false_fact() -> None:
    result = validation_result("customer_specific_relation", domain_ok=False, range_ok=False, known_predicate=False)
    assert result.status is ValidationStatus.EXTENSION
