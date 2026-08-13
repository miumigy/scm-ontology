"""Load a validated canonical SCM dataset into Neo4j."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .graph import load_yaml, validate_graph_dataset


def build_statements(dataset: dict[str, Any]) -> list[str]:
    """Build idempotent Cypher statements using dataset IDs as node identity."""
    statements: list[str] = []
    for node in dataset.get("nodes", []):
        label = node["type"]
        props = node.get("properties", {})
        assignments = ", ".join(f"n.{key} = $p_{key}" for key in props)
        suffix = f" SET {assignments}" if assignments else ""
        statements.append(
            f"MERGE (n:{label} {{id: $node_id}}){suffix}"
        )
    for edge in dataset.get("edges", []):
        rel = edge["type"]
        props = edge.get("properties", {})
        assignments = ", ".join(f"r.{key} = $p_{key}" for key in props)
        suffix = f" SET {assignments}" if assignments else ""
        statements.append(
            f"MATCH (a {{id: $from_id}}), (b {{id: $to_id}}) "
            f"MERGE (a)-[r:{rel}]->(b){suffix}"
        )
    return statements


def load_into_neo4j(
    dataset_path: str | Path,
    *,
    uri: str,
    user: str,
    password: str,
    relationships_path: str | Path = "ontology/relationships.yaml",
    entities_path: str | Path = "ontology/entities.yaml",
) -> int:
    """Validate then load a YAML dataset. Returns the number of statements run."""
    from neo4j import GraphDatabase

    dataset_path = Path(dataset_path)
    errors = validate_graph_dataset(dataset_path, Path(relationships_path), Path(entities_path))
    if errors:
        raise ValueError("Dataset validation failed:\n" + "\n".join(errors))

    dataset = load_yaml(dataset_path)
    statements = build_statements(dataset)
    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        driver.verify_connectivity()
        with driver.session() as session:
            for node in dataset.get("nodes", []):
                props = node.get("properties", {})
                params = {"node_id": node["id"], **{f"p_{k}": v for k, v in props.items()}}
                session.run(statements.pop(0), params).consume()
            for edge in dataset.get("edges", []):
                props = edge.get("properties", {})
                params = {
                    "from_id": edge["from"],
                    "to_id": edge["to"],
                    **{f"p_{k}": v for k, v in props.items()},
                }
                session.run(statements.pop(0), params).consume()
    return len(dataset.get("nodes", [])) + len(dataset.get("edges", []))
