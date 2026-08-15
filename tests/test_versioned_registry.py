import pytest

from scm_ontology.versioned_registry import RegistrySnapshot, RegistryVersionError, VersionedRegistry


def test_registry_snapshots_form_a_version_lineage() -> None:
    registry = VersionedRegistry()
    registry = registry.append(RegistrySnapshot("v1", "registry:v1"))
    registry = registry.append(RegistrySnapshot("v2", "registry:v2", "v1"))
    assert registry.current.version_ref == "v2"
    assert registry.rollback_target("v1").content_ref == "registry:v1"


def test_registry_rejects_broken_parent_lineage() -> None:
    registry = VersionedRegistry().append(RegistrySnapshot("v1", "registry:v1"))
    with pytest.raises(RegistryVersionError):
        registry.append(RegistrySnapshot("v2", "registry:v2", "wrong"))
