"""Read-only projection of a governed execution trace into a canonical graph."""
from __future__ import annotations

from .canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from .execution_trace import ExecutionTrace
from .relationship_identity import RelationshipInstance


class ExecutionTraceGraphProjectionError(ValueError):
    """Raised when an execution trace cannot be projected safely."""


class ExecutionTracePredicate:
    """Canonical predicates for the governed execution trace chain."""

    HAS_PROPOSAL = "has_proposal"
    AUTHORIZED_AS = "authorized_as"
    RESULTED_IN = "resulted_in"
    RECORDED_BY = "recorded_by"


_RELATIONSHIP_SPECS = (
    ("context", "proposal", ExecutionTracePredicate.HAS_PROPOSAL, "DecisionContext", "DecisionProposal"),
    ("proposal", "command", ExecutionTracePredicate.AUTHORIZED_AS, "DecisionProposal", "ExecutionCommand"),
    ("command", "outcome", ExecutionTracePredicate.RESULTED_IN, "ExecutionCommand", "ExecutionOutcome"),
    ("outcome", "event", ExecutionTracePredicate.RECORDED_BY, "ExecutionOutcome", "CanonicalEvent"),
)


def _relationship_id(predicate: str, from_id: str, to_id: str) -> str:
    return f"{predicate}:{from_id}:{to_id}"


def execution_trace_relationships(trace: ExecutionTrace) -> tuple[CanonicalRelationship, ...]:
    """Build the deterministic semantic edges for one governed execution trace."""
    if not isinstance(trace, ExecutionTrace):
        raise ExecutionTraceGraphProjectionError("trace must be an ExecutionTrace")

    node_ids = {
        "context": trace.context_id,
        "proposal": f"proposal:{trace.command_id}",
        "command": f"command:{trace.command_id}",
        "outcome": f"outcome:{trace.command_id}",
        "event": trace.event_id,
    }
    node_types = {
        "context": "DecisionContext",
        "proposal": "DecisionProposal",
        "command": "ExecutionCommand",
        "outcome": "ExecutionOutcome",
        "event": "CanonicalEvent",
    }

    relationships = []
    for source_key, target_key, predicate, source_type, target_type in _RELATIONSHIP_SPECS:
        if node_types[source_key] != source_type or node_types[target_key] != target_type:
            raise ExecutionTraceGraphProjectionError("invalid relationship node type contract")
        from_id = node_ids[source_key]
        to_id = node_ids[target_key]
        relationships.append(
            CanonicalRelationship(
                RelationshipInstance(
                    relationship_id=_relationship_id(predicate, from_id, to_id),
                    from_id=from_id,
                    predicate=predicate,
                    to_id=to_id,
                )
            )
        )
    return tuple(relationships)


def execution_trace_to_graph(trace: ExecutionTrace) -> CanonicalGraph:
    """Project a governed execution trace into a transport-neutral canonical graph."""
    if not isinstance(trace, ExecutionTrace):
        raise ExecutionTraceGraphProjectionError("trace must be an ExecutionTrace")

    nodes = (
        SemanticNode(node_id=trace.context_id, node_type="DecisionContext"),
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
    return CanonicalGraph(nodes=nodes, relationships=execution_trace_relationships(trace))
