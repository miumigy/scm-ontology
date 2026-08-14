import pytest

from scm_ontology.s138_plan import Plan, PlanStatus, create_plan


def test_plan_preserves_objectives_constraints_and_policy() -> None:
    plan = create_plan(
        ref="plan:production:1",
        subject_ref="facility:factory-a",
        plan_type="production_plan",
        objective_refs=("objective:service",),
        constraint_refs=("constraint:capacity",),
        policy_refs=("policy:priority",),
        status=PlanStatus.PROPOSED,
    )
    assert plan.objective_refs == ("objective:service",)
    assert plan.constraint_refs == ("constraint:capacity",)
    assert plan.policy_refs == ("policy:priority",)


def test_plan_is_not_schedule_commitment_or_actual() -> None:
    plan = Plan(
        ref="plan:1",
        subject_ref="network:1",
        plan_type="distribution_plan",
    )
    assert plan.is_schedule is False
    assert plan.is_commitment is False
    assert plan.is_actual is False


def test_scenario_plan_remains_scenario_scoped() -> None:
    plan = create_plan(
        ref="plan:scenario:1",
        subject_ref="network:1",
        plan_type="distribution_plan",
        scenario_ref="scenario:capacity-up",
    )
    assert plan.is_scenario_plan is True


def test_plan_revision_keeps_predecessor() -> None:
    plan = create_plan(
        ref="plan:v2",
        subject_ref="network:1",
        plan_type="distribution_plan",
        predecessor_ref="plan:v1",
        status=PlanStatus.SUPERSEDED,
    )
    assert plan.predecessor_ref == "plan:v1"


def test_plan_requires_identity_and_type() -> None:
    with pytest.raises(ValueError):
        Plan(ref="plan:bad", subject_ref="", plan_type="")
