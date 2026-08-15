from scm_ontology.core_instance import CanonicalEntity
from scm_ontology.graph_identity import GraphNodeIdentity, graph_node_identity


def test_graph_identity_is_derived_from_canonical_entity_identity() -> None:
    entity = CanonicalEntity("entity:1", "Product", {"sku": "P-1"})
    identity = graph_node_identity(entity)
    assert identity == GraphNodeIdentity("entity:1", "Product")
