import pytest
from scm_ontology.schema_versioning import negotiate_schema_version


def test_same_version_is_compatible():
    result = negotiate_schema_version("1.0.0", "1.0.0")
    assert result.compatible is True


def test_newer_producer_minor_is_rejected_by_older_consumer():
    result = negotiate_schema_version("1.1.0", "1.0.0")
    assert result.compatible is False
    assert "minor" in result.reason


def test_different_major_versions_are_rejected():
    result = negotiate_schema_version("2.0.0", "1.9.9")
    assert result.compatible is False
    assert "major" in result.reason


def test_older_producer_minor_is_compatible_with_newer_consumer():
    assert negotiate_schema_version("1.0.0", "1.1.0").compatible is True


def test_invalid_semver_is_rejected():
    with pytest.raises(ValueError):
        negotiate_schema_version("1.0", "1.0.0")
