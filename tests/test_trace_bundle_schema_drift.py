import json
from pathlib import Path

from scm_ontology.trace_bundle_schema import SCM_TRACE_SCHEMA_ID, SCM_TRACE_SCHEMA_VERSION

SCHEMA_PATH = Path("schemas/trace-bundle.schema.json")


def test_python_and_published_schema_contract_cannot_drift():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    assert schema["$id"] == SCM_TRACE_SCHEMA_ID
    assert schema["properties"]["$schema"]["const"] == SCM_TRACE_SCHEMA_ID
    assert schema["properties"]["schema_version"]["const"] == SCM_TRACE_SCHEMA_VERSION
    bundle = schema["properties"]["bundle"]
    assert set(bundle["required"]) == {"decision_trace", "execution_request", "execution_event", "reasoning_provenance", "validation"}


def test_schema_requires_a_successfully_validated_bundle():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validation = schema["properties"]["bundle"]["properties"]["validation"]
    assert validation["properties"]["valid"]["const"] is True
    assert validation["properties"]["errors"]["const"] == []
