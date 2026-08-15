import pytest

from scm_ontology.canonical_relations import CANONICAL_RELATION_TYPES, CanonicalRelationType, RelationKind
from scm_ontology.reasoning_compatibility import (
    ReasoningCompatibilityError,
    validate_reasoning_compatibility,
)


def test_canonical_relations_are_reasoning_compatible() -> None:
    validate_reasoning_compatibility(CANONICAL_RELATION_TYPES)


def test_non_reciprocal_declared_inverse_is_rejected() -> None:
    relations = (
        CanonicalRelationType("supports", RelationKind.OPERATIONAL, "supported_by"),
        CanonicalRelationType("supported_by", RelationKind.OPERATIONAL, "wrong_inverse"),
    )
    with pytest.raises(ReasoningCompatibilityError):
        validate_reasoning_compatibility(relations)
