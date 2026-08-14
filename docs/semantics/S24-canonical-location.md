# S24 — Canonical Location Concept

## Definition

**Location** is a canonical place or organizational point at which supply-chain activity is situated.

## Minimal concept contract

```text
CanonicalLocation
├─ location_id
├─ location_type
└─ name
```

The concept provides a stable semantic reference for "where" without prescribing a particular physical, geographic, organizational, or system representation.

## Relationship to Inventory

Inventory identifies a held quantity of an item at a location. Therefore Location is a reusable domain concept rather than an attribute embedded inside Inventory.

```text
Inventory
├─ item_id
└─ location_id ──→ Location
```

## Boundaries

Location is distinct from:

- **Address** — a representation of postal/geographic addressing.
- **Facility** — a domain concept that may be situated at a Location.
- **Organization** — an actor or organizational entity, not necessarily a place.
- **Route / Lane** — movement/network semantics between locations.

## Non-goals

S24 does not define:

- latitude/longitude or geocoding
- postal addresses
- facility hierarchy
- organization ownership
- geographic regions
- network topology
- route optimization
- warehouse-specific operational attributes
