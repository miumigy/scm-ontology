from pathlib import Path


DOC = Path("docs/milestones/S270-m7-canonicalization-batch-reconciliation-contract.md")


def test_s270_defines_reconciliation_identity() -> None:
    text = DOC.read_text(encoding="utf-8")
    for field in (
        "reconciliation_id",
        "execution/result references",
        "adapter version",
        "mapping configuration version",
        "reconciliation scope",
        "reconciliation criteria",
        "created_at",
    ):
        assert field in text
    assert "MUST remain traceable to the individual executions" in text


def test_s270_preserves_individual_provenance() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Aggregated counts MUST NOT erase the underlying result references" in text
    assert "their individual provenance" in text


def test_s270_bounds_reconciliation_scope() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "declared enterprise, source, mapping, version, and time scope" in text
    assert "MUST NOT be generalized beyond that scope" in text


def test_s270_preserves_canonical_truth_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT create a new canonical entity, attribute, or predicate automatically" in text
    assert "MUST NOT mutate canonical facts" in text
    assert "MUST NOT infer canonical facts from aggregate counts or patterns alone" in text
    assert "MUST NOT rewrite historical audit records" in text
    assert "MUST NOT silently change Governance Decisions or approved mappings" in text


def test_s270_limits_governance_handoff() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MAY produce Governance Signals" in text
    assert "MUST retain references to the underlying observations" in text
    assert "MUST NOT itself authorize mapping replacement" in text


def test_s270_requires_explainable_rollup() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "move from the reconciliation summary to the affected individual results" in text
    assert "versions, provenance, and applicable Governance Decisions" in text
