import json
from pathlib import Path


def load_fixture() -> dict:
    return json.loads(Path("fixtures/m6/supply-dependency-chain.json").read_text(encoding="utf-8"))


def test_fixture_has_canonical_nodes_and_edges() -> None:
    fixture = load_fixture()
    assert {node["type"] for node in fixture["nodes"]} == {"material", "supplier", "site"}
    assert [(edge["predicate"]) for edge in fixture["edges"]] == ["supplied_by", "located_at"]


def test_fixture_queries_match_declared_paths() -> None:
    fixture = load_fixture()
    assert fixture["queries"][0]["expected_path"] == ["material:M-001", "supplied_by", "supplier:S-001"]
    assert fixture["queries"][1]["expected_path"] == ["material:M-001", "supplied_by", "supplier:S-001", "located_at", "site:SITE-001"]


def test_fixture_preserves_m6_invariants() -> None:
    fixture = load_fixture()
    assert fixture["invariants"] == {
        "read_only": True,
        "inference_creates_canonical_fact": False,
        "enterprise_specific_semantics": False,
    }
