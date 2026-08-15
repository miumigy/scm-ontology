from __future__ import annotations

from dataclasses import dataclass


class RegistryVersionError(ValueError):
    pass


@dataclass(frozen=True)
class RegistrySnapshot:
    version_ref: str
    content_ref: str
    parent_version_ref: str | None = None


@dataclass(frozen=True)
class VersionedRegistry:
    snapshots: tuple[RegistrySnapshot, ...] = ()

    @property
    def current(self) -> RegistrySnapshot | None:
        return self.snapshots[-1] if self.snapshots else None

    def append(self, snapshot: RegistrySnapshot) -> VersionedRegistry:
        current = self.current
        if current is not None and snapshot.parent_version_ref != current.version_ref:
            raise RegistryVersionError("snapshot parent must match current version")
        if any(item.version_ref == snapshot.version_ref for item in self.snapshots):
            raise RegistryVersionError("registry version must be unique")
        return VersionedRegistry(self.snapshots + (snapshot,))

    def rollback_target(self, version_ref: str) -> RegistrySnapshot:
        for snapshot in self.snapshots:
            if snapshot.version_ref == version_ref:
                return snapshot
        raise RegistryVersionError(f"unknown registry version: {version_ref}")
