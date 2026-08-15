from scm_ontology.evidence_provenance import EvidenceSet, EvidenceRef
from scm_ontology.path_evidence import PathEvidence
from scm_ontology.path_reasoning_result import PathReasoningResult
from scm_ontology.reasoning_explanation import ExplanationStep, explain_path_reasoning
from scm_ontology.relation_path_query import RelationPathMatch


def test_explanation_contains_relationships_and_evidence() -> None:
    path = RelationPathMatch(("product:1", "supplier:1", "site:1"), ("rel:1", "rel:2"))
    result = PathReasoningResult(
        "result:1",
        "matched",
        (PathEvidence(path, EvidenceSet((EvidenceRef("erp:order:1"),))),),
    )
    explanation = explain_path_reasoning(result)
    assert explanation.steps == (
        ExplanationStep("relationship", "rel:1"),
        ExplanationStep("relationship", "rel:2"),
        ExplanationStep("evidence", "erp:order:1"),
    )


def test_explanation_for_empty_result_is_still_explicit() -> None:
    explanation = explain_path_reasoning(PathReasoningResult("result:2", "no_match"))
    assert explanation.steps == (ExplanationStep("result", "no_match"),)
