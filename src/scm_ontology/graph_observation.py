"""Convert graph query results into governed decision observations.

S339 is an adapter boundary: graph retrieval is not itself a decision. The
adapter preserves the existing DecisionObservation contract and carries
query/provenance identifiers without inference or graph mutation.
"""
from __future__ import annotations

from typing import Any

from .decision_context import DecisionObservation
from .graph_query import GraphQueryResult


def graph_query_to_observation(
    result: GraphQueryResult,
    *,
    question_id: str,
    query_id: str,
) -> DecisionObservation:
    """Turn a graph query result into an existing DecisionObservation.

    The value is a canonical, deterministic mapping of the query result;
    evidence and provenance are carried through without interpretation.
    """
    if not question_id.strip():
        raise ValueError("question_id must be non-empty")
    if not query_id.strip():
        raise ValueError("query_id must be non-empty")

    value: dict[str, Any] = result.to_mapping()
    evidence_ids = tuple(
        node.node_id for node in result.nodes
    )
    return DecisionObservation(
        question_id=question_id,
        value={"query_id": query_id, "result": value},
        evidence_ids=evidence_ids,
        provenance_ids=result.provenance_ids,
    )
