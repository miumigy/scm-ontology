from scm_ontology.core_instance import CanonicalRelation
from scm_ontology.relation_instance_projection import (
    RelationGraphEdge,
    project_relation_instance_to_graph,
)


def test_relation_instance_projection_preserves_identity_and_semantics() -> None:
    relation = CanonicalRelation(
        relation_id="rel:1",
        subject_id="entity:1",
        predicate_ref="supplies",
        object_id="entity:2",
        qualifiers={"effective_from": "2026-01-01"},
    )
    edge = project_relation_instance_to_graph(relation)
    assert isinstance(edge, RelationGraphEdge)
    assert edge.relation_id == relation.relation_id
    assert edge.subject_id == relation.subject_id
    assert edge.predicate_ref == relation.predicate_ref
    assert edge.object_id == relation.object_id
    assert dict(edge.qualifiers) == dict(relation.qualifiers)
