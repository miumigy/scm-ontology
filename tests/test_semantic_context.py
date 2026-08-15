import pytest

from scm_ontology.provenance import Provenance
from scm_ontology.semantic_context import EpistemicKind, SemanticContext
from scm_ontology.temporal_state_event import TemporalAssertion, TemporalKind, TimeInterval


def temporal(kind: TemporalKind) -> TemporalAssertion:
    return TemporalAssertion(
        ref=f"t:{kind}",
        subject_ref="inventory:1",
        kind=kind,
        interval=TimeInterval("2026-01-01"),
    )


def test_context_can_bind_epistemic_temporal_and_provenance_dimensions() -> None:
    context = SemanticContext(
        assertion_ref="assertion:1",
        subject_ref="inventory:1",
        epistemic_kind=EpistemicKind.OBSERVATION,
        temporal_assertions=(temporal(TemporalKind.OBSERVATION),),
        provenance=Provenance("rule:source", ("source:1",)),
        source_ref="source:1",
    )
    assert context.has_provenance is True
    assert context.temporal_kinds() == frozenset({TemporalKind.OBSERVATION})


def test_confidence_does_not_turn_an_assertion_into_a_different_epistemic_kind() -> None:
    context = SemanticContext(
        "assertion:2", "inventory:1", EpistemicKind.INFERENCE, confidence=0.8
    )
    assert context.epistemic_kind is EpistemicKind.INFERENCE


def test_fact_does_not_use_confidence_as_its_status() -> None:
    with pytest.raises(ValueError, match="confidence"):
        SemanticContext("assertion:3", "inventory:1", EpistemicKind.FACT, confidence=1.0)


def test_unknown_cannot_claim_actual_time() -> None:
    with pytest.raises(ValueError, match="actual temporal"):
        SemanticContext(
            "assertion:4", "inventory:1", EpistemicKind.UNKNOWN,
            temporal_assertions=(temporal(TemporalKind.ACTUAL),),
        )


def test_confidence_is_bounded() -> None:
    with pytest.raises(ValueError, match="between 0 and 1"):
        SemanticContext("assertion:5", "inventory:1", EpistemicKind.ESTIMATE, confidence=1.2)
