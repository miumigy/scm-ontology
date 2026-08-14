"""Cross-entity semantic validation for canonical SCM relationships."""
from __future__ import annotations

from dataclasses import dataclass

from .ontology_linter import ValidationIssue, ValidationResult, ValidationSeverity
from .relationship_identity import RelationshipInstance


@dataclass(frozen=True)
class SemanticNode:
    """A minimal semantic node reference used for cross-entity validation."""

    node_id: str
    node_type: str


@dataclass(frozen=True)
class SemanticGraph:
    """Minimal cross-entity semantic context.

    The model deliberately does not define persistence, graph storage, or a
    closed-world entity registry.
    """

    nodes: tuple[SemanticNode, ...]
    relationships: tuple[RelationshipInstance, ...] = ()


def validate_cross_entity(graph: SemanticGraph) -> ValidationResult:
    """Validate cross-entity consistency available in a semantic graph.

    The first S48 rules are intentionally small:
    - relationship endpoints should resolve when their nodes are present;
    - one node identifier must not be assigned conflicting semantic types;
    - relationship identifiers must identify only one relationship instance.

    Missing nodes are warnings rather than errors because a canonical graph may
    legitimately be a partial view of a larger enterprise semantic graph.
    """

    issues: list[ValidationIssue] = []

    node_types: dict[str, str] = {}
    for node in graph.nodes:
        if not node.node_id.strip():
            issues.append(
                ValidationIssue(
                    "INVALID_NODE_ID",
                    ValidationSeverity.ERROR,
                    "node identifier must be non-empty",
                )
            )
            continue
        if not node.node_type.strip():
            issues.append(
                ValidationIssue(
                    "INVALID_NODE_TYPE",
                    ValidationSeverity.ERROR,
                    f"node {node.node_id!r} has an empty semantic type",
                )
            )
            continue

        previous_type = node_types.get(node.node_id)
        if previous_type is not None and previous_type != node.node_type:
            issues.append(
                ValidationIssue(
                    "ENTITY_TYPE_CONFLICT",
                    ValidationSeverity.ERROR,
                    f"node {node.node_id!r} has conflicting semantic types: "
                    f"{previous_type} vs {node.node_type}",
                )
            )
        else:
            node_types[node.node_id] = node.node_type

    seen_relationships: dict[str, RelationshipInstance] = {}
    for relationship in graph.relationships:
        previous = seen_relationships.get(relationship.relationship_id)
        if previous is not None and previous != relationship:
            issues.append(
                ValidationIssue(
                    "RELATIONSHIP_IDENTITY_CONFLICT",
                    ValidationSeverity.ERROR,
                    f"relationship_id {relationship.relationship_id!r} identifies conflicting relationships",
                )
            )
        else:
            seen_relationships[relationship.relationship_id] = relationship

        for endpoint_id in relationship.endpoints():
            if endpoint_id not in node_types:
                issues.append(
                    ValidationIssue(
                        "UNRESOLVED_ENDPOINT",
                        ValidationSeverity.WARNING,
                        f"relationship endpoint is not resolved in this graph: {endpoint_id}",
                    )
                )

    return ValidationResult(tuple(issues))


def is_semantic_graph(value: object) -> bool:
    return isinstance(value, SemanticGraph)
