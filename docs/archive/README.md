# Documentation Archive

This directory records documentation that is no longer part of the current normative documentation surface.

Archived copies are historical reference material, not implementation authority. Where an archived note has been condensed, the complete original remains recoverable from Git history.

## Archived legacy documents

| Document | Historical role | Current source |
|---|---|---|
| `S116-README.md` | S116 machine-readable ontology schema note | Current schema and architecture documentation |
| `m6-e2e-business-questions.md` | M6 end-to-end graph/business-question acceptance note | M8 acceptance and architecture documentation |
| `s6-transition-chain-v0.1.md` | Early simulation transition-chain contract | Post-M8 implementation roadmap |
| `S7-causal-transition-contract.md` | Early causal-transition contract | Current governed causal semantics |
| `scm-simulation-causal-v0.1.md` | S4 simulation causal contract | Post-M8 implementation roadmap |
| `scm-simulation-contract-v0.1.md` | S1 simulation semantic contract | Post-M8 implementation roadmap |
| `scm-simulation-redesign-v0.1.md` | Pre-M8 simulation redesign baseline | `docs/roadmap-post-m8.md` |
| `scm-simulation-state-transition-v0.1.md` | S5 state-transition contract | Post-M8 implementation roadmap |

## Policy

These documents are historical design artifacts, not current normative contracts. They MUST NOT be treated as the current semantic authority after M8 completion.

When a historical document is still needed for regression tests or provenance, reference its archived path explicitly. New normative documentation belongs under the current architecture and milestone surfaces rather than at the root of `docs/`.

For current project orientation, start at the repository README and `docs/README.md`.
