"""Load non-authoritative multi-source canonicalization fixtures.

The loader deliberately stops at reference canonicalization. It does not
perform identity resolution or mutate Canonical Truth.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .reference_canonicalization import (
    CanonicalizationResult,
    ReferenceCanonicalizer,
    ReferenceMapping,
)


@dataclass(frozen=True)
class SourceRecord:
    source_system: str
    label: str
    reference_id: str


@dataclass(frozen=True)
class FixturePipelineResult:
    records: tuple[SourceRecord, ...]
    results: tuple[CanonicalizationResult, ...]


def load_fixture(path: str | Path) -> tuple[tuple[SourceRecord, ...], ReferenceCanonicalizer]:
    payload: dict[str, Any] = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    records = tuple(
        SourceRecord(
            source_system=source["source_system"],
            label=record["label"],
            reference_id=record["reference_id"],
        )
        for source in payload["sources"]
        for record in source["records"]
    )
    mappings = tuple(
        ReferenceMapping(
            source_label=mapping["source_label"],
            canonical_id=mapping["canonical_id"],
        )
        for mapping in payload["mappings"]
    )
    return records, ReferenceCanonicalizer(mappings)


def run_fixture(path: str | Path) -> FixturePipelineResult:
    records, canonicalizer = load_fixture(path)
    results = canonicalizer.canonicalize_many(record.label for record in records)
    return FixturePipelineResult(records=records, results=results)
