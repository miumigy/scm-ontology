# S206 — Registry Serialization Round-trip

S206 defines a JSON-compatible representation for versioned registry snapshots.

```text
VersionedRegistry
      ↓ serialize
 JSON-compatible payload
      ↓ JSON encode/decode
      ↓ deserialize
VersionedRegistry
```

Round-trip equality is checked at the semantic payload level. Serialization is read-only and does not mutate the registry.
