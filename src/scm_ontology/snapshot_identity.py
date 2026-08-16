"""Deterministic identity for reproducible SCM snapshots."""
from __future__ import annotations
import hashlib
import json
from .temporal_snapshot import SCMSnapshot

def snapshot_fingerprint(snapshot: SCMSnapshot) -> str:
    payload = {
        "at": snapshot.at,
        "facts": [
            {"fact_id": f.fact_id, "predicate": f.predicate, "subject_id": f.subject_id, "value": f.value,
             "provenance": {"source": f.provenance.source, "source_record": f.provenance.source_record,
                             "observed_at": f.provenance.observed_at, "valid_from": f.provenance.valid_from,
                             "valid_to": f.provenance.valid_to, "confidence": f.provenance.confidence}}
            for f in sorted(snapshot.facts, key=lambda x: x.fact_id)
        ],
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
