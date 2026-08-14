from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    path: str


class OntologyValidator:
    """Validate semantic consistency beyond JSON Schema structure."""

    def validate(self, document: dict[str, Any]) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        concepts = document.get("concepts", [])
        relationships = document.get("relationships", [])
        concept_names = [c.get("name") for c in concepts]
        concept_set = {n for n in concept_names if n}

        for i, name in enumerate(concept_names):
            if not name:
                issues.append(ValidationIssue("CONCEPT_NAME_REQUIRED", "Concept name is required.", f"concepts[{i}].name"))
            if concept_names.count(name) > 1:
                issues.append(ValidationIssue("DUPLICATE_CONCEPT", f"Concept '{name}' is declared more than once.", f"concepts[{i}].name"))

        for i, concept in enumerate(concepts):
            for j, attr in enumerate(concept.get("attributes", [])):
                role = attr.get("role")
                value_type = attr.get("value_type")
                if role == "identity" and value_type not in {"Identifier", "Reference", "CanonicalReference"}:
                    issues.append(ValidationIssue("IDENTITY_TYPE_MISMATCH", "Identity attributes must use identifier/reference semantics.", f"concepts[{i}].attributes[{j}]"))
                if role == "measure" and value_type in {"String", "Boolean"}:
                    issues.append(ValidationIssue("MEASURE_TYPE_MISMATCH", "Measure attributes should not use String or Boolean value types.", f"concepts[{i}].attributes[{j}]"))

        seen_relationships: set[tuple[str, str, str]] = set()
        for i, rel in enumerate(relationships):
            source, target, predicate = rel.get("source"), rel.get("target"), rel.get("predicate")
            for endpoint, value in (("source", source), ("target", target)):
                if value not in concept_set:
                    issues.append(ValidationIssue("UNKNOWN_RELATION_ENDPOINT", f"Relationship {endpoint} '{value}' is not a declared concept.", f"relationships[{i}].{endpoint}"))
            key = (str(source), str(predicate), str(target))
            if key in seen_relationships:
                issues.append(ValidationIssue("DUPLICATE_RELATIONSHIP", f"Relationship '{predicate}' is duplicated for {source} -> {target}.", f"relationships[{i}]"))
            seen_relationships.add(key)

        return issues

    def is_valid(self, document: dict[str, Any]) -> bool:
        return not self.validate(document)
