from scm_ontology.registry_serialization import roundtrip_registry, serialize_registry
from scm_ontology.versioned_registry import RegistrySnapshot, VersionedRegistry


def test_registry_serialization_is_json_compatible_and_roundtrips() -> None:
    registry = VersionedRegistry().append(RegistrySnapshot("v1", "registry:v1"))
    registry = registry.append(RegistrySnapshot("v2", "registry:v2", "v1"))
    restored = roundtrip_registry(registry)
    assert serialize_registry(restored) == serialize_registry(registry)
