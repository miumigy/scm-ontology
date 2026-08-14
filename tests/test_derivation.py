import pytest

from scm_ontology.derivation import Derivation, InferenceStep


def test_derivation_allows_chain_from_earlier_outputs() -> None:
    derivation = Derivation(
        steps=(
            InferenceStep("rule-a", ("fact-0",), "fact-1"),
            InferenceStep("rule-b", ("fact-1",), "fact-2"),
        )
    )
    derivation.validate_forward_references({"fact-0"})


def test_derivation_rejects_forward_reference() -> None:
    derivation = Derivation(
        steps=(
            InferenceStep("rule-a", ("fact-2",), "fact-1"),
            InferenceStep("rule-b", ("fact-0",), "fact-2"),
        )
    )
    with pytest.raises(ValueError, match="unavailable facts"):
        derivation.validate_forward_references({"fact-0"})


def test_derivation_rejects_duplicate_outputs() -> None:
    with pytest.raises(ValueError, match="output_fact_id must be unique"):
        Derivation(
            steps=(
                InferenceStep("rule-a", ("fact-0",), "fact-1"),
                InferenceStep("rule-b", ("fact-0",), "fact-1"),
            )
        )


def test_derivation_rejects_self_reference() -> None:
    with pytest.raises(ValueError, match="cannot consume its own output"):
        Derivation(steps=(InferenceStep("rule-a", ("fact-1",), "fact-1"),))
