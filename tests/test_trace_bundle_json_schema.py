import json
from pathlib import Path


def test_published_trace_bundle_schema_has_stable_contract():
    schema = json.loads(Path("schemas/trace-bundle.schema.json").read_text())
    assert schema["$id"] == "https://scm-ontology.dev/schema/trace-bundle"
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["properties"]["schema_version"]["const"] == "1.0.0"
    validation = schema["properties"]["bundle"]["properties"]["validation"]
    assert validation["properties"]["valid"]["const"] is True
    assert validation["properties"]["errors"]["const"] == []
