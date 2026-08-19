# Primary Launch Demo — Multi-source SCM Reference Graph

The repository contains a small deterministic scenario that makes the semantic boundary visible without requiring a live ERP/WMS/TMS environment.

## Source representations

```text
ERP (CSV-shaped) ─┐
WMS (JSON-shaped) ├─ quality gate → mapping → identity resolution → reference graph
TMS (SQL-shaped) ┘
```

The ERP and WMS product records share an explicit GTIN identity signal and converge onto the same reference Product nodes. TMS shipment records contribute `carriedBy` relationships to those products.

## Run

From the repository root:

```bash
PYTHONPATH=src python examples/primary_launch_demo.py
```

The output shows:

- source-system diversity;
- converged node and relationship counts;
- identity links;
- source members/provenance attached to converged nodes;
- the `reference` truth boundary;
- the deterministic content hash;
- the resulting relationships.

## Why this matters

The example demonstrates the central SCM Ontology claim in a compact form:

> Heterogeneous enterprise evidence can be brought into a common semantic space without silently promoting the source representation or the derived reference projection into governed Canonical Truth.

The demo is intentionally reference-only. It does not connect to external systems or create external side effects.
