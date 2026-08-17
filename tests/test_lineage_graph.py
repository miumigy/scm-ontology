import pytest

from scm_ontology.canonical_event_lineage import CanonicalEventLineage
from scm_ontology.lineage_graph import LineageGraph, LineageGraphError, build_lineage_graph


def test_build_lineage_graph_is_deterministic_and_typed():
    lineage = CanonicalEventLineage(
        event_id="event-1",
        evidence_ids=("e1", "e2"),
        provenance_ids=("p1", "p2"),
    )
    result = build_lineage_graph(lineage)
    assert isinstance(result, LineageGraph)
    assert [node.node_id for node in result.graph.nodes] == ["event-1", "e1", "e2", "p1", "p2"]
    assert [node.node_type for node in result.graph.nodes] == [
        "CanonicalEvent", "Evidence", "Evidence", "Provenance", "Provenance"
    ]
    assert [(r.instance.predicate, r.instance.from_id, r.instance.to_id) for r in result.graph.relationships] == [
        ("evidence_for", "e1", "event-1"),
        ("evidence_for", "e2", "event-1"),
        ("provenance_for", "p1", "event-1"),
        ("provenance_for", "p2", "event-1"),
    ]
    assert result.to_mapping() == build_lineage_graph(lineage).to_mapping()


def test_lineage_graph_rejects_wrong_contract_type():
    with pytest.raises(LineageGraphError):
        build_lineage_graph(object())


def test_lineage_graph_has_deterministic_relationship_ids():
    lineage = CanonicalEventLineage("event-1", ("e1",), ("p1",))
    result = build_lineage_graph(lineage)
    assert [r.instance.relationship_id for r in result.graph.relationships] == [
        "evidence_for:e1:event-1",
        "provenance_for:p1:event-1",
    ]
