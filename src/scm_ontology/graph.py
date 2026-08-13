"""Validation and Cypher generation for canonical SCM graph datasets."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _entity_definitions(entities_path: Path):
    return load_yaml(entities_path)["entities"]


def _inheritance_closure(entities: dict):
    """Return each entity and all of its transitive supertypes."""
    closure = {}

    def visit(name, trail=()):
        if name in closure:
            return closure[name]
        if name not in entities:
            raise ValueError(f"Unknown entity in inheritance chain: {name}")
        if name in trail:
            cycle = " -> ".join((*trail, name))
            raise ValueError(f"Entity inheritance cycle: {cycle}")
        parent = entities[name].get("extends")
        result = {name}
        if parent:
            result |= visit(parent, (*trail, name))
        closure[name] = result
        return result

    for name in entities:
        visit(name)
    return closure


def _is_compatible(actual: str, expected: str, closure: dict):
    return expected == "*" or expected in closure.get(actual, {actual})


def validate_graph_dataset(
    dataset_path: Path,
    relationships_path: Path,
    entities_path: Path | None = None,
):
    """Validate a graph dataset against ontology-driven entity inheritance and relationships."""
    dataset = load_yaml(dataset_path) or {}
    relationships = load_yaml(relationships_path)["relationships"]
    entities_path = entities_path or ROOT / "ontology" / "entities.yaml"
    entities = _entity_definitions(entities_path)
    closure = _inheritance_closure(entities)
    errors = []

    raw_nodes = dataset.get("nodes", [])
    raw_edges = dataset.get("edges", [])
    if not isinstance(raw_nodes, list):
        errors.append("Dataset nodes must be a list")
        raw_nodes = []
    if not isinstance(raw_edges, list):
        errors.append("Dataset edges must be a list")
        raw_edges = []

    nodes = {}
    for node in raw_nodes:
        if not isinstance(node, dict):
            errors.append("Node definition must be an object")
            continue
        node_id = node.get("id")
        if not node_id:
            errors.append("Node is missing id")
            continue
        if node_id in nodes:
            errors.append(f"Duplicate node id {node_id}")
            continue
        nodes[node_id] = node

        node_type = node.get("type")
        if node_type not in entities:
            errors.append(f"Node {node_id}: unknown type {node_type}")
            continue
        properties = node.get("properties", {})
        if not isinstance(properties, dict):
            errors.append(f"Node {node_id}: properties must be an object")
            continue
        allowed = set()
        for ancestor in closure[node_type]:
            allowed.update(entities[ancestor].get("properties", []))
        unknown = set(properties) - allowed
        if unknown:
            errors.append(f"Node {node_id}: unknown properties {sorted(unknown)}")

    for edge in raw_edges:
        if not isinstance(edge, dict):
            errors.append("Edge definition must be an object")
            continue
        rel = edge.get("type")
        source_id = edge.get("from")
        target_id = edge.get("to")
        if not rel:
            errors.append("Edge is missing relationship type")
            continue
        if rel not in relationships:
            errors.append(f"Edge {rel}: relationship is not defined")
            continue
        source = nodes.get(source_id)
        target = nodes.get(target_id)
        if source is None or target is None:
            errors.append(f"Edge {rel}: unknown endpoint {source_id} -> {target_id}")
            continue
        spec = relationships[rel]
        if not _is_compatible(source["type"], spec["from"], closure):
            errors.append(f"Edge {rel}: expected from {spec['from']}, got {source['type']}")
        if not _is_compatible(target["type"], spec["to"], closure):
            errors.append(f"Edge {rel}: expected to {spec['to']}, got {target['type']}")
        properties = edge.get("properties", {})
        if not isinstance(properties, dict):
            errors.append(f"Edge {rel}: properties must be an object")
            continue
        allowed = set(spec.get("properties", []))
        unknown = set(properties) - allowed
        if unknown:
            errors.append(f"Edge {rel}: unknown properties {sorted(unknown)}")
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
    """Generate idempotent Cypher using node IDs as stable identity."""
    dataset = load_yaml(dataset_path)
    lines = ["// Generated from canonical SCM Ontology dataset; do not edit manually."]

    for node in dataset.get("nodes", []):
        label = node["type"]
        props = node.get("properties", {})
        lines.append(f"MERGE (n:{label} {{id: {_cypher_value(node['id'])}}})")
        if props:
            rendered = ", ".join(
                f"{key}: {_cypher_value(value)}" for key, value in props.items()
            )
            lines.append(f"SET n += {{{rendered}}}")
        lines.append(";")

    for edge in dataset.get("edges", []):
        props = edge.get("properties", {})
        lines.append(
            f"MATCH (a {{id: {_cypher_value(edge['from'])}}}), "
            f"(b {{id: {_cypher_value(edge['to'])}}}) "
            f"MERGE (a)-[r:{edge['type']}]->(b)"
        )
        if props:
            rendered = ", ".join(
                f"{key}: {_cypher_value(value)}" for key, value in props.items()
            )
            lines.append(f"SET r += {{{rendered}}}")
        lines.append(";")

    return "\n".join(lines) + "\n"
