import pytest

from scm_ontology.identity_reference import (
    Alias,
    CanonicalReference,
    Identifier,
    IdentifierAssignment,
    IdentifierNamespace,
    IdentityResolutionAssertion,
    ResolutionStatus,
    identifier_key,
)


def test_identifier_requires_contextual_namespace():
    namespace = IdentifierNamespace("ERP-A/customer")
    identifier = Identifier("12345", namespace)
    assert identifier_key(identifier) == ("ERP-A/customer", "12345", None)


def test_same_lexical_value_in_different_namespaces_is_distinct_reference():
    a = Identifier("12345", IdentifierNamespace("ERP-A/customer"))
    b = Identifier("12345", IdentifierNamespace("ERP-B/customer"))
    assert identifier_key(a) != identifier_key(b)


def test_identifier_is_not_entity_identity():
    assignment = IdentifierAssignment(
        Identifier("12345", IdentifierNamespace("ERP-A/customer")),
        entity_ref="Customer:E1",
    )
    assert assignment.entity_ref == "Customer:E1"
    assert assignment.identifier.value == "12345"


def test_identifier_validity_is_temporal():
    with pytest.raises(ValueError):
        IdentifierAssignment(
            Identifier("A", IdentifierNamespace("supplier")),
            entity_ref="Supplier:E1",
            valid_from="2026-02-01",
            valid_to="2026-01-01",
        )


def test_reference_preserves_resolution_status():
    reference = CanonicalReference(
        target_ref="Supplier:E1",
        resolution_status=ResolutionStatus.PROBABLE,
        confidence=0.92,
    )
    assert reference.resolution_status == ResolutionStatus.PROBABLE
    assert reference.confidence == 0.92


def test_unresolved_resolution_is_allowed_without_forcing_same_as():
    assertion = IdentityResolutionAssertion(
        left_ref=Identifier("A", IdentifierNamespace("source")),
        right_ref=Identifier("B", IdentifierNamespace("source")),
        status=ResolutionStatus.UNRESOLVED,
    )
    assert assertion.status == ResolutionStatus.UNRESOLVED


def test_confidence_is_bounded():
    with pytest.raises(ValueError):
        CanonicalReference("Supplier:E1", confidence=1.1)


def test_alias_is_distinct_from_identifier():
    alias = Alias("Acme", entity_ref="Supplier:E1")
    assert alias.value == "Acme"
    assert alias.entity_ref == "Supplier:E1"
