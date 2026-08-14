import pytest

from scm_ontology.constraint_policy import Constraint, Policy


def test_constraint_is_distinct_semantic_object():
    item = Constraint("C1", "Supplier-A", "gte", 80)
    assert item.constraint_id == "C1"
    assert item.subject == "Supplier-A"
    assert item.operator == "gte"
    assert item.value == 80


def test_policy_is_distinct_from_constraint():
    item = Policy("P1", "Supplier-A", "prefer", True)
    assert item.policy_id == "P1"
    assert item.directive == "prefer"


def test_constraint_does_not_evaluate_itself():
    item = Constraint("C1", "Supplier-A", "gte", 80)
    assert not hasattr(item, "evaluate")


def test_policy_does_not_select_itself():
    item = Policy("P1", "Supplier-A", "prefer", True)
    assert not hasattr(item, "select")
