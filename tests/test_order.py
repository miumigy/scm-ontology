import pytest

from scm_ontology.order import CanonicalOrder, OrderConceptError, is_order


def test_creates_canonical_order():
    order = CanonicalOrder(
        order_id="ORD-001",
        item_id="ITEM-001",
        quantity=25,
        unit="EA",
        order_type="customer_request",
    )
    assert order.order_id == "ORD-001"
    assert is_order(order)


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"order_id": "", "item_id": "I", "quantity": 1, "unit": "EA"}, "order_id"),
        ({"order_id": "O", "item_id": "", "quantity": 1, "unit": "EA"}, "item_id"),
        ({"order_id": "O", "item_id": "I", "quantity": -1, "unit": "EA"}, "non-negative"),
        ({"order_id": "O", "item_id": "I", "quantity": 1, "unit": ""}, "unit"),
    ],
)
def test_rejects_invalid_order(kwargs, message):
    with pytest.raises(OrderConceptError, match=message):
        CanonicalOrder(**kwargs)
