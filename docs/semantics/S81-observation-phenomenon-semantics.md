# S81 — Observation Phenomenon Semantics

S81 defines how the semantics of "what was observed" relate to the canonical Observation primitive.

## Canonical decision

S81 does **not** introduce a new canonical `Phenomenon` primitive and does not add `phenomenon`, `value`, `predicate`, or `object` fields to `Observation`.

The current Observation remains deliberately minimal:

```text
Observation
├─ observation_id
├─ observed_at
└─ subject_id
```

This preserves the S80 boundary between an observation reference and the domain-specific semantics of the observed content.

## Why no Phenomenon primitive yet

A generic `Phenomenon` entity would require another identity and vocabulary model without a demonstrated canonical need. It would also risk turning domain concepts such as inventory level, temperature, location, arrival status, demand, or emissions into an ontology-wide hierarchy prematurely.

The observed phenomenon can instead be resolved by a domain-specific semantic layer or mapping contract when the concrete observation source is interpreted.

## Observation versus Claim

An Observation does not use Claim's `subject / predicate / object` assertion structure as its canonical identity.

```text
Observation
  = temporal observation reference

Claim
  = semantic assertion
```

A concrete application may derive a Claim from an Observation, or use an Observation as Evidence for a Claim, but neither transformation is implied by the existence of an Observation.

## Observation versus value

A measured or observed value is not currently a canonical field of Observation. This avoids prematurely standardizing units, datatypes, measurement scales, qualifiers, and domain-specific value semantics.

For example, the application layer may interpret an observation as:

```text
subject = Warehouse-A
phenomenon = inventory_level
value = 120
unit = pieces
```

but S81 does not make those fields part of the canonical Observation primitive.

## Future extension point

If repeated cross-domain requirements establish a stable need for a canonical Phenomenon abstraction, it can be introduced later as an explicit semantic primitive or relationship. Such an extension must preserve:

```text
Observation ≠ Phenomenon
Observation ≠ Value
Observation ≠ Claim
```

and must not silently change the meaning of existing Observation identifiers.

## Non-goals

S81 does not define a Phenomenon hierarchy, Measurement ontology, unit vocabulary, value datatype model, automatic observation interpretation, Claim inference, or domain-specific Observation subclasses.
