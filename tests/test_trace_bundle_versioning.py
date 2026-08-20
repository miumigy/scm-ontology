import json
from pathlib import Path


def test_trace_bundle_versioning_policy_is_documented():
    policy = Path("docs/reference/trace-bundle-versioning.md").read_text(encoding="utf-8")
    assert "PATCH" in policy
    assert "MINOR" in policy
    assert "MAJOR" in policy
    assert "1.0.0" in policy


def test_trace_bundle_schema_declares_initial_version():
    schema = json.loads(Path("schemas/trace-bundle.schema.json").read_text(encoding="utf-8"))
    assert schema["properties"]["schema_version"]["const"] == "1.0.0"
