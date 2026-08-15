import pytest

from scm_ontology.canonical_relations import CanonicalRelationType, RelationKind
from scm_ontology.registry_integrity import RegistryIntegrityError, validate_relation_registry


def test_registered_inverse_must_point_back_to_original_predicate() -> None:
    relations = (
        CanonicalRelationType("supports", RelationKind.OPERATIONAL, "supported_by"),
        CanonicalRelationType("supported_by", RelationKind.OPERATIONAL, "wrong_ref"),
    )
    with pytest.raises(RegistryIntegrityError, match="reciprocal"):
        validate_relation_registry(relations)
