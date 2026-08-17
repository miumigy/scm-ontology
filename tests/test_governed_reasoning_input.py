from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.execution_trace import ExecutionTrace
from scm_ontology.execution_trace_graph_validation import ExecutionTraceGraphValidation
from scm_ontology.graph_query import GraphQueryResult
from scm_ontology.governed_query_context import GraphQuerySpec, build_governed_query_context
from scm_ontology.governed_reasoning_input import (
    GovernedReasoningInputError,
    build_reasoning_input_from_governed_query_context,
)


def trace():
    return ExecutionTrace(
        context_id="ctx-1", proposal="p", actor_id="a", authority="auth",
        command_id="cmd-1", command_type="replenishment", outcome_status="ok",
        event_id="evt-1", event_type="execution_outcome_recorded",
        evidence_ids=("e2", "e1"), provenance_ids=("p2", "p1"),
    )


def graph():
    return CanonicalGraph(
        nodes=(SemanticNode("ctx-1", "DecisionContext"), SemanticNode("evt-1", "CanonicalEvent"),
               SemanticNode("proposal:cmd-1", "DecisionProposal"), SemanticNode("command:cmd-1", "ExecutionCommand"),
               SemanticNode("outcome:cmd-1", "ExecutionOutcome")),
        relationships=(),
    )


def context():
    return build_governed_query_context(
        trace(), graph(), GraphQueryResult(), ExecutionTraceGraphValidation(valid=True),
        query=GraphQuerySpec("nodes", node_type="CanonicalEvent"),
    )


def test_adapter_is_immutable_and_deterministic():
    result = build_reasoning_input_from_governed_query_context(context())
    assert result.context_id == "ctx-1"
    assert result.evidence_ids == ("e1", "e2")
    assert result.provenance_ids == ("p1", "p2")
    assert result.observations[0].question_id == "graph_query:nodes"
    assert result.observations[0].evidence_ids == ("e1", "e2")
    assert result.observations[0].provenance_ids == ("p1", "p2")
    assert result.observations[0].value["graph_identity"].startswith("sha256:")
    with pytest.raises(FrozenInstanceError):
        result.context_id = "other"


def test_adapter_preserves_query_result_ids():
    ctx = build_governed_query_context(
        trace(), graph(),
        GraphQueryResult(nodes=(SemanticNode("evt-1", "CanonicalEvent"),), relationships=()),
        ExecutionTraceGraphValidation(valid=True),
        query=GraphQuerySpec("nodes", node_type="CanonicalEvent"),
    )
    result = build_reasoning_input_from_governed_query_context(ctx)
    assert result.observations[0].value["node_ids"] == ["evt-1"]
    assert result.observations[0].value["relationship_ids"] == []


def test_adapter_rejects_invalid_graph_identity():
    ctx = context()
    object.__setattr__(ctx, "graph_identity", "invalid")
    with pytest.raises(GovernedReasoningInputError, match="sha256"):
        build_reasoning_input_from_governed_query_context(ctx)
