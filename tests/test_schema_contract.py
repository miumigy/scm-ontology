import pytest

from scm_ontology.canonical_model import ConceptLayer, RelationshipCategory, WorldLayer
from scm_ontology.schema_contract import (
    CoreSchemaDocument,
    SchemaConcept,
    SchemaRelationship,
    schema_from_registry,
)


def test_registry_can_be_materialized_as_schema_contract() -> None:
    document = schema_from_registry()
    assert document.version == "0.1"
    assert document.concepts
    assert document.relationships
    assert all(relation.source for relation in document.relationships)
    assert all(relation.target for relation in document.relationships)


def test_schema_preserves_derived_layer() -> None:
    document = schema_from_registry()
    kpi = next(concept for concept in document.concepts if concept.name == "KPI")
    assert kpi.layer is ConceptLayer.DERIVED


def test_schema_preserves_world_classification() -> None:
    document = schema_from_registry()
    action = next(concept for concept in document.concepts if concept.name == "Action")
    assert WorldLayer.DECISION in action.worlds
    assert WorldLayer.PHYSICAL in action.worlds


def test_duplicate_concepts_are_rejected() -> None:
    concept = SchemaConcept("Entity", ConceptLayer.PRIMITIVE, (WorldLayer.SEMANTIC,), "x")
    with pytest.raises(ValueError, match="concept names"):
        CoreSchemaDocument("0.1", (concept, concept), ())


def test_duplicate_predicates_are_rejected() -> None:
    concepts = (
        SchemaConcept("A", ConceptLayer.CORE, (WorldLayer.SEMANTIC,), "a"),
        SchemaConcept("B", ConceptLayer.CORE, (WorldLayer.SEMANTIC,), "b"),
    )
    relation = SchemaRelationship("rel", "A", "B", RelationshipCategory.STRUCTURAL)
    with pytest.raises(ValueError, match="relationship predicates"):
        CoreSchemaDocument("0.1", concepts, (relation, relation))


def test_unresolved_relationship_endpoint_is_rejected() -> None:
    concepts = (SchemaConcept("A", ConceptLayer.CORE, (WorldLayer.SEMANTIC,), "a"),)
    relation = SchemaRelationship("rel", "A", "Missing", RelationshipCategory.STRUCTURAL)
    with pytest.raises(ValueError, match="endpoints"):
        CoreSchemaDocument("0.1", concepts, (relation,))
