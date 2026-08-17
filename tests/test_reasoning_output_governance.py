from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.governed_query_context import GovernedQueryContext, GraphQuerySpec
from scm_ontology.reasoning_output import ReasoningOutput
from scm_ontology.reasoning_output_governance import (
    GovernedReasoningOutput,
    ReasoningOutputGovernanceError,
    govern_reasoning_output,
)


def context() -> GovernedQueryContext:
    return GovernedQueryContext(
        contract_version="S357.1",
        context_id="ctx-1",
        graph_identity="sha256:" + "a" * 64,
        query=GraphQuerySpec(operation="nodes", node_type="Location"),
        node_ids=("a", "b"),
        relationship_ids=("r1",),
        evidence_ids=("e1", "e2"),
        provenance_ids=("p1", "p2"),
    )


def output() -> ReasoningOutput:
    return ReasoningOutput(
        context_id="ctx-1",
        proposal="replenish",
        rationale="stock is below threshold",
        evidence_ids=("e2", "e1", "e1"),
        provenance_ids=("p2", "p1", "p2"),
        confidence=0.9,
    )


def test_governed_output_is_immutable_and_deterministic():
    result = govern_reasoning_output(context(), output())
    assert isinstance(result, GovernedReasoningOutput)
    assert result.context_id == "ctx-1"
    assert result.graph_identity == "sha256:" + "a" * 64
    assert result.evidence_ids == ("e1", "e2")
    assert result.provenance_ids == ("p1", "p2")
    with pytest.raises(FrozenInstanceError):
        result.context_id = "other"


def test_governance_rejects_context_mismatch():
    wrong = ReasoningOutput(
        context_id="ctx-2",
        proposal="replenish",
        rationale="stock is below threshold",
    )
    with pytest.raises(ReasoningOutputGovernanceError):
        govern_reasoning_output(context(), wrong)


def test_governance_rejects_unknown_evidence_and_provenance():
    bad = ReasoningOutput(
        context_id="ctx-1",
        proposal="replenish",
        rationale="stock is below threshold",
        evidence_ids=("e3",),
        provenance_ids=("p3",),
    )
    with pytest.raises(ReasoningOutputGovernanceError):
        govern_reasoning_output(context(), bad)


def test_governance_rejects_malformed_graph_identity():
    bad_context = GovernedQueryContext(
        contract_version="S357.1",
        context_id="ctx-1",
        graph_identity="not-a-graph-identity",
        query=context().query,
        node_ids=context().node_ids,
        relationship_ids=context().relationship_ids,
        evidence_ids=context().evidence_ids,
        provenance_ids=context().provenance_ids,
    )
    with pytest.raises(ReasoningOutputGovernanceError):
        govern_reasoning_output(bad_context, output())
