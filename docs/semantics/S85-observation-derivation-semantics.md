# S85 — Observation Derivation Semantics

S85 defines how derived Observations relate to source observations and other information artifacts.

## Canonical decision

A derived Observation is still an `Observation`; it is **not** a separate canonical subtype.

The canonical Observation remains:

```text
Observation
├─ observation_id
├─ observed_at
└─ subject_id
```

Derivation is represented as separate semantic/provenance information rather than by adding `derived_from` fields to Observation.

## Observation identity

A derived Observation receives its own `observation_id`.

```text
Observation O1
       │
       │ contributes to derivation
       ▼
Observation O3
```

`O3` is not an alias for `O1`, even if O3 preserves or summarizes information from O1.

This preserves S83:

```text
Observation identity
    ≠
real-world equivalence
    ≠
source-record identity
```

## Derivation is not Claim inference

Derivation describes how one information artifact or observation is produced from other inputs. It does not by itself assert that a proposition is true.

```text
Observation O1 ─┐
Observation O2 ─┼─ derivation ─→ Observation O3
Source Record R ─┘
```

By contrast:

```text
Evidence ── supports / contradicts ──→ Claim
```

A derived Observation may subsequently be used as Evidence for a Claim, but derivation and epistemic support remain distinct semantics.

## Examples

### Reconciliation

```text
WMS inventory observation = 120
ERP inventory observation = 118
        │
        ▼
reconciliation activity
        │
        ▼
Observation O3
  reconciled inventory = 119
```

O3 is a new Observation instance. The reconciliation process belongs to provenance/derivation semantics, not Observation identity.

### Forecasting

Historical demand observations may be used to derive a forecast observation:

```text
Demand O1 ─┐
Demand O2 ─┼─ forecasting activity ─→ Forecast Observation O3
Demand O4 ─┘
```

The forecast result is not retroactively an historical observation, and the derivation does not make the forecast a Claim.

## Provenance relationship

S84 establishes provenance as a separate semantic layer. S85 extends that principle to derivation:

```text
Input Observations / Source Records
              │
              │ derivation activity
              ▼
       Derived Observation
```

A provenance implementation may record the inputs, activity, agent, method, or transformation used to create the derived Observation. S85 does not prescribe a specific provenance graph schema.

## Direct versus derived observation

The distinction between directly observed and derived content is a semantic qualification, not a new Observation class.

```text
Observation
├─ direct observation
└─ derived observation
```

Both use the same canonical identity and core fields.

## No automatic inference

The existence of source observations does not automatically imply a derived Observation. A derivation relationship requires an explicit application, process, or semantic assertion establishing that relationship.

Likewise, a mathematically calculated value is not automatically a Claim or Evidence.

## Non-goals

S85 does not define a derivation vocabulary, transformation language, calculation engine, forecast model, reconciliation algorithm, provenance graph schema, automatic inference, or derived-observation subclass hierarchy.
