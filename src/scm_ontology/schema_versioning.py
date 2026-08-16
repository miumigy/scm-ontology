"""Compatibility policy for versioned SCM Trace Bundle contracts."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class SchemaCompatibility:
    producer_version: str
    consumer_version: str
    compatible: bool
    reason: str

def _parse(version: str) -> tuple[int, int, int]:
    parts = version.split(".")
    if len(parts) != 3 or any(not part.isdigit() for part in parts):
        raise ValueError(f"invalid semantic version: {version}")
    return tuple(int(part) for part in parts)  # type: ignore[return-value]

def negotiate_schema_version(producer_version: str, consumer_version: str) -> SchemaCompatibility:
    producer = _parse(producer_version)
    consumer = _parse(consumer_version)
    if producer[0] != consumer[0]:
        return SchemaCompatibility(producer_version, consumer_version, False, "major versions differ")
    if producer[1] > consumer[1]:
        return SchemaCompatibility(producer_version, consumer_version, False, "producer minor version is newer")
    return SchemaCompatibility(producer_version, consumer_version, True, "same major version and producer is not newer")
