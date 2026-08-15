from scm_ontology.evidence_aggregation import aggregate_evidence
from scm_ontology.evidence_provenance import EvidenceRef, EvidenceSet


def test_aggregate_evidence_deduplicates_source_refs() -> None:
    result = aggregate_evidence(
        EvidenceSet((EvidenceRef("erp:1"), EvidenceRef("wms:1"))),
        EvidenceSet((EvidenceRef("wms:1"), EvidenceRef("tms:1"))),
    )
    assert tuple(ref.source_ref for ref in result.evidence.refs) == ("erp:1", "wms:1", "tms:1")
    assert result.source_count == 3


def test_aggregate_empty_evidence_is_explicit() -> None:
    result = aggregate_evidence(EvidenceSet(), EvidenceSet())
    assert result.evidence.refs == ()
    assert result.source_count == 0
