# S158 — Contextual Value Assertion Model

S158 generalizes S157 assertion context from relations to attribute values.

## Model

```text
Canonical Entity
      ↓
Attribute
      ↓
Value Assertion
      ↓
Assertion Context
   ├─ Temporal
   ├─ Epistemic
   └─ Provenance
```

The value itself is not treated as timeless truth. Its semantic context is explicit.

## Boundaries

- Attribute definition ≠ attribute value
- Value ≠ measurement
- Observation ≠ inference
- Current value ≠ historical truth
- Null/unknown ≠ numeric zero
- Source value ≠ canonical identity

## Invariants

1. A value assertion has a canonical subject and attribute reference.
2. Its assertion context must refer to the same assertion and subject.
3. `None` is not a semantic value; absence/null semantics belong to the attribute/schema layer.
4. Temporal, epistemic, and provenance context remain separate dimensions.

## Example

```text
Inventory:001
  quantity_on_hand
       ↓
ValueAssertion = 100
       ↓
Observation
+ WMS provenance
+ observation time
```

A later observation can coexist without overwriting the earlier assertion.

## Non-goals

No metric calculation, unit conversion, inference engine, storage model, or enterprise mapping is introduced.
