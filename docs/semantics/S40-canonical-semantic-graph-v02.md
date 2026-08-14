# S40 — Canonical Semantic Graph v0.2 Integration & Consistency

## Purpose

S40 is an integration milestone rather than a new domain concept. It verifies that the semantic primitives accumulated through S31–S39 can coexist as one canonical SCM graph without collapsing their boundaries.

## Canonical layers

```text
Entity
  ↓
Relationship
  ↓
Transaction
  ↓
Planning
  ↓
Physical Flow
  ↓
Event
  ↓
State
  ↓
Temporal Semantics
```

The layers are semantic categories, not necessarily implementation modules or database labels.

## Participant layer

```text
Party
  ↓ plays_role
PartyRole
  ↓ contextual relationship
Transaction / Shipment / Location
```

Party identity remains distinct from operational roles.

## Temporal layer

```text
Event ──occurred_at──→ TimeReference
State ──effective_at─→ TimeReference

TimeReference
    ├─ TimeInterval
    └─ Duration
```

Time meaning, interval, and duration remain separate primitives.

## Event / State bridge

The canonical ontology already contains the graph-level relationship:

```text
Event ──CHANGES──→ State
```

S37's `EventStateTransition` is the semantic vocabulary/contract describing event-type effects; it does not replace the graph relationship or become a universal state machine.

## Consistency rules

S40 verifies that:

1. canonical participant, transaction, planning, flow, event, and state entities remain available;
2. transaction/flow relationships retain explicit direction;
3. Event and State remain distinct concepts;
4. Event → State is represented by the existing `CHANGES` graph relationship;
5. temporal semantics do not collapse planned, requested, confirmed, occurred, and effective time;
6. v0.1 ontology source files are not silently schema-migrated by the integration milestone.

## Intentional non-goals

S40 does not add:

- a universal state machine
- a new database schema version
- domain-specific lifecycle enums
- temporal arithmetic
- automatic Event → State derivation
- a replacement for existing ontology YAML

The purpose is to establish a stable **Canonical Semantic Graph v0.2 integration boundary** before adding further domain concepts.
