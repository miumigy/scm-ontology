import pytest

from scm_ontology.observation_provenance_contract import (
    ObservationProvenanceContractError,
    validate_source_ref,
)


def test_accepts_non_empty_source_ref():
    assert validate_source_ref("erp://sap/stock/123") == "erp://sap/stock/123"


def test_rejects_blank_source_ref():
    with pytest.raises(ObservationProvenanceContractError, match="source_ref is required"):
        validate_source_ref("   ")


def test_rejects_non_string_source_ref():
    with pytest.raises(ObservationProvenanceContractError, match="must be a string"):
        validate_source_ref(123)
