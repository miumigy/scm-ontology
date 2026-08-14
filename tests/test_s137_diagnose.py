import pytest

from scm_ontology.s137_diagnose import (
    Diagnosis,
    DiagnosisEpistemicStatus,
    DiagnosticFinding,
    FindingType,
    build_diagnosis,
)


def test_deviation_does_not_imply_cause() -> None:
    finding = DiagnosticFinding(
        ref="finding:deviation:1",
        finding_type=FindingType.DEVIATION,
        subject_ref="kpi:service-level",
        description="Actual service level is below target",
        epistemic_status=DiagnosisEpistemicStatus.OBSERVED,
    )
    assert finding.causal_assessment_refs == ()


def test_diagnosis_can_have_multiple_candidate_causes() -> None:
    diagnosis = build_diagnosis(
        ref="diagnosis:1",
        subject_ref="process:fulfillment",
        finding_refs=("finding:deviation:1", "finding:exception:1"),
        causal_assessment_refs=("assessment:capacity", "assessment:transport"),
        hypothesis_refs=("hypothesis:capacity", "hypothesis:transport"),
        epistemic_status=DiagnosisEpistemicStatus.INFERRED,
    )
    assert len(diagnosis.hypothesis_refs) == 2
    assert diagnosis.is_decision is False
    assert diagnosis.is_action is False


def test_hypothesized_diagnosis_remains_hypothesis() -> None:
    diagnosis = Diagnosis(
        ref="diagnosis:hypothesis",
        subject_ref="flow:1",
        finding_refs=("finding:cause:1",),
        epistemic_status=DiagnosisEpistemicStatus.HYPOTHESIZED,
    )
    assert diagnosis.epistemic_status is DiagnosisEpistemicStatus.HYPOTHESIZED


def test_scenario_diagnosis_is_isolated() -> None:
    diagnosis = build_diagnosis(
        ref="diagnosis:scenario",
        subject_ref="network:1",
        finding_refs=("finding:capacity:1",),
        scenario_ref="scenario:1",
        epistemic_status=DiagnosisEpistemicStatus.ESTIMATED,
    )
    assert diagnosis.is_scenario_diagnosis is True


def test_diagnosis_requires_finding() -> None:
    with pytest.raises(ValueError):
        Diagnosis(ref="diagnosis:bad", subject_ref="process:1", finding_refs=())
