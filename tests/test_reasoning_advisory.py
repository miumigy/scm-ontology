from scm_ontology.learned_knowledge import LearnedKnowledge
from scm_ontology.reasoning_advisory import build_reasoning_advisories, reasoning_advisories_to_mapping


def test_learned_knowledge_enters_reasoning_only_as_advisory():
    item = LearnedKnowledge("k1", "lead_time_days", "Observed lead time variance mean is 1.8 across 20 execution events", 0.9, 20, ("e1",), "empirical")
    advisories = build_reasoning_advisories([item], min_confidence=0.8)
    assert len(advisories) == 1
    assert advisories[0].knowledge_id == "k1"
    assert advisories[0].mode == "advisory"
    assert reasoning_advisories_to_mapping(advisories)["advisories"][0]["confidence"] == 0.9


def test_low_confidence_advisory_is_filtered():
    item = LearnedKnowledge("k1", "cost", "Observed cost variance mean is 2 across 2 execution events", 0.4, 2, ("e1", "e2"), "empirical")
    assert build_reasoning_advisories([item], min_confidence=0.5) == ()


def test_non_empirical_knowledge_cannot_enter_advisory_boundary():
    item = LearnedKnowledge("k1", "cost", "canonical-looking statement", 1.0, 1, ("e1",), "canonical")
    try:
        build_reasoning_advisories([item])
    except ValueError as exc:
        assert "empirical" in str(exc)
    else:
        raise AssertionError("non-empirical knowledge must be rejected")
