from scm_ontology.canonical_relations import CANONICAL_RELATION_TYPES
from scm_ontology.registry_graph_projection import RegistryGraphEdge, project_relation_registry_to_graph


def test_registry_projection_preserves_relation_semantics() -> None:
    edges = project_relation_registry_to_graph(CANONICAL_RELATION_TYPES)
    assert edges
    assert all(isinstance(edge, RegistryGraphEdge) for edge in edges)
    assert {edge.predicate_ref for edge in edges} == {
        relation.predicate_ref for relation in CANONICAL_RELATION_TYPES
    }
    assert {edge.kind for edge in edges} == {
        relation.kind for relation in CANONICAL_RELATION_TYPES
    }
    assert {edge.inverse_ref for edge in edges} == {
        relation.inverse_ref for relation in CANONICAL_RELATION_TYPES
    }
