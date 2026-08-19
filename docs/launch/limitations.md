# Primary Launch — Explicit Boundaries

This document defines the claims that SCM Ontology / SCM OS Reference v0.1 **does not make**.

## Reference implementation, not a production service

The release demonstrates a governed, deterministic reference architecture. It does not certify a production deployment, availability target, security posture, or operational SLA.

## Connectors

The release does not provide a universal production connector suite for SAP, ERP, WMS, TMS, APS, or planning products. The multi-source reference path uses deterministic adapters and synthetic/reference data to demonstrate the semantic boundary.

## Data scale and persistence

Relational and Neo4j reference backends exist, but this release does not claim production-scale throughput, high availability, disaster recovery, backup policy, or a managed graph service.

## Security and tenancy

The release does not claim enterprise IAM integration, multi-tenant isolation, security certification, secrets management, or a hardened internet-facing deployment.

## AI and autonomy

AI and agents are reasoning/proposal providers. They do not directly mutate governed SCM state. Autonomous control is bounded by explicit validation, authorization, execution boundaries, and audit. The release does not claim unrestricted autonomy.

## Canonical Truth

A mapping result, inference, projection, materialization, similarity result, or successful ingestion does not become Canonical Truth merely because it succeeded. Governed application remains an explicit boundary.

## Optimization and planning

Reference simulation and deterministic planning/optimization demonstrate integration boundaries. They are not positioned as a replacement for production APS, optimizer, scheduler, or planning suites.

## Post-launch direction

Enterprise connectors, production observability, scale, tenancy, security, richer SCM applications, and more capable policy-bounded agents belong to post-launch releases and are tracked in `BACKLOG.yaml`.
