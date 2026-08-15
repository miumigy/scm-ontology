from scm_ontology.evidence_provenance import EvidenceSet
from scm_ontology.path_evidence import attach_path_evidence, evidence_from_sources
from scm_ontology.relation_path_query import RelationPathMatch


def path() -> RelationPathMatch:
    return RelationPathMatch(
        node_ids=("product:1", "supplier:1", "site:1"),
        relationship_ids=("rel:1", "rel:2"),
    )


def test_attach_path_evidence_preserves_path_and_sources() -> None:
    result = attach_path_evidence(path(), EvidenceSet())
    assert result.path.node_ids[-1] == "site:1"
    assert result.evidence.refs == ()


def test_evidence_from_sources_builds_transport_neutral_refs() -> None:
    result = evidence_from_sources(path(), ("erp:order:1", "wms:stock:2"))
    assert tuple(ref.source_ref for ref in result.evidence.refs) == ("erp:order:1", "wms:stock:2")
