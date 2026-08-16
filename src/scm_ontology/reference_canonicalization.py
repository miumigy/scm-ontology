"""S335 reference implementation for governed source-to-canonical mapping."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
from typing import Any, Mapping


class CanonicalizationError(ValueError):
    """Raised when a source record cannot be governed into canonical form."""


class CanonicalizationOutcome(str, Enum):
    """Explicit outcome of a governed reference canonicalization."""

    APPLIED = "applied"
    SEMANTIC_GAP = "semantic_gap"
    CONFLICT = "conflict"


@dataclass(frozen=True)
class ReferenceMapping:
    """Explicit mapping from a source label to one canonical identifier."""

    source_label: str
    canonical_id: str

    def __post_init__(self) -> None:
        if not self.source_label.strip():
            raise CanonicalizationError("source_label must be non-empty")
        if not self.canonical_id.strip():
            raise CanonicalizationError("canonical_id must be non-empty")


@dataclass(frozen=True)
class CanonicalizationResult:
    """Governed result; unresolved or conflicting mappings remain unresolved."""

    source_label: str
    canonical_id: str | None
    outcome: CanonicalizationOutcome


class ReferenceCanonicalizer:
    """Resolve only explicit reference mappings; never infer identity."""

    def __init__(self, mappings: tuple[ReferenceMapping, ...] | list[ReferenceMapping]) -> None:
        self._mappings = tuple(mappings)

    def canonicalize(self, source_label: str) -> CanonicalizationResult:
        matches = [m.canonical_id for m in self._mappings if m.source_label == source_label]
        if not matches:
            return CanonicalizationResult(source_label, None, CanonicalizationOutcome.SEMANTIC_GAP)
        unique = tuple(dict.fromkeys(matches))
        if len(unique) != 1:
            return CanonicalizationResult(source_label, None, CanonicalizationOutcome.CONFLICT)
        return CanonicalizationResult(source_label, unique[0], CanonicalizationOutcome.APPLIED)

    def canonicalize_many(self, source_labels: Any) -> tuple[CanonicalizationResult, ...]:
        return tuple(self.canonicalize(label) for label in source_labels)


@dataclass(frozen=True)
class SourceMapping:
    """Explicit source-field mapping; no implicit identity resolution."""

    source_id: str
    field_map: tuple[tuple[str, str], ...]
    mapping_version: str = "S335.1"

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise CanonicalizationError("source_id must be non-empty")
        if not self.mapping_version.strip():
            raise CanonicalizationError("mapping_version must be non-empty")
        keys = [source for source, _ in self.field_map]
        if len(keys) != len(set(keys)):
            raise CanonicalizationError("source fields must be unique")
        if any(not source.strip() or not target.strip() for source, target in self.field_map):
            raise CanonicalizationError("mapping fields must be non-empty")


def canonicalize_record(record: Mapping[str, Any], mapping: SourceMapping) -> dict[str, Any]:
    """Map only explicitly declared fields and fail closed on missing input."""
    missing = [source for source, _ in mapping.field_map if source not in record]
    if missing:
        raise CanonicalizationError(f"missing source fields: {', '.join(missing)}")
    canonical = {target: record[source] for source, target in mapping.field_map}
    return {
        "contract_version": "S335.1",
        "canonical": canonical,
        "source_id": mapping.source_id,
        "mapping_version": mapping.mapping_version,
        "source_fields": [source for source, _ in mapping.field_map],
    }


def canonicalize_to_json(record: Mapping[str, Any], mapping: SourceMapping) -> str:
    return json.dumps(
        canonicalize_record(record, mapping),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


# Backward-compatible alias for callers that used the earlier result naming.
CanonicalizationOutcomeType = CanonicalizationOutcome
