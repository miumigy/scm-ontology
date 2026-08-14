import pytest
from scm_ontology.relationship_version import (
    RelationshipVersion,
    RelationshipVersionError,
    is_relationship_version,
)


def test_relationship_version_has_validity_and_qualifiers():
    version = RelationshipVersion(
        valid_from="2026-01-01",
        valid_to="2026-06-30",
        qualifiers={"priority": 1},
    )
    assert version.valid_from == "2026-01-01"
    assert version.valid_to == "2026-06-30"
    assert version.qualifiers == {"priority": 1}
    assert is_relationship_version(version)


def test_relationship_version_supports_open_ended_validity():
    version = RelationshipVersion(valid_from="2026-07-01")
    assert version.valid_to is None


@pytest.mark.parametrize("field", ["valid_from", "valid_to"])
def test_rejects_empty_validity_boundary(field):
    values = {"valid_from": "2026-01-01", "valid_to": "2026-06-30"}
    values[field] = ""
    with pytest.raises(RelationshipVersionError, match=field):
        RelationshipVersion(**values)


def test_rejects_non_mapping_qualifiers():
    with pytest.raises(RelationshipVersionError, match="qualifiers"):
        RelationshipVersion("2026-01-01", qualifiers=[("priority", 1)])


def test_version_does_not_require_version_id():
    version = RelationshipVersion("2026-01-01")
    assert not hasattr(version, "version_id")
