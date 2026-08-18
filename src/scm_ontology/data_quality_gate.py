"""P7-D Data Quality / Freshness Gate (Phase 7, SCM OS Real Data Plane).

A deterministic, read-only gate that validates the completeness, freshness,
scope, unit, and provenance of P7-A ``SourceEvidence`` before it proceeds to
canonicalization. The gate is fail-closed: a batch that fails any required check
is flagged as ``blocked`` and never silently proceeds.

P7-D composes the P7-A Reference Data Adapter (``SourceDataset`` /
``SourceEvidence``). It DOES NOT map, resolve identity, or mutate Canonical
Truth: it only *validates evidence* and reports explicit per-record, per-check
outcomes. A quality gate report is metadata about the evidence, never Canonical
Truth. Provenance, scope, temporal (freshness), unit, and completeness are
validated at the evidence boundary (S309 / P7-D roadmap contract).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import json
from typing import Sequence

from .reference_data_adapter import SourceDataset, SourceEvidence


class DataQualityGateError(ValueError):
    """Raised when a gate policy or an evidence batch is invalid."""


class CheckType(str):
    COMPLETENESS = "completeness"
    FRESHNESS = "freshness"
    SCOPE = "scope"
    UNIT = "unit"
    PROVENANCE = "provenance"


class CheckOutcome(str):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


# ---------------------------------------------------------------------------
# Policy
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class UnitConstraint:
    """Allowed unit for a declared evidence field (representation only)."""

    field: str
    allowed_units: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.field.strip():
            raise DataQualityGateError("field must be non-empty")
        if not self.allowed_units:
            raise DataQualityGateError("allowed_units must be non-empty")
        if any(not unit.strip() for unit in self.allowed_units):
            raise DataQualityGateError("allowed_units entries must be non-empty")


@dataclass(frozen=True)
class DataQualityPolicy:
    """Quality / freshness gate configuration with explicit scope bounds."""

    policy_id: str
    policy_version: str
    required_fields: tuple[str, ...] = ()
    allowed_scopes: tuple[str, ...] = ()
    unit_constraints: tuple[UnitConstraint, ...] = ()
    max_age_seconds: float | None = None
    provenance_required: bool = True

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise DataQualityGateError("policy_id must be non-empty")
        if not self.policy_version.strip():
            raise DataQualityGateError("policy_version must be non-empty")
        if any(not field_name.strip() for field_name in self.required_fields):
            raise DataQualityGateError("required_fields entries must be non-empty")
        if any(not scope.strip() for scope in self.allowed_scopes):
            raise DataQualityGateError("allowed_scopes entries must be non-empty")
        fields = [constraint.field for constraint in self.unit_constraints]
        if len(fields) != len(set(fields)):
            raise DataQualityGateError("unit_constraints fields must be unique")


@dataclass(frozen=True)
class QualityCheckResult:
    """Explicit outcome of one quality check on one record."""

    check: str
    outcome: str
    message: str = ""

    def __post_init__(self) -> None:
        if self.check not in {
            CheckType.COMPLETENESS, CheckType.FRESHNESS, CheckType.SCOPE,
            CheckType.UNIT, CheckType.PROVENANCE,
        }:
            raise DataQualityGateError(f"invalid check: {self.check}")
        if self.outcome not in {CheckOutcome.PASS, CheckOutcome.WARN, CheckOutcome.FAIL}:
            raise DataQualityGateError(f"invalid outcome: {self.outcome}")


@dataclass(frozen=True)
class RecordQuality:
    """Per-record quality summary with explicit per-check outcomes."""

    evidence_id: str
    source_system: str
    source_location: str
    record_id: str
    checks: tuple[QualityCheckResult, ...] = field(default_factory=tuple)

    @property
    def passed(self) -> bool:
        return all(check.outcome == CheckOutcome.PASS for check in self.checks)

    @property
    def failed_checks(self) -> tuple[str, ...]:
        return tuple(check.check for check in self.checks if check.outcome == CheckOutcome.FAIL)


@dataclass(frozen=True)
class DataQualityReport:
    """Deterministic quality gate report over an evidence batch."""

    run_id: str
    policy: DataQualityPolicy
    records: tuple[RecordQuality, ...] = field(default_factory=tuple)

    @property
    def evaluated_count(self) -> int:
        return len(self.records)

    @property
    def passed_count(self) -> int:
        return sum(1 for record in self.records if record.passed)

    @property
    def failed_count(self) -> int:
        return self.evaluated_count - self.passed_count

    @property
    def blocked(self) -> bool:
        return self.failed_count > 0

    @property
    def all_passed(self) -> bool:
        return self.evaluated_count > 0 and self.failed_count == 0

    def to_json(self) -> str:
        return json.dumps(
            {
                "contract_version": "P7D.1",
                "run_id": self.run_id,
                "policy_id": self.policy.policy_id,
                "policy_version": self.policy.policy_version,
                "evaluated_count": self.evaluated_count,
                "passed_count": self.passed_count,
                "failed_count": self.failed_count,
                "blocked": self.blocked,
                "records": [
                    {
                        "evidence_id": record.evidence_id,
                        "source_system": record.source_system,
                        "passed": record.passed,
                        "failed_checks": list(record.failed_checks),
                        "checks": [
                            {"check": check.check, "outcome": check.outcome, "message": check.message}
                            for check in record.checks
                        ],
                    }
                    for record in self.records
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def _parse_time(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise DataQualityGateError(f"invalid ISO-8601 timestamp: {value!r}") from exc


def _run_hash(*parts: str) -> str:
    from hashlib import sha256

    joined = "\u001f".join(parts)
    return sha256(joined.encode("utf-8")).hexdigest()[:32]


class DataQualityGate:
    """Deterministic, read-only quality / freshness gate over source evidence.

    ``evaluate`` runs every check for every record in a ``SourceDataset`` and
    returns an immutable ``DataQualityReport`` with an explicit ``blocked`` flag.
    """

    def __init__(self, policy: DataQualityPolicy, *, now: str) -> None:
        self.policy = policy
        self._now = _parse_time(now)

    def evaluate(self, dataset: SourceDataset) -> DataQualityReport:
        records = tuple(self._evaluate_record(record) for record in dataset.records)
        run_id = _run_hash(
            self.policy.policy_version, dataset.manifest.extracted_at,
            *[record.evidence_id for record in dataset.records],
        )
        return DataQualityReport(run_id=run_id, policy=self.policy, records=records)

    def evaluate_many(self, datasets: Sequence[SourceDataset]) -> DataQualityReport:
        records: list[RecordQuality] = []
        for dataset in datasets:
            records.extend(self._evaluate_record(record) for record in dataset.records)
        return DataQualityReport(
            run_id=_run_hash(self.policy.policy_version, "many", *[r.evidence_id for r in records]),
            policy=self.policy,
            records=tuple(records),
        )

    def _evaluate_record(self, record: SourceEvidence) -> RecordQuality:
        checks = (
            self._check_completeness(record),
            self._check_freshness(record),
            self._check_scope(record),
            self._check_unit(record),
            self._check_provenance(record),
        )
        return RecordQuality(
            evidence_id=record.evidence_id,
            source_system=record.source_system,
            source_location=record.source_location,
            record_id=record.record_id,
            checks=checks,
        )

    def _check_completeness(self, record: SourceEvidence) -> QualityCheckResult:
        missing = [field_name for field_name in self.policy.required_fields if field_name not in record.payload]
        if not missing:
            return QualityCheckResult(CheckType.COMPLETENESS, CheckOutcome.PASS)
        return QualityCheckResult(
            CheckType.COMPLETENESS, CheckOutcome.FAIL,
            message=f"missing required fields: {', '.join(missing)}",
        )

    def _check_freshness(self, record: SourceEvidence) -> QualityCheckResult:
        if self.policy.max_age_seconds is None:
            return QualityCheckResult(
                CheckType.FRESHNESS, CheckOutcome.PASS, message="no freshness policy",
            )
        try:
            observed = _parse_time(record.observed_at)
        except DataQualityGateError:
            return QualityCheckResult(
                CheckType.FRESHNESS, CheckOutcome.FAIL,
                message="unparseable observed_at",
            )
        age = (self._now - observed).total_seconds()
        if age <= self.policy.max_age_seconds:
            return QualityCheckResult(
                CheckType.FRESHNESS, CheckOutcome.PASS,
                message=f"age {age:.0f}s within limit",
            )
        return QualityCheckResult(
            CheckType.FRESHNESS, CheckOutcome.FAIL,
            message=f"stale: age {age:.0f}s > {self.policy.max_age_seconds:.0f}s",
        )

    def _check_scope(self, record: SourceEvidence) -> QualityCheckResult:
        if not self.policy.allowed_scopes:
            return QualityCheckResult(CheckType.SCOPE, CheckOutcome.PASS)
        if record.scope in self.policy.allowed_scopes:
            return QualityCheckResult(CheckType.SCOPE, CheckOutcome.PASS)
        return QualityCheckResult(
            CheckType.SCOPE, CheckOutcome.FAIL,
            message=f"scope {record.scope!r} not allowed",
        )

    def _check_unit(self, record: SourceEvidence) -> QualityCheckResult:
        for constraint in self.policy.unit_constraints:
            value = record.payload.get(constraint.field)
            if value is None:
                continue
            if str(value) in constraint.allowed_units:
                continue
            return QualityCheckResult(
                CheckType.UNIT, CheckOutcome.FAIL,
                message=f"unit {value!r} for {constraint.field!r} not allowed",
            )
        return QualityCheckResult(CheckType.UNIT, CheckOutcome.PASS)

    def _check_provenance(self, record: SourceEvidence) -> QualityCheckResult:
        if not self.policy.provenance_required:
            return QualityCheckResult(CheckType.PROVENANCE, CheckOutcome.PASS)
        if not record.source_location:
            return QualityCheckResult(
                CheckType.PROVENANCE, CheckOutcome.FAIL, message="missing source_location",
            )
        if not record.field_evidence:
            return QualityCheckResult(
                CheckType.PROVENANCE, CheckOutcome.FAIL, message="missing field-level provenance",
            )
        return QualityCheckResult(CheckType.PROVENANCE, CheckOutcome.PASS)


# ---------------------------------------------------------------------------
# Deterministic reference path
# ---------------------------------------------------------------------------
REFERENCE_POLICY = DataQualityPolicy(
    policy_id="p7d-reference-policy",
    policy_version="P7D.1",
    required_fields=("material_id", "description"),
    allowed_scopes=("enterprise:acme",),
    max_age_seconds=86400.0,
)


def run_reference_data_quality_path() -> DataQualityReport:
    """Deterministic reference path: P7-A evidence -> quality gate."""
    from .reference_data_adapter import (
        CsvAdapterConfig,
        SourceManifest,
        adapt_csv,
    )

    now = "2026-08-19T09:30:00Z"
    manifest = SourceManifest(
        source_system="erp",
        adapter_version="P7A.1",
        data_contract_version="P7A.1",
        mapping_config_version="M8-reference",
        extracted_at="2026-08-19T09:00:00Z",
        scope="enterprise:acme",
        adapter_kind="csv",
    )
    dataset = adapt_csv(
        [
            {"material_id": "MAT-1000", "description": "Raw aluminium", "plant": "PLT-E"},
            {"material_id": "MAT-1001", "description": "Finished assembly", "plant": "PLT-E"},
        ],
        manifest,
        CsvAdapterConfig(source_system="erp", record_id_column="material_id"),
    )
    return DataQualityGate(REFERENCE_POLICY, now=now).evaluate(dataset)
