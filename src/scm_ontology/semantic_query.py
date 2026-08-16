"""Semantic, read-only queries over the canonical SCM Graph."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .canonical_graph import CanonicalRelationship, SemanticNode
from .scm_graph import SCMGraph
from .temporal_query import _contains
from .temporal_traversal import TemporalPath, supply_chain_paths_at


@dataclass(frozen=True)
class NodeMatch:
    node: SemanticNode


@dataclass(frozen=True)
class RelationshipMatch:
    relationship: CanonicalRelationship


@dataclass(frozen=True)
class SemanticPathStep:
    relationship_id: str
    predicate: str
    from_id: str
    to_id: str
    qualifiers: dict[str, Any]


@dataclass(frozen=True)
class SemanticSupplyChainPath:
    at: str
    node_ids: tuple[str, ...]
    steps: tuple[SemanticPathStep, ...]


class SemanticQuery:
    """Read-only query facade; it retrieves graph facts without inference."""

    def __init__(self, graph: SCMGraph) -> None:
        self._graph = graph

    def nodes(self, *, node_type: str | None = None) -> tuple[NodeMatch, ...]:
        return tuple(NodeMatch(node) for node in self._graph.canonical.nodes if node_type is None or node.node_type == node_type)

    def relationships(self, *, predicate: str | None = None, from_id: str | None = None, to_id: str | None = None) -> tuple[RelationshipMatch, ...]:
        return tuple(
            RelationshipMatch(rel)
            for rel in self._graph.canonical.relationships
            if (predicate is None or rel.instance.predicate == predicate)
            and (from_id is None or rel.instance.from_id == from_id)
            and (to_id is None or rel.instance.to_id == to_id)
        )

    def neighbors(self, node_id: str, *, predicate: str | None = None, direction: str = "out") -> tuple[NodeMatch, ...]:
        return tuple(NodeMatch(node) for node in self._graph.related(node_id, predicate=predicate, direction=direction))

    def fact_count(self) -> int:
        return len(self._graph.canonical.nodes) + len(self._graph.canonical.relationships)


def _step_index(graph: Any, at: datetime) -> dict[str, SemanticPathStep]:
    result: dict[str, SemanticPathStep] = {}
    for rel in graph.relationships:
        for version in rel.versions:
            if _contains(version, at):
                result[rel.instance.relationship_id] = SemanticPathStep(
                    rel.instance.relationship_id, rel.instance.predicate,
                    rel.instance.from_id, rel.instance.to_id,
                    dict(version.qualifiers or {}),
                )
                break
    return result


def _enrich(graph: Any, paths: tuple[TemporalPath, ...], at: str) -> tuple[SemanticSupplyChainPath, ...]:
    instant = datetime.fromisoformat(at.replace("Z", "+00:00"))
    index = _step_index(graph, instant)
    return tuple(
        SemanticSupplyChainPath(at, path.node_ids, tuple(index[rid] for rid in path.relationship_ids))
        for path in paths
    )


def semantic_supply_chain_paths(graph: Any, at: str, *, from_id: str, to_id: str, predicates: set[str] | None = None, max_hops: int = 8) -> tuple[SemanticSupplyChainPath, ...]:
    """Return temporal paths enriched with predicate and version qualifiers."""
    paths = supply_chain_paths_at(graph, at, from_id=from_id, to_id=to_id, predicates=predicates, max_hops=max_hops)
    return _enrich(graph, paths, at)
