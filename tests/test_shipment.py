import pytest

from scm_ontology.shipment import CanonicalShipment, ShipmentConceptError, is_shipment


def test_creates_canonical_shipment():
    shipment = CanonicalShipment(
        shipment_id="SHP-001",
        item_id="ITEM-001",
        quantity=20,
        unit="EA",
        origin_location_id="WH-001",
        destination_location_id="WH-002",
    )
    assert shipment.item_id == "ITEM-001"
    assert is_shipment(shipment)


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"shipment_id": "", "item_id": "I", "quantity": 1, "unit": "EA", "origin_location_id": "A", "destination_location_id": "B"}, "shipment_id"),
        ({"shipment_id": "S", "item_id": "", "quantity": 1, "unit": "EA", "origin_location_id": "A", "destination_location_id": "B"}, "item_id"),
        ({"shipment_id": "S", "item_id": "I", "quantity": -1, "unit": "EA", "origin_location_id": "A", "destination_location_id": "B"}, "non-negative"),
        ({"shipment_id": "S", "item_id": "I", "quantity": 1, "unit": "EA", "origin_location_id": "A", "destination_location_id": "A"}, "differ"),
    ],
)
def test_rejects_invalid_shipment(kwargs, message):
    with pytest.raises(ShipmentConceptError, match=message):
        CanonicalShipment(**kwargs)
