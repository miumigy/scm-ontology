# S89 — Observation State Semantics

S89 defines the semantic boundary between an Observation and a domain State inferred or represented from observations over time.

## Canonical decision

A State is **not** a subtype of Observation.

```text
Observation
    ≠ State
```

An Observation records an observation instance at an observation time. A State represents a condition of a domain object or system, potentially over a validity interval.

The canonical Observation remains:

```text
Observation
├─ observation_id
├─ observed_at
└─ subject_id
```

## Observation versus State

Consider:

```text
10:00  inventory_level = 120
11:00  inventory_level = 105
12:00  inventory_level = 130
```

These are Observation instances. An application may infer a state interval such as:

```text
inventory_level = 120
valid from 10:00 until 11:00
```

The interval boundary is a semantic inference or domain rule; it is not an implicit attribute of the 10:00 Observation.

## State validity is distinct from observation time

```text
Observation
  observed_at = T

State
  valid_from = T1
  valid_to   = T2
```

These temporal concepts must not be collapsed.

In particular, the next Observation does not universally prove that the preceding State ended at exactly that instant. That interpretation depends on domain assumptions about continuity, sampling, missing data, and state transitions.

## State as a domain semantic

A State may describe a condition such as:

```text
Warehouse-A
  inventory_level = 120

Plant-A
  production_status = running

Vehicle-17
  location = Depot-B

Network-A
  capacity_utilization = 82%
```

Whether such a condition is modeled as a State, property value, snapshot, or another domain object depends on the domain contract. S89 only establishes that the State concept must not be conflated with Observation identity.

## Derivation from observations

A State may be derived from one or more Observations:

```text
Observation O1 ─┐
Observation O2 ─┼─ interpretation / derivation ─→ State S1
Observation O3 ─┘
```

The derivation may use domain rules, continuity assumptions, interpolation, reconciliation, or other application logic.

S85's derivation boundary applies: the existence of input observations does not automatically imply a particular State.

## State versus Claim

A State is not automatically a Claim.

```text
State
  = domain condition / condition representation

Claim
  = assertion that may be supported or challenged
```

A State can be referenced as Evidence for a Claim, and Observations can provide Evidence for a Claim about a State. These are separate semantic roles.

## Snapshot semantics

A system may expose a State as a snapshot:

```text
State snapshot at 12:00
  inventory_level = 130
```

This does not make the snapshot itself an Observation. The snapshot may be constructed from an Observation, a set of Observations, or another state-management process.

## No automatic interval inference

S89 deliberately does not define the rule:

```text
Observation at T1
Observation at T2
→ State valid from T1 to T2
```

Such a rule is domain-specific and may be invalid when observations are sparse, delayed, corrected, or non-continuous.

## Relationship to S86

S86 establishes `observed_at` as the canonical Observation time and keeps interval semantics outside the Observation primitive. S89 extends this boundary by defining State validity as a separate domain semantic.

## Non-goals

S89 does not define a universal State primitive schema, state-transition algebra, interval inference algorithm, temporal database model, continuity assumption, snapshot standard, or state-machine ontology.
