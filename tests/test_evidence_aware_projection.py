import pytest

from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.evidence_aware_projection import (
    EvidenceAwareProjectionDefinition,
    ProjectionEvidenceMissing,
    evidence_aware_projection_to_json,
    evidence_aware_projection_to_mapping,
    materialize_evidence_aware_projection,
)
from scm_ontology.relationship_identity import RelationshipInstance


def graph() -> CanonicalGraph:
    return CanonicalGraph(
        nodes=(
            SemanticNode("A", "Site", {"name": "東京"}),
            SemanticNode("B", "Site", {"name": "大阪"}),
        ),
        relationships=(
            CanonicalRelationship(
                RelationshipInstance("r1", "A", "ships_to", "B")
            ),
        ),
    )


def definition() -> EvidenceAwareProjectionDefinition:
    return EvidenceAwareProjectionDefinition(
        "site-evidence-summary",
        "1",
        lambda source, evidence: {
            "site_count": len(source.nodes),
            "relationship_ids": [r.instance.relationship_id for r in source.relationships],
            "evidence_ids": list(evidence.evidence_ids("r1")),
            "site_names": [n.properties["name"] for n in source.nodes],
        },
    )


def test_projection_materializes_with_accessed_evidence_and_lineage() -> None:
    source = graph()
    before = source.to_json()
    result = materialize_evidence_aware_projection(
        source,
        definition(),
        evidence_ids_by_relationship_id={"r1": ("ev2", "ev1")},
    )

    assert result.status == "materialized"
    assert result.value["evidence_ids"] == ["ev1", "ev2"]
    assert result.evidence_by_relationship_id == {"r1": ("ev1", "ev2")}
    assert result.lineage.evidence_by_relationship_id == result.evidence_by_relationship_id
    assert source.to_json() == before


def test_projection_fails_closed_when_required_evidence_is_missing() -> None:
    with pytest.raises(ProjectionEvidenceMissing):
        materialize_evidence_aware_projection(
            graph(),
            definition(),
            evidence_ids_by_relationship_id={},
        )


def test_projection_can_explicitly_allow_missing_evidence() -> None:
    result = materialize_evidence_aware_projection(
        graph(),
        definition(),
        evidence_ids_by_relationship_id={},
        require_evidence=False,
    )

    assert result.evidence_by_relationship_id == {"r1": ()}
    assert result.value["evidence_ids"] == []


def test_projection_json_is_deterministic_and_utf8_safe() -> None:
    result = materialize_evidence_aware_projection(
        graph(),
        definition(),
        evidence_ids_by_relationship_id={"r1": "ev1"},
    )
    payload = evidence_aware_projection_to_json(result)

    assert payload == evidence_aware_projection_to_json(result)
    assert "東京" in payload
    assert '"evidence_by_relationship_id":{"r1":["ev1"]}' in payload
    assert evidence_aware_projection_to_mapping(result)["contract_version"] == "1.0.0"
