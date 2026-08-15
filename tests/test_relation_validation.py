import pytest

from scm_ontology.core_instance import CanonicalRelation
from scm_ontology.relation_validation import (
    CanonicalRelationValidationError,
    validate_canonical_relation,
)


def test_registered_predicate_is_accepted() -> None:
    relation = CanonicalRelation("r:1", "order:1", "fulfills", "demand:1")
    validate_canonical_relation(relation)


def test_unknown_predicate_is_rejected() -> None:
    relation = CanonicalRelation("r:1", "order:1", "ships_to_customer_system_specific", "demand:1")
    with pytest.raises(CanonicalRelationValidationError):
        validate_canonical_relation(relation)
