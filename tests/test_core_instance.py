import pytest

from scm_ontology.core_instance import (
    CanonicalEntity,
    CanonicalRelation,
    CoreInstanceError,
    CoreInstanceModel,
)


def test_core_instance_model_accepts_resolved_entities_and_relations() -> None:
    material = CanonicalEntity("material:001", "Material", {"code": "M-001"})
    warehouse = CanonicalEntity("site:001", "Site")
    relation = CanonicalRelation("rel:001", material.entity_id, "stored_at", warehouse.entity_id)
    model = CoreInstanceModel((material, warehouse), (relation,))
    assert len(model.entities) == 2
    assert model.relations[0].predicate_ref == "stored_at"


def test_relation_endpoints_must_resolve() -> None:
    entity = CanonicalEntity("material:001", "Material")
    relation = CanonicalRelation("rel:001", entity.entity_id, "stored_at", "site:missing")
    with pytest.raises(CoreInstanceError, match="object"):
        CoreInstanceModel((entity,), (relation,))


def test_entity_and_relation_ids_are_unique() -> None:
    a = CanonicalEntity("x", "Material")
    b = CanonicalEntity("x", "Site")
    with pytest.raises(CoreInstanceError, match="entity_id"):
        CoreInstanceModel((a, b))
