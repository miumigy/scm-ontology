from pathlib import Path


DOC = Path("docs/milestones/S275-m7-e2e-canonicalization-pipeline.md")


def test_s275_defines_end_to_end_stages() -> None:
    text = DOC.read_text(encoding="utf-8")
    for stage in (
        "Enterprise Data",
        "Entity Mapping",
        "Attribute Mapping",
        "Predicate / Relation Mapping",
        "Mapping Decision",
        "Canonicalization Result",
        "Provenance / Audit",
        "Canonical Graph",
    ):
        assert stage in text


def test_s275_requires_versioned_deterministic_execution() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "source representation and adapter version",
        "mapping configuration and decision versions",
        "apply only approved mappings",
        "preserve provenance and mapping confidence",
        "preserve explicit ambiguity and Semantic Gap outcomes",
        "produce a deterministic Canonicalization Result",
    ):
        assert phrase in text


def test_s275_forbids_implicit_canonical_mutation() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "MUST NOT create a new canonical entity, attribute, or predicate automatically",
        "MUST NOT mutate canonical facts without an explicit governed application step",
        "MUST NOT infer Canonical Truth from mapping success alone",
        "MUST NOT silently resolve ambiguous mappings",
        "MUST NOT silently discard unmappable data or provenance",
        "MUST NOT import vendor-specific semantics into the Canonical Ontology",
        "MUST NOT rewrite historical Canonicalization Results",
    ):
        assert phrase in text


def test_s275_separates_result_from_graph_application() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Canonicalization Result and Canonical Graph mutation are distinct stages" in text
    assert "MUST NOT be treated as authorization to mutate Canonical Facts" in text
    assert "Every applied graph change MUST remain traceable" in text


def test_s275_supports_replay_without_history_rewrite() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST support replay" in text
    assert "MUST NOT rewrite the historical execution record" in text


def test_s275_requires_explicit_failure_outcomes() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "SHOULD return an explicit non-success outcome" in text
    assert "rather than inventing a Canonical value" in text
