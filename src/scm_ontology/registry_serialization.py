from __future__ import annotations

from dataclasses import asdict
import json

from .versioned_registry import RegistrySnapshot, VersionedRegistry


def serialize_registry(registry: VersionedRegistry) -> dict[str, object]:
    return {
        "snapshots": [asdict(snapshot) for snapshot in registry.snapshots],
    }


def deserialize_registry(payload: dict[str, object]) -> VersionedRegistry:
    raw_snapshots = payload.get("snapshots", [])
    if not isinstance(raw_snapshots, list):
        raise ValueError("snapshots must be a list")
    registry = VersionedRegistry()
    for raw in raw_snapshots:
        if not isinstance(raw, dict):
            raise ValueError("snapshot must be an object")
        snapshot = RegistrySnapshot(
            version_ref=str(raw["version_ref"]),
            content_ref=str(raw["content_ref"]),
            parent_version_ref=(
                None
                if raw.get("parent_version_ref") is None
                else str(raw["parent_version_ref"])
            ),
        )
        registry = registry.append(snapshot)
    return registry


def roundtrip_registry(registry: VersionedRegistry) -> VersionedRegistry:
    payload = serialize_registry(registry)
    # JSON encode/decode proves the public payload is JSON-compatible.
    return deserialize_registry(json.loads(json.dumps(payload)))
