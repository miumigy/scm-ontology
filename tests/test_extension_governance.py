from scm_ontology.extension_candidate_report import build_extension_candidate_report
from scm_ontology.extension_governance import ExtensionDecision, initial_extension_decision
from scm_ontology.relation_validation_batch import validate_relations


def test_extension_candidate_starts_pending() -> None:
    results = validate_relations((("customer_specific_relation", "Order", "Location"),))
    report = build_extension_candidate_report(results)
    assert len(report.candidates) == 1
    assert initial_extension_decision(report.candidates[0]) is ExtensionDecision.PENDING
