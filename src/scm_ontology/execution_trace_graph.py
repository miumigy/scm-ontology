"""Read-only projection of an execution trace into the canonical graph model."""
from __future__ import annotations

from .canonical_graph import CanonicalGraph, SemanticNode
from .execution_trace import ExecutionTrace


class ExecutionTraceGraphProjectionError(ValueError):
    """Raised when an execution trace cannot be projected safely."""


def execution_trace_to_graph(trace: ExecutionTrace) -> CanonicalGraph:
    """Project a governed execution trace into transport-neutral canonical nodes.

    This function performs no persistence and does not mutate the supplied trace.
    Relationships are deliberately deferred until their semantic predicates are
    established by a later graph contract.
    """
    if not isinstance(trace, ExecutionTrace):
        raise ExecutionTraceGraphProjectionError("trace must be an ExecutionTrace")

    nodes = (
        SemanticNode(
            node_id=trace.context_id,
            node_type="DecisionContext",
        ),
        SemanticNode(
            node_id=f"proposal:{trace.command_id}",
            node_type="DecisionProposal",
            properties={"proposal": trace.proposal, "context_id": trace.context_id},
        ),
        SemanticNode(
            node_id=f"command:{trace.command_id}",
            node_type="ExecutionCommand",
            properties={
                "command_id": trace.command_id,
                "command_type": trace.command_type,
                "context_id": trace.context_id,
                "actor_id": trace.actor_id,
                "authority": trace.authority,
            },
        ),
        SemanticNode(
            node_id=f"outcome:{trace.command_id}",
            node_type="ExecutionOutcome",
            properties={"status": trace.outcome_status, "command_id": trace.command_id},
        ),
        SemanticNode(
            node_id=trace.event_id,
            node_type="CanonicalEvent",
            properties={"event_type": trace.event_type, "command_id": trace.command_id},
        ),
    )
    return CanonicalGraph(nodes=nodes)
