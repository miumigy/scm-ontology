import pytest

from scm_ontology.s142_learn import (
    LearningResult,
    LearningStatus,
    LearningTargetType,
    record_learning,
)


def test_learning_preserves_evidence_and_prior_target() -> None:
    learning = record_learning(
        ref="learning:1",
        subject_ref="service-level:1",
        target_type=LearningTargetType.ASSUMPTION,
        conclusion="Peak demand variability was underestimated.",
        evidence_refs=("measurement:1", "measurement:2"),
        prior_target_ref="assumption:peak-demand:v1",
        confidence_ref="confidence:1",
        status=LearningStatus.ACCEPTED,
    )
    assert learning.evidence_refs == ("measurement:1", "measurement:2")
    assert learning.prior_target_ref == "assumption:peak-demand:v1"


def test_learning_is_not_measurement_or_decision() -> None:
    learning = LearningResult(
        ref="learning:2",
        subject_ref="network:1",
        target_type=LearningTargetType.KNOWLEDGE,
        conclusion="Lead time distribution changed.",
    )
    assert learning.is_measurement is False
    assert learning.is_decision is False


def test_learning_can_inform_policy_without_being_policy() -> None:
    learning = record_learning(
        ref="learning:3",
        subject_ref="inventory:1",
        target_type=LearningTargetType.POLICY,
        conclusion="Increase safety stock during peak season.",
    )
    assert learning.is_policy is True
    assert learning.is_decision is False


def test_scenario_learning_remains_scoped() -> None:
    learning = record_learning(
        ref="learning:scenario:1",
        subject_ref="network:1",
        target_type=LearningTargetType.MODEL,
        conclusion="Alternative lane reduces simulated delay.",
        scenario_ref="scenario:lane-change",
    )
    assert learning.is_scenario_learning is True


def test_learning_requires_conclusion() -> None:
    with pytest.raises(ValueError):
        LearningResult(
            ref="learning:bad",
            subject_ref="network:1",
            target_type=LearningTargetType.KNOWLEDGE,
            conclusion="",
        )
