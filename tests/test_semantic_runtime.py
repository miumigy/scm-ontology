from scm_ontology.semantic_runtime import DecisionTrace, build_runtime_pipeline


def test_runtime_pipeline_preserves_trace_provenance_and_request_lineage():
    trace = DecisionTrace("d1", {"action": "expedite"}, evidence=({"fact": "late"},))
    pipeline = build_runtime_pipeline(trace, rationale="supplier delay requires mitigation", request_id="r1")

    assert pipeline.trace is trace
    assert pipeline.provenance.decision_id == "d1"
    assert pipeline.provenance.evidence == trace.evidence
    assert pipeline.request.request_id == "r1"
    assert pipeline.request.decision_id == "d1"
    assert pipeline.request.action == trace.decision
    assert pipeline.request.provenance is pipeline.provenance
