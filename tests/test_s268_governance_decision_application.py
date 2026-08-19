from pathlib import Path


DOC = Path("docs/history/phase7/S268-m7-governance-decision-application-contract.md")


def test_s268_requires_approved_scoped_decision() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "the decision state is `approved`" in text
    assert "the approved scope is explicit" in text
    assert "application MUST NOT proceed silently" in text


def test_s268_is_forward_only() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "changes the configuration used by subsequent canonicalization executions" in text
    assert "MUST NOT silently modify historical audit records" in text
    assert "Historical executions remain associated" in text


def test_s268_requires_version_traceability() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "mapping configuration version" in text
    assert "Governance Decision" in text
    assert "mapping rule version" in text
    assert "adapter version" in text


def test_s268_preserves_canonical_truth_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT create a new canonical entity, attribute, or predicate automatically" in text
    assert "MUST NOT mutate existing canonical facts as a side effect" in text
    assert "MUST NOT infer a canonical fact from the approval or configuration change alone" in text
    assert "MUST NOT rewrite historical audit records" in text
    assert "MUST NOT retroactively reclassify prior canonicalization results" in text


def test_s268_isolates_scope() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT implicitly apply to unrelated representations" in text
    assert "Vendor-specific semantics remain behind the Adapter Boundary" in text


def test_s268_requires_observable_failure_handling() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "previous effective configuration MUST remain identifiable" in text
    assert "A partial application MUST be observable" in text
    assert "MUST NOT be represented as a successful governance decision application" in text
