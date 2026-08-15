import pytest

from scm_ontology.reasoning_confidence import (
    ConfidenceFactors,
    ReasoningConfidenceError,
    calculate_reasoning_confidence,
)


def test_confidence_is_transparent_mean_of_factors() -> None:
    factors = ConfidenceFactors(1.0, 0.8, 0.9, 1.0)
    confidence = calculate_reasoning_confidence(factors)
    assert confidence.score == pytest.approx(0.925)
    assert confidence.factors == factors


def test_confidence_factors_are_bounded() -> None:
    with pytest.raises(ReasoningConfidenceError):
        ConfidenceFactors(1.1, 0.8, 0.9, 1.0)
