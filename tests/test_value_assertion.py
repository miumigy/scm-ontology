import pytest

from scm_ontology.assertion_context import AssertionContext
from scm_ontology.semantic_context import EpistemicKind, SemanticContext
from scm_ontology.value_assertion import ValueAssertion


def context(ref: str = "a:1", subject: str = "inventory:1") -> AssertionContext:
    return AssertionContext(ref, SemanticContext(ref, subject, EpistemicKind.OBSERVATION))


def test_value_assertion_binds_subject_and_attribute() -> None:
    assertion = ValueAssertion("a:1", "inventory:1", "quantity_on_hand", 100, context())
    assert assertion.value == 100


def test_context_subject_must_match() -> None:
    with pytest.raises(ValueError, match="subject_ref"):
        ValueAssertion("a:1", "inventory:2", "quantity_on_hand", 100, context())


def test_null_is_not_a_value_assertion() -> None:
    with pytest.raises(ValueError, match="null"):
        ValueAssertion("a:1", "inventory:1", "quantity_on_hand", None, context())
