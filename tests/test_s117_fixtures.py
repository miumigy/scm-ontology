from pathlib import Path

import yaml


FIXTURE_DIR = Path(__file__).parents[1] / "examples" / "canonical-scm"
FIXTURE_DIR2 = Path(__file__).parents[1] / "examples" / "plan-actual-epistemic"


def test_canonical_fixture_has_required_sections() -> None:
    data = yaml.safe_load((FIXTURE_DIR / "canonical-scm-fixture.yaml").read_text())
    assert data["ontology"] == "scm-ontology"
    assert data["concepts"]
    assert data["relationships"]
    assert data["identifiers"]
    assert data["provenance"]


def test_fixture_contains_core_and_derived_concepts() -> None:
    data = yaml.safe_load((FIXTURE_DIR / "canonical-scm-fixture.yaml").read_text())
    layers = {concept["layer"] for concept in data["concepts"]}
    assert "core" in layers
    assert "derived" in layers


def test_plan_actual_epistemic_distinctions_are_explicit() -> None:
    data = yaml.safe_load((FIXTURE_DIR2 / "plan-actual-epistemic-fixture.yaml").read_text())
    pairs = {tuple(pair) for pair in data["non_equivalences"]}
    assert ("planned", "actual") in pairs
    assert ("observed", "inferred") in pairs
    assert ("predicted", "actual") in pairs
