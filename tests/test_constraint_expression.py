from scm_ontology.constraint_expression import ConstraintExpression


def test_atomic_expression():
    expr = ConstraintExpression.atomic("capacity >= demand")
    assert expr.kind == "atomic"
    assert expr.value == "capacity >= demand"
    assert expr.children == ()


def test_all_expression_preserves_order():
    left = ConstraintExpression.atomic("capacity >= demand")
    right = ConstraintExpression.atomic("status = active")
    expr = ConstraintExpression.all(left, right)
    assert expr.kind == "all"
    assert expr.children == (left, right)


def test_any_expression():
    left = ConstraintExpression.atomic("route = air")
    right = ConstraintExpression.atomic("route = sea")
    expr = ConstraintExpression.any(left, right)
    assert expr.kind == "any"
    assert expr.children == (left, right)


def test_not_expression_has_one_child():
    child = ConstraintExpression.atomic("status = blocked")
    expr = ConstraintExpression.not_(child)
    assert expr.kind == "not"
    assert expr.children == (child,)


def test_expression_does_not_evaluate_itself():
    expr = ConstraintExpression.atomic("capacity >= demand")
    assert not hasattr(expr, "evaluate")
