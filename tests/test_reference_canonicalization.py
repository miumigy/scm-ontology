from scm_ontology.reference_canonicalization import (
    CanonicalizationOutcome,
    ReferenceCanonicalizer,
    ReferenceMapping,
)


def test_explicit_mapping_is_applied_without_inference() -> None:
    canonicalizer = ReferenceCanonicalizer(
        [ReferenceMapping("customer_order", "Order")]
    )

    result = canonicalizer.canonicalize("customer_order")

    assert result.outcome == CanonicalizationOutcome.APPLIED
    assert result.canonical_id == "Order"


def test_unmapped_label_remains_a_semantic_gap() -> None:
    canonicalizer = ReferenceCanonicalizer(
        [ReferenceMapping("customer_order", "Order")]
    )

    result = canonicalizer.canonicalize("mystery_record")

    assert result.outcome == CanonicalizationOutcome.SEMANTIC_GAP
    assert result.canonical_id is None


def test_conflicting_explicit_mappings_remain_observable() -> None:
    canonicalizer = ReferenceCanonicalizer(
        [
            ReferenceMapping("stock", "Inventory"),
            ReferenceMapping("stock", "Supply"),
        ]
    )

    result = canonicalizer.canonicalize("stock")

    assert result.outcome == CanonicalizationOutcome.CONFLICT
    assert result.canonical_id is None


def test_unknown_canonical_target_is_rejected() -> None:
    try:
        ReferenceCanonicalizer([ReferenceMapping("x", "NotCanonical")])
    except ValueError as exc:
        assert "mapping target is not canonical" in str(exc)
    else:
        raise AssertionError("unknown canonical target must be rejected")


def test_batch_order_is_deterministic() -> None:
    canonicalizer = ReferenceCanonicalizer(
        [ReferenceMapping("order", "Order")]
    )

    results = canonicalizer.canonicalize_many(["order", "unknown", "order"])

    assert [result.outcome for result in results] == [
        CanonicalizationOutcome.APPLIED,
        CanonicalizationOutcome.SEMANTIC_GAP,
        CanonicalizationOutcome.APPLIED,
    ]
