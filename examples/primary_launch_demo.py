"""Human-readable Primary Launch demo.

This is intentionally a thin presentation layer over the existing governed
reference-data pipeline. It does not introduce new SCM semantics or mutate
Canonical Truth.
"""
from __future__ import annotations

import json

from scm_ontology.multi_source_reference import run_multi_source_reference_path


def main() -> int:
    graph = run_multi_source_reference_path()
    print("SCM Ontology Primary Launch — multi-source reference demo")
    print()
    print("Sources: ERP (CSV) + WMS (JSON) + TMS (SQL-shaped adapter)")
    print(f"Reference nodes: {graph.node_count}")
    print(f"Reference relationships: {graph.edge_count}")
    print(f"Identity links: {len(graph.identity_links)}")
    print(f"Boundary: {graph.canonical_truth_boundary}")
    print(f"Content hash: {graph.content_hash}")
    print()
    print("Converged products:")
    for node in graph.nodes:
        if node.canonical_type == "Product":
            systems = ", ".join(source[0] for source in node.sources)
            print(f"  - {node.key}: {systems}")
    print()
    print("Relationships:")
    for edge in graph.edges:
        print(f"  - {edge.subject_key} -[{edge.predicate}]-> {edge.object_key}")
    print()
    print("Invariant: this is a reference projection; Canonical Truth is not mutated.")
    print()
    print(json.dumps(json.loads(graph.to_json()), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
