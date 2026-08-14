from __future__ import annotations

from dataclasses import dataclass

from .canonical_model import ConceptLayer, RelationshipCategory, WorldLayer


@dataclass(frozen=True)
class SchemaConcept:
    """Minimal serialization-neutral representation of a canonical concept."""

    name: str
    layer: ConceptLayer
    worlds: tuple[WorldLayer, ...]
    description: str
    abstract: bool = False


@dataclass(frozen=True)
class SchemaRelationship:
    """Minimal serialization-neutral representation of a canonical relationship."""

    predicate: str
    source: str
    target: str
    category: RelationshipCategory


@dataclass(frozen=True)
class CoreSchemaDocument:
    """Serialization-neutral document contract for the canonical model."""

    version: str
    concepts: tuple[SchemaConcept, ...]
    relationships: tuple[SchemaRelationship, ...]

    def __post_init__(self) -> None:
        if not self.version:
            raise ValueError("version is required")
        concept_names = [concept.name for concept in self.concepts]
        if len(concept_names) != len(set(concept_names)):
            raise ValueError("concept names must be unique")
        predicates = [relationship.predicate for relationship in self.relationships]
        if len(predicates) != len(set(predicates)):
            raise ValueError("relationship predicates must be unique")
        known = set(concept_names)
        for relationship in self.relationships:
            if relationship.source not in known or relationship.target not in known:
                raise ValueError("relationship endpoints must resolve to concepts")


def schema_from_registry(version: str = "0.1") -> CoreSchemaDocument:
    """Build the neutral schema contract from the canonical registry."""
    from .canonical_model import CANONICAL_CONCEPTS, CANONICAL_RELATIONSHIPS

    return CoreSchemaDocument(
        version=version,
        concepts=tuple(
            SchemaConcept(
                name=concept.name,
                layer=concept.layer,
                worlds=concept.worlds,
                description=concept.description,
                abstract=concept.abstract,
            )
            for concept in CANONICAL_CONCEPTS
        ),
        relationships=tuple(
            SchemaRelationship(
                predicate=relationship.predicate,
                source=relationship.source,
                target=relationship.target,
                category=relationship.category,
            )
            for relationship in CANONICAL_RELATIONSHIPS
        ),
    )
