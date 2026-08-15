from __future__ import annotations

from dataclasses import dataclass

from .canonical_graph import CanonicalGraph
from .reasoning_result import ReasoningResult
from .reasoning_query import NodeQuery, query_nodes


class ReasoningRoundTripError(ValueError):
    pass


@dataclass(frozen=True)
class ReasoningRoundTrip:
    query: NodeQuery
    result: ReasoningResult


def validate_reasoning_round_trip(
    graph: CanonicalGraph,
    round_trip: ReasoningRoundTrip,
) -> None:
    """Validate that a reasoning result only references nodes selected by its query."""
    selected = {node.node_id for node in query_nodes(graph, round_trip.query)}
    unknown = set(round_trip.result.matches) - selected
    if unknown:
        raise ReasoningRoundTripError(
            f"reasoning result references nodes outside query scope: {sorted(unknown)}"
        )
