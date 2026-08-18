"""P7-A Reference Data Adapter (Phase 7, SCM OS Real Data Plane).

Portable CSV / JSON / SQL source adapters that turn heterogeneous enterprise
representations into an explicit, provenance-bearing **source evidence** set.

P7-A is strictly the *adapter* side of the Post-M8 data plane. It extracts
enterprise rows and packages them as immutable ``SourceEvidence`` records with a
``SourceManifest``. It performs **no** source-to-canonical mapping (that is the
P7-B canonicalization runtime), **no** identity resolution (P7-C), and **no**
Canonical Truth mutation. Evidence is not truth; it is the traceable input that
later slices may drive, through the governed application boundary, toward
Canonical Facts.

Design rules honored:
  - ``Enterprise Representation -> Source Evidence`` directionality only;
  - provenance / evidence are first-class (every field keeps an ``EvidenceRef``);
  - fail closed: missing source identity, scope, provenance, or extraction time
    blocks the batch from becoming evidence;
  - deterministic reference path first (SQL is backend-neutral via a row
    provider, no live database required);
  - side effects are explicit: adapters only read, never mutate.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping, Protocol

from .evidence import EvidenceReference
from .evidence_provenance import EvidenceRef


class AdapterError(ValueError):
    """Raised when a source batch cannot be governed into evidence."""


@dataclass(frozen=True)
class SourceManifest:
    """Provenance for one evidence batch (one adapter invocation)."""

    source_system: str
    adapter_version: str
    data_contract_version: str
    mapping_config_version: str
    extracted_at: str
    scope: str
    adapter_kind: str

    def __post_init__(self) -> None:
        for name in (
            "source_system",
            "adapter_version",
            "data_contract_version",
            "mapping_config_version",
            "extracted_at",
            "scope",
            "adapter_kind",
        ):
            if not getattr(self, name).strip():
                raise AdapterError(f"{name} must be non-empty")
        if self.adapter_kind not in ("csv", "json", "sql"):
            raise AdapterError(f"unsupported adapter_kind: {self.adapter_kind}")


@dataclass(frozen=True)
class SourceEvidence:
    """One immutable, explicitly attested source row packaged as evidence."""

    evidence_id: str
    source_system: str
    source_location: str
    record_id: str
    payload: Mapping[str, Any]
    observed_at: str
    scope: str
    mapping_config_version: str
    evidence_type: str = "source_reference"
    field_evidence: tuple[EvidenceRef, ...] = ()

    def __post_init__(self) -> None:
        if not self.evidence_id.strip():
            raise AdapterError("evidence_id must be non-empty")
        if not self.source_system.strip():
            raise AdapterError("source_system must be non-empty")
        if not self.source_location.strip():
            raise AdapterError("source_location must be non-empty")
        if not self.record_id.strip():
            raise AdapterError("record_id must be non-empty")
        if not self.observed_at.strip():
            raise AdapterError("observed_at must be non-empty")
        if not self.scope.strip():
            raise AdapterError("scope must be non-empty")
        if not self.mapping_config_version.strip():
            raise AdapterError("mapping_config_version must be non-empty")
        if not isinstance(self.payload, Mapping):
            raise AdapterError("payload must be a mapping")

        refs = self.field_evidence
        sources = [ref.source_ref for ref in refs]
        if len(sources) != len(set(sources)):
            raise AdapterError("field_evidence source_ref must be unique")

    def as_evidence_reference(self) -> EvidenceReference:
        """Canonical reference form for downstream evidence consumers (P7-B+)."""
        return EvidenceReference(
            evidence_id=self.evidence_id,
            evidence_type=self.evidence_type,
            reference=self.source_location,
        )


@dataclass(frozen=True)
class SourceDataset:
    """Immutable evidence batch plus its provenance manifest."""

    manifest: SourceManifest
    records: tuple[SourceEvidence, ...]

    def __post_init__(self) -> None:
        if not self.records:
            raise AdapterError("dataset must contain at least one evidence record")
        if self.manifest.adapter_kind == "sql" and len(self.records) != len(
            {record.record_id for record in self.records}
        ):
            raise AdapterError("sql adapter record_id must be unique within a batch")
        if any(record.source_system != self.manifest.source_system for record in self.records):
            raise AdapterError("record source_system must match the manifest")
        if any(record.scope != self.manifest.scope for record in self.records):
            raise AdapterError("record scope must match the manifest")
        if any(record.mapping_config_version != self.manifest.mapping_config_version for record in self.records):
            raise AdapterError("record mapping_config_version must match the manifest")

    @property
    def record_count(self) -> int:
        return len(self.records)

    @property
    def content_hash(self) -> str:
        canonical = json.dumps(
            [self._record_to_map(record) for record in self.records],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return sha256(canonical.encode("utf-8")).hexdigest()

    @staticmethod
    def _record_to_map(record: SourceEvidence) -> dict[str, Any]:
        return {
            "evidence_id": record.evidence_id,
            "source_location": record.source_location,
            "record_id": record.record_id,
            "payload": _freeze(record.payload),
            "observed_at": record.observed_at,
            "scope": record.scope,
        }

    def to_json(self) -> str:
        return json.dumps(
            {
                "contract_version": self.manifest.data_contract_version,
                "manifest": {
                    "source_system": self.manifest.source_system,
                    "adapter_version": self.manifest.adapter_version,
                    "mapping_config_version": self.manifest.mapping_config_version,
                    "extracted_at": self.manifest.extracted_at,
                    "scope": self.manifest.scope,
                    "adapter_kind": self.manifest.adapter_kind,
                },
                "record_count": self.record_count,
                "content_hash": self.content_hash,
                "records": [self._record_to_map(record) for record in self.records],
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _freeze(item) for key, item in sorted(value.items())}
    if isinstance(value, (list, tuple)):
        return [_freeze(item) for item in value]
    return value


class SourceAdapter(Protocol):
    """Boundary that every P7-A source adapter must satisfy."""

    def adapt(self) -> SourceDataset:
        """Extract and attest one evidence batch. Never mutates Canonical Truth."""
        ...


@dataclass(frozen=True)
class AdapterConformance:
    """S273-style conformance result for an adapter invocation."""

    adapter_version: str
    mapping_config_version: str
    contract_version: str
    checked_scope: str
    status: str
    findings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.status not in ("conformant", "non_conformant", "inconclusive"):
            raise AdapterError(f"invalid conformance status: {self.status}")


def conformant(adapter_source: SourceDataset) -> AdapterConformance:
    """Deterministic conformance check; evidence is never promoted to truth."""
    findings: list[str] = []
    manifest = adapter_source.manifest
    if not manifest.source_system:
        findings.append("manifest.source_system is empty")
    if not manifest.adapter_version:
        findings.append("manifest.adapter_version is empty")
    if not manifest.mapping_config_version:
        findings.append("manifest.mapping_config_version is empty")
    if not manifest.scope:
        findings.append("manifest.scope is empty")
    return AdapterConformance(
        adapter_version=manifest.adapter_version,
        mapping_config_version=manifest.mapping_config_version,
        contract_version=manifest.data_contract_version,
        checked_scope=manifest.scope,
        status=("conformant" if not findings else "non_conformant"),
        findings=tuple(findings),
    )


@dataclass(frozen=True)
class CsvAdapterConfig:
    """CSV layout: which source columns map to record identity / data / context."""

    source_system: str
    record_id_column: str
    source_location_template: str = "{path}:row={row_number}"
    path: str = "reference"

    def __post_init__(self) -> None:
        if not self.source_system.strip():
            raise AdapterError("source_system must be non-empty")
        if not self.record_id_column.strip():
            raise AdapterError("record_id_column must be non-empty")
        if not self.source_location_template.strip():
            raise AdapterError("source_location_template must be non-empty")


def adapt_csv(
    rows: Iterable[Mapping[str, Any]],
    manifest: SourceManifest,
    config: CsvAdapterConfig,
    *,
    start_row: int = 1,
) -> SourceDataset:
    """Turn CSV-style rows into a governed evidence batch.

    ``rows`` are already decoded records (dicts keyed by source column). The
    adapter enforces field-level provenance (``field_evidence``) for every
    payload field and fails closed if identity, scope, or provenance is missing.
    """
    if manifest.adapter_kind != "csv":
        raise AdapterError("manifest.adapter_kind must be 'csv' for adapt_csv")
    if config.source_system != manifest.source_system:
        raise AdapterError("config.source_system must match the manifest")

    evidence: list[SourceEvidence] = []
    for index, row in enumerate(rows, start=start_row):
        if config.record_id_column not in row:
            raise AdapterError(
                f"csv row {index}: missing record identity column '{config.record_id_column}'"
            )
        record_id = row[config.record_id_column]
        if record_id is None or (isinstance(record_id, str) and not record_id.strip()):
            raise AdapterError(f"csv row {index}: empty record_id")
        if record_id in {existing.record_id for existing in evidence}:
            raise AdapterError(f"csv row {index}: duplicate record_id '{record_id}'")

        source_location = config.source_location_template.format(
            path=config.path, row_number=index
        )
        field_evidence = tuple(
            EvidenceRef(
                source_ref=f"{source_location}:{column}",
                observed_at=manifest.extracted_at,
                metadata={"column": column},
            )
            for column in sorted(row.keys())
        )
        evidence.append(
            SourceEvidence(
                evidence_id=f"{manifest.source_system}:{record_id}",
                source_system=manifest.source_system,
                source_location=source_location,
                record_id=str(record_id),
                payload=dict(row),
                observed_at=manifest.extracted_at,
                scope=manifest.scope,
                mapping_config_version=manifest.mapping_config_version,
                field_evidence=field_evidence,
            )
        )
    return SourceDataset(manifest=manifest, records=tuple(evidence))


def adapt_json(
    payload: Mapping[str, Any] | Iterable[Mapping[str, Any]],
    manifest: SourceManifest,
    *,
    record_id_key: str = "record_id",
    path: str = "reference.jsonl",
) -> SourceDataset:
    """Turn a JSON object or array of rows into a governed evidence batch."""
    if manifest.adapter_kind != "json":
        raise AdapterError("manifest.adapter_kind must be 'json' for adapt_json")

    rows: list[Mapping[str, Any]]
    if isinstance(payload, Mapping):
        items = payload.get("records")
        if not isinstance(items, list):
            raise AdapterError("json payload must have a 'records' list")
        rows = items
    else:
        rows = list(payload)

    if not rows:
        raise AdapterError("json payload contains no records")

    evidence: list[SourceEvidence] = []
    for index, row in enumerate(rows, start=1):
        if record_id_key not in row:
            raise AdapterError(
                f"json record {index}: missing record identity key '{record_id_key}'"
            )
        record_id = row[record_id_key]
        if record_id is None or (isinstance(record_id, str) and not record_id.strip()):
            raise AdapterError(f"json record {index}: empty record_id")
        if record_id in {existing.record_id for existing in evidence}:
            raise AdapterError(f"json record {index}: duplicate record_id '{record_id}'")

        source_location = f"{path}[{index}]"
        field_evidence = tuple(
            EvidenceRef(
                source_ref=f"{source_location}:{key}",
                observed_at=manifest.extracted_at,
                metadata={"key": key},
            )
            for key in sorted(row.keys())
        )
        evidence.append(
            SourceEvidence(
                evidence_id=f"{manifest.source_system}:{record_id}",
                source_system=manifest.source_system,
                source_location=source_location,
                record_id=str(record_id),
                payload=dict(row),
                observed_at=manifest.extracted_at,
                scope=manifest.scope,
                mapping_config_version=manifest.mapping_config_version,
                field_evidence=field_evidence,
            )
        )
    return SourceDataset(manifest=manifest, records=tuple(evidence))


@dataclass(frozen=True)
class SqlSourceConfig:
    """Backend-neutral SQL adapter configuration.

    ``table``/``query`` are provenance labels; the actual row production is
    delegated to an injected ``row_provider`` so no live database is needed for
    the deterministic reference path (backend-neutrality per the roadmap).
    """

    table: str
    scope: str
    primary_key: str

    def __post_init__(self) -> None:
        if not self.table.strip():
            raise AdapterError("table must be non-empty")
        if not self.scope.strip():
            raise AdapterError("scope must be non-empty")
        if not self.primary_key.strip():
            raise AdapterError("primary_key must be non-empty")


def adapt_sql(
    row_provider: Iterable[Mapping[str, Any]],
    manifest: SourceManifest,
    config: SqlSourceConfig,
    *,
    query: str | None = None,
) -> SourceDataset:
    """Turn SQL-query rows into a governed evidence batch.

    ``row_provider`` is an injected row iterator (e.g. sqlite3 cursor, a test
    stub, or any backend adapter) mapping column names to values. The adapter is
    backend-neutral: it never imports a database driver.
    """
    if manifest.adapter_kind != "sql":
        raise AdapterError("manifest.adapter_kind must be 'sql' for adapt_sql")
    if config.scope != manifest.scope:
        raise AdapterError("config.scope must match the manifest")

    sql_ref = query or f"SELECT * FROM {config.table}"
    source_location = f"sql:{config.table}:{config.primary_key}"

    evidence: list[SourceEvidence] = []
    for index, row in enumerate(row_provider, start=1):
        if config.primary_key not in row:
            raise AdapterError(
                f"sql row {index}: missing primary key '{config.primary_key}'"
            )
        record_id = row[config.primary_key]
        if record_id is None or (isinstance(record_id, str) and not record_id.strip()):
            raise AdapterError(f"sql row {index}: empty primary key value")
        if record_id in {existing.record_id for existing in evidence}:
            raise AdapterError(f"sql row {index}: duplicate primary key '{record_id}'")

        field_evidence = tuple(
            EvidenceRef(
                source_ref=f"{source_location}.{column}::{sql_ref}",
                observed_at=manifest.extracted_at,
                metadata={"column": column},
            )
            for column in sorted(row.keys())
        )
        evidence.append(
            SourceEvidence(
                evidence_id=f"{manifest.source_system}:{record_id}",
                source_system=manifest.source_system,
                source_location=source_location,
                record_id=str(record_id),
                payload=dict(row),
                observed_at=manifest.extracted_at,
                scope=manifest.scope,
                mapping_config_version=manifest.mapping_config_version,
                field_evidence=field_evidence,
            )
        )
    return SourceDataset(manifest=manifest, records=tuple(evidence))


@dataclass(frozen=True)
class ReferenceEvidenceBundle:
    """Converged evidence from several distinct source systems.

    Each source system keeps its own manifest. The bundle is a *reference
    evidence* aggregate only: it never collapses scope, source identity, or
    canonical identity, and it performs no canonicalization.
    """

    datasets: tuple[SourceDataset, ...]

    def __post_init__(self) -> None:
        if not self.datasets:
            raise AdapterError("bundle must contain at least one dataset")
        for dataset in self.datasets:
            if not isinstance(dataset, SourceDataset):
                raise AdapterError("bundle datasets must be SourceDataset instances")

    @property
    def record_count(self) -> int:
        return sum(dataset.record_count for dataset in self.datasets)

    @property
    def sources(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(d.manifest.source_system for d in self.datasets))

    @property
    def content_hash(self) -> str:
        canonical = json.dumps(
            [json.loads(d.to_json()) for d in self.datasets],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return sha256(canonical.encode("utf-8")).hexdigest()

    def to_json(self) -> str:
        return json.dumps(
            {
                "contract_version": "P7A.1",
                "record_count": self.record_count,
                "sources": list(self.sources),
                "content_hash": self.content_hash,
                "source_datasets": [json.loads(d.to_json()) for d in self.datasets],
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


# Deterministic reference path: one ERP (@csv), one WMS (@json), one TMS (@sql)
# source each produce an attested evidence batch. They are *aggregated*, not
# canonicalized: scope, source-system identity, and record identity stay
# distinct so downstream slices (P7-B canonicalization, P7-C identity
# resolution) operate on traceable evidence without conflating identity.
def run_reference_data_adapter_path() -> ReferenceEvidenceBundle:
    def manifest(source: str, adapter_kind: str, at: str) -> SourceManifest:
        return SourceManifest(
            source_system=source,
            adapter_version="P7A.1",
            data_contract_version="P7A.1",
            mapping_config_version="M8-reference",
            extracted_at=at,
            scope="enterprise:acme",
            adapter_kind=adapter_kind,
        )

    return ReferenceEvidenceBundle(
        datasets=(
            adapt_csv(
                [
                    {"material_id": "MAT-1000", "description": "Raw aluminium", "plant": "PLT-E"},
                    {"material_id": "MAT-1001", "description": "Finished assembly", "plant": "PLT-E"},
                ],
                manifest("erp", "csv", "2026-08-19T09:00:00Z"),
                CsvAdapterConfig(source_system="erp", record_id_column="material_id"),
            ),
            adapt_json(
                {
                    "records": [
                        {"stock_id": "STK-1", "location": "WH-1", "qty": 120.0},
                        {"stock_id": "STK-2", "location": "WH-2", "qty": 40.0},
                    ]
                },
                manifest("wms", "json", "2026-08-19T09:00:01Z"),
                record_id_key="stock_id",
            ),
            adapt_sql(
                [
                    {"shipment_id": "SHIP-1", "carrier": "carrier-a", "lanes": 2},
                    {"shipment_id": "SHIP-2", "carrier": "carrier-b", "lanes": 1},
                ],
                manifest("tms", "sql", "2026-08-19T09:00:02Z"),
                SqlSourceConfig(table="shipment", scope="enterprise:acme", primary_key="shipment_id"),
            ),
        )
    )
