# S18 — Canonical State Model

## Definition

A **State** is a condition or configuration that holds for a canonical entity over a period.

## Required semantics

A canonical state has:

- an explicit `entity_id` identifying what the condition applies to;
- an explicit `state_type` identifying the kind of condition/configuration;
- explicit state attributes describing the condition.

## Boundary rules

- A State is not a MetricObservation.
- A MetricObservation does not automatically create or imply a State.
- A State is not an Event; an Event represents an occurrence, while a State represents a condition that holds.
- `state_type` remains framework-independent and must not encode ERP/WMS/TMS-specific object types.
- State transitions and temporal lifecycle semantics are deferred to a later milestone.

## Canonical intent

S18 establishes the minimum semantic shape of State without attempting to enumerate SCM-specific states such as inventory status, capacity status, transport status, or production status.
