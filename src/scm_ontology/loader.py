"""CLI for validating an SCM graph dataset and generating Neo4j Cypher."""
import argparse
from pathlib import Path

from scm_ontology.graph import ROOT, generate_cypher, validate_graph_dataset


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    relationships = ROOT / "ontology" / "relationships.yaml"
    errors = validate_graph_dataset(args.dataset, relationships)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)

    cypher = generate_cypher(args.dataset)
    if args.output:
        args.output.write_text(cypher, encoding="utf-8")
        print(f"Generated {args.output}")
    else:
        print(cypher, end="")


if __name__ == "__main__":
    main()
