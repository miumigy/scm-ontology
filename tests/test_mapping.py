import pytest

from scm_ontology.mapping import (
    CanonicalTarget,
    MappingStatus,
    SemanticMapping,
    SourceField,
    Transformation,
    TransformationKind,
)


def test_mapping_preserves_source_and_canonical_target() -> None:
    mapping = SemanticMapping(
        source=SourceField("SAP", "Material", "MATNR", "sap.material"),
        target=CanonicalTarget("Material", "identifier"),
        transformations=(Transformation(TransformationKind.NORMALIZATION),),
        status=MappingStatus.REVIEWED,
        provenance_ref="prov-001",
    )

    assert mapping.source.system == "SAP"
    assert mapping.target.concept == "Material"
    assert mapping.status is MappingStatus.REVIEWED
    assert mapping.is_approved is False


def test_mapping_confidence_is_bounded() -> None:
    with pytest.raises(ValueError):
        SemanticMapping(
            source=SourceField("WMS", "Item", "item_code"),
            target=CanonicalTarget("Item"),
            confidence=1.1,
        )


def test_identity_resolution_is_explicit() -> None:
    mapping = SemanticMapping(
        source=SourceField("ERP", "Customer", "customer_id"),
        target=CanonicalTarget("Organization", "identifier"),
        transformations=(Transformation(TransformationKind.IDENTITY_RESOLUTION),),
        identity_resolution_ref="resolution-42",
    )

    assert mapping.identity_resolution_ref == "resolution-42"
    assert mapping.transformations[0].kind is TransformationKind.IDENTITY_RESOLUTION
