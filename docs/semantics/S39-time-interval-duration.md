# S39 — Canonical Time Interval / Duration

## Purpose

S39 adds generic temporal primitives for representing time spans without prematurely defining SCM-specific concepts such as lead time or transit time.

## Canonical concepts

```text
CanonicalDuration
├─ value
└─ unit

CanonicalTimeInterval
├─ start
└─ end
```

A Duration represents a non-negative temporal magnitude. A TimeInterval represents a span bounded by explicit temporal references.

## Semantic boundary

```text
TimeReference = a temporal point / meaning
Duration      = how much time
TimeInterval  = from when to when
```

These concepts are related but not interchangeable.

## SCM examples

```text
planned_at → occurred_at
    └─ schedule variance

shipment departed → shipment arrived
    └─ transit interval / duration

order created → order fulfilled
    └─ cycle interval / duration
```

S39 defines only the primitives. Domain-specific metrics should be derived later.

## Units

`CanonicalDuration.unit` remains explicit rather than enforcing a universal enum. Implementations should use an unambiguous vocabulary such as `seconds`, `minutes`, `hours`, or `days`.

## Important boundary

S39 does not define:

- lead time
- transit time
- cycle time
- waiting time
- processing time
- schedule variance
- SLA duration
- business calendars
- working-time calendars
- timezone conversion
- interval arithmetic
- duration derivation algorithms

Those are derived or domain-specific semantics.

## Graph impact

```text
TimeReference ──────┐
                    ├─→ TimeInterval
TimeReference ──────┘

TimeInterval ──has_duration──→ Duration
```

The relationship between interval and duration is conceptual; S39 does not require a particular calculation or storage strategy.
