from pathlib import Path

import yaml


FIXTURE = Path(__file__).parents[1] / "examples" / "s120" / "erp-wms-tms-mapping.yaml"


def test_representative_source_domains_are_present() -> None:
    data = yaml.safe_load(FIXTURE.read_text())
    systems = {item["source"]["system"] for item in data["source_examples"]}
    assert systems == {"ERP", "WMS", "TMS"}


def test_identity_resolution_is_explicit_for_identifiers() -> None:
    data = yaml.safe_load(FIXTURE.read_text())
    identifier_mappings = [
        item for item in data["source_examples"] if item["target"].get("attribute") == "identifier"
    ]
    assert identifier_mappings
    for item in identifier_mappings:
        kinds = {t["kind"] for t in item.get("transformations", [])}
        assert "identity_resolution" in kinds


def test_planned_actual_semantics_are_not_collapsed() -> None:
    data = yaml.safe_load(FIXTURE.read_text())
    statuses = {x["semantic_status"] for x in data["planned_actual_separation"]}
    assert {"planned", "actual", "committed"} <= statuses
