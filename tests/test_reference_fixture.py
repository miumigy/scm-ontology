from pathlib import Path

from scm_ontology.reference_canonicalization import CanonicalizationOutcome
from scm_ontology.reference_fixture import run_fixture


FIXTURE = Path(__file__).parents[1] / "examples" / "reference-canonicalization-pipeline.yaml"


def test_fixture_loader_preserves_source_records_and_mapping_outcomes() -> None:
    result = run_fixture(FIXTURE)

    assert len(result.records) == 4
    assert [(record.source_system, record.label) for record in result.records] == [
        ("erp", "customer_order"),
        ("erp", "inventory"),
        ("wms", "stock"),
        ("wms", "unknown_record"),
    ]
    assert [item.canonical_id for item in result.results] == [
        "Order",
        "Inventory",
        "Inventory",
        None,
    ]
    assert [item.outcome for item in result.results] == [
        CanonicalizationOutcome.APPLIED,
        CanonicalizationOutcome.APPLIED,
        CanonicalizationOutcome.APPLIED,
        CanonicalizationOutcome.SEMANTIC_GAP,
    ]
