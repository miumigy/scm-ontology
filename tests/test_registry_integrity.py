import pytest

from scm_ontology.canonical_relations import (
    CANONICAL_RELATION_TYPES,
    CanonicalRelationType,
    RelationKind,
)
from scm_ontology.registry_integrity import RegistryIntegrityError, validate_relation_registry


def test_canonical_registry_has_valid_inverse_integrity() -> None:
    validate_relation_registry(CANONICAL_RELATION_TYPES)


def test_unregistered_inverse_is_allowed() -> None:
    relation = CanonicalRelationType("supports", RelationKind.OPERATIONAL, "supported_by")
    validate_relation_registry((*CANONICAL_RELATION_TYPES, relation))


def test_registered_inverse_must_be_reciprocal() -> None:
    relation = CanonicalRelationType("supports", RelationKind.OPERATIONAL, "supported_by")
    inverse = CanonicalRelationType("supported_by", RelationKind.OPERATIONAL, "wrong_inverse")
    with pytest.raises(RegistryIntegrityError):
        validate_relation_registry((*CANONICAL_RELATION_TYPES, relation, inverse))
