from scm_ontology.inventory_position import (
    InventoryPositionError,
    InventoryPositionRecord,
    inventory_position_to_json,
    inventory_position_to_mapping,
    resolve_inventory_position,
)


def test_resolves_explicit_inventory_position_with_lineage():
    result = resolve_inventory_position(
        [
            InventoryPositionRecord("P-1", "東京", 100, evidence_id="e2", provenance_id="wms"),
            InventoryPositionRecord("P-1", "東京", 20, "inbound", evidence_id="e1", provenance_id="erp"),
            InventoryPositionRecord("P-1", "東京", 15, "outbound", evidence_id="e3", provenance_id="tms"),
        ]
    )

    assert len(result) == 1
    assert result[0].on_hand == 100
    assert result[0].inbound == 20
    assert result[0].outbound == 15
    assert result[0].available == 105
    assert result[0].evidence_ids == ("e1", "e2", "e3")
    assert result[0].provenance_ids == ("erp", "tms", "wms")


def test_grouping_is_scoped_to_explicit_product_location_and_unit():
    result = resolve_inventory_position(
        [
            InventoryPositionRecord("P-2", "A", 10),
            InventoryPositionRecord("P-1", "A", 20),
            InventoryPositionRecord("P-1", "B", 30),
        ]
    )
    assert [(p.product_id, p.location_id) for p in result] == [
        ("P-1", "A"),
        ("P-1", "B"),
        ("P-2", "A"),
    ]


def test_missing_quantity_classes_are_zero():
    result = resolve_inventory_position([InventoryPositionRecord("P-1", "A", 7)])
    assert result[0].inbound == 0
    assert result[0].outbound == 0
    assert result[0].available == 7


def test_invalid_quantity_class_fails_closed():
    try:
        InventoryPositionRecord("P-1", "A", 1, "forecast")
    except InventoryPositionError as exc:
        assert "quantity_class" in str(exc)
    else:
        raise AssertionError("invalid quantity class must fail")


def test_mapping_and_json_are_deterministic_and_utf8_safe():
    result = resolve_inventory_position(
        [InventoryPositionRecord("P-1", "東京", 10, evidence_id="証拠-1")]
    )
    mapping = inventory_position_to_mapping(result)
    assert mapping["contract_version"] == "S326.1"
    assert "東京" in inventory_position_to_json(result)
    assert inventory_position_to_json(result) == inventory_position_to_json(result)


def test_empty_input_is_a_valid_empty_answer():
    assert inventory_position_to_mapping(()) == {
        "contract_version": "S326.1",
        "positions": [],
    }
