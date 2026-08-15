import pytest

from scm_ontology.subtype_validation import (
    SubtypeValidationError,
    validate_subtype_compatible_relation,
)


def test_facility_is_compatible_with_location_range() -> None:
    validate_subtype_compatible_relation("located_at", "PhysicalEntity", "Facility")


def test_kpi_is_compatible_with_metric_range() -> None:
    validate_subtype_compatible_relation("evaluated_by", "Entity", "KPI")


def test_unrelated_type_is_rejected() -> None:
    with pytest.raises(SubtypeValidationError):
        validate_subtype_compatible_relation("located_at", "Order", "Facility")


def test_unknown_type_is_not_coerced() -> None:
    with pytest.raises(SubtypeValidationError):
        validate_subtype_compatible_relation("located_at", "PhysicalEntity", "CustomerSpecificLocation")
