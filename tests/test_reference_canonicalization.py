import pytest

from scm_ontology.reference_canonicalization import (
    CanonicalizationError,
    SourceMapping,
    canonicalize_record,
    canonicalize_to_json,
)


def test_reference_mapping_is_explicit_and_deterministic() -> None:
    mapping = SourceMapping("erp-fixture", (("MATNR", "item_id"), ("WERKS", "location_id"), ("QTY", "quantity"), ("MEINS", "unit")))
    record = {"MEINS": "EA", "QTY": 12, "WERKS": "TOKYO", "MATNR": "P-001"}
    expected = {"contract_version": "S335.1", "canonical": {"item_id": "P-001", "location_id": "TOKYO", "quantity": 12, "unit": "EA"}, "source_id": "erp-fixture", "mapping_version": "S335.1", "source_fields": ["MATNR", "WERKS", "QTY", "MEINS"]}
    assert canonicalize_record(record, mapping) == expected
    assert canonicalize_to_json(record, mapping) == canonicalize_to_json(dict(reversed(list(record.items()))), mapping)


def test_missing_source_field_fails_closed() -> None:
    mapping = SourceMapping("wms-fixture", (("sku", "item_id"), ("qty", "quantity")))
    with pytest.raises(CanonicalizationError):
        canonicalize_record({"sku": "P-001"}, mapping)


def test_duplicate_mapping_field_is_rejected() -> None:
    with pytest.raises(CanonicalizationError):
        SourceMapping("fixture", (("sku", "item_id"), ("sku", "location_id")))


def test_utf8_is_preserved() -> None:
    mapping = SourceMapping("fixture", (("品目", "item_id"),))
    payload = canonicalize_to_json({"品目": "東京P"}, mapping)
    assert "東京P" in payload
