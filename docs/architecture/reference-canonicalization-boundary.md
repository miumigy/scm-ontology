# S335 — Reference Canonicalization Fixture

S335 is the minimal reference boundary from a heterogeneous source record to a governed canonical record.

## Contract

A `SourceMapping` explicitly declares every source field and canonical target field. Missing fields fail closed. No identity resolution, inference, normalization by guess, graph mutation, or decision execution occurs here.

The serialized result contains `contract_version: S335.1`, source identity, mapping version, explicit source fields, and the canonical payload. JSON is deterministic and preserves UTF-8 characters.

## Purpose

This fixture is intentionally small. It demonstrates the integration boundary that later SCM OS implementations can replace with enterprise ERP/WMS/TMS adapters without changing canonical semantics.
