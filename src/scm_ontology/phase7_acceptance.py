"""SCM OS Phase 7 Acceptance (P7-F).

Closes Phase 7 (SCM OS Real Data Plane) with a deterministic acceptance
contract: heterogeneous inputs are adapted, validated, canonicalized, identity
resolved, and converged into a reproducible and traceable reference Canonical
Graph, while preserving the Canonical Truth boundary.

P7-F defines an explicit Phase 7 capability inventory (P7-A..P7-E) and probes
each capability deterministically, folding results into an immutable,
content-addressed ``Phase7AcceptanceReport`` with an overall ``accepted`` flag.
The acceptance gate is two-fold: every capability must be operable, and the
converged reference graph must be reproducible (stable content hash) and
traceable (every node/edge/identity link carries provenance) without claiming
Canonical Truth.

P7-F composes the existing P7-A..P7-E reference paths. It performs no external
side effect and never mutates Canonical Truth.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Callable

from .data_quality_gate import run_reference_data_quality_path
from .identity_resolution_runtime import run_reference_identity_path
from .mapping_canonicalization_runtime import run_reference_mapping_path
from .multi_source_reference import run_multi_source_reference_path
from .reference_data_adapter import run_reference_data_adapter_path


class Phase7AcceptanceError(ValueError):
    """Raised when an acceptance input or invocation is invalid."""


def _converged_probe() -> dict[str, Any]:
    """Probe P7-E and verify reproducibility + traceability + truth boundary."""
    graph = run_multi_source_reference_path()
    # Reproducibility: identical JSON and content hash across runs.
    repeat = run_multi_source_reference_path()
    reproducible = (
        graph.content_hash == repeat.content_hash
        and graph.to_json() == repeat.to_json()
        and graph.node_count == repeat.node_count
    )
    # Traceability: every node carries at least one source member, every edge a
    # provenance, and identity links reference resolved members.
    traceable = (
        all(node.sources for node in graph.nodes)
        and all(edge.provenance for edge in graph.edges)
        and bool(graph.identity_links)
    )
    # The converged view must never claim Canonical Truth.
    reference_boundary = graph.canonical_truth_boundary == "reference"
    accepted = reproducible and traceable and reference_boundary
    return {
        "node_count": graph.node_count,
        "edge_count": graph.edge_count,
        "identity_link_count": len(graph.identity_links),
        "reproducible": reproducible,
        "traceable": traceable,
        "reference_boundary": reference_boundary,
        "accepted": accepted,
    }


_CAPABILITIES: tuple[tuple[str, str, Callable[[], Any]], ...] = (
    (
        "reference_data_adapter",
        "Reference Data Adapter (P7-A)",
        lambda: run_reference_data_adapter_path().to_json(),
    ),
    (
        "mapping_canonicalization",
        "Mapping / Canonicalization Runtime (P7-B)",
        lambda: run_reference_mapping_path().to_json(),
    ),
    (
        "identity_resolution",
        "Identity Resolution Runtime (P7-C)",
        lambda: run_reference_identity_path().to_json(),
    ),
    (
        "data_quality_freshness_gate",
        "Data Quality / Freshness Gate (P7-D)",
        lambda: run_reference_data_quality_path().to_json(),
    ),
    (
        "multi_source_reference_convergence",
        "Multi-source Reference Dataset (P7-E)",
        _converged_probe,
    ),
)



@dataclass(frozen=True)
class CapabilityResult:
    """Deterministic probe result for one Phase 7 capability."""

    key: str
    name: str
    operable: bool
    evidence_id: str
    detail: dict[str, Any] | None = None

    def to_mapping(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "key": self.key,
            "name": self.name,
            "operable": self.operable,
            "evidence_id": self.evidence_id,
        }
        if self.detail is not None:
            value["detail"] = self.detail
        return value


@dataclass(frozen=True)
class AcceptanceSummary:
    """Deterministic aggregate counts across the capability probes."""

    capability_count: int
    operable_count: int
    failed_count: int

    def to_mapping(self) -> dict[str, Any]:
        return {
            "capability_count": self.capability_count,
            "operable_count": self.operable_count,
            "failed_count": self.failed_count,
        }


@dataclass(frozen=True)
class Phase7AcceptanceReport:
    """Immutable, content-addressed Phase 7 acceptance report."""

    report_id: str
    accepted: bool
    accepted_at: str
    capabilities: tuple[CapabilityResult, ...]
    summary: AcceptanceSummary

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P7F.1",
            "is_phase7_acceptance": True,
            "report_id": self.report_id,
            "accepted": self.accepted,
            "accepted_at": self.accepted_at,
            "summary": self.summary.to_mapping(),
            "capabilities": [cap.to_mapping() for cap in self.capabilities],
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def _evidence_id(output: Any) -> str:
    payload = json.dumps(
        output, ensure_ascii=False, sort_keys=True,
        separators=(",", ":"), default=str,
    )
    return sha256(payload.encode()).hexdigest()


def _probe(key: str, name: str, fn: Callable[[], Any]) -> CapabilityResult:
    try:
        output = fn()
    except Exception as exc:  # noqa: BLE001 - acceptance probe must fail closed
        return CapabilityResult(
            key=key, name=name, operable=False,
            evidence_id="", detail={"error": f"{type(exc).__name__}: {exc}"},
        )
    if output is None or output is False:
        return CapabilityResult(
            key=key, name=name, operable=False,
            evidence_id="", detail={"error": "probe produced no usable output"},
        )
    return CapabilityResult(
        key=key, name=name, operable=True, evidence_id=_evidence_id(output),
    )


def run_phase7_acceptance(*, accepted_at: str) -> Phase7AcceptanceReport:
    """Run the Phase 7 capability probes and produce an acceptance report.

    A capability is operable when its deterministic probe returns a usable
    result without error. The phase is accepted when every capability is
    operable, including the P7-E convergence gate (reproducible + traceable +
    reference boundary).
    """
    if not isinstance(accepted_at, str) or not accepted_at.strip():
        raise Phase7AcceptanceError("accepted_at must be non-empty")

    capabilities = tuple(
        _probe(key, name, fn) for key, name, fn in _CAPABILITIES
    )
    operable = sum(1 for cap in capabilities if cap.operable)
    summary = AcceptanceSummary(
        capability_count=len(capabilities),
        operable_count=operable,
        failed_count=len(capabilities) - operable,
    )
    accepted = operable == len(capabilities)

    payload = {
        "accepted_at": accepted_at,
        "capabilities": [cap.to_mapping() for cap in capabilities],
    }
    report_id = sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return Phase7AcceptanceReport(
        report_id=report_id,
        accepted=accepted,
        accepted_at=accepted_at,
        capabilities=tuple(capabilities),
        summary=summary,
    )
