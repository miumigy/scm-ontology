# Contributing to SCM Ontology

Thank you for contributing to SCM Ontology.

## Start here

1. Read [`AGENTS.md`](AGENTS.md).
2. Read [`README.md`](README.md) and [`README.ja.md`](README.ja.md) when working on public semantics or documentation.
3. Read [`docs/launch/README.md`](docs/launch/README.md) to understand the current public boundary.
4. Run the validation suite before changing behavior.

```bash
export PYTHONPATH=src
python -m scm_ontology.validator
python -m scm_ontology.primary_launch --self-check
python -m scm_ontology.primary_launch_acceptance --self-check
pytest -q
```

## Semantic discipline

- Prefer existing definitions and governed contracts before introducing new abstractions.
- Do not make a source-system representation become truth implicitly.
- Preserve provenance, scope, temporal context, uncertainty, and history.
- Keep derived/projected state distinct from governed facts.
- Keep authorization and external side effects behind explicit boundaries.
- AI and agents may propose or reason, but must not bypass governance.

## Release-oriented planning

The project is now managed by releases rather than an unbounded sequence of internal `Sxxx`, `Mxx`, or `Phase` identifiers.

Before starting work, classify it as one of:

- **Primary Launch blocker** — prevents the current release from satisfying its acceptance gate.
- **Important improvement** — valuable before a release but not release-blocking.
- **Post-launch capability** — belongs in the release backlog.

Do not create a new Phase merely to organize an idea. Record genuine post-launch work in [`BACKLOG.yaml`](BACKLOG.yaml).

## Pull requests

Keep pull requests focused and deterministic. The PR description should explain:

- what changed;
- why it changed;
- which semantic or operational boundary it affects;
- how it was validated;
- whether the public documentation needs to change.

Never weaken tests or acceptance conditions simply to obtain green CI.

## Documentation

Public documentation should be understandable without knowledge of the project's historical internal numbering. When terminology has a natural Japanese expression, prefer the Japanese expression in `README.ja.md` rather than leaving unnecessary English-derived jargon.
