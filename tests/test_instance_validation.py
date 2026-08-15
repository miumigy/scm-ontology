import pytest

from scm_ontology.canonical_model import relationship_predicates
from scm_ontology.core_instance import CanonicalEntity, CanonicalRelation, CoreInstanceModel
from scm_ontology.instance_validation import assert_core_instances_valid, validate_core_instances


def test_valid_instance_references_canonical_concept_and_predicate() -> None:
    material = CanonicalEntity("material:001", "Material")
    site = CanonicalEntity("site:001", "Site")
    relation = CanonicalRelation("rel:001", material.entity_id, "located_at", site.entity_id)
    model = CoreInstanceModel((material, site), (relation,))
    assert validate_core_instances(model, concept_types={"material:001": "Material", "site:001": "Location"}) == ()


def test_unknown_concept_is_rejected() -> None:
    entity = CanonicalEntity("x:001", "NotAConcept")
    model = CoreInstanceModel((entity,))
    issues = validate_core_instances(model, concept_types={"x:001": "NotAConcept"})
    assert any(issue.code == "CON002" for issue in issues)


def test_unknown_predicate_is_rejected() -> None:
    a = CanonicalEntity("a:001", "Material")
    b = CanonicalEntity("b:001", "Location")
    relation = CanonicalRelation("r:001", "a:001", "not_a_predicate", "b:001")
    issues = validate_core_instances(CoreInstanceModel((a, b), (relation,)), concept_types={"a:001": "Material", "b:001": "Location"})
    assert any(issue.code == "REL001" for issue in issues)


def test_assertion_raises_for_invalid_instance() -> None:
    entity = CanonicalEntity("x:001", "Material")
    with pytest.raises(ValueError, match="invalid canonical instances"):
        assert_core_instances_valid(CoreInstanceModel((entity,)), concept_types={"x:001": "Missing"})


def test_registry_predicates_are_nonempty() -> None:
    assert "located_at" in relationship_predicates()
