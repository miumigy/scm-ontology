import pytest

from scm_ontology.identity_reference import (
    EntityReference,
    Identifier,
    IdentifierNamespace,
    IdentifierRole,
    ResolutionStatus,
    resolve_reference,
)


def test_source_identifier_requires_no_canonical_identity() -> None:
    identifier = Identifier(
        "M-001",
        IdentifierNamespace("ERP-A/material"),
        role=IdentifierRole.SOURCE,
        entity_type_ref="Material",
    )
    reference = EntityReference(
        ref="reference:1",
        entity_type_ref="Material",
        identifier=identifier,
    )
    assert reference.is_resolved is False


def test_confirmed_resolution_requires_canonical_entity() -> None:
    identifier = Identifier(
        "M-001",
        IdentifierNamespace("ERP-A/material"),
        role=IdentifierRole.SOURCE,
        entity_type_ref="Material",
    )
    with pytest.raises(ValueError, match="canonical_entity_ref"):
        EntityReference(
            ref="reference:1",
            entity_type_ref="Material",
            identifier=identifier,
            resolution_status=ResolutionStatus.CONFIRMED,
        )


def test_resolution_keeps_provenance() -> None:
    identifier = Identifier(
        "M-001",
        IdentifierNamespace("ERP-A/material"),
        role=IdentifierRole.SOURCE,
        entity_type_ref="Material",
    )
    unresolved = EntityReference(
        ref="reference:1",
        entity_type_ref="Material",
        identifier=identifier,
        provenance_refs=("source-record:1",),
    )
    resolved = resolve_reference(unresolved, "Material:CANONICAL-1", confidence=0.98)
    assert resolved.is_resolved is True
    assert resolved.canonical_entity_ref == "Material:CANONICAL-1"
    assert resolved.provenance_refs == ("source-record:1",)


def test_same_code_in_different_namespaces_remains_distinct() -> None:
    a = Identifier("123", IdentifierNamespace("ERP-A/material"))
    b = Identifier("123", IdentifierNamespace("ERP-B/material"))
    assert (a.namespace.name, a.value) != (b.namespace.name, b.value)
