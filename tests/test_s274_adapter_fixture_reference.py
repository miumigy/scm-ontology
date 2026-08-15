from pathlib import Path


DOC = Path("docs/milestones/S274-m7-adapter-fixture-reference.md")


def test_s274_defines_vendor_neutral_fixture_scope() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "material master representation",
        "supplier master representation",
        "site / plant representation",
        "enterprise identifiers",
        "enterprise material classification",
    ):
        assert phrase in text
    assert "vendor-neutral Enterprise Adapter Fixture" in text


def test_s274_uses_existing_canonical_semantics() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST use only mappings that already exist in the Canonical Ontology" in text
    assert "MUST NOT require a new canonical concept" in text


def test_s274_requires_provenance() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "fixture/source record",
        "source field or relation",
        "adapter version",
        "mapping configuration version",
        "mapping decision reference",
    ):
        assert phrase in text


def test_s274_requires_deterministic_and_explicit_results() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "produce deterministic mapping results" in text
    assert "preserve mapping confidence" in text
    assert "represent unsupported or ambiguous input explicitly" in text
    assert "leave Canonical Facts unchanged as an implicit side effect" in text


def test_s274_negative_cases_do_not_expand_canonical_semantics() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "vendor-style classification with no approved Canonical mapping",
        "ambiguous enterprise label",
        "missing provenance",
        "unmappable enterprise field",
    ):
        assert phrase in text
    assert "MUST result in explicit mapping outcomes or Semantic Gap classifications" in text


def test_s274_forbids_canonical_contamination() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "MUST NOT create a new canonical entity, attribute, or predicate automatically",
        "MUST NOT mutate canonical facts",
        "MUST NOT infer Canonical Truth from source labels or vendor-style codes alone",
        "MUST NOT promote an enterprise classification into Canonical Semantics without an approved mapping",
        "MUST NOT silently discard unmappable or ambiguous input",
    ):
        assert phrase in text


def test_s274_fixture_is_replayable() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "stable and versioned" in text
    assert "replay the same input" in text
    assert "without relying on live enterprise systems" in text
