from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .canonical_model import ConceptLayer, RelationshipCategory, WorldLayer

@dataclass(frozen=True)
class SchemaConcept:
    name: str
    layer: ConceptLayer
    worlds: tuple[WorldLayer, ...]
    description: str
    abstract: bool = False

@dataclass(frozen=True)
class SchemaRelationship:
    predicate: str
    source: str
    target: str
    category: RelationshipCategory

@dataclass(frozen=True)
class CoreSchemaDocument:
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
    from .canonical_model import CANONICAL_CONCEPTS, CANONICAL_RELATIONSHIPS
    return CoreSchemaDocument(
        version=version,
        concepts=tuple(SchemaConcept(concept.name, concept.layer, concept.worlds, concept.description, concept.abstract) for concept in CANONICAL_CONCEPTS),
        relationships=tuple(SchemaRelationship(relationship.predicate, relationship.source, relationship.target, relationship.category) for relationship in CANONICAL_RELATIONSHIPS),
    )

TRACE_BUNDLE_SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas" / "trace-bundle.schema.json"

def load_trace_bundle_schema() -> dict[str, Any]:
    return json.loads(TRACE_BUNDLE_SCHEMA_PATH.read_text(encoding="utf-8"))

def validate_trace_bundle_document(document: dict[str, Any]) -> tuple[str, ...]:
    """Validate against constraints loaded from the published schema."""
    schema = load_trace_bundle_schema()
    errors: list[str] = []
    if document.get("$schema") != schema["properties"]["$schema"]["const"]:
        errors.append("$schema does not match published contract")
    if document.get("schema_version") != schema["properties"]["schema_version"]["const"]:
        errors.append("schema_version does not match published contract")
    bundle = document.get("bundle")
    if not isinstance(bundle, dict):
        errors.append("bundle must be an object")
        return tuple(errors)
    for key in schema["properties"]["bundle"]["required"]:
        if key not in bundle:
            errors.append(f"bundle missing required property: {key}")
    validation = bundle.get("validation")
    if isinstance(validation, dict):
        if validation.get("valid") is not True:
            errors.append("validation.valid must be true")
        if validation.get("errors") != []:
            errors.append("validation.errors must be empty")
    return tuple(errors)
