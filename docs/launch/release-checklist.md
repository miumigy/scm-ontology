# SCM Ontology v0.1.0 / SCM OS Reference v0.1.0 — Release Checklist

This is the release gate for the first public OSS/reference release.

## Launch Readiness

- [x] Public README explains the problem, model, SCM OS boundary, and non-goals.
- [x] Japanese README provides the same conceptual path using Japanese terminology.
- [x] One executable Golden Path exists.
- [x] Multi-source reference data path demonstrates ERP + WMS + TMS convergence.
- [x] Demo output exposes node/relationship counts, identity links, provenance-bearing source members, and the reference-only boundary.
- [x] Demo is deterministic and regression-tested.
- [x] Quick-start commands are documented.

## Launch Gate

- [x] Semantic validator is a CI step.
- [x] Golden Path self-check is a CI step.
- [x] L5 primary-launch acceptance is a CI step.
- [x] Full pytest suite is a CI step.
- [x] Installed-package Golden Path is checked without `PYTHONPATH`.
- [x] Acceptance fails closed when a probe errors or produces an unusable result.
- [x] Determinism, provenance, governance, bounded execution, and replay/audit are explicitly tested.

## Release Package

- [x] Package metadata declares version `0.1.0`.
- [x] MIT `LICENSE` is present and linked from both READMEs.
- [x] `CHANGELOG.md` exists.
- [x] `CONTRIBUTING.md` exists.
- [x] Primary-launch limitations are documented.
- [x] Release notes exist.
- [x] Post-launch backlog is release-oriented rather than an instruction to create new S/M/Phase numbers.
- [ ] Git tag `v0.1.0` and GitHub Release are created after the release commit is merged.

## Release decision

The source tree is release-ready when CI is green and every checked item above is satisfied. The tag/release is deliberately the final repository-level publication step after the merge commit is stable.
