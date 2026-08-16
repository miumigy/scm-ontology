from scm_ontology.capability_negotiation import CapabilitySet, negotiate_capabilities


def test_capability_negotiation_finds_shared_versions_and_features():
    producer = CapabilitySet(frozenset({"1.0.0", "1.1.0"}), frozenset({"provenance", "learning", "planning"}))
    consumer = CapabilitySet(frozenset({"1.0.0"}), frozenset({"provenance", "planning", "execution"}))
    result = negotiate_capabilities(producer, consumer)
    assert result.compatible is True
    assert result.compatible_versions == ("1.0.0",)
    assert result.shared_features == ("planning", "provenance")


def test_capability_negotiation_rejects_no_shared_schema_version():
    producer = CapabilitySet(frozenset({"2.0.0"}), frozenset({"provenance"}))
    consumer = CapabilitySet(frozenset({"1.0.0"}), frozenset({"provenance"}))
    result = negotiate_capabilities(producer, consumer)
    assert result.compatible is False
    assert result.compatible_versions == ()
