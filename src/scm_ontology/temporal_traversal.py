"""Temporal supply-chain traversal over the transport-neutral CanonicalGraph."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .canonical_graph import CanonicalGraph
from .temporal_query import _contains


@dataclass(frozen=True)
class TemporalPath:
    node_ids: tuple[str, ...]
    relationship_ids: tuple[str, ...]


def supply_chain_paths_at(
    graph: CanonicalGraph,
    at: str,
    *,
    from_id: str,
    to_id: str,
    predicates: set[str] | None = None,
    max_hops: int = 8,
) -> tuple[TemporalPath, ...]:
    """Find deterministic simple paths whose relationship versions are valid at an instant."""
    instant = datetime.fromisoformat(at.replace("Z", "+00:00"))
    adjacency: dict[str, list[tuple[str, str, str]]] = {}
    for rel in graph.relationships:
        if predicates is not None and rel.instance.predicate not in predicates:
            continue
        for version in rel.versions:
            if _contains(version, instant):
                adjacency.setdefault(rel.instance.from_id, []).append(
                    (rel.instance.to_id, rel.instance.relationship_id, rel.instance.predicate)
                )
                break
    for edges in adjacency.values():
        edges.sort(key=lambda item: (item[0], item[1], item[2]))

    paths: list[TemporalPath] = []

    def visit(node: str, nodes: tuple[str, ...], relationships: tuple[str, ...]) -> None:
        if node == to_id:
            paths.append(TemporalPath(nodes, relationships))
            return
        if len(relationships) >= max_hops:
            return
        for next_node, relationship_id, _ in adjacency.get(node, []):
            if next_node in nodes:
                continue
            visit(next_node, nodes + (next_node,), relationships + (relationship_id,))

    visit(from_id, (from_id,), ())
    return tuple(paths)
