"""Immutable evidence and provenance lineage for canonical events."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .canonical_event import CanonicalEvent


class CanonicalEventLineageError(ValueError):
    """Raised when canonical event lineage is incomplete or malformed."""


@dataclass(frozen=True)
class CanonicalEventLineage:
    """Immutable identifiers linking a canonical event to its evidence and provenance."""

    event_id: str
    evidence_ids: tuple[str, ...]
    provenance_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.event_id.strip():
            raise CanonicalEventLineageError("event_id must be non-empty")
        if any(not value.strip() for value in self.evidence_ids):
            raise CanonicalEventLineageError("evidence_ids must contain non-empty identifiers")
        if any(not value.strip() for value in self.provenance_ids):
            raise CanonicalEventLineageError("provenance_ids must contain non-empty identifiers")

    def to_mapping(self) -> dict[str, object]:
        return {
            "contract_version": "S349.1",
            "event_id": self.event_id,
            "evidence_ids": list(self.evidence_ids),
            "provenance_ids": list(self.provenance_ids),
        }


def extract_event_lineage(event: CanonicalEvent) -> CanonicalEventLineage:
    """Extract and freeze lineage identifiers from a canonical event without mutation."""
    attributes: Mapping[str, object] = event.attributes
    evidence = attributes.get("evidence_ids", ())
    provenance = attributes.get("provenance_ids", ())
    if not isinstance(evidence, (list, tuple)) or not all(isinstance(v, str) for v in evidence):
        raise CanonicalEventLineageError("evidence_ids must be a sequence of strings")
    if not isinstance(provenance, (list, tuple)) or not all(isinstance(v, str) for v in provenance):
        raise CanonicalEventLineageError("provenance_ids must be a sequence of strings")
    return CanonicalEventLineage(
        event_id=event.entity_id,
        evidence_ids=tuple(evidence),
        provenance_ids=tuple(provenance),
    )
