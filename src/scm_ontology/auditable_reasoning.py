"""Deterministic, auditable contract for constraint reasoning results."""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any

from .constraint_reasoning import ConstrainedPathResult


@dataclass(frozen=True)
class ReasoningEvidence:
    relationship_id: str
    predicate: str
    from_id: str
    to_id: str
    qualifiers: dict[str, Any]


@dataclass(frozen=True)
class AuditableReasoningResult:
    result_id: str
    status: str
    at: str
    node_ids: tuple[str, ...]
    checks: tuple[dict[str, Any], ...]
    evidence: tuple[ReasoningEvidence, ...]


def build_reasoning_result(result: ConstrainedPathResult) -> AuditableReasoningResult:
    checks = tuple(
        {"name": c.name, "passed": c.passed, "actual": c.actual, "expected": c.expected, "reason": c.reason}
        for c in result.checks
    )
    evidence = tuple(
        ReasoningEvidence(s.relationship_id, s.predicate, s.from_id, s.to_id, dict(s.qualifiers))
        for s in result.path.steps
    )
    canonical = {
        "status": "feasible" if result.feasible else "infeasible",
        "at": result.path.at,
        "node_ids": result.path.node_ids,
        "checks": checks,
        "evidence": evidence,
    }
    digest = sha256(json.dumps(canonical, default=lambda o: o.__dict__, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return AuditableReasoningResult(digest, canonical["status"], result.path.at, result.path.node_ids, checks, evidence)
