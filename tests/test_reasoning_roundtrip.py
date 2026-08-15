import pytest

from scm_ontology.canonical_graph import CanonicalGraph, SemanticNode
from scm_ontology.reasoning_query import NodeQuery
from scm_ontology.reasoning_result import ReasoningResult
from scm_ontology.reasoning_roundtrip import (
    ReasoningRoundTrip,
    ReasoningRoundTripError,
    validate_reasoning_round_trip,
)


def test_reasoning_result_must_stay_within_query_scope() -> None:
    graph = CanonicalGraph(
        nodes=(
            SemanticNode("product:1", "Product"),
            SemanticNode("site:1", "Site"),
        )
    )
    round_trip = ReasoningRoundTrip(
        NodeQuery(node_type="Product"),
        ReasoningResult("result:1", "matched", ("product:1",)),
    )
    validate_reasoning_round_trip(graph, round_trip)


def test_reasoning_result_rejects_out_of_scope_match() -> None:
    graph = CanonicalGraph(
        nodes=(SemanticNode("product:1", "Product"), SemanticNode("site:1", "Site"))
    )
    round_trip = ReasoningRoundTrip(
        NodeQuery(node_type="Product"),
        ReasoningResult("result:1", "matched", ("site:1",)),
    )
    with pytest.raises(ReasoningRoundTripError):
        validate_reasoning_round_trip(graph, round_trip)
