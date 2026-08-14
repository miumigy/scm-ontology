"""Consistency checks for the canonical SCM semantic graph v0.2."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_ENTITIES = {
    "Party",
    "Order",
    "PurchaseOrder",
    "ProductionOrder",
    "Shipment",
    "Demand",
    "State",
    "Event",
}

REQUIRED_RELATIONSHIPS = {
    "FROM",
    "TO",
    "PRODUCES_ORDER",
    "SHIPS",
    "CARRIED_BY",
    "CHANGES",
}

CANONICAL_SEMANTIC_LAYERS = (
    "entity",
    "relationship",
    "transaction",
    "planning",
    "physical_flow",
    "event",
    "state",
    "temporal",
)


def validate_semantic_graph_v02(
    entities_path: Path | None = None,
    relationships_path: Path | None = None,
) -> list[str]:
    """Return consistency errors for the v0.2 canonical semantic graph contract."""
    entities_path = entities_path or ROOT / "ontology" / "entities.yaml"
    relationships_path = relationships_path or ROOT / "ontology" / "relationships.yaml"

    entities_doc = yaml.safe_load(entities_path.read_text(encoding="utf-8")) or {}
    relationships_doc = yaml.safe_load(relationships_path.read_text(encoding="utf-8")) or {}
    entities = entities_doc.get("entities", {})
    relationships = relationships_doc.get("relationships", {})

    errors: list[str] = []
    missing_entities = REQUIRED_ENTITIES - set(entities)
    missing_relationships = REQUIRED_RELATIONSHIPS - set(relationships)

    if missing_entities:
        errors.append(f"Missing canonical entities: {sorted(missing_entities)}")
    if missing_relationships:
        errors.append(f"Missing canonical relationships: {sorted(missing_relationships)}")

    if entities_doc.get("version") != "0.1":
        errors.append("Ontology entity source version must remain 0.1 until an explicit schema migration")
    if relationships_doc.get("version") != "0.1":
        errors.append("Ontology relationship source version must remain 0.1 until an explicit schema migration")

    if "CHANGES" not in relationships:
        errors.append("Event-to-State bridge requires the existing CHANGES relationship")
    elif relationships["CHANGES"].get("from") != "Event" or relationships["CHANGES"].get("to") != "State":
        errors.append("CHANGES must connect Event to State")

    return errors
