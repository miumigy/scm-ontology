import pytest

from scm_ontology.item import CanonicalItem, ItemConceptError, is_item


def test_creates_canonical_item():
    item = CanonicalItem(
        item_id="ITEM-001",
        item_type="finished_good",
        name="Widget A",
    )
    assert item.item_id == "ITEM-001"
    assert is_item(item)


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"item_id": "", "item_type": "material", "name": "Steel"}, "item_id"),
        ({"item_id": "I", "item_type": "", "name": "Steel"}, "item_type"),
        ({"item_id": "I", "item_type": "material", "name": ""}, "name"),
    ],
)
def test_rejects_invalid_item(kwargs, message):
    with pytest.raises(ItemConceptError, match=message):
        CanonicalItem(**kwargs)
