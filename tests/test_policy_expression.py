from scm_ontology.policy_expression import PolicyExpression


def test_atomic_expression():
    expr = PolicyExpression.atomic("prefer supplier A")
    assert expr.kind == "atomic"
    assert expr.value == "prefer supplier A"
    assert expr.children == ()


def test_all_expression_preserves_order():
    left = PolicyExpression.atomic("domestic")
    right = PolicyExpression.atomic("available")
    expr = PolicyExpression.all(left, right)
    assert expr.kind == "all"
    assert expr.children == (left, right)


def test_any_expression():
    left = PolicyExpression.atomic("air")
    right = PolicyExpression.atomic("sea")
    expr = PolicyExpression.any(left, right)
    assert expr.kind == "any"
    assert expr.children == (left, right)


def test_not_expression():
    child = PolicyExpression.atomic("blocked")
    expr = PolicyExpression.not_(child)
    assert expr.kind == "not"
    assert expr.children == (child,)


def test_expression_does_not_select_or_evaluate():
    expr = PolicyExpression.atomic("prefer supplier A")
    assert not hasattr(expr, "select")
    assert not hasattr(expr, "evaluate")
