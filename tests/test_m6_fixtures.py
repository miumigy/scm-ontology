import json
from pathlib import Path


FIXTURES = [
    Path("fixtures/supply-dependency/supply-dependency-chain.json"),
    Path("fixtures/inventory-capacity/inventory-capacity-chain.json"),
]


def load_fixture(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_m6_fixtures_are_valid_json_and_have_identity() -> None:
    for path in FIXTURES:
        fixture = load_fixture(path)
        assert fixture["fixture_id"].startswith("M6-FX-")
        assert fixture["nodes"]
        assert fixture["edges"]


def test_m6_fixtures_have_evidence_bound_edges() -> None:
    for path in FIXTURES:
        fixture = load_fixture(path)
        for edge in fixture["edges"]:
            assert edge.get("evidence") or edge.get("evidence_id")


def test_m6_fixtures_preserve_read_only_invariants() -> None:
    for path in FIXTURES:
        fixture = load_fixture(path)
        invariants = fixture.get("m6_invariants", fixture.get("invariants", {}))
        assert invariants["read_only"] is True
        assert invariants["inference_creates_canonical_fact"] is False
        assert invariants["enterprise_specific_semantics"] is False


def test_m6_fixture_business_questions_have_expected_paths() -> None:
    for path in FIXTURES:
        fixture = load_fixture(path)
        questions = fixture.get("business_questions", fixture.get("queries", []))
        assert questions
        for question in questions:
            assert question["expected_path"]
