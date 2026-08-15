import pytest

from scm_ontology.canonical_relations import RelationKind
from scm_ontology.relation_semantics import is_causal_relation, is_operational_relation, relation_kind


def test_causal_predicates_are_classified() -> None:
    assert relation_kind("causes") is RelationKind.CAUSAL
    assert is_causal_relation("results_in")


def test_operational_predicates_are_classified() -> None:
    assert relation_kind("fulfills") is RelationKind.OPERATIONAL
    assert is_operational_relation("supplies")


def test_non_causal_relation_is_not_causal() -> None:
    assert not is_causal_relation("located_at")


def test_unknown_predicate_is_rejected() -> None:
    with pytest.raises(ValueError, match="unknown canonical predicate"):
        relation_kind("customer_specific_relation")
