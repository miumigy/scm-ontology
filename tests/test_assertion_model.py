import pytest

from scm_ontology.assertion_context import AssertionContext
from scm_ontology.assertion_model import (
    AssertionModelError,
    CanonicalAssertionSet,
    EntityAssertion,
    RelationAssertion,
)
from scm_ontology.core_instance import CanonicalRelation
from scm_ontology.semantic_context import EpistemicKind, SemanticContext


def context(ref: str, subject: str) -> AssertionContext:
    return AssertionContext(ref, SemanticContext(ref, subject, EpistemicKind.OBSERVATION))


def test_entity_and_relation_assertions_share_one_assertion_contract() -> None:
    entity = EntityAssertion("a:entity", "inventory:1", "quantity_on_hand", 100, context("a:entity", "inventory:1"))
    relation = CanonicalRelation("a:relation", "inventory:1", "stored_at", "site:1")
    relation_assertion = RelationAssertion(relation, context("a:relation", "inventory:1"))
    model = CanonicalAssertionSet((entity,), (relation_assertion,))
    assert len(model.entity_assertions) == 1
    assert len(model.relation_assertions) == 1


def test_assertion_references_are_unique() -> None:
    c = context("a:1", "inventory:1")
    first = EntityAssertion("a:1", "inventory:1", "quantity_on_hand", 100, c)
    second = EntityAssertion("a:1", "inventory:1", "quantity_on_hand", 90, c)
    with pytest.raises(AssertionModelError, match="unique"):
        CanonicalAssertionSet((first, second))
