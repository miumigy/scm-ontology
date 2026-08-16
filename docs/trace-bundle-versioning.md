# Trace Bundle Schema Versioning Policy

The Trace Bundle interchange contract follows Semantic Versioning.

- **PATCH** (`1.0.x`): clarifications or backward-compatible fixes that do not change the accepted semantic shape.
- **MINOR** (`1.x.0`): backward-compatible additions. Existing valid bundles remain valid and consumers must ignore unknown optional fields.
- **MAJOR** (`x.0.0`): incompatible semantic or structural changes. Required fields, meaning, or validation rules may change.

## Compatibility rules

1. `schema_version` identifies the interchange contract, not the Python package version.
2. A consumer must reject an unsupported major version rather than silently interpreting it.
3. A consumer may accept a newer minor/patch version only when its compatibility policy explicitly permits it.
4. Removing a field, changing a field's meaning, or making an optional field required requires a major version.
5. Adding an optional field is a minor version change.
6. Every version change must update the published JSON Schema and its drift/compatibility tests in the same change.

Version `1.0.0` is the initial public Trace Bundle contract.
