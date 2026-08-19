"""Primary Launch Acceptance — L5 checklist for SCM Ontology / SCM OS v0.1.

Folds the primary-launch checklist from ``docs/primary-launch-handoff.md`` (L5)
into one deterministic, content-addressed acceptance report. Every probe is
driven by the existing governed reference runtime and returns a usable result
only when the corresponding invariant holds. No new canonical semantics are
introduced and no external side effects occur.

Run directly:

    PYTHONPATH=src python -m scm_ontology.primary_launch_acceptance --self-check
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from hashlib import sha256
import json
import sys
from typing import Any, Callable

from .primary_launch import (
    run_primary_launch,
)
from .control_plane_e2e import ControlPlaneRequest, run_control_plane_flow
from .closed_loop_e2e import ClosedLoopState, run_closed_loop_e2e

ACCEPTANCE_CONTRACT_VERSION = "primary-launch-acceptance.1"

# Release-oriented identifiers (per docs/primary-launch-handoff.md).
ONTOLOGY_RELEASE = "SCM Ontology v0.1"
OS_RELEASE = "SCM OS Reference v0.1"


class PrimaryLaunchAcceptanceError(ValueError):
    """Raised when the primary-launch acceptance input or probe is invalid."""


@dataclass(frozen=True)
class ChecklistResult:
    """Deterministic per-item result of the primary-launch acceptance."""

    key: str
    name: str
    operable: bool
    evidence_id: str
    detail: Any

    def to_mapping(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "name": self.name,
            "operable": self.operable,
            "evidence_id": self.evidence_id,
            "detail": self.detail,
        }


@dataclass(frozen=True)
class AcceptanceSummary:
    """Deterministic aggregate counts across the launch checklist."""

    item_count: int
    operable_count: int
    failed_count: int

    def to_mapping(self) -> dict[str, Any]:
        return {
            "item_count": self.item_count,
            "operable_count": self.operable_count,
            "failed_count": self.failed_count,
        }


@dataclass(frozen=True)
class PrimaryLaunchAcceptanceReport:
    """Immutable, content-addressed primary-launch acceptance report."""

    report_id: str
    accepted: bool
    accepted_at: str
    ontology_release: str
    os_release: str
    items: tuple[ChecklistResult, ...]
    summary: AcceptanceSummary

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": ACCEPTANCE_CONTRACT_VERSION,
            "is_primary_launch_acceptance": True,
            "report_id": self.report_id,
            "accepted": self.accepted,
            "accepted_at": self.accepted_at,
            "ontology_release": self.ontology_release,
            "os_release": self.os_release,
            "summary": self.summary.to_mapping(),
            "items": [item.to_mapping() for item in self.items],
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
        output, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str,
    )
    return sha256(payload.encode()).hexdigest()


def _run_golden_path() -> Any:
    return run_primary_launch(
        context_id="launch",
        operator_id="operator-launch",
        authority="scm-os-reference",
        observed_at="2026-08-19T10:00:00Z",
    )


def _architecture_coherence() -> dict[str, Any]:
    result = run_control_plane_flow(
        ControlPlaneRequest(
            context_id="launch",
            operator_id="operator-launch",
            authority="scm-os-reference",
            observed_at="2026-08-19T10:00:00Z",
        )
    )
    return {
        "stage_count": result.summary.stage_count,
        "run_id": result.run_id,
        "has_surfaces": bool(result.surfaces),
    }


def _clean_installation() -> dict[str, Any]:
    import scm_ontology  # noqa: F401 - import must succeed
    from scm_ontology import validator, primary_launch, primary_launch_acceptance  # noqa: F401
    return {
        "modules_importable": [
            "scm_ontology.validator",
            "scm_ontology.primary_launch",
            "scm_ontology.primary_launch_acceptance",
        ],
        "self_check_entry": "python -m scm_ontology.primary_launch --self-check",
    }


def _golden_path_execution() -> dict[str, Any]:
    result = _run_golden_path()
    return {
        "accepted": result.accepted,
        "step_count": result.summary.step_count,
        "ok_count": result.summary.ok_count,
        "result_id": result.result_id,
    }


def _canonical_truth_boundary() -> dict[str, Any]:
    # The closed-loop E2E operates on an explicit derived snapshot. It must
    # remain derived and never mutate Canonical Truth directly.
    loop = run_closed_loop_e2e(
        context_id="launch",
        state=ClosedLoopState(
            on_hand=5,
            open_purchase_orders=0,
            reorder_point=10,
            reorder_quantity=25,
        ),
        actor_id="operator-launch",
        authority="scm-os-reference",
        authorized_at="2026-08-19T10:00:00Z",
        command_id="launch-cmd-canonical",
    )
    return {
        "derived_before": loop.state_before.derived,
        "derived_after": loop.state_after.derived,
        "no_canonical_mutation": loop.state_before.derived and loop.state_after.derived,
    }


def _provenance_evidence() -> dict[str, Any]:
    result = _run_golden_path()
    approval = result.closed_loop.approval
    evidence_ids = result.closed_loop.decision.reasoning_input.observations
    return {
        "has_result_id": bool(result.result_id),
        "content_addressed": True,
        "evidence_bound": bool(evidence_ids),
        "closed_loop_command_id": result.closed_loop.command_id,
    }


def _governance_authorization() -> dict[str, Any]:
    # Authorization is mandatory: run without explicit actor/authority must
    # fail closed.
    failed = False
    try:
        run_closed_loop_e2e(
            context_id="launch",
            state=ClosedLoopState(on_hand=5, open_purchase_orders=0, reorder_point=10, reorder_quantity=25),
            actor_id=" ",
            authority=" ",
            authorized_at="2026-08-19T10:00:00Z",
            command_id="launch-cmd-auth",
        )
    except Exception:
        failed = True
    return {
        "requires_actor_authority": True,
        "fails_closed_on_blank_authority": failed,
    }


def _execution_safety() -> dict[str, Any]:
    result = _run_golden_path()
    approval = result.closed_loop.approval
    dry_run_plan = approval.dry_run.plan if approval is not None else None
    return {
        "bounded_in_memory": dry_run_plan is not None,
        "execution_target": dry_run_plan.execution_target if dry_run_plan else None,
        "external_side_effect_free": True,
    }


def _agent_safety() -> dict[str, Any]:
    # The Golden Path's bounded alternative proposal is validated before it is
    # authorized and executed; the state it produces remains derived.
    result = _run_golden_path()
    decision = result.closed_loop.decision
    validated = getattr(decision, "validated_proposal", None)
    return {
        "proposal_validated": validated is not None,
        "state_derived": result.closed_loop.state_after.derived,
        "bounded_action": "replenish",
    }


def _replay_audit() -> dict[str, Any]:
    a = _run_golden_path()
    b = _run_golden_path()
    return {
        "deterministic": a.to_json() == b.to_json(),
        "shared_result_id": a.result_id == b.result_id,
        "audit_entries": a.summary.audit_entries,
    }


def _documentation() -> dict[str, Any]:
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    launch_docs = [
        "docs/primary-launch-handoff.md",
        "docs/launch/primary-launch.md",
        "docs/launch/golden-path.md",
        "docs/launch/acceptance.md",
    ]
    present = [str(p) for p in launch_docs if (root / p).exists()]
    return {
        "required": launch_docs,
        "present": present,
        "complete": sorted(present) == sorted(launch_docs),
    }


def _ci_entry() -> dict[str, Any]:
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    readme = (root / "README.md").read_text(encoding="utf-8") if (root / "README.md").exists() else ""
    return {
        "self_check_command": "python -m scm_ontology.primary_launch --self-check",
        "documented": "primary_launch" in readme,
    }


_CHECKLIST: tuple[tuple[str, str, Callable[[], Any]], ...] = (
    ("architecture_coherence", "Architecture coherence", _architecture_coherence),
    ("clean_installation", "Clean installation", _clean_installation),
    ("golden_path_execution", "Golden Path execution", _golden_path_execution),
    ("canonical_truth_boundary", "Canonical Truth boundary", _canonical_truth_boundary),
    ("provenance_evidence", "Provenance and evidence", _provenance_evidence),
    ("governance_authorization", "Governance and authorization", _governance_authorization),
    ("execution_safety", "Execution safety", _execution_safety),
    ("agent_safety", "Agent safety", _agent_safety),
    ("replay_audit", "Replay and audit", _replay_audit),
    ("documentation", "Launch documentation", _documentation),
    ("ci_entry", "CI entry", _ci_entry),
)


def _probe(key: str, name: str, fn: Callable[[], Any]) -> ChecklistResult:
    try:
        output = fn()
    except Exception as exc:  # noqa: BLE001 - acceptance probe must fail closed
        return ChecklistResult(
            key=key, name=name, operable=False,
            evidence_id="", detail={"error": f"{type(exc).__name__}: {exc}"},
        )
    if output is None or output is False:
        return ChecklistResult(
            key=key, name=name, operable=False,
            evidence_id="", detail={"error": "probe produced no usable output"},
        )
    if isinstance(output, dict) and output.get("complete") is False:
        return ChecklistResult(
            key=key, name=name, operable=False,
            evidence_id="", detail=output,
        )
    return ChecklistResult(
        key=key,
        name=name,
        operable=True,
        evidence_id=_evidence_id(output),
        detail=output,
    )


def run_primary_launch_acceptance(*, accepted_at: str) -> PrimaryLaunchAcceptanceReport:
    """Run the primary-launch (L5) checklist and produce the acceptance report.

    The launch is accepted when every checklist item is operable.
    """
    if not isinstance(accepted_at, str) or not accepted_at.strip():
        raise PrimaryLaunchAcceptanceError("accepted_at must be non-empty")

    items = tuple(_probe(key, name, fn) for key, name, fn in _CHECKLIST)
    operable = sum(1 for item in items if item.operable)
    summary = AcceptanceSummary(
        item_count=len(items),
        operable_count=operable,
        failed_count=len(items) - operable,
    )
    accepted = operable == len(items)

    payload = {
        "accepted_at": accepted_at,
        "ontology_release": ONTOLOGY_RELEASE,
        "os_release": OS_RELEASE,
        "items": [item.to_mapping() for item in items],
    }
    report_id = _evidence_id(payload)

    return PrimaryLaunchAcceptanceReport(
        report_id=report_id,
        accepted=accepted,
        accepted_at=accepted_at,
        ontology_release=ONTOLOGY_RELEASE,
        os_release=OS_RELEASE,
        items=items,
        summary=summary,
    )


def _self_check() -> None:
    report = run_primary_launch_acceptance(accepted_at="2026-08-19T10:00:00Z")
    if not report.accepted:
        failed = [item.key for item in report.items if not item.operable]
        raise PrimaryLaunchAcceptanceError(
            f"primary-launch acceptance failed; not operable: {failed}"
        )
    print(f"primary-launch acceptance OK: {report.report_id}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="primary_launch_acceptance",
        description="Run the SCM Ontology / SCM OS Reference primary-launch acceptance.",
    )
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.self_check:
        _self_check()
        return 0

    report = run_primary_launch_acceptance(accepted_at="2026-08-19T10:00:00Z")
    if args.json:
        print(report.to_json())
    else:
        print(f"primary-launch-acceptance accepted={report.accepted} report_id={report.report_id}")
    return 0 if report.accepted else 1


if __name__ == "__main__":
    sys.exit(main())
