"""Versioned serialization contract for validated SCM lifecycle traces."""
from __future__ import annotations
from dataclasses import dataclass
import json
from typing import Any

SCM_TRACE_SCHEMA_ID = "https://scm-ontology.dev/schema/trace-bundle"
SCM_TRACE_SCHEMA_VERSION = "1.0.0"

@dataclass(frozen=True)
class TraceBundleDocument:
    schema_id: str
    schema_version: str
    bundle: dict[str, Any]

def serialize_trace_bundle(bundle: dict[str, Any]) -> str:
    document = {"$schema": SCM_TRACE_SCHEMA_ID, "schema_version": SCM_TRACE_SCHEMA_VERSION, "bundle": bundle}
    return json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def parse_trace_bundle(payload: str) -> TraceBundleDocument:
    document = json.loads(payload)
    if not isinstance(document, dict):
        raise ValueError("trace bundle document must be an object")
    if document.get("$schema") != SCM_TRACE_SCHEMA_ID:
        raise ValueError("unsupported trace bundle schema")
    if document.get("schema_version") != SCM_TRACE_SCHEMA_VERSION:
        raise ValueError("unsupported trace bundle schema version")
    bundle = document.get("bundle")
    if not isinstance(bundle, dict):
        raise ValueError("trace bundle bundle must be an object")
    return TraceBundleDocument(SCM_TRACE_SCHEMA_ID, SCM_TRACE_SCHEMA_VERSION, bundle)
