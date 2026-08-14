# S105 — Identity, Entity Resolution & Temporal Identity Semantics

S105 defines how SCM Ontology distinguishes an Entity from the identifiers, aliases, records, and observations used to refer to it, and how identity changes over time are represented without destroying historical meaning.

## Canonical decision

Identity and identification are distinct.

```text
Entity
  ↑
Identifier / Alias / Record
```

An Identifier is a way to refer to an Entity. It is not the Entity itself.

Entity Resolution is the process of determining whether different references refer to the same Entity, a different Entity, or an unresolved possibility.

Temporal Identity preserves the fact that an Entity's identity, attributes, relationships, organizational status, or identifiers may change over time.

## Entity

An Entity is a distinguishable thing, organization, place, person, role, product, asset, event, or other domain object that the ontology treats as having identity across relevant observations or relationships.

Examples:

```text
Supplier
Customer
Product
Material
SKU
Site
Warehouse
Factory
Carrier
Vehicle
Order
Shipment
```

The exact entity types are domain-specific.

## Identity

Identity is the semantic continuity by which an Entity is treated as the same Entity across references, observations, or time.

Identity is not merely a string value.

```text
Entity E1
  ├─ ERP ID 12345
  ├─ Supplier Code ABC
  └─ legal name "Example Corp."
```

These may be multiple identifiers or representations of one Entity.

## Identifier

An Identifier is a value assigned or used to refer to an Entity within a defined identification context.

Examples:

```text
customer_id
supplier_code
material_number
SKU
DUNS-like identifier
UUID
ERP primary key
```

Identifier semantics are scoped by the system, namespace, issuer, and relevant time.

## Identifier versus Identity

```text
Identifier
  = reference token

Identity
  = semantic continuity of the Entity
```

Therefore:

```text
identifier changed
  ≠ necessarily Entity changed
```

and:

```text
same identifier
  ≠ necessarily same Entity
```

if identifiers are reused or their namespace changes.

## Identifier namespace

An Identifier should be interpreted within its namespace or issuing context where ambiguity is possible.

```text
ERP-A / CUSTOMER / 12345
ERP-B / CUSTOMER / 12345
```

may refer to different Entities.

The raw value `12345` alone is insufficient to establish identity.

## Canonical Identity

A Canonical Identity is the ontology-level representation selected as the authoritative or preferred representation of an Entity within a defined scope.

Canonical does not mean universally true.

A canonical identity may be organization-specific, application-specific, or governance-specific.

## Alias

An Alias is an alternate name or representation used to refer to an Entity.

Examples:

```text
株式会社SUBARU
Subaru Corporation
SUBARU
OEM-001
```

An Alias may be valid only during a defined period or within a defined context.

## Record

A Record is a representation of information about an Entity in a source system, document, dataset, or other information artifact.

A Record is not necessarily an Entity.

```text
ERP Customer Record
       ↓ refers to
Customer Entity
```

Multiple records may refer to the same Entity.

## Entity Resolution

Entity Resolution determines the relationship between references or records.

Possible outcomes include:

```text
same Entity
possible same Entity
different Entities
merged identity
split identity
unresolved
```

Resolution is an analytical or governance result, not a property that can always be inferred from string equality.

## Match versus resolution

A similarity match is evidence for resolution, not necessarily the final identity decision.

```text
Name similarity = high
  ≠
Identity equivalence = confirmed
```

A system may retain both the matching evidence and the resulting resolution status.

## Resolution confidence

Entity resolution may have uncertainty.

```text
Record A
   ↘
    possible match → Entity E1
   ↗
Record B
```

The resolution assessment should preserve its method and confidence where material, following S103.

Confidence does not transform a probabilistic match into an established identity.

## Same-as

`Same-as` expresses that two references are determined to denote the same Entity under a defined scope and epistemic basis.

```text
Record A ──same-as──→ Entity E1
Record B ──same-as──→ Entity E1
```

A same-as assertion should be attributable when it has material operational or audit consequences.

## Different-from

`Different-from` expresses that two references are determined to denote different Entities.

```text
Entity E1 ──different-from──→ Entity E2
```

This should not be inferred solely from different identifiers because multiple identifiers may represent the same Entity.

## Unresolved identity

When available evidence is insufficient, identity should remain unresolved rather than being forced into a same-as or different-from decision.

```text
Record A
   ↓
Unresolved
   ↓
more evidence
   ↓
Resolution
```

This is especially important for automated entity matching.

## Identity scope

Identity may be scoped by:

```text
organization
system
namespace
jurisdiction
business context
time
```

An Entity may therefore have different identifiers in different contexts without becoming multiple Entities.

## Temporal identity

An Entity may retain identity while its attributes, identifiers, organizational structure, or relationships change.

```text
Entity E1
  2024: Supplier A
  2025: Supplier A, renamed
  2026: Supplier A, new address
```

These changes do not automatically imply that E1 ceased to exist.

## Identity versus attributes

A change in an Entity's attribute does not necessarily create a new Entity.

```text
Supplier E1
  name: A
  ↓ rename
Supplier E1
  name: B
```

Identity continuity and attribute history should be represented separately.

## Identity change

Some events may represent a genuine change in identity or legal/operational continuity.

Examples include:

```text
legal succession
merger
acquisition
spin-off
entity dissolution
organizational split
asset replacement
product successor
```

S105 does not prescribe one universal legal interpretation; the ontology should preserve the relevant succession relationship.

## Merge

A Merge represents a transition in which multiple prior Entities become represented by one successor or combined Entity under the applicable domain semantics.

```text
E1 ──┐
     ├──→ E3
E2 ──┘
```

The historical identities E1 and E2 must remain available for historical observations.

## Split

A Split represents a transition in which one prior Entity gives rise to multiple successor Entities.

```text
        ┌──→ E2
E1 ─────┤
        └──→ E3
```

Historical records referring to E1 should not be rewritten as if they originally referred to E2 or E3.

## Succession

Succession represents continuity or transfer between predecessor and successor Entities.

```text
Predecessor E1
      ↓ succeeds / succeeded-by
Successor E2
```

The direction and semantics should be explicit.

## Replacement

Replacement is a domain-specific relation indicating that one operational object is replaced by another.

```text
Machine E1
   ↓ replaced-by
Machine E2
```

Replacement does not necessarily mean that E1 and E2 are the same Entity.

## Product identity

Product identity requires explicit distinction between concepts such as:

```text
Product family
Product model
Material
SKU
Packaging variant
Configuration
Revision
```

A change in packaging, revision, or commercial code does not automatically establish either identity continuity or identity discontinuity.

The applicable identity policy must be explicit.

## Material versus SKU

A Material may represent an operationally defined item while a SKU may represent a stock-keeping representation in a particular organizational or channel context.

```text
Material M1
  ↔ SKU S1 in Location L1
  ↔ SKU S2 in Location L2
```

The ontology should avoid assuming that Material ID and SKU are globally interchangeable.

## Location identity

A physical or logical location may have:

```text
site code
warehouse code
address
GPS coordinates
facility identifier
```

Changes in address, code, ownership, or operational status do not automatically establish whether the underlying Location Entity remains the same.

## Organizational identity

Organizations may change names, ownership, legal status, structure, or identifiers over time.

The ontology should distinguish:

```text
organization identity
organizational unit
legal entity
operating site
ownership relationship
```

This prevents a name change from being mistaken for an Entity replacement.

## Asset identity

An asset may retain identity while undergoing maintenance, relocation, configuration change, or ownership transfer.

```text
Asset E1
  ↓ relocation
Asset E1
```

A replacement asset is generally a distinct Entity unless the domain explicitly defines continuity.

## Event identity

Events may be uniquely identified independently of the Entities participating in them.

```text
Shipment Event E1
  references
Shipment S1
Vehicle V1
Carrier C1
```

Changing an associated Entity does not necessarily change the identity of the historical Event.

## Observation and identity

An Observation refers to an Entity as understood at the observation time and under the source context.

```text
Observation O1
  subject → Entity E1
  observed_at → T1
```

Later identity resolution may improve the mapping without rewriting the original observation content.

## Late identity resolution

An Observation may initially refer to an unresolved source record.

```text
Observation O1
  subject_ref = "SUP-ABC"
  resolution = unresolved

Later:
  "SUP-ABC" same-as Entity E1
```

The original observation and later resolution assessment remain distinguishable.

## Identity provenance

Identity decisions should retain provenance when consequential.

```text
Resolution
  ├─ source records
  ├─ matching method
  ├─ actor / system
  ├─ decision time
  └─ confidence / status
```

This connects S105 to S103 and S104.

## Identity history

Historical identity states should be reconstructable when required.

```text
E1
 ├─ identifier A valid 2024–2025
 ├─ identifier B valid 2025–2026
 └─ alias C valid 2026–
```

Validity periods should not be inferred from current values alone.

## Identifier validity

An identifier may have a validity interval.

```text
Identifier I1
  valid_from = T1
  valid_to   = T2
```

An expired identifier may remain valid for historical references even if it is no longer valid for new transactions.

## Identifier reuse

An identifier may be reused by a system or namespace after an Entity is retired.

Therefore:

```text
same identifier value
  + different validity period
  → potentially different Entity
```

Historical temporal context is required where reuse is possible.

## Entity version versus Entity identity

A changed representation or version of an Entity does not automatically constitute a new Entity.

```text
Entity E1
  Version 1
  Version 2
```

Versioning may describe state/configuration history while identity remains continuous.

Conversely, a successor Entity may require a new identity even when it is commercially described as a new version.

## Identity resolution and temporal context

Entity resolution should consider time when identity evidence changes over time.

```text
Record A at T1 → E1
Record A at T2 → E2
```

A global same-as assertion without temporal scope may be incorrect.

## Historical preservation

When identity resolution changes, historical references should remain reconstructable.

```text
Historical Record
   ↓ originally resolved as
E1

Later governance decision
   ↓
E2
```

The ontology should preserve the historical resolution state where auditability matters.

## Identity uncertainty

Identity may be uncertain without the underlying Entity being uncertain.

```text
Entity exists
  but
record-to-entity mapping is uncertain
```

This distinction is important for data integration and AI-assisted entity resolution.

## No forced canonicalization

A canonical master Entity should not be created merely because multiple records look similar.

Canonicalization requires an explicit resolution basis appropriate to the domain.

## No string-equality identity rule

The ontology must not define:

```text
same string → same Entity
```

as a universal identity rule.

Likewise:

```text
different string → different Entity
```

is not universally valid.

## No universal Entity Resolution algorithm

S105 defines semantic outcomes and boundaries, not a universal matching algorithm.

Implementations may use:

```text
exact matching
rules
master data
graph matching
probabilistic matching
ML
LLM-assisted resolution
human review
```

The method and epistemic status should be preserved where material.

## Relationship to Provenance

S104 answers where a record or assertion came from.

S105 answers what Entity that record or assertion refers to.

```text
Provenance
   ↓
Record
   ↓ entity resolution
Entity
```

These semantics should remain distinct.

## Relationship to Epistemic Status

S103 provides the uncertainty and epistemic vocabulary for identity resolution.

For example:

```text
same-as
status = probable
confidence = 0.92
method = probabilistic matching
```

The exact numeric interpretation of confidence remains governed by S103.

## Relationship to Scenario and Counterfactual

Scenario analysis may refer to Entity identities that are hypothetical, projected, or alternative.

```text
Actual Supplier E1
       ↓
Scenario assumption
Supplier E2
```

Scenario identity must not overwrite actual historical identity.

## Relationship to Decision and Action

Decisions and Actions should reference the Entity identity applicable at their relevant time and context.

```text
Decision D1 at T1
  → Supplier E1

Decision D2 at T2
  → Successor E2
```

This supports historical reconstruction and prevents current master data from rewriting past decisions.

## No mandatory identity fields on every entity

S105 does not mandate a universal property set such as:

```text
canonical_id
name
source_id
valid_from
valid_to
```

for every Entity.

Identity, identifiers, aliases, and temporal validity should be modeled according to the applicable entity type and governance requirements.

## Non-goals

S105 does not define a universal master-data-management product, matching algorithm, legal-entity ontology, identifier standard, UUID policy, database primary-key strategy, or global canonical master.
