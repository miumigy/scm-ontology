"""Audit provenance of advisory inputs used by a reasoning decision."""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Iterable

from .reasoning_advisory import ReasoningAdvisory


@dataclass(frozen=True)
class ReasoningProvenance:
    provenance_id: str
    reasoning_result_id: str
    advisory_ids: tuple[str, ...]
    canonical_fact_only: bool


def record_reasoning_provenance(reasoning_result_id: str, advisories: Iterable[ReasoningAdvisory]) -> ReasoningProvenance:
    """Record advisory provenance without changing the reasoning result or facts."""
    if not reasoning_result_id.strip():
        raise ValueError("reasoning_result_id must be non-empty")
    advisory_ids = tuple(sorted({item.advisory_id for item in advisories}))
    canonical = {"reasoning_result_id": reasoning_result_id, "advisory_ids": list(advisory_ids)}
    provenance_id = sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return ReasoningProvenance(provenance_id, reasoning_result_id, advisory_ids, not advisory_ids)


def reasoning_provenance_to_mapping(item: ReasoningProvenance) -> dict[str, Any]:
    return {"provenance_id": item.provenance_id, "reasoning_result_id": item.reasoning_result_id, "advisory_ids": list(item.advisory_ids), "canonical_fact_only": item.canonical_fact_only}
