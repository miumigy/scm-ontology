from scm_ontology.trace_bundle_schema import parse_trace_bundle, serialize_trace_bundle


def test_trace_bundle_json_round_trip_preserves_semantic_mapping():
    bundle = {
        "decision_trace": {"trace_id": "t1", "reasoning_result_id": "r1"},
        "execution_request": {"request_id": "x1", "plan_id": "p1"},
        "execution_event": {"event_id": "e1", "plan_id": "p1"},
        "reasoning_provenance": {"provenance_id": "pr1", "advisory_ids": ["a1"]},
        "validation": {"valid": True, "errors": []},
    }
    payload = serialize_trace_bundle(bundle)
    parsed = parse_trace_bundle(payload)
    payload_again = serialize_trace_bundle(parsed.bundle)
    assert parsed.bundle == bundle
    assert payload_again == payload


def test_trace_bundle_round_trip_does_not_silently_drop_empty_fields():
    bundle = {"validation": {"valid": True, "errors": []}, "advisories": []}
    parsed = parse_trace_bundle(serialize_trace_bundle(bundle))
    assert "advisories" in parsed.bundle
    assert parsed.bundle["advisories"] == []
