from scm_ontology.learned_knowledge import learned_knowledge_to_mapping, promote_learning_evidence
from scm_ontology.learning_evidence import LearningEvidence


def test_learned_knowledge_is_separate_empirical_layer_and_deterministic():
    evidence = LearningEvidence("lead_time_days", 3, 1.5, -1, 4, "persistent_positive_variance", ("e1", "e2", "e3"))
    first = promote_learning_evidence(evidence, confidence=0.8)
    second = promote_learning_evidence(evidence, confidence=0.8)
    assert first == second
    assert first.source_layer == "empirical"
    assert first.evidence_count == 3
    assert first.source_event_ids == ("e1", "e2", "e3")
    assert "Observed lead_time_days variance" in first.statement
    assert learned_knowledge_to_mapping([first])["learned_knowledge"][0]["source_layer"] == "empirical"


def test_confidence_is_bounded():
    evidence = LearningEvidence("cost", 1, 2, 2, 2, "persistent_positive_variance", ("e1",))
    for value in (-0.1, 1.1):
        try:
            promote_learning_evidence(evidence, confidence=value)
        except ValueError:
            pass
        else:
            raise AssertionError("confidence outside [0,1] must be rejected")
