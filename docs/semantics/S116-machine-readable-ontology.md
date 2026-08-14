# S116 — Machine-readable Ontology

S116 turns the S113-S115 semantic contracts into an implementation-neutral machine-readable serialization contract.

## Scope

S113 defined canonical concepts and relationship signatures.
S114 defined type, attribute, value, role, and cardinality semantics.
S115 defined identifiers and canonical references.

S116 defines the minimum serialization envelope and validation vocabulary. It does not yet attempt to encode every S101-S115 semantic detail.

## Canonical serialization

```text
Ontology
 ├─ version
 ├─ concepts
 │   ├─ layer
 │   ├─ dimension
 │   └─ attributes
 └─ relationships
     ├─ predicate
     ├─ source
     ├─ target
     └─ category
```

The JSON Schema in `schema/canonical-ontology.schema.json` is the normative machine-readable contract for this milestone.

## Design rules

1. Serialization is not the ontology itself; it is a representation of the canonical model.
2. Storage-specific concerns remain outside Core.
3. Concept layer and dimension are explicit.
4. Attribute type, role, and cardinality are explicit.
5. Relationship source, target, predicate, and semantic category are explicit.
6. Unknown semantics must not be silently inferred from field names.
7. Planned, actual, observed, estimated, predicted, and counterfactual states remain semantic distinctions rather than datatype distinctions.
8. Identifier and provenance extensions must remain compatible with S115 and S104 rather than redefining them.

## Validation boundary

S116 validates structural shape. It does not yet prove:

- that a relationship endpoint exists;
- that a referenced value type is defined;
- that an attribute owner is unique;
- that historical constraints are satisfied;
- that semantic dependencies are acyclic;
- that source mappings are valid.

Those belong to S118-level semantic validation.

## Serialization neutrality

The canonical model can later be rendered into JSON, YAML, RDF, property graphs, relational schemas, or other representations. None of those formats becomes authoritative merely by being used for serialization.

## Example

See `schema/canonical-ontology.example.yaml` for a minimal human-readable instance corresponding to the JSON Schema.

## Exit criteria

S116 is complete when:

- a normative machine-readable structural schema exists;
- a minimal canonical instance can be represented;
- S113/S114 semantics are represented without vendor coupling;
- serialization and ontology semantics remain conceptually separate;
- deeper semantic validation is explicitly deferred to S118.
