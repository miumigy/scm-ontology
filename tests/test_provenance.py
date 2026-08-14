import pytest

from scm_ontology.provenance import (
    ExplanationStep,
    Provenance,
    SemanticExplanation,
)


def test_provenance_preserves_rule_and_source_relationships():
    provenance = Provenance(
        rule_id="order-product-rule",
        source_relationship_ids=("R1", "R2"),
    )

    assert provenance.rule_id == "order-product-rule"
    assert provenance.source_relationship_ids == ("R1", "R2")


def test_explanation_is_structured_and_deterministic():
    explanation = SemanticExplanation(
        steps=(
            ExplanationStep("Order-1 contains Line-1"),
            ExplanationStep("Line-1 references Product-A"),
            ExplanationStep("Therefore Order-1 concerns Product-A"),
        )
    )

    assert [step.statement for step in explanation.steps] == [
        "Order-1 contains Line-1",
        "Line-1 references Product-A",
        "Therefore Order-1 concerns Product-A",
    ]


def test_provenance_requires_rule_and_sources():
    with pytest.raises(ValueError):
        Provenance(rule_id="", source_relationship_ids=("R1",))

    with pytest.raises(ValueError):
        Provenance(rule_id="rule", source_relationship_ids=())


def test_explanation_requires_steps():
    with pytest.raises(ValueError):
        SemanticExplanation(steps=())

    with pytest.raises(ValueError):
        ExplanationStep("")
