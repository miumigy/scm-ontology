import pytest

from scm_ontology.evidence_provenance import EvidenceSet
from scm_ontology.path_evidence import PathEvidence
from scm_ontology.path_reasoning_result import PathReasoningResult, PathReasoningResultError
from scm_ontology.relation_path_query import RelationPathMatch


def test_path_reasoning_result_preserves_evidenced_paths() -> None:
    path = RelationPathMatch(("product:1", "supplier:1", "site:1"), ("rel:1", "rel:2"))
    result = PathReasoningResult("path-result:1", "matched", (PathEvidence(path, EvidenceSet()),))
    assert result.paths[0].path.node_ids[-1] == "site:1"


def test_path_reasoning_result_rejects_non_path_evidence() -> None:
    with pytest.raises(PathReasoningResultError):
        PathReasoningResult("path-result:1", "matched", ("not-path-evidence",))
