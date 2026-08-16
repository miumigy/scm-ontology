"""Stable, JSON-safe contract for end-to-end accountability results."""
from __future__ import annotations
import json
from dataclasses import fields, is_dataclass
from typing import Any
from .end_to_end_accountability import EndToEndAccountability

ACCOUNTABILITY_CONTRACT_VERSION = "1.0.0"

class AccountabilityContractError(ValueError):
    pass

def _json_safe(value: Any) -> Any:
    if is_dataclass(value):
        return {field.name: _json_safe(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, tuple):
        return [_json_safe(v) for v in value]
    if isinstance(value, dict):
        payload = {str(k): _json_safe(v) for k, v in value.items()}
        evidence_id = getattr(value, "evidence_id", None)
        if evidence_id is not None:
            payload = {"evidence_id": evidence_id, **payload}
        return payload
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise AccountabilityContractError(f"unsupported accountability value: {type(value).__name__}")

def accountability_to_mapping(result: EndToEndAccountability) -> dict[str, Any]:
    evidence_records: list[Any] = []
    for accountability in result.evidence:
        evidence = accountability.evidence
        if isinstance(evidence, tuple):
            evidence_records.extend(evidence)
            continue
        # Backward-compatible shape: EvidenceAccountability(evidence_id, fact).
        serialized = _json_safe(evidence)
        if isinstance(serialized, dict):
            evidence_records.append({"evidence_id": accountability.evidence_id, **serialized})
        else:
            evidence_records.append({"evidence_id": accountability.evidence_id, "value": serialized})
    return {
        "contract_version": ACCOUNTABILITY_CONTRACT_VERSION,
        "decision": _json_safe(result.decision),
        "evidence": _json_safe(tuple(evidence_records)),
        "provenance": _json_safe(result.provenance),
    }

def accountability_to_json(result: EndToEndAccountability) -> str:
    return json.dumps(accountability_to_mapping(result), ensure_ascii=False, sort_keys=True)
