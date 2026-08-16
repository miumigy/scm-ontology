from scm_ontology.reference_canonicalization import (
    CanonicalizationOutcome,
    ReferenceCanonicalizer,
    ReferenceMapping,
)


def test_multi_source_labels_canonicalize_without_cross_source_identity_inference() -> None:
    canonicalizer = ReferenceCanonicalizer(
        [
            ReferenceMapping("customer_order", "Order"),
            ReferenceMapping("inventory", "Inventory"),
            ReferenceMapping("stock", "Inventory"),
        ]
    )

    results = canonicalizer.canonicalize_many(
        ["customer_order", "inventory", "stock", "unknown_record"]
    )

    assert [result.canonical_id for result in results] == [
        "Order",
        "Inventory",
        "Inventory",
        None,
    ]
    assert [result.outcome for result in results] == [
        CanonicalizationOutcome.APPLIED,
        CanonicalizationOutcome.APPLIED,
        CanonicalizationOutcome.APPLIED,
        CanonicalizationOutcome.SEMANTIC_GAP,
    ]


def test_same_source_label_with_multiple_targets_remains_conflict() -> None:
    canonicalizer = ReferenceCanonicalizer(
        [
            ReferenceMapping("stock", "Inventory"),
            ReferenceMapping("stock", "Supply"),
        ]
    )

    result = canonicalizer.canonicalize("stock")

    assert result.outcome == CanonicalizationOutcome.CONFLICT
    assert result.canonical_id is None
