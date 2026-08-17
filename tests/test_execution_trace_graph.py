from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.execution_trace import ExecutionTrace
from scm_ontology.execution_trace_graph import (
    ExecutionTraceGraphProjectionError,
    execution_trace_to_graph,
)


def trace():
    return ExecutionTrace(
        context_id="ctx-1",
        proposal="replenish",
        actor_id="planner-1",
        authority="supply-chain-manager",
        command_id="cmd-1",
        command_type="replenishment",
        outcome_status="success",
        event_id="cmd-1",
        event_type="execution_outcome_recorded",
        evidence_ids=("e1", "e2"),
        provenance_ids=("p1", "p2"),
    )


def test_trace_projects_to_deterministic_canonical_nodes():
    result = execution_trace_to_graph(trace())
    assert [node.node_id for node in result.nodes] == [
        "ctx-1",
        "proposal:cmd-1",
        "command:cmd-1",
        "outcome:cmd-1",
        "cmd-1",
    ]
    assert [node.node_type for node in result.nodes] == [
        "DecisionContext",
        "DecisionProposal",
        "ExecutionCommand",
        "ExecutionOutcome",
        "CanonicalEvent",
    ]
    assert result.to_mapping()["relationships"] == []


def test_projection_is_read_only_and_trace_remains_immutable():
    source = trace()
    result = execution_trace_to_graph(source)
    assert source.command_id == "cmd-1"
    assert result.nodes[1].properties["proposal"] == "replenish"
    with pytest.raises(FrozenInstanceError):
        source.command_id = "cmd-2"


def test_projection_rejects_non_trace_input():
    with pytest.raises(ExecutionTraceGraphProjectionError):
        execution_trace_to_graph(object())
