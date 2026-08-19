from pathlib import Path


DOC = Path("docs/history/phase7/S263-m7-adapter-audit-contract.md")


def test_s263_preserves_audit_lineage() -> None:
    text = DOC.read_text(encoding="utf-8")
    for field in (
        "audit_id",
        "result_id",
        "source_representation",
        "mapping_rule_id",
        "adapter_version",
        "decision_state",
        "provenance",
        "semantic_gap",
        "reason",
        "transformation_metadata",
        "recorded_at",
    ):
        assert f"`{field}`" in text


def test_s263_requires_append_only_audit_history() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "audit history MUST be append-only" in text
    assert "MUST NOT silently rewriting the historical decision" in text


def test_s263_separates_recorded_time_from_business_time() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "recorded_at" in text
    assert "MUST NOT be confused with the effective time" in text


def test_s263_preserves_non_mapped_decisions() -> None:
    text = DOC.read_text(encoding="utf-8")
    for state in (
        "ambiguous",
        "unmappable",
        "unsupported",
        "vendor_specific",
        "insufficient_evidence",
        "conflicting_semantics",
        "rejected",
    ):
        assert f"`{state}`" in text


def test_s263_separates_audit_from_canonical_truth() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT be interpreted as a Canonical Fact" in text
    assert "MUST NOT be used as an implicit canonical-fact ingestion mechanism" in text


def test_s263_forbids_canonical_mutation() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT create a new canonical entity, attribute, or predicate automatically" in text
    assert "MUST NOT mutate canonical facts" in text
    assert "MUST NOT infer a canonical fact from an audit record alone" in text


def test_s263_separates_governance_from_audit_recording() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "separate workflows" in text
    assert "MUST NOT mutate the Canonical Ontology as a side effect of audit recording" in text
