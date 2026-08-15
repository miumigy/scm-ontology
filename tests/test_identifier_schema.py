import pytest

from scm_ontology.identity_reference import Identifier, IdentifierNamespace, ResolutionStatus
from scm_ontology.identifier_schema import CanonicalIdentifierDefinition, ReferenceResolution


def identifier() -> Identifier:
    return Identifier(
        value="MAT-001",
        namespace=IdentifierNamespace("erp-material"),
        entity_type_ref="Material",
    )


def test_identifier_definition_is_contextual_not_identity() -> None:
    definition = CanonicalIdentifierDefinition(
        ref="iddef:material",
        namespace_ref="ns:erp-material",
        value_type_ref="String",
        role="source",
        entity_type_ref="Material",
    )
    assert definition.entity_type_ref == "Material"


def test_confirmed_resolution_requires_target() -> None:
    with pytest.raises(ValueError, match="target_entity_ref"):
        ReferenceResolution("rr:1", identifier(), None, ResolutionStatus.CONFIRMED)


def test_unresolved_reference_can_exist_without_target() -> None:
    resolution = ReferenceResolution("rr:2", identifier(), None, ResolutionStatus.UNRESOLVED)
    assert resolution.is_canonical is False


def test_confirmed_resolution_is_explicitly_canonical() -> None:
    resolution = ReferenceResolution(
        "rr:3", identifier(), "material:001", ResolutionStatus.CONFIRMED,
        confidence=0.99, provenance_refs=("prov:1",),
    )
    assert resolution.is_canonical is True
    assert resolution.provenance_refs == ("prov:1",)


def test_confidence_is_bounded() -> None:
    with pytest.raises(ValueError, match="between 0 and 1"):
        ReferenceResolution("rr:4", identifier(), "material:001", ResolutionStatus.PROBABLE, confidence=1.1)
