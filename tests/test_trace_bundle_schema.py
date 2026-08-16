from scm_ontology.trace_bundle_schema import SCM_TRACE_SCHEMA_ID, SCM_TRACE_SCHEMA_VERSION, parse_trace_bundle, serialize_trace_bundle


def test_trace_bundle_serialization_is_deterministic_and_versioned():
    first = serialize_trace_bundle({"execution_event_id": "e1", "status": "succeeded"})
    second = serialize_trace_bundle({"status": "succeeded", "execution_event_id": "e1"})
    assert first == second
    parsed = parse_trace_bundle(first)
    assert parsed.schema_id == SCM_TRACE_SCHEMA_ID
    assert parsed.schema_version == SCM_TRACE_SCHEMA_VERSION
    assert parsed.bundle["execution_event_id"] == "e1"


def test_trace_bundle_rejects_unknown_schema_version():
    payload = serialize_trace_bundle({})
    payload = payload.replace(SCM_TRACE_SCHEMA_VERSION, "9.0.0")
    try:
        parse_trace_bundle(payload)
    except ValueError as exc:
        assert "schema version" in str(exc)
    else:
        raise AssertionError("unknown schema version must be rejected")
