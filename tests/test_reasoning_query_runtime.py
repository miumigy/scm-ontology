from scm_ontology.constraint_reasoning import PathConstraint
from scm_ontology.reasoning_query import ReasoningQuery, ReasoningQueryError, ReasoningQueryRuntime, reasoning_result_to_mapping
from scm_ontology.semantic_query import SemanticPathStep, SemanticSupplyChainPath


def _path(at="2026-06-01T00:00:00+00:00"):
    return SemanticSupplyChainPath(
        at=at,
        node_ids=("supplier", "factory"),
        steps=(SemanticPathStep("r1", "supplies", "supplier", "factory", {"lead_time_days": 3}),),
    )


def test_runtime_returns_stable_agent_contract():
    query = ReasoningQuery(_path().at, _path(), PathConstraint(max_total_lead_time_days=5))
    result = ReasoningQueryRuntime().execute(query)
    payload = reasoning_result_to_mapping(result)
    assert payload["status"] == "feasible"
    assert payload["result_id"] == result.result_id
    assert payload["evidence"][0]["relationship_id"] == "r1"


def test_runtime_rejects_timestamp_mismatch():
    try:
        ReasoningQueryRuntime().execute(
            ReasoningQuery("2026-06-02T00:00:00+00:00", _path(), PathConstraint())
        )
    except ReasoningQueryError as exc:
        assert "timestamp" in str(exc)
    else:
        raise AssertionError("timestamp mismatch must be rejected")
