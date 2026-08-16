from scm_ontology.machine_registry import load_canonical_registry


def test_machine_registry_loads_and_is_unique() -> None:
    registry = load_canonical_registry()
    registry.validate()
    assert registry.registry_id == "scm-ontology-canonical-registry"
    assert registry.version == "0.2.0"
    assert len(registry.concepts) >= 40
    assert len(registry.relationships) >= 35


def test_machine_registry_matches_canonical_model() -> None:
    registry = load_canonical_registry()
    registry.assert_matches_python_registry()


def test_machine_registry_matches_versioned_schema() -> None:
    registry = load_canonical_registry()
    registry.validate_schema()


def test_machine_registry_preserves_semantic_boundaries() -> None:
    registry = load_canonical_registry()
    concepts = {item["id"]: item for item in registry.concepts}
    assert concepts["Entity"]["abstract"] is True
    assert concepts["Observation"]["layer"] == "primitive"
    assert concepts["KPI"]["layer"] == "derived"
    assert concepts["Identity"]["layer"] == "contextual"

    relationships = {item["predicate"]: item for item in registry.relationships}
    assert relationships["causes"]["category"] == "causal"
    assert relationships["supported_by"]["category"] == "provenance"
    assert relationships["derived_from"]["category"] == "derivation"
