from scm_ontology.validation import OntologyValidator


def test_valid_document_passes() -> None:
    doc = {
        "concepts": [
            {"name": "Inventory", "layer": "core", "dimension": "physical", "attributes": [
                {"name": "id", "value_type": "Identifier", "role": "identity", "cardinality": "1"},
                {"name": "quantity", "value_type": "Quantity", "role": "measure", "cardinality": "1"},
            ]},
            {"name": "Measurement", "layer": "core", "dimension": "information", "attributes": []},
        ],
        "relationships": [{"predicate": "measured_by", "source": "Inventory", "target": "Measurement", "category": "informational"}],
    }
    assert OntologyValidator().is_valid(doc)


def test_unknown_endpoint_is_rejected() -> None:
    doc = {"concepts": [{"name": "Inventory", "layer": "core", "dimension": "physical"}], "relationships": [{"predicate": "contains", "source": "Warehouse", "target": "Inventory", "category": "physical"}]}
    issues = OntologyValidator().validate(doc)
    assert any(i.code == "UNKNOWN_RELATION_ENDPOINT" for i in issues)


def test_duplicate_concept_is_rejected() -> None:
    doc = {"concepts": [{"name": "Inventory", "layer": "core", "dimension": "physical"}, {"name": "Inventory", "layer": "core", "dimension": "physical"}], "relationships": []}
    assert any(i.code == "DUPLICATE_CONCEPT" for i in OntologyValidator().validate(doc))


def test_identity_attribute_requires_identity_semantics() -> None:
    doc = {"concepts": [{"name": "Order", "layer": "core", "dimension": "information", "attributes": [{"name": "id", "value_type": "String", "role": "identity", "cardinality": "1"}]}], "relationships": []}
    assert any(i.code == "IDENTITY_TYPE_MISMATCH" for i in OntologyValidator().validate(doc))
