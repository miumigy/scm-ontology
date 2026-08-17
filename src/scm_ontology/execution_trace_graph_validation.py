"""Read-only integrity validation for governed execution trace graphs."""
from __future__ import annotations

from dataclasses import dataclass

from .canonical_graph import CanonicalGraph
from .execution_trace import ExecutionTrace
from .execution_trace_graph import ExecutionTracePredicate, execution_trace_relationships
from .lineage_graph import LineageGraph


class ExecutionTraceGraphValidationError(ValueError):
    """Raised when a trace graph violates its semantic contract."""


@dataclass(frozen=True)
class ExecutionTraceGraphValidation:
    valid: bool
    errors: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.valid and self.errors:
            raise ExecutionTraceGraphValidationError("valid result cannot contain errors")
        if not self.valid and not self.errors:
            raise ExecutionTraceGraphValidationError("invalid result must contain errors")


def validate_execution_trace_graph(
    trace: ExecutionTrace,
    graph: CanonicalGraph,
    lineage_graph: LineageGraph | None = None,
) -> ExecutionTraceGraphValidation:
    """Validate node, edge, and optional lineage semantics without side effects."""
    if not isinstance(trace, ExecutionTrace):
        raise ExecutionTraceGraphValidationError("trace must be an ExecutionTrace")
    if not isinstance(graph, CanonicalGraph):
        raise ExecutionTraceGraphValidationError("graph must be a CanonicalGraph")
    if lineage_graph is not None and not isinstance(lineage_graph, LineageGraph):
        raise ExecutionTraceGraphValidationError("lineage_graph must be a LineageGraph")

    errors: list[str] = []
    nodes = {node.node_id: node.node_type for node in graph.nodes}
    expected_nodes = {
        trace.context_id: "DecisionContext",
        f"proposal:{trace.command_id}": "DecisionProposal",
        f"command:{trace.command_id}": "ExecutionCommand",
        f"outcome:{trace.command_id}": "ExecutionOutcome",
        trace.event_id: "CanonicalEvent",
    }
    for node_id, node_type in expected_nodes.items():
        if nodes.get(node_id) != node_type:
            errors.append(f"missing or mistyped node: {node_id} ({node_type})")

    actual = {relationship.instance.relationship_id: relationship for relationship in graph.relationships}
    for expected in execution_trace_relationships(trace):
        if actual.get(expected.instance.relationship_id) != expected:
            errors.append(f"missing or mismatched relationship: {expected.instance.relationship_id}")

    allowed = {
        ExecutionTracePredicate.HAS_PROPOSAL,
        ExecutionTracePredicate.AUTHORIZED_AS,
        ExecutionTracePredicate.RESULTED_IN,
        ExecutionTracePredicate.RECORDED_BY,
    }
    for relationship in graph.relationships:
        instance = relationship.instance
        if instance.from_id not in nodes:
            errors.append(f"relationship source node is missing: {instance.from_id}")
        if instance.to_id not in nodes:
            errors.append(f"relationship target node is missing: {instance.to_id}")
        if instance.predicate not in allowed:
            errors.append(f"unknown execution trace predicate: {instance.predicate}")

    if lineage_graph is not None:
        lineage = lineage_graph.graph
        lineage_nodes = {node.node_id: node.node_type for node in lineage.nodes}
        if lineage_nodes.get(trace.event_id) != "CanonicalEvent":
            errors.append(f"lineage event node is missing or mistyped: {trace.event_id}")
        if {node.node_id for node in lineage.nodes if node.node_type == "Evidence"} != set(trace.evidence_ids):
            errors.append("evidence node set does not match trace lineage")
        if {node.node_id for node in lineage.nodes if node.node_type == "Provenance"} != set(trace.provenance_ids):
            errors.append("provenance node set does not match trace lineage")
        for relationship in lineage.relationships:
            instance = relationship.instance
            if instance.predicate == "evidence_for" and (
                instance.to_id != trace.event_id or instance.from_id not in trace.evidence_ids
            ):
                errors.append(f"invalid evidence_for relationship: {instance.relationship_id}")
            elif instance.predicate == "provenance_for" and (
                instance.to_id != trace.event_id or instance.from_id not in trace.provenance_ids
            ):
                errors.append(f"invalid provenance_for relationship: {instance.relationship_id}")
            elif instance.predicate not in {"evidence_for", "provenance_for"}:
                errors.append(f"unknown lineage predicate: {instance.predicate}")

    return ExecutionTraceGraphValidation(valid=not errors, errors=tuple(errors))
