from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.execution_trace_graph_validation import ExecutionTraceGraphValidation
from scm_ontology.graph_query import GraphQueryResult
from scm_ontology.governed_query_context import (
    GraphQuerySpec,
    GovernedQueryContextError,
    build_governed_query_context,
)


def trace():
    from scm_ontology.execution_trace import ExecutionTrace
    return ExecutionTrace(
        context_id="ctx-1",
        command_id="cmd-1",
        event_id="evt-1",
        evidence_ids=("e2", "e1"),
        provenance_ids=("p2", "p1"),
    )


def graph():
    from scm_ontology.relationship_identity import RelationshipInstance
    return CanonicalGraph(
        nodes=(
            SemanticNode("ctx-1", "DecisionContext"),
            SemanticNode("evt-1", "CanonicalEvent"),
        ),
        relationships=(
            CanonicalRelationship(
                RelationshipInstance("r1", "ctx-1", "recorded_by", "evt-1")
            ),
        ),
    )


def result():
    return GraphQueryResult()


def valid():
    return ExecutionTraceGraphValidation(valid=True)


def test_context_is_immutable_and_deterministic():
    context = build_governed_query_context(
        trace(), graph(), result(), valid(), query=GraphQuerySpec("nodes", node_type="CanonicalEvent")
    )
    assert context.contract_version == "S357.1"
    assert context.context_id == "ctx-1"
    assert context.node_ids == ()
    assert context.relationship_ids == ()
    assert context.evidence_ids == ("e1", "e2")
    assert context.provenance_ids == ("p1", "p2")
    assert context.graph_identity.startswith("sha256:")
    with pytest.raises(FrozenInstanceError):
        context.context_id = "other"
    assert context.to_mapping()["query"] == {"operation": "nodes", "node_type": "CanonicalEvent"}


def test_invalid_graph_is_rejected():
    with pytest.raises(GovernedQueryContextError, match="invalid graph"):
        build_governed_query_context(
            trace(), graph(), result(), ExecutionTraceGraphValidation(valid=False, errors=("broken",)),
            query=GraphQuerySpec("nodes"),
        )


def test_query_spec_rejects_blank_values():
    with pytest.raises(GovernedQueryContextError):
        GraphQuerySpec(" ")
    with pytest.raises(GovernedQueryContextError):
        GraphQuerySpec("nodes", node_id=" ")
