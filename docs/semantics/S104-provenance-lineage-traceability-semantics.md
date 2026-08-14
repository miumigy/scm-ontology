# S104 — Provenance, Lineage & Traceability Semantics

S104 defines how SCM Ontology preserves the origin, derivation, transformation, custody, and traceability of information and operational artifacts.

## Canonical decision

Provenance, Lineage, Audit Trail, and Traceability are related but distinct semantics.

```text
Source
  ↓
Observation / Artifact
  ↓
Transformation / Derivation
  ↓
Derived Value / Assessment
  ↓
Decision
  ↓
Action
  ↓
Outcome
```

The ontology should be able to explain both **where information came from** and **how it participated in downstream operational decisions**.

## Provenance

Provenance describes the origin, source, actor, system, method, time, or other contextual information that establishes how an artifact came to exist.

Examples:

```text
ERP transaction
IoT sensor
planner input
supplier report
forecast model
optimization solver
LLM inference
```

Provenance answers:

> Where did this artifact or assertion come from?

## Lineage

Lineage describes the chain of transformations, derivations, dependencies, or relationships through which an artifact was produced from other artifacts.

```text
Raw Data
   ↓ ETL
Canonical Observation
   ↓ aggregation
KPI
   ↓ evaluation
Exception
```

Lineage answers:

> How was this artifact derived from upstream artifacts?

## Traceability

Traceability is the ability to follow an artifact, event, decision, or result across relevant upstream and downstream relationships.

```text
Source → Observation → Decision → Action → Outcome
```

Traceability answers:

> Can we follow the chain from origin to consequence, or from consequence back to origin?

## Audit Trail

An Audit Trail records relevant historical activities, changes, accesses, approvals, or state transitions for accountability.

```text
Actor
  ↓
Operation
  ↓
Timestamp
  ↓
Before / After
```

Audit Trail is primarily about historical accountability; Lineage is primarily about derivation and dependency.

## Semantic distinction

```text
Provenance
  = origin/context

Lineage
  = derivation/dependency chain

Traceability
  = ability to traverse relevant relationships

Audit Trail
  = historical record of accountable activity
```

Implementations may use the same technical infrastructure for all four, but their semantic meanings should remain distinct.

## Source

A Source is an identifiable origin of information or an artifact.

Examples include:

```text
system
organization
person
sensor
transaction
file
API
external dataset
model
```

A Source is not necessarily the same as the Actor who produced or supplied the information.

## Origin

Origin identifies the point or context from which an artifact ultimately derives.

Origin may be more stable than a particular transmission or transformation step.

```text
Supplier ERP
   ↓
Integration Platform
   ↓
Data Warehouse
```

The ERP may remain the origin even though the warehouse is the immediate source of a downstream query.

## Immediate source versus ultimate origin

Where useful, the ontology should distinguish:

```text
Immediate Source
  = direct provider of an artifact

Ultimate Origin
  = originating system / actor / event from which it ultimately derives
```

This prevents lineage from stopping at the last data pipeline hop.

## Actor

An Actor is a person, organization, role, system, service, or agent responsible for an activity or assertion.

Actor semantics should be distinguished from Source semantics.

```text
Source = supplier report
Actor  = supplier organization
```

A system can also be an Actor when it autonomously performs an operation.

## System

A System identifies a technical or operational system participating in creation, transformation, storage, or execution.

Examples:

```text
ERP
WMS
TMS
planning engine
IoT platform
LLM agent
```

System identity is provenance information and does not by itself establish truth or quality.

## Method

Method identifies the process, algorithm, procedure, rule, or reasoning mechanism used to create or transform an artifact.

Examples:

```text
ETL mapping
aggregation rule
forecast model
optimization solver
causal analysis
human assessment
LLM prompt + model
```

Method provenance is especially important for derived values and AI-generated assertions.

## Transformation

A Transformation changes the representation, structure, granularity, or content of an upstream artifact to produce a downstream artifact.

```text
CSV
 ↓ parse
Structured Record
 ↓ normalize
Canonical Observation
```

A Transformation does not necessarily change semantic meaning; it may only change representation.

## Derivation

Derivation creates a downstream artifact whose meaning depends on upstream artifacts, a method, or assumptions.

```text
Observations
   ↓ calculation
Inventory KPI
```

Derivation therefore expresses semantic dependency, not merely technical data movement.

## Transformation versus derivation

```text
Transformation
  = representation/process change

Derivation
  = semantic dependence on upstream information
```

A single pipeline operation may perform both.

## Dependency

A Dependency expresses that a downstream artifact relies on an upstream artifact for its validity, calculation, interpretation, or existence.

```text
KPI K1
  depends on
Observation O1
```

Dependency should remain directional.

## Lineage graph

Lineage can be represented as a directed graph:

```text
O1 ──→ D1 ──→ K1 ──→ E1 ──→ X1
```

where:

```text
O1 = Observation
D1 = Derived value
K1 = KPI
E1 = Evaluation
X1 = Exception
```

The exact artifact types may vary by domain.

## End-to-end operational lineage

For SCM decision auditability, a complete chain may look like:

```text
Raw Transaction
      ↓
Canonical Observation
      ↓
Derived KPI
      ↓
Evaluation
      ↓
Exception
      ↓
Decision
      ↓
Action
      ↓
Outcome
      ↓
New Observation
```

This chain connects data lineage with operational traceability.

## Decision provenance

A Decision should be traceable to the information and context that materially informed it when auditability matters.

```text
Observation
Evaluation
Exception
Policy
Constraint
Scenario
Recommendation
      ↓
Decision
```

This does not imply that every input must be recorded for every Decision.

## Action provenance

An Action should be traceable to its originating Decision where one exists.

```text
Decision D1
   ↓
Action A1
```

If an Action is autonomous and has no formal Decision artifact, its triggering context and execution provenance should be represented where material.

## Outcome provenance

An Outcome should be traceable to the Action or process with which it is associated.

```text
Action A1
   ↓
Outcome R1
```

Subsequent Observations provide evidence about the Outcome but should not be substituted for the Outcome itself.

## Evidence provenance

Evidence should retain sufficient provenance to answer:

```text
Who / what supplied it?
When was it obtained?
By what method?
From which system?
Under which version?
Was it transformed?
```

The required level depends on risk and auditability requirements.

## Version provenance

A derived artifact may depend on versions of:

```text
data
schema
mapping
model
rules
policy
code
prompt
configuration
scenario
```

Where reproducibility matters, the relevant version identifiers should be retained.

## Temporal provenance

Lineage should distinguish relevant timestamps where they have different meanings.

```text
source_time
observed_at
received_at
transformed_at
derived_at
published_at
decided_at
executed_at
```

A system should not silently treat these timestamps as interchangeable.

## Time of knowledge

S103 defines the epistemic importance of knowing when information became available.

S104 complements this with provenance of when and through which path the information was produced or transmitted.

```text
Reference Time
    ≠
Source Time
    ≠
Available Time
    ≠
Decision Time
```

This is essential for reconstructing what was knowable at a historical Decision point.

## Provenance of AI-generated information

AI-generated outputs should preserve, where material:

```text
model identity
model version
prompt / instruction context
input artifacts
retrieval sources
timestamp
tool calls
human validation
```

An AI-generated assertion should not inherit the provenance or epistemic status of source data merely because the source data was reliable.

## Human-in-the-loop provenance

Where an AI system proposes and a human approves an action:

```text
AI Recommendation
      ↓
Human Decision
      ↓
Action
```

The AI and human contributions should remain distinguishable where accountability matters.

## Provenance of recommendations

A Recommendation may depend on:

```text
Observations
Forecasts
Scenarios
Policies
Constraints
Optimization results
Model outputs
```

Its provenance should not be confused with the provenance of the eventual Decision.

## Auditability of changes

When an artifact is corrected, superseded, or reclassified, historical lineage should remain reconstructable where required.

```text
Artifact v1
   ↓ correction
Artifact v2
```

The ontology should avoid destructive replacement when the historical state is material to auditability.

## Correction versus rewrite

A correction creates a new semantic state or artifact that explains the correction.

It should not silently rewrite historical meaning.

```text
Original Observation
       ↓
Correction / Assessment
       ↓
Current interpretation
```

This follows the immutability principles established in S99–S103.

## Traceability directions

Traceability may be:

```text
forward / downstream
Source → Decision → Action → Outcome

backward / upstream
Outcome → Action → Decision → Evidence → Source
```

Both directions are required for robust SCM audit and investigation.

## Traceability scope

Not every relationship in the ontology must be traceable indefinitely.

Traceability scope should reflect:

```text
regulatory requirements
business risk
financial impact
operational criticality
security requirements
retention policy
```

S104 defines the semantics, not a universal retention period.

## Chain of custody

Chain of Custody is a specialized provenance concept describing controlled possession, transfer, or handling of an artifact.

It is particularly relevant when evidence integrity matters.

```text
Actor A
  ↓ transfer
Actor B
  ↓ transfer
System C
```

Chain of Custody should not be used as a synonym for general Lineage.

## Data lineage versus business lineage

Technical data lineage may describe:

```text
Table → Column → Transformation → Table
```

Business lineage may describe:

```text
Observation → KPI → Evaluation → Decision
```

Both are useful, but they answer different questions.

## Semantic lineage versus physical lineage

Physical lineage describes where data physically moved.

Semantic lineage describes how meaning or operational dependency was derived.

```text
Physical:
ERP DB → ETL → Warehouse

Semantic:
Order Transaction → Delivery Observation → OTIF KPI → Evaluation
```

S104 primarily defines the semantic layer while allowing integration with physical lineage systems.

## Provenance and epistemic status

Provenance supports epistemic interpretation but does not determine truth by itself.

```text
Source = trusted ERP
  ≠ automatically
Assertion = true
```

Likewise:

```text
LLM source
  ≠ automatically
Assertion = false
```

Epistemic status remains governed by S103.

## Provenance and causal attribution

Causal attribution may use provenance to establish the chain of evidence, but provenance alone does not establish causality.

```text
Evidence provenance
      ↓
Causal analysis
      ↓
Causal conclusion
```

S101 causal semantics remain applicable.

## Scenario lineage

Scenario results should preserve their dependence on:

```text
base context
assumptions
scenario version
model version
input data
candidate decisions
```

```text
Base Context
   ↓
Scenario A
   ↓
Simulation v3
   ↓
Scenario Result
```

Scenario lineage must remain distinct from actual operational lineage.

## Forecast lineage

Forecasts should be traceable to:

```text
input observations
feature transformations
forecast method
model version
forecast horizon
creation time
```

A later actual Observation may be compared with a Forecast without replacing its historical forecast provenance.

## Reproducibility

Where a result is used for consequential decisions, lineage should support reconstruction of the relevant computation or reasoning context to an appropriate degree.

Conceptually:

```text
Inputs
 + Versions
 + Method
 + Configuration
 + Time
 → Result
```

S104 does not require bit-for-bit reproducibility in every domain.

## Lineage breaks

A lineage chain may contain unresolved gaps.

For example:

```text
Source
  ↓
Observation
  ↓
???
  ↓
Decision
```

A missing lineage segment should be represented as a traceability limitation rather than invented.

## Trust boundary

Crossing system, organizational, or methodological boundaries may change the provenance context.

```text
Internal ERP
      ↓
External Supplier Feed
      ↓
AI Model
```

The boundary itself may be material to trust, validation, or audit requirements.

## No mandatory lineage fields on Observation

S104 does not add a universal set of fields such as:

```text
source_id
lineage_id
created_by
created_at
updated_by
version
```

to the canonical Observation primitive.

These belong to provenance, lineage, audit, identity, or metadata models and should be linked according to implementation needs.

## Non-goals

S104 does not define a universal data-lineage product, retention policy, audit standard, chain-of-custody regulation, event-sourcing architecture, metadata catalog, or physical ETL implementation.
