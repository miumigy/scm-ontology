from scm_ontology.ontology_linter import ValidationSeverity, lint_relationship
from scm_ontology.relationship_identity import RelationshipInstance
from scm_ontology.relationship_version import RelationshipVersion


def relationship(predicate: str = "places") -> RelationshipInstance:
    return RelationshipInstance("R1", "party-1", predicate, "order-1")


def test_valid_canonical_relationship():
    result = lint_relationship(relationship(), "Party", "CustomerOrder")

    assert result.valid
    assert result.issues == ()


def test_endpoint_constraint_violation_is_error():
    result = lint_relationship(relationship(), "Shipment", "Party")

    assert not result.valid
    assert result.issues[0].code == "ENDPOINT_CONSTRAINT_VIOLATION"
    assert result.issues[0].severity == ValidationSeverity.ERROR


def test_unknown_predicate_is_not_rejected():
    result = lint_relationship(relationship("custom_scm_relation"), "Shipment", "Party")

    assert result.valid
    assert result.issues[0].code == "UNKNOWN_PREDICATE"
    assert result.issues[0].severity == ValidationSeverity.INFO


def test_cardinality_is_checked_when_counts_are_supplied():
    result = lint_relationship(
        relationship(),
        "Party",
        "CustomerOrder",
        from_count=0,
        to_count=1,
    )

    assert not result.valid
    assert result.issues[0].code == "FROM_CARDINALITY_VIOLATION"


def test_cardinality_is_not_invented_without_observed_counts():
    result = lint_relationship(relationship(), "Party", "CustomerOrder")

    assert result.valid


def test_relationship_version_can_be_linted():
    result = lint_relationship(
        relationship(),
        "Party",
        "CustomerOrder",
        version=RelationshipVersion(
            valid_from="2026-01-01",
            valid_to=None,
            qualifiers={"priority": 1},
        ),
    )

    assert result.valid
