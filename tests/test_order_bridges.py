import pytest

from scm_ontology.order_bridges import (
    CANONICAL_ORDER_PLANNING_BRIDGES,
    OrderPlanningBridge,
    OrderPlanningBridgeError,
    is_order_planning_bridge,
)


def test_canonical_order_planning_bridges_are_explicit():
    bridges = {
        (b.order_type, b.predicate, b.planning_type)
        for b in CANONICAL_ORDER_PLANNING_BRIDGES
    }
    assert bridges == {
        ("CustomerOrder", "contributes_to", "Demand"),
        ("PurchaseOrder", "creates", "Supply"),
        ("ProductionOrder", "creates", "Supply"),
    }
    assert all(is_order_planning_bridge(b) for b in CANONICAL_ORDER_PLANNING_BRIDGES)


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"order_type": "", "predicate": "creates", "planning_type": "Supply"}, "order_type"),
        ({"order_type": "PurchaseOrder", "predicate": "", "planning_type": "Supply"}, "predicate"),
        ({"order_type": "PurchaseOrder", "predicate": "creates", "planning_type": ""}, "planning_type"),
    ],
)
def test_rejects_invalid_bridge(kwargs, message):
    with pytest.raises(OrderPlanningBridgeError, match=message):
        OrderPlanningBridge(**kwargs)
