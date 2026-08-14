# S38 — Canonical Time Reference

## Purpose

S38 introduces an explicit temporal reference concept so that SCM semantics can distinguish different meanings of a timestamp without conflating planning time, requested time, confirmed time, effective time, and occurrence time.

## Minimal contract

```text
CanonicalTimeReference
├─ value
└─ time_type
```

The `value` carries the temporal value in an agreed representation. S38 does not prescribe a storage format beyond requiring a non-empty value; implementations should use an unambiguous, timezone-aware representation when a clock timestamp is intended.

## Canonical time vocabulary

```text
occurred_at   = when an event actually occurred
 effective_at = when a state/condition becomes effective
planned_at    = when an activity is planned to occur
requested_at  = when an occurrence was requested
confirmed_at  = when a time was confirmed/committed
```

These are semantic types, not interchangeable timestamp fields.

## Critical SCM boundary

```text
planned_at   ≠ occurred_at
requested_at ≠ confirmed_at
occurred_at  ≠ effective_at
```

For example, a shipment may be planned for 09:00, depart at 09:17, and have its resulting state become effective at 09:17. Those are related facts but have different semantic meanings.

## Graph impact

```text
Event ──occurred_at──→ TimeReference
State ──effective_at─→ TimeReference
Order ──requested_at─→ TimeReference
Order ──confirmed_at─→ TimeReference
Plan  ──planned_at───→ TimeReference
```

S38 does not define every owner of each time type; it only provides the canonical temporal vocabulary and reference shape.

## Non-goals

S38 does not define:

- calendars
- business days
- time zones as a master concept
- durations
- intervals
- scheduling algorithms
- lead-time calculation
- SLA semantics
- event ordering
- temporal precedence

Those can be introduced as separate contracts when required.
