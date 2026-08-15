import pytest

from scm_ontology.evidence_provenance import EvidenceProvenanceError, EvidenceRef, EvidenceSet


def test_evidence_set_preserves_distinct_source_refs() -> None:
    evidence = EvidenceSet(
        refs=(
            EvidenceRef("erp:order:123", observed_at="2026-08-15T00:00:00Z"),
            EvidenceRef("wms:stock:456"),
        )
    )
    assert tuple(ref.source_ref for ref in evidence.refs) == ("erp:order:123", "wms:stock:456")


def test_evidence_set_rejects_duplicate_source_refs() -> None:
    with pytest.raises(EvidenceProvenanceError):
        EvidenceSet(refs=(EvidenceRef("erp:order:123"), EvidenceRef("erp:order:123")))
