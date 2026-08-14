import pytest

from scm_ontology.inventory import CanonicalInventory, InventoryConceptError, is_inventory


def test_creates_canonical_inventory():
    inventory = CanonicalInventory(
        item_id="ITEM-001",
        location_id="WH-001",
        quantity=120,
        unit="EA",
    )
    assert inventory.quantity == 120
    assert is_inventory(inventory)


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"item_id": "", "location_id": "WH-1", "quantity": 1, "unit": "EA"}, "item_id"),
        ({"item_id": "I", "location_id": "", "quantity": 1, "unit": "EA"}, "location_id"),
        ({"item_id": "I", "location_id": "L", "quantity": -1, "unit": "EA"}, "non-negative"),
        ({"item_id": "I", "location_id": "L", "quantity": 1, "unit": ""}, "unit"),
    ],
)
def test_rejects_invalid_inventory(kwargs, message):
    with pytest.raises(InventoryConceptError, match=message):
        CanonicalInventory(**kwargs)
