import pytest

from scm_ontology.demand import CanonicalDemand, DemandConceptError, is_demand


def test_creates_canonical_demand():
    demand = CanonicalDemand(
        item_id="ITEM-001",
        quantity=100,
        unit="EA",
        period_start="2026-09-01",
        period_end="2026-09-30",
    )
    assert demand.quantity == 100
    assert is_demand(demand)


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"item_id": "", "quantity": 1, "unit": "EA", "period_start": "2026-09-01", "period_end": "2026-09-30"}, "item_id"),
        ({"item_id": "I", "quantity": -1, "unit": "EA", "period_start": "2026-09-01", "period_end": "2026-09-30"}, "non-negative"),
        ({"item_id": "I", "quantity": 1, "unit": "", "period_start": "2026-09-01", "period_end": "2026-09-30"}, "unit"),
        ({"item_id": "I", "quantity": 1, "unit": "EA", "period_start": "2026-09-30", "period_end": "2026-09-01"}, "precede"),
    ],
)
def test_rejects_invalid_demand(kwargs, message):
    with pytest.raises(DemandConceptError, match=message):
        CanonicalDemand(**kwargs)
