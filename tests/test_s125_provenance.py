from pathlib import Path

import yaml


FIXTURE = Path(__file__).parents[1] / "examples" / "provenance-graph" / "provenance-graph-fixture.yaml"


def test_provenance_fixture_has_explicit_predicates() -> None:
    data = yaml.safe_load(FIXTURE.read_text())
    predicates = {edge["predicate"] for edge in data["edges"]}
    assert {
        "supported_by",
        "measured_from",
        "transformed_from",
        "derived_from",
        "evaluated_from",
        "decided_from",
    } <= predicates


def test_decision_can_be_traced_to_source() -> None:
    data = yaml.safe_load(FIXTURE.read_text())
    incoming = {}
    for edge in data["edges"]:
        incoming.setdefault(edge["source"], []).append(edge["target"])

    current = ["decision.replenishment_001"]
    visited = set()
    while current:
        node = current.pop()
        if node in visited:
            continue
        visited.add(node)
        current.extend(incoming.get(node, []))

    assert "source.wms_stock_001" in visited
    assert "evidence.stock_snapshot_001" in visited
    assert "observation.inventory_001" in visited


def test_provenance_does_not_upgrade_epistemic_status() -> None:
    data = yaml.safe_load(FIXTURE.read_text())
    nodes = {node["id"]: node for node in data["nodes"]}
    assert nodes["observation.inventory_001"]["epistemic_status"] == "observed"
    assert nodes["metric.service_level_001"]["epistemic_status"] == "derived"
