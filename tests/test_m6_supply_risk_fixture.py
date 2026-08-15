import json
from pathlib import Path


def test_supply_risk_fixture_has_three_hops() -> None:
    fixture = json.loads(Path("fixtures/m6/supply-risk-chain.json").read_text(encoding="utf-8"))
    question = fixture["business_questions"][0]
    assert question["expected_path"] == [
        "MAT-001", "supplied_by", "SUP-001",
        "located_at", "SITE-001",
        "exposed_to", "RISK-001",
    ]


def test_supply_risk_fixture_is_evidence_bound_and_read_only() -> None:
    fixture = json.loads(Path("fixtures/m6/supply-risk-chain.json").read_text(encoding="utf-8"))
    assert all(edge.get("evidence") for edge in fixture["edges"])
    invariants = fixture["m6_invariants"]
    assert invariants["read_only"] is True
    assert invariants["inference_creates_canonical_fact"] is False
    assert invariants["enterprise_specific_semantics"] is False
