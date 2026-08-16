# Reference Canonicalization Pipeline — PR

## Summary

Implements the next post-M8 slice for multi-source reference canonicalization.

## Changes

- Add a realistic ERP/WMS fixture.
- Add regression tests for explicit cross-source mappings.
- Preserve `semantic_gap` for unmapped labels.
- Preserve `conflict` for multiple explicit targets.
- Document the boundary between canonical concept mapping and identity resolution.
- Explicitly preserve the no-Canonical-Truth-mutation rule.

## Validation intent

This change is deliberately additive. It does not change the canonical registry, canonical facts, identity resolution, or graph persistence contracts.

## Next step

Add an executable YAML fixture loader/pipeline adapter, then connect its output to the existing governed application transition without bypassing provenance or lifecycle controls.
