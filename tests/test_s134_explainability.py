import pytest

from scm_ontology.s134_explainability import (
    EvidenceReference,
    EvidenceRole,
    Explanation,
    ReasoningStep,
    build_explanation,
)


def test_evidence_preserves_role_and_epistemic_status() -> None:
    evidence = EvidenceReference(
        ref="observation:1",
        role=EvidenceRole.SUPPORTING,
        epistemic_status="observed",
        authority_ref="source:wms",
    )
    assert evidence.role is EvidenceRole.SUPPORTING
    assert evidence.epistemic_status == "observed"


def test_reasoning_step_can_reference_provenance_inputs() -> None:
    step = ReasoningStep(
        ref="step:1",
        kind="constraint_evaluation",
        input_refs=("state:1",),
        evidence_refs=("observation:1",),
        output_refs=("evaluation:1",),
        epistemic_status="evaluated",
        semantic_version="s134",
    )
    assert step.evidence_refs == ("observation:1",)
    assert step.output_refs == ("evaluation:1",)


def test_explanation_is_not_decision() -> None:
    explanation = build_explanation(
        ref="explanation:1",
        subject_ref="decision:1",
        step_refs=("step:1",),
        evidence_refs=("observation:1",),
    )
    assert explanation.is_decision is False
    assert explanation.invents_evidence is False


def test_scenario_explanation_remains_scenario_scoped() -> None:
    explanation = build_explanation(
        ref="explanation:scenario",
        subject_ref="outcome:hypothetical",
        scenario_ref="scenario:1",
    )
    assert explanation.scenario_ref == "scenario:1"


def test_explanation_requires_subject() -> None:
    with pytest.raises(ValueError):
        build_explanation(ref="explanation:bad", subject_ref="")
