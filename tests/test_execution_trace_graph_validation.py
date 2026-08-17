import pytest

from scm_ontology.canonical_event_lineage import CanonicalEventLineage
from scm_ontology.execution_trace import ExecutionTrace
from scm_ontology.execution_trace_graph import execution_trace_to_graph
from scm_ontology.execution_trace_graph_validation import (
    ExecutionTraceGraphValidation,
    ExecutionTraceGraphValidationError,
    validate_execution_trace_graph,
)
from scm_ontology.lineage_graph import build_lineage_graph


def trace():
    return ExecutionTrace(
        context_id="ctx-1", proposal="replenish", actor_id="planner-1",
        authority="supply-chain-manager", command_id="cmd-1",
        command_type="replenishment", outcome_status="success",
        event_id="cmd-1", event_type="execution_outcome_recorded",
        evidence_ids=("e1", "e2"), provenance_ids=("p1", "p2"),
    )


def test_validation_accepts_core_and_lineage_graphs():
    source = trace()
    result = validate_execution_trace_graph(
        source,
        execution_trace_to_graph(source),
        build_lineage_graph(CanonicalEventLineage("cmd-1", ("e1", "e2"), ("p1", "p2"))),
    )
    assert isinstance(result, ExecutionTraceGraphValidation)
    assert result.valid is True
    assert result.errors == ()


def test_validation_is_deterministic_and_detects_missing_relationship():
    source = trace()
    graph = execution_trace_to_graph(source)
    broken = graph.__class__(nodes=graph.nodes, relationships=graph.relationships[:-1])
    result = validate_execution_trace_graph(source, broken)
    assert result.valid is False
    assert result.errors == ("missing or mismatched relationship: recorded_by:outcome:cmd-1:cmd-1",)


def test_validation_detects_wrong_node_type_and_unknown_edge():
    source = trace()
    graph = execution_trace_to_graph(source)
    from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
    from scm_ontology.relationship_identity import RelationshipInstance
    nodes = tuple(SemanticNode(n.node_id, "WrongType" if n.node_id == "ctx-1" else n.node_type, n.properties) for n in graph.nodes)
    rels = graph.relationships + (CanonicalRelationship(RelationshipInstance("x", "ctx-1", "unknown", "proposal:cmd-1")),)
    result = validate_execution_trace_graph(source, CanonicalGraph(nodes, rels))
    assert result.valid is False
    assert "missing or mistyped node: ctx-1 (DecisionContext)" in result.errors
    assert "unknown execution trace predicate: unknown" in result.errors


def test_validation_rejects_wrong_input_types():
    with pytest.raises(ExecutionTraceGraphValidationError):
        validate_execution_trace_graph(object(), execution_trace_to_graph(trace()))
    with pytest.raises(ExecutionTraceGraphValidationError):
        validate_execution_trace_graph(trace(), object())


def test_validation_result_contract_is_immutable():
    with pytest.raises(ExecutionTraceGraphValidationError):
        ExecutionTraceGraphValidation(True, ("unexpected",))
    with pytest.raises(ExecutionTraceGraphValidationError):
        ExecutionTraceGraphValidation(False, ())
