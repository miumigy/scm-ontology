import pytest

from scm_ontology.canonical_relations import CANONICAL_RELATION_TYPES, CanonicalRelationType, RelationKind
from scm_ontology.registry_integrity import RegistryIntegrityError, validate_relation_registry


def test_canonical_registry_has_complete_inverse_namespace() -> None:
    validate_relation_registry(CANONICAL_RELATION_TYPES)


def test_undeclared_inverse_is_rejected() -> None:
    relation = CanonicalRelationType("supports", RelationKind.OPERATIONAL, "supported_by")
    with pytest.raises(RegistryIntegrityError):
        validate_relation_registry((*CANONICAL_RELATION_TYPES, relation))
