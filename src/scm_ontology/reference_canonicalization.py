"""Governed reference canonicalization against the machine-readable registry.

This module intentionally performs only explicit reference mapping. It does not
resolve identity, infer new semantics, mutate Canonical Truth, or create facts.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable

from .machine_registry import MachineRegistry, load_canonical_registry


class CanonicalizationOutcome(StrEnum):
    APPLIED = "applied"
    CONFLICT = "conflict"
    SEMANTIC_GAP = "semantic_gap"


@dataclass(frozen=True)
class ReferenceMapping:
    source_label: str
    canonical_id: str


@dataclass(frozen=True)
class CanonicalizationResult:
    source_label: str
    canonical_id: str | None
    outcome: CanonicalizationOutcome


class ReferenceCanonicalizer:
    """Canonicalize source labels only through explicit reference mappings."""

    def __init__(
        self,
        mappings: Iterable[ReferenceMapping],
        registry: MachineRegistry | None = None,
    ) -> None:
        self.registry = registry or load_canonical_registry()
        canonical_ids = {item["id"] for item in self.registry.concepts}
        self._mappings: dict[str, tuple[str, ...]] = {}
        for mapping in mappings:
            if mapping.canonical_id not in canonical_ids:
                raise ValueError(f"mapping target is not canonical: {mapping.canonical_id}")
            self._mappings.setdefault(mapping.source_label, tuple())
            self._mappings[mapping.source_label] += (mapping.canonical_id,)

    def canonicalize(self, source_label: str) -> CanonicalizationResult:
        targets = self._mappings.get(source_label)
        if not targets:
            return CanonicalizationResult(
                source_label, None, CanonicalizationOutcome.SEMANTIC_GAP
            )
        unique_targets = tuple(dict.fromkeys(targets))
        if len(unique_targets) > 1:
            return CanonicalizationResult(
                source_label, None, CanonicalizationOutcome.CONFLICT
            )
        return CanonicalizationResult(
            source_label, unique_targets[0], CanonicalizationOutcome.APPLIED
        )

    def canonicalize_many(
        self, source_labels: Iterable[str]
    ) -> tuple[CanonicalizationResult, ...]:
        return tuple(self.canonicalize(label) for label in source_labels)
