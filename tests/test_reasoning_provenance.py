from scm_ontology.reasoning_advisory import ReasoningAdvisory
from scm_ontology.reasoning_provenance import record_reasoning_provenance, reasoning_provenance_to_mapping


def test_reasoning_provenance_is_deterministic_and_records_advisories():
    items = [ReasoningAdvisory("b", "b", "cost", "cost variance", 0.8), ReasoningAdvisory("a", "a", "lead_time_days", "lead time variance", 0.9)]
    first = record_reasoning_provenance("reason-1", items)
    second = record_reasoning_provenance("reason-1", reversed(items))
    assert first == second
    assert first.advisory_ids == ("a", "b")
    assert first.canonical_fact_only is False
    assert reasoning_provenance_to_mapping(first)["reasoning_result_id"] == "reason-1"


def test_reasoning_provenance_marks_canonical_only_when_no_advisory_is_used():
    result = record_reasoning_provenance("reason-2", [])
    assert result.canonical_fact_only is True
    assert result.advisory_ids == ()


def test_reasoning_result_id_is_required():
    try:
        record_reasoning_provenance("", [])
    except ValueError as exc:
        assert "reasoning_result_id" in str(exc)
    else:
        raise AssertionError("empty reasoning_result_id must be rejected")
