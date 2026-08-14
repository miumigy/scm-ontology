import pytest

from scm_ontology.supply import CanonicalSupply, SupplyConceptError, is_supply


def test_creates_canonical_supply():
    supply = CanonicalSupply(
        item_id="ITEM-001",
        quantity=80,
        unit="EA",
        period_start="2026-09-01",
        period_end="2026-09-30",
    )
    assert supply.quantity == 80
    assert is_supply(supply)


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"item_id": "", "quantity": 1, "unit": "EA", "period_start": "2026-09-01", "period_end": "2026-09-30"}, "item_id"),
        ({"item_id": "I", "quantity": -1, "unit": "EA", "period_start": "2026-09-01", "period_end": "2026-09-30"}, "non-negative"),
        ({"item_id": "I", "quantity": 1, "unit": "", "period_start": "2026-09-01", "period_end": "2026-09-30"}, "unit"),
        ({"item_id": "I", "quantity": 1, "unit": "EA", "period_start": "2026-09-30", "period_end": "2026-09-01"}, "precede"),
    ],
)
def test_rejects_invalid_supply(kwargs, message):
    with pytest.raises(SupplyConceptError, match=message):
        CanonicalSupply(**kwargs)
