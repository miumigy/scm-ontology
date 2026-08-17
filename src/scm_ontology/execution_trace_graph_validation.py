"""Read-only integrity validation for governed execution trace graphs."""
from __future__ import annotations
from dataclasses import dataclass
from .canonical_graph import CanonicalGraph
from .execution_trace import ExecutionTrace
from .execution_trace_graph import execution_trace_relationships, ExecutionTracePredicate
from .lineage_graph import LineageGraph

class ExecutionTraceGraphValidationError(ValueError):
    """Raised when a trace graph violates its semantic contract."""

@dataclass(frozen=True)
class ExecutionTraceGraphValidation:
    valid: bool
    errors: tuple[str, ...] = ()
    def __post_init__(self) -> None:
        if self.valid and self.errors: raise ExecutionTraceGraphValidationError("valid result cannot contain errors")
        if not self.valid and not self.errors: raise ExecutionTraceGraphValidationError("invalid result must contain errors")

def validate_execution_trace_graph(trace: ExecutionTrace, graph: CanonicalGraph, lineage_graph: LineageGraph | None = None) -> ExecutionTraceGraphValidation:
    """Validate node, edge, and optional lineage semantics without side effects."""
    if not isinstance(trace, ExecutionTrace): raise ExecutionTraceGraphValidationError("trace must be an ExecutionTrace")
    if not isinstance(graph, CanonicalGraph): raise ExecutionTraceGraphValidationError("graph must be a CanonicalGraph")
    if lineage_graph is not None and not isinstance(lineage_graph, LineageGraph): raise ExecutionTraceGraphValidationError("lineage_graph must be a LineageGraph")
    errors: list[str] = []
    nodes = {n.node_id:n.node_type for n in graph.nodes}
    expected = {trace.context_id:"DecisionContext", f"proposal:{trace.command_id}":"DecisionProposal", f"command:{trace.command_id}":"ExecutionCommand", f"outcome:{trace.command_id}":"ExecutionOutcome", trace.event_id:"CanonicalEvent"}
    for node_id, node_type in expected.items():
        if nodes.get(node_id) != node_type: errors.append(f"missing or mistyped node: {node_id} ({node_type})")
    actual = {r.instance.relationship_id:r for r in graph.relationships}
    for expected_rel in execution_trace_relationships(trace):
        if actual.get(expected_rel.instance.relationship_id) != expected_rel: errors.append(f"missing or mismatched relationship: {expected_rel.instance.relationship_id}")
    allowed = {ExecutionTracePredicate.HAS_PROPOSAL, ExecutionTracePredicate.AUTHORIZED_AS, ExecutionTracePredicate.RESULTED_IN, ExecutionTracePredicate.RECORDED_BY}
    for rel in graph.relationships:
        if rel.instance.from_id not in nodes: errors.append(f"relationship source node is missing: {rel.instance.from_id}")
        if rel.instance.to_id not in nodes: errors.append(f"relationship target node is missing: {rel.instance.to_id}")
        if rel.instance.predicate not in allowed: errors.append(f"unknown execution trace predicate: {rel.instance.predicate}")
    if lineage_graph is not None:
        lg = lineage_graph.graph
        lnodes = {n.node_id:n.node_type for n in lg.nodes}
        if lnodes.get(trace.event_id) != "CanonicalEvent": errors.append(f"lineage event node is missing or mistyped: {trace.event_id}")
        if {n.node_id for n in lg.nodes if n.node_type == "Evidence"} != set(trace.evidence_ids): errors.append("evidence node set does not match trace lineage")
        if {n.node_id for n in lg.nodes if n.node_type == "Provenance"} != set(trace.provenance_ids): errors.append("provenance node set does not match trace lineage")
        for rel in lg.relationships:
            if rel.instance.predicate == "evidence_for" and (rel.instance.to_id != trace.event_id or rel.instance.from_id not in trace.evidence_ids): errors.append(f"invalid evidence_for relationship: {rel.instance.relationship_id}")
            elif rel.instance.predicate == "provenance_for" and (rel.instance.to_id != trace.event_id or rel.instance.from_id not in trace.provenance_ids): errors.append(f"invalid provenance_for relationship: {rel.instance.relationship_id}")
            elif rel.instance.predicate not in {"evidence_for", "provenance_for"}: errors.append(f"unknown lineage predicate: {rel.instance.predicate}")
    return ExecutionTraceGraphValidation(valid=not errors, errors=tuple(errors))
