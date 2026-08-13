"""Validation and Cypher generation for canonical SCM graph datasets."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_graph_dataset(dataset_path: Path, relationships_path: Path):
    dataset = load_yaml(dataset_path)
    relationships = load_yaml(relationships_path)["relationships"]
    nodes = {node["id"]: node for node in dataset.get("nodes", [])}
    errors = []

    for node in dataset.get("nodes", []):
        if node.get("type") not in {
            "Party", "Site", "Location", "Lane", "Product", "Material",
            "ProductLocation", "BOM", "BOMLine", "InventoryPosition", "Demand",
            "Forecast", "Plan", "Order", "PurchaseOrder", "ProductionOrder",
            "Shipment", "Capacity", "Constraint", "Policy", "Decision",
            "DecisionOption", "Event", "State", "KPI", "Risk", "Cost",
        }:
            errors.append(f"Node {node.get('id')}: unknown type {node.get('type')}")
        if not node.get("id"):
            errors.append("Node is missing id")

    for edge in dataset.get("edges", []):
        rel = edge.get("type")
        if rel not in relationships:
            errors.append(f"Edge {rel}: relationship is not defined")
            continue
        source = nodes.get(edge.get("from"))
        target = nodes.get(edge.get("to"))
        if source is None or target is None:
            errors.append(f"Edge {rel}: unknown endpoint {edge.get('from')} -> {edge.get('to')}")
            continue
        spec = relationships[rel]
        if spec["from"] != "*" and source["type"] != spec["from"]:
            errors.append(f"Edge {rel}: expected from {spec['from']}, got {source['type']}")
        if spec["to"] != "*" and target["type"] != spec["to"]:
            errors.append(f"Edge {rel}: expected to {spec['to']}, got {target['type']}")
    return errors


def _cypher_value(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        escaped = value.replace("\\", "\\\\").replace("'", "\\'")
        return f"'{escaped}'"
    raise TypeError(f"Unsupported Cypher value: {type(value).__name__}")


def generate_cypher(dataset_path: Path) -> str:
    dataset = load_yaml(dataset_path)
    lines = ["// Generated from canonical SCM Ontology dataset; do not edit manually."]
    for node in dataset.get("nodes", []):
        label = node["type"]
        props = {"id": node["id"], **node.get("properties", {})}
        rendered = ", ".join(f"{k}: {_cypher_value(v)}" for k, v in props.items())
        lines.append(f"MERGE (n:{label} {{{rendered}}});")
    for edge in dataset.get("edges", []):
        props = edge.get("properties", {})
        suffix = ""
        if props:
            rendered = ", ".join(f"{k}: {_cypher_value(v)}" for k, v in props.items())
            suffix = f" SET r += {{{rendered}}}"
        lines.append(
            f"MATCH (a {{id: {_cypher_value(edge['from'])}}}), "
            f"(b {{id: {_cypher_value(edge['to'])}}}) "
            f"MERGE (a)-[r:{edge['type']}]->(b){suffix};"
        )
    return "\n".join(lines) + "\n"
