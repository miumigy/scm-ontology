# S107 — Constraint, Policy, Rule & Decision Semantics

S107 defines the semantics by which SCM Ontology represents constraints, policies, rules, requirements, objectives, preferences, eligibility, permissions, prohibitions, obligations, decision criteria, recommendations, and decisions.

## Canonical decision

A decision context should distinguish what **must**, **may**, **should**, or **cannot** happen from what is merely preferred or optimized.

```text
Context / State / Observation
          ↓
Requirements / Constraints / Policies
          ↓
Objectives / Preferences
          ↓
Candidate Options
          ↓
Evaluation / Decision Criteria
          ↓
Recommendation
          ↓
Decision
          ↓
Action
```

These concepts are related but are not interchangeable.

## Constraint

A Constraint restricts the set of admissible states, actions, plans, assignments, or outcomes.

Examples:

```text
capacity <= 100
service_level >= 0.95
budget <= ¥10M
MOQ >= 500
lead_time <= 5 days
```

A Constraint answers:

> What possibilities are not admissible?

## Hard Constraint

A Hard Constraint is a constraint that must be satisfied for a candidate to remain admissible.

```text
capacity <= 100
```

A candidate violating a Hard Constraint is normally infeasible unless the governing policy explicitly permits an exception or relaxation.

## Soft Constraint

A Soft Constraint expresses a desired condition that may be violated at a defined cost, penalty, or priority.

```text
preferred_supplier = true
```

Soft constraints should not be represented as hard constraints merely because they are desirable.

## Constraint versus Objective

```text
Constraint
  = defines admissibility

Objective
  = defines what to optimize or improve
```

For example:

```text
Constraint: capacity <= 100
Objective: minimize total cost
```

A candidate can satisfy every constraint while still being inferior under the objective.

## Requirement

A Requirement states a condition that a product, process, plan, service, or outcome is expected or required to satisfy.

A Requirement may become operationalized through one or more Constraints, Rules, Tests, or Policies.

```text
Business Requirement
        ↓
Operational Constraint
```

A Requirement is not automatically equivalent to a mathematical constraint.

## Policy

A Policy is a governed directive that establishes permitted, required, preferred, or prohibited behavior within a defined scope.

Examples:

```text
use preferred carrier when feasible
maintain service level >= 95%
no shipment without required documentation
```

Policy semantics may generate Rules, Constraints, Obligations, or Decision Criteria.

## Rule

A Rule is an explicit conditional or logical relation used to determine an outcome, classification, action, eligibility, or constraint.

```text
IF stock < reorder_point
THEN create replenishment recommendation
```

A Rule is an implementation or reasoning construct; a Policy is the governing directive or intent from which rules may derive.

## Policy versus Rule

```text
Policy
  = governed directive / intent

Rule
  = operationalized logic
```

One Policy may be implemented by multiple Rules.

```text
Policy P1
  ↓
Rule R1
Rule R2
Rule R3
```

## Requirement versus Policy

A Requirement describes something that must be satisfied in a relevant context.

A Policy describes an organizational or governance directive.

A Requirement may originate from:

```text
customer
contract
regulation
business strategy
engineering specification
internal governance
```

A Policy may determine how the organization satisfies or prioritizes that Requirement.

## Obligation

An Obligation represents behavior that is required under a governing context.

```text
Actor A
  ──obligated-to──→ Action X
```

Obligations may arise from Policy, Regulation, Contract, or another governing source.

## Permission

A Permission represents behavior that is allowed under a governing context.

```text
Actor A
  ──permitted-to──→ Action X
```

Permission does not imply that the action is required or preferred.

## Prohibition

A Prohibition represents behavior that is forbidden under a governing context.

```text
Actor A
  ──prohibited-from──→ Action X
```

Prohibition is stronger than a Soft Constraint or Preference.

## Eligibility

Eligibility determines whether an Entity, Candidate, Action, or Plan qualifies for consideration under defined conditions.

```text
Candidate
  ↓ eligibility test
eligible / ineligible / unresolved
```

Eligibility is not itself a Decision; it is an input to decision-making.

## Preference

A Preference expresses a desirable option or ordering without necessarily creating an admissibility requirement.

Examples:

```text
prefer local supplier
prefer lower carbon option
prefer existing carrier
```

Preferences may influence Objectives or Decision Criteria.

## Priority

Priority expresses relative importance among requirements, constraints, objectives, or preferences.

```text
service > cost > carbon
```

Priority is contextual and should not automatically be interpreted as a numerical weight unless the decision method defines such a mapping.

## Objective

An Objective expresses a desired direction or outcome to optimize, maximize, minimize, or otherwise improve.

Examples:

```text
minimize cost
maximize service level
minimize CO2e
maximize utilization
```

An Objective may be single or multi-objective.

## Objective function

An Objective Function is a formal computational representation of an Objective.

```text
minimize:
  total_cost
```

The ontology should distinguish the business Objective from its particular mathematical formulation.

## Multi-objective decision

A Decision may balance multiple Objectives.

```text
cost
service
carbon
risk
```

The method used to trade them off should be preserved where material.

## Trade-off

A Trade-off represents a decision relationship in which improving one objective or criterion may worsen another.

```text
lower cost
   ↕
higher service
```

Trade-offs should not be mistaken for violations of Constraints.

## Decision Criterion

A Decision Criterion is a basis used to compare, rank, evaluate, or select among candidates.

Examples:

```text
total cost
service level
risk
lead time
carbon intensity
```

A Criterion may operationalize an Objective, Requirement, Policy, or Preference.

## Candidate

A Candidate is a possible option under consideration for a Decision.

Examples:

```text
supplier A
supplier B
route X
route Y
production plan P1
production plan P2
```

Candidate status should remain distinct from the final Decision.

## Feasibility

Feasibility indicates whether a Candidate satisfies the applicable Hard Constraints.

```text
Candidate
   ↓ constraints
feasible / infeasible
```

Feasibility is not equivalent to desirability.

## Infeasibility

Infeasibility indicates that a Candidate violates one or more mandatory conditions under the current context.

The violated Constraint should be traceable where explainability matters.

## Constraint relaxation

A Constraint may be relaxed only under an explicit mechanism such as:

```text
exception approval
emergency policy
priority override
constraint softening
```

A violated Hard Constraint must not silently become a Soft Constraint.

## Exception

An Exception represents a recognized deviation from an applicable normal rule, constraint, policy, or expected condition.

An Exception may authorize or explain a deviation but does not automatically change the underlying Policy or Constraint.

## Policy override

An Override represents an explicit authority to supersede an otherwise applicable Policy, Rule, Constraint, or Preference within a defined scope.

```text
Normal Policy
     ↓ override
Exception Decision
     ↓
Alternative Action
```

Override authority and provenance should be preserved when consequential.

## Decision

A Decision is an adopted selection, commitment, authorization, or determination by an Actor or Agent under a defined Decision Context.

```text
Candidates
   ↓
Evaluation
   ↓
Decision
```

A Decision is not merely an analysis result or recommendation.

## Recommendation

A Recommendation is a proposed option or course of action that has not necessarily been adopted.

```text
Analysis
  ↓
Recommendation
  ↓ human / agent decision
Decision
```

Recommendation and Decision must remain distinct.

## Decision Context

A Decision Context contains the relevant information, State, Constraints, Policies, Objectives, Preferences, Candidates, and temporal context used to make a Decision.

Conceptually:

```text
Decision Context
 ├─ Observations
 ├─ States
 ├─ Constraints
 ├─ Policies
 ├─ Objectives
 ├─ Preferences
 ├─ Candidates
 ├─ Scenarios
 └─ Time / Knowledge Context
```

Not every input must be recorded in every implementation.

## Decision authority

A Decision may require a defined authority.

```text
Actor
  ↓
authorized-to-decide
  ↓
Decision
```

Authorization is distinct from participation in analysis or execution.

## Decision responsibility

Where accountability matters, the ontology should distinguish:

```text
Decision maker
Recommendation provider
Action executor
Policy owner
Constraint owner
```

One Actor may occupy multiple roles, but the roles should remain semantically distinct.

## Decision method

A Decision may be produced through:

```text
human judgment
rule engine
optimization
simulation
forecasting
LLM agent
hybrid human + AI process
```

The method should be preserved as provenance where it materially affects interpretation or auditability.

## Decision rationale

A Decision may have a Rationale describing why it was selected.

A Rationale should be distinguishable from the underlying evidence and from the Decision itself.

```text
Evidence
  ↓
Evaluation
  ↓
Rationale
  ↓
Decision
```

## Decision explanation

An Explanation communicates the reasoning or basis for a Decision to an audience.

An Explanation is not necessarily a complete causal or computational proof of the Decision.

This distinction is particularly important for AI-generated explanations.

## Decision evidence

Evidence supporting a Decision may include:

```text
Observation
State
Forecast
Scenario Result
Constraint
Policy
Rule evaluation
Optimization result
Human assessment
```

Evidence provenance follows S104.

## Decision epistemic status

A Decision can have an epistemic status concerning its basis or expected consequences, but the fact that a Decision was made should remain distinct from whether the Decision was correct.

```text
Decision made
  ≠
Decision correct
```

S103 governs epistemic status and uncertainty.

## Decision versus Outcome

```text
Decision
  = adopted choice

Outcome
  = resulting consequence / result
```

An outcome may validate or invalidate expectations but does not retroactively alter the historical fact that a Decision was made.

## Policy evaluation

A Policy may be evaluated against a State or Candidate.

```text
State
 ↓
Policy Evaluation
 ↓
compliant / non-compliant / unresolved
```

Compliance status is distinct from the Policy itself.

## Rule evaluation

A Rule Evaluation records the result of applying a Rule to a context.

```text
Inputs
  ↓
Rule R1
  ↓
true / false / indeterminate
```

The Rule remains unchanged by an individual evaluation.

## Constraint evaluation

A Constraint Evaluation determines whether a Candidate or State satisfies a Constraint.

```text
Candidate P1
   ↓
capacity <= 100
   ↓
satisfied
```

Constraint evaluation should be traceable to the values and method used when required.

## Indeterminate evaluation

A Rule, Policy, or Constraint evaluation may be indeterminate because required information is missing, uncertain, or unresolved.

```text
unknown input
   ↓
indeterminate
```

Indeterminate must not automatically become false.

## Compliance

Compliance describes whether a relevant Entity, Action, State, or process satisfies an applicable Requirement, Policy, Rule, or Regulation.

Possible statuses include:

```text
compliant
non-compliant
partially compliant
exempt
indeterminate
not applicable
```

The vocabulary is extensible by domain.

## Exemption

An Exemption explicitly removes or modifies the applicability of a Requirement, Policy, Rule, or Constraint for a defined scope and period.

```text
Policy P1
  ↓ exemption
Entity E1
```

An exemption should have authority and validity context where material.

## Applicability

Applicability determines whether a Policy, Rule, Requirement, or Constraint applies to a particular context.

```text
Policy P1
  ↓ applicability
Entity E1 / Context C1
```

An inapplicable Policy should not be treated as a violated Policy.

## Scope

Policies, Rules, Constraints, Requirements, and Objectives should have an explicit or inferable scope.

Scope may include:

```text
Entity
Location
Product
Process
Time
Organization
Scenario
Decision context
```

A constraint without scope can be ambiguous.

## Validity period

Governance artifacts may have temporal validity.

```text
Policy P1
valid_from = T1
valid_to   = T2
```

A currently active Policy should not automatically be applied to historical Decisions outside its validity period.

## Versioning

Policies, Rules, Constraints, Objectives, and Decision Methods may be versioned.

```text
Policy v1
   ↓
Policy v2
```

Historical Decisions should remain linked to the version applicable at Decision Time where auditability matters.

## Policy conflict

Multiple Policies or Constraints may conflict.

```text
P1 requires X
P2 prohibits X
```

The ontology should represent the conflict rather than silently selecting one rule.

Conflict resolution requires a governing precedence, authority, or Decision mechanism.

## Precedence

Precedence establishes which applicable Policy, Rule, Constraint, or Requirement has priority when multiple directives interact.

Precedence should be explicit where conflicts are possible.

## Constraint hierarchy

Constraints may form a hierarchy.

```text
Regulatory Requirement
        ↓
Corporate Policy
        ↓
Business Rule
        ↓
Planning Constraint
```

A lower-level implementation should not silently contradict a higher-level governing condition.

## Hardness is contextual

Whether a condition is Hard or Soft may depend on the Decision Context.

```text
Capacity <= 100
```

may be a Hard Constraint during normal planning but a Soft Constraint under an explicitly authorized emergency policy.

The context of relaxation must be preserved.

## Objective versus KPI

A KPI measures or summarizes a condition.

An Objective expresses a desired direction.

```text
KPI: service level = 93%
Objective: service level >= 95%
```

A KPI should not automatically become an Objective merely because it is monitored.

## Target

A Target specifies a desired value, range, threshold, or condition associated with an Objective, KPI, or Requirement.

```text
service level target = 95%
```

Target and Constraint remain distinct:

```text
Target
  = desired

Constraint
  = admissibility condition
```

## Threshold

A Threshold defines a boundary used for evaluation, alerting, classification, or decision logic.

```text
stock < 100 → alert
```

A Threshold is not necessarily a Policy or Constraint.

## Trigger

A Trigger is an Event, condition, or state transition that initiates a Rule, Workflow, Action, or Evaluation.

```text
stockout risk detected
   ↓ trigger
replenishment workflow
```

Trigger semantics should remain distinct from the Rule that determines what happens after triggering.

## Decision and scenario

S102 defines Scenario and Counterfactual semantics.

A Scenario can provide candidate assumptions and projected results for a Decision Context.

```text
Scenario A
  ↓
Projected Result
  ↓
Decision Evaluation
```

Scenario results remain hypothetical until actual events and observations establish corresponding reality.

## Decision and forecast

A Forecast may be evidence for a Decision but is not itself a Decision.

```text
Forecast
  ↓
Evaluation
  ↓
Decision
```

Forecast provenance and epistemic status follow S103/S104.

## Decision and causality

A Decision may be evaluated as a potential cause of an Action or Outcome.

```text
Decision
  ↓
Action
  ↓
Outcome
```

Temporal sequence alone does not establish causal effectiveness. S101 governs causal claims.

## Decision audit chain

A consequential Decision should be traceable through:

```text
Decision
 ├─ authority
 ├─ context
 ├─ applicable policies
 ├─ constraints
 ├─ objectives
 ├─ candidates
 ├─ evaluations
 ├─ recommendation
 ├─ rationale
 └─ evidence
```

S104 provides provenance and lineage semantics for this chain.

## AI decision semantics

An AI Agent may produce:

```text
analysis
prediction
recommendation
Decision
Action
```

These must not be collapsed into one concept.

A system may recommend an Action without having authority to execute it.

```text
AI Recommendation
      ↓ human approval
Decision
      ↓
Action
```

Alternatively, an autonomous agent may have explicit authority to make the Decision and execute the Action. The authority must be represented explicitly.

## AI policy compliance

AI-generated recommendations should be evaluated against applicable Policies and Constraints before execution where required.

```text
LLM Recommendation
       ↓
Policy / Constraint Evaluation
       ↓
Eligible / Ineligible / Indeterminate
       ↓
Decision
```

This provides a semantic basis for governed AI Agents in SCM.

## Human override

A Human Override is an explicit Decision or Action that supersedes an automated recommendation or rule outcome under defined authority.

```text
Automated Recommendation
       ↓
Human Override
       ↓
Decision
```

Override provenance should be preserved where consequential.

## No automatic decision from rule evaluation

A Rule Evaluation may produce `true`, but that does not necessarily mean an Action must be executed.

```text
Rule = true
  ≠
Decision = execute
```

Other Policies, Constraints, Objectives, Authorities, or Human judgments may intervene.

## No automatic truth from compliance

A Candidate being compliant does not imply that it is optimal or selected.

```text
compliant
  ≠
preferred
  ≠
selected
```

## No automatic optimality from objective score

An optimization score is meaningful only relative to its Objective, Constraints, Method, and Decision Context.

```text
score = 10
```

has no universal semantic meaning.

## No universal policy priority

S107 does not define a universal global precedence such as:

```text
law > policy > rule > preference
```

Actual precedence must be established by the relevant governance context.

## No mandatory decision fields

S107 does not mandate that every Decision contain:

```text
reason
score
policy_id
constraint_id
recommendation_id
actor_id
```

These are context-dependent semantic relationships.

## Non-goals

S107 does not define a universal rules engine, optimization solver, policy language, regulatory ontology, workflow engine, decision procedure, AI agent framework, or numerical scoring model.
