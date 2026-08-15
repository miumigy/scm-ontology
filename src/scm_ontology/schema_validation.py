from __future__ import annotations

from dataclasses import dataclass

from .canonical_model import CANONICAL_CONCEPTS, CANONICAL_RELATIONSHIPS, ConceptLayer
from .schema_contract import CoreSchemaDocument, schema_from_registry


@dataclass(frozen=True)
class SchemaIssue:
    code: str
    message: str
    subject: str


def validate_core_schema(document: CoreSchemaDocument | None = None) -> tuple[SchemaIssue, ...]:
    """Validate cross-layer invariants of the canonical schema.

    This validator checks integration invariants rather than business rules.
    """
    document = document or schema_from_registry()
    issues: list[SchemaIssue] = []
    concept_names = {concept.name for concept in document.concepts}

    for relation in document.relationships:
        if relation.source not in concept_names:
            issues.append(SchemaIssue("REL001", "unknown relationship source", relation.predicate))
        if relation.target not in concept_names:
            issues.append(SchemaIssue("REL002", "unknown relationship target", relation.predicate))

    for concept in document.concepts:
        if concept.layer is ConceptLayer.DERIVED and concept.name in {"Inventory", "Demand", "Supply", "Capacity"}:
            issues.append(SchemaIssue("LAYER001", "operational primitive/core concept classified as derived", concept.name))

    # The registry itself must remain the source of truth for this contract.
    if {concept.name for concept in document.concepts} != {concept.name for concept in CANONICAL_CONCEPTS}:
        issues.append(SchemaIssue("REG001", "schema concept set diverges from canonical registry", "CoreSchemaDocument"))
    if {relation.predicate for relation in document.relationships} != {relation.predicate for relation in CANONICAL_RELATIONSHIPS}:
        issues.append(SchemaIssue("REG002", "schema relationship set diverges from canonical registry", "CoreSchemaDocument"))

    return tuple(issues)


def assert_core_schema_valid(document: CoreSchemaDocument | None = None) -> None:
    issues = validate_core_schema(document)
    if issues:
        details = "; ".join(f"{issue.code}: {issue.subject} — {issue.message}" for issue in issues)
        raise ValueError(f"invalid canonical schema: {details}")
