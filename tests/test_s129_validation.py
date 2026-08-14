from scm_ontology.s129_validation import SemanticModelValidator


def test_valid_canonical_document_passes() -> None:
    document = {
        "concepts": [
            {"name": "Inventory", "category": "core"},
            {"name": "ServiceLevel", "category": "derived", "derived_from": ["Inventory"]},
            {"name": "Decision", "category": "core"},
            {"name": "Action", "category": "core"},
        ],
        "relationships": [
            {"source": "Decision", "target": "Action", "predicate": "results_in"},
        ],
    }
    assert SemanticModelValidator().is_valid(document)


def test_forbidden_semantic_conflation_is_rejected() -> None:
    document = {
        "concepts": [
            {"name": "Measurement", "category": "core"},
            {"name": "Metric", "category": "core"},
        ],
        "relationships": [
            {"source": "Measurement", "target": "Metric", "predicate": "equals"},
        ],
    }
    result = SemanticModelValidator().validate(document)
    assert any(issue.code == "SEMANTIC_CONFLATION" for issue in result.issues)


def test_derived_concept_must_be_explicit() -> None:
    document = {
        "concepts": [
            {"name": "InventoryTurns", "category": "core", "derived_from": ["Inventory"]},
        ],
        "relationships": [],
    }
    result = SemanticModelValidator().validate(document)
    assert any(issue.code == "DERIVATION_CATEGORY_MISMATCH" for issue in result.issues)


def test_primitive_operational_concept_cannot_be_derived() -> None:
    document = {
        "concepts": [{"name": "Inventory", "category": "derived"}],
        "relationships": [],
    }
    result = SemanticModelValidator().validate(document)
    assert any(issue.code == "PRIMITIVE_DERIVED_MISMATCH" for issue in result.issues)
