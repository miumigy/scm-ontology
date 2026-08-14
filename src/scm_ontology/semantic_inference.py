"""Minimal canonical semantic inference over explicit SCM Graph facts.

This module defines inference as a semantic rule boundary, not as an LLM,
graph database, query language, or domain-specific reasoning engine.
"""
from __future__ import annotations

from dataclasses import dataclass

from .canonical_graph import CanonicalRelationship, SemanticNode
from .scm_graph import SCMGraph


class SemanticInferenceError(ValueError):
    """Raised when an inference rule is structurally invalid."""


@dataclass(frozen=True)
class RelationshipPattern:
    """Minimal pattern describing one explicit relationship fact."""

    predicate: str
    from_type: str | None = None
    to_type: str | None = None


@dataclass(frozen=True)
class InferenceRule:
    """A deterministic two-hop semantic composition rule."""

    rule_id: str
    antecedent: tuple[RelationshipPattern, RelationshipPattern]
    conclusion_predicate: str

    def __post_init__(self) -> None:
        if not self.rule_id.strip():
            raise SemanticInferenceError("rule_id must be non-empty")
        if not self.conclusion_predicate.strip():
            raise SemanticInferenceError("conclusion_predicate must be non-empty")


@dataclass(frozen=True)
class DerivedRelationship:
    """A fact derived from explicit relationships with provenance."""

    from_id: str
    predicate: str
    to_id: str
    rule_id: str
    source_relationship_ids: tuple[str, ...]


def _matches(
    relationship: CanonicalRelationship,
    pattern: RelationshipPattern,
    nodes: dict[str, SemanticNode],
) -> bool:
    instance = relationship.instance
    if instance.predicate != pattern.predicate:
        return False
    from_node = nodes.get(instance.from_id)
    to_node = nodes.get(instance.to_id)
    if from_node is None or to_node is None:
        return False
    if pattern.from_type is not None and from_node.node_type != pattern.from_type:
        return False
    if pattern.to_type is not None and to_node.node_type != pattern.to_type:
        return False
    return True


def infer(graph: SCMGraph, rule: InferenceRule) -> tuple[DerivedRelationship, ...]:
    """Derive explicit semantic facts from a two-hop relationship pattern.

    The engine only derives facts that have two matching explicit antecedents
    sharing an endpoint. It does not recursively consume its own output.
    """
    nodes = {node.node_id: node for node in graph.canonical.nodes}
    first_pattern, second_pattern = rule.antecedent
    first_matches = tuple(
        rel
        for rel in graph.canonical.relationships
        if _matches(rel, first_pattern, nodes)
    )
    second_matches = tuple(
        rel
        for rel in graph.canonical.relationships
        if _matches(rel, second_pattern, nodes)
    )

    derived: list[DerivedRelationship] = []
    for first in first_matches:
        for second in second_matches:
            if first.instance.to_id != second.instance.from_id:
                continue
            derived.append(
                DerivedRelationship(
                    from_id=first.instance.from_id,
                    predicate=rule.conclusion_predicate,
                    to_id=second.instance.to_id,
                    rule_id=rule.rule_id,
                    source_relationship_ids=(
                        first.instance.relationship_id,
                        second.instance.relationship_id,
                    ),
                )
            )
    return tuple(derived)
