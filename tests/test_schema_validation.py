from dataclasses import replace

from scm_ontology.schema_contract import schema_from_registry
from scm_ontology.schema_validation import assert_core_schema_valid, validate_core_schema


def test_canonical_schema_passes_integration_validation() -> None:
    document = schema_from_registry()
    assert validate_core_schema(document) == ()
    assert_core_schema_valid(document)


def test_registry_drift_is_detected() -> None:
    document = schema_from_registry()
    altered = replace(document, concepts=document.concepts[:-1])
    issues = validate_core_schema(altered)
    assert any(issue.code == "REG001" for issue in issues)


def test_relationship_endpoint_drift_is_detected() -> None:
    document = schema_from_registry()
    relation = document.relationships[0]
    altered_relation = replace(relation, source="MissingConcept")
    altered = replace(document, relationships=(altered_relation, *document.relationships[1:]))
    issues = validate_core_schema(altered)
    assert any(issue.code == "REL001" for issue in issues)
