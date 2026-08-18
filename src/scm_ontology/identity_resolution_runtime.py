"""P7-C Identity Resolution Runtime (Phase 7, SCM OS Real Data Plane).

Deterministic, governed entity matching that decides whether distinct source
identities refer to the same Canonical Entity, with first-class ambiguous /
unresolved / conflict outcomes.

P7-C composes the P7-A Reference Data Adapter and the P7-B Mapping /
Canonicalization Runtime: identity signals are *explicitly declared* canonical
attributes, and the resolver never infers identity from similarity, field-name
resemblance, or adapter / matching success.

Guardrails honored (S279 / S280 / S288 / S290 / S297):
  - similarity or confidence never establishes Canonical Identity;
  - a CandidateMatch is NOT a Governed Canonical Identity;
  - ambiguous / unresolved / conflict are first-class, never coerced to a match;
  - source identity, provenance, and evidence are preserved;
  - decisions are append-only and replayable;
  - resolution never creates canonical entities and never mutates Canonical
    Truth (canonical_mutation is always False here).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping, Sequence

from .mapping_canonicalization_runtime import CanonicalizationResult, MappingState


class IdentityResolutionError(ValueError):
    """Raised when an identity policy, record, or invocation is invalid."""


# Outcome vocabulary from the S297 multi-source identity-resolution contract.
class ResolutionOutcome(str):
    MATCHED = "matched"
    NOT_MATCHED = "not_matched"
    AMBIGUOUS = "ambiguous"
    UNRESOLVED = "unresolved"
    CONFLICT = "conflict"


# Decision outcomes from the S290 decision contract.
class DecisionOutcome(str):
    ACCEPTED = "accepted_for_governed_application"
    REJECTED = "rejected"
    UNRESOLVED = "unresolved"
    CONFLICTING = "conflicting"
    DEFERRED = "deferred_for_review"


@dataclass(frozen=True)
class IdentitySignal:
    """An explicit canonical attribute used as an identity key signal."""

    canonical_attribute: str
    required: bool = True

    def __post_init__(self) -> None:
        if not self.canonical_attribute.strip():
            raise IdentityResolutionError("canonical_attribute must be non-empty")


@dataclass(frozen=True)
class IdentityResolutionPolicy:
    """Explicit matching policy and evidence interpretation for a run."""

    policy_id: str
    policy_version: str
    signals: tuple[IdentitySignal, ...] = (IdentitySignal("gtin"),)

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise IdentityResolutionError("policy_id must be non-empty")
        if not self.policy_version.strip():
            raise IdentityResolutionError("policy_version must be non-empty")
        if not self.signals:
            raise IdentityResolutionError("at least one identity signal is required")
        attrs = [signal.canonical_attribute for signal in self.signals]
        if len(attrs) != len(set(attrs)):
            raise IdentityResolutionError("identity signals must be unique")


@dataclass(frozen=True)
class IdentityEvidence:
    """Attributeable evidence for one candidate / decision (S289)."""

    source_system: str
    source_identity: str
    signal: str
    value: str | None
    provenance: str

    def __post_init__(self) -> None:
        if not self.source_system.strip():
            raise IdentityResolutionError("source_system must be non-empty")
        if not self.source_identity.strip():
            raise IdentityResolutionError("source_identity must be non-empty")
        if not self.signal.strip():
            raise IdentityResolutionError("signal must be non-empty")
        if not self.provenance.strip():
            raise IdentityResolutionError("provenance must be non-empty")


@dataclass(frozen=True)
class IdentityRecord:
    """One canonicalized reference record as identity-resolution input."""

    source_system: str
    source_identity: str
    canonical_entity_ref: str
    canonical_attributes: Mapping[str, Any]
    provenance: str
    result_id: str = ""

    def __post_init__(self) -> None:
        if not self.source_system.strip():
            raise IdentityResolutionError("source_system must be non-empty")
        if not self.source_identity.strip():
            raise IdentityResolutionError("source_identity must be non-empty")
        if not self.canonical_entity_ref.strip():
            raise IdentityResolutionError("canonical_entity_ref must be non-empty")
        if not self.provenance.strip():
            raise IdentityResolutionError("provenance must be non-empty")

    @classmethod
    def from_canonicalization(cls, result: CanonicalizationResult) -> "IdentityRecord":
        if result.decision_state != MappingState.MAPPED:
            raise IdentityResolutionError(
                f"cannot identity-resolve an unmapped record ({result.decision_state})"
            )
        return IdentityRecord(
            source_system=result.source_system,
            source_identity=result.result_id,
            canonical_entity_ref=result.canonical_target,
            canonical_attributes=result.canonical_attributes,
            provenance=result.source_location,
        )

    @property
    def is_resolved_label(self) -> str:
        return f"{self.source_system}:{self.source_identity}"

    def identity_key(self, policy: IdentityResolutionPolicy) -> tuple[str | None, ...]:
        """Explicit key from declared signals; None = insufficient evidence."""
        key: list[str | None] = []
        for signal in policy.signals:
            value = self.canonical_attributes.get(signal.canonical_attribute)
            if value is None or (isinstance(value, str) and not value.strip()):
                key.append(None)
            else:
                key.append(str(value))
        return tuple(key)

    def is_complete(self, policy: IdentityResolutionPolicy) -> bool:
        return all(value is not None for value in self.identity_key(policy))


@dataclass(frozen=True)
class IdentityCandidate:
    """A proposed, NOT yet governed, correspondence among source identities."""

    candidate_id: str
    outcome: str
    members: tuple[IdentityRecord, ...] = ()
    canonical_entity_ref: str | None = None
    evidence: tuple[IdentityEvidence, ...] = ()
    confidence: float | None = None
    rationale: str = ""

    def __post_init__(self) -> None:
        if not self.candidate_id.strip():
            raise IdentityResolutionError("candidate_id must be non-empty")
        if self.outcome not in {
            ResolutionOutcome.MATCHED,
            ResolutionOutcome.NOT_MATCHED,
            ResolutionOutcome.AMBIGUOUS,
            ResolutionOutcome.UNRESOLVED,
            ResolutionOutcome.CONFLICT,
        }:
            raise IdentityResolutionError(f"invalid outcome: {self.outcome}")
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise IdentityResolutionError("confidence must be in [0,1]")


class IdentityDecision:
    """An append-only governed decision over a candidate (S290).

    A decision is a *decision*, never an implicit Canonical Truth mutation.
    """

    __slots__ = (
        "decision_id", "outcome", "policy_id", "policy_version", "candidate_id",
        "decision_at", "prev_decision_id", "rationale", "canonical_mutation",
    )

    def __init__(
        self,
        decision_id: str,
        outcome: DecisionOutcome,
        policy_id: str,
        policy_version: str,
        candidate_id: str,
        *,
        decision_at: str,
        rationale: str = "",
        prev_decision_id: str | None = None,
        canonical_mutation: bool = False,
    ) -> None:
        if not decision_id.strip():
            raise IdentityResolutionError("decision_id must be non-empty")
        if not policy_id.strip():
            raise IdentityResolutionError("policy_id must be non-empty")
        if not policy_version.strip():
            raise IdentityResolutionError("policy_version must be non-empty")
        if not candidate_id.strip():
            raise IdentityResolutionError("candidate_id must be non-empty")
        if not decision_at.strip():
            raise IdentityResolutionError("decision_at must be non-empty")
        if outcome not in {
            DecisionOutcome.ACCEPTED,
            DecisionOutcome.REJECTED,
            DecisionOutcome.UNRESOLVED,
            DecisionOutcome.CONFLICTING,
            DecisionOutcome.DEFERRED,
        }:
            raise IdentityResolutionError(f"invalid decision outcome: {outcome}")
        if canonical_mutation:
            raise IdentityResolutionError("P7-C identity resolution must not mutate truth")
        self.decision_id = decision_id
        self.outcome = outcome
        self.policy_id = policy_id
        self.policy_version = policy_version
        self.candidate_id = candidate_id
        self.decision_at = decision_at
        self.prev_decision_id = prev_decision_id
        self.rationale = rationale
        self.canonical_mutation = False


@dataclass(frozen=True)
class IdentityResolutionRun:
    """Deterministic, replayable aggregate of a resolution run."""

    run_id: str
    policy: IdentityResolutionPolicy
    records: tuple[IdentityRecord, ...] = field(default_factory=tuple)
    candidates: tuple[IdentityCandidate, ...] = field(default_factory=tuple)
    decisions: tuple[IdentityDecision, ...] = field(default_factory=tuple)
    decision_at: str = ""

    @property
    def matched_count(self) -> int:
        return sum(1 for c in self.candidates if c.outcome == ResolutionOutcome.MATCHED)

    @property
    def conflict_count(self) -> int:
        return sum(1 for c in self.candidates if c.outcome == ResolutionOutcome.CONFLICT)

    @property
    def ambiguous_count(self) -> int:
        return sum(1 for c in self.candidates if c.outcome == ResolutionOutcome.AMBIGUOUS)

    @property
    def unresolved_count(self) -> int:
        return sum(1 for c in self.candidates if c.outcome == ResolutionOutcome.UNRESOLVED)

    def to_json(self) -> str:
        return json.dumps(
            {
                "contract_version": "P7C.1",
                "run_id": self.run_id,
                "policy_id": self.policy.policy_id,
                "policy_version": self.policy.policy_version,
                "decision_at": self.decision_at,
                "matched_count": self.matched_count,
                "conflict_count": self.conflict_count,
                "ambiguous_count": self.ambiguous_count,
                "unresolved_count": self.unresolved_count,
                "candidates": [self._candidate_to_map(c) for c in self.candidates],
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

    @staticmethod
    def _candidate_to_map(candidate: IdentityCandidate) -> dict[str, Any]:
        return {
            "candidate_id": candidate.candidate_id,
            "outcome": candidate.outcome,
            "members": [
                {
                    "source_system": m.source_system,
                    "source_identity": m.source_identity,
                    "canonical_entity_ref": m.canonical_entity_ref,
                    "provenance": m.provenance,
                }
                for m in candidate.members
            ],
            "canonical_entity_ref": candidate.canonical_entity_ref,
            "confidence": candidate.confidence,
            "rationale": candidate.rationale,
            "evidence": [
                {
                    "source_system": e.source_system,
                    "signal": e.signal,
                    "value": e.value,
                    "provenance": e.provenance,
                }
                for e in candidate.evidence
            ],
            "canonical_mutation": False,
        }


def _stable_hash(*parts: str) -> str:
    joined = "\u001f".join(parts)
    return sha256(joined.encode("utf-8")).hexdigest()


class IdentityResolver:
    """Deterministic, read-only governed entity matcher.

    ``identify`` groups IdentityRecords by their explicit identity key and
    reports candidate matches plus ambiguous / unresolved / conflict outcomes,
    then folds them into first-class governed decisions. Nothing mutates truth.
    """

    def __init__(self, policy: IdentityResolutionPolicy) -> None:
        self.policy = policy

    def identify(
        self, records: Iterable[IdentityRecord], *, decision_at: str
    ) -> IdentityResolutionRun:
        records = tuple(records)
        run_id = _stable_hash(
            self.policy.policy_id, self.policy.policy_version, decision_at,
            *[record.is_resolved_label for record in records],
        )

        buckets: dict[tuple[str | None, ...], list[IdentityRecord]] = {}
        for record in records:
            buckets.setdefault(record.identity_key(self.policy), []).append(record)

        candidates: list[IdentityCandidate] = []

        # ambiguous + conflict within a shared key bucket
        for key, members in buckets.items():
            if any(value is None for value in key):
                # unresolved: insufficient identity evidence
                continue
            canonical_refs = {member.canonical_entity_ref for member in members}
            if len(canonical_refs) > 1:
                # the same identity key points to different canonical entities
                candidates.append(self._candidate_conflict(key, members))
                continue
            canonical_ref = members[0].canonical_entity_ref
            sources = {member.source_system for member in members}
            if len(sources) >= 2 and len(members) == len(sources):
                # exactly one record per source, all on the same canonical entity
                candidates.append(self._candidate_matched(key, members, canonical_ref))
            elif len(sources) >= 2:
                # several records on one source share the key -> ambiguous
                candidates.append(self._candidate_ambiguous(key, members, canonical_ref))
            else:
                # a key present in one source only -> not matched to another source
                candidates.append(self._candidate_not_matched(key, members, canonical_ref))

        # records with an incomplete identity signal -> unresolved
        for record in records:
            if not record.is_complete(self.policy):
                candidates.append(self._candidate_unresolved(record))

        candidates = _deduplicate_candidates(candidates)
        decisions = self._decide(candidates, decision_at)

        return IdentityResolutionRun(
            run_id=run_id,
            policy=self.policy,
            records=records,
            candidates=tuple(candidates),
            decisions=tuple(decisions),
            decision_at=decision_at,
        )

    # -- candidate builders ------------------------------------------------
    def _candidate_conflict(
        self, key, members
    ) -> IdentityCandidate:
        return IdentityCandidate(
            candidate_id=_stable_hash(self.policy.policy_id, "conflict",
                                       *sorted(member.is_resolved_label for member in members)),
            outcome=ResolutionOutcome.CONFLICT,
            members=tuple(members),
            canonical_entity_ref=None,
            evidence=self._evidence(members),
            confidence=None,
            rationale="members sharing an identity key point to different canonical entities",
        )

    def _candidate_ambiguous(
        self, key, members, canonical_ref
    ) -> IdentityCandidate:
        return IdentityCandidate(
            candidate_id=_stable_hash(self.policy.policy_id, "ambig",
                                       *sorted(member.is_resolved_label for member in members)),
            outcome=ResolutionOutcome.AMBIGUOUS,
            members=tuple(members),
            canonical_entity_ref=canonical_ref,
            evidence=self._evidence(members),
            confidence=None,
            rationale="multiple records share an identity key; no unique member set",
        )

    def _candidate_matched(
        self, key, members, canonical_ref
    ) -> IdentityCandidate:
        return IdentityCandidate(
            candidate_id=_stable_hash(self.policy.policy_id, "match",
                                       *sorted(member.is_resolved_label for member in members)),
            outcome=ResolutionOutcome.MATCHED,
            members=tuple(members),
            canonical_entity_ref=canonical_ref,
            evidence=self._evidence(members),
            confidence=1.0,
            rationale="explicit identity key across source systems aligns on one canonical entity",
        )

    def _candidate_not_matched(
        self, key, members, canonical_ref
    ) -> IdentityCandidate:
        return IdentityCandidate(
            candidate_id=_stable_hash(self.policy.policy_id, "none",
                                       *sorted(member.is_resolved_label for member in members)),
            outcome=ResolutionOutcome.NOT_MATCHED,
            members=tuple(members),
            canonical_entity_ref=canonical_ref,
            evidence=self._evidence(members),
            confidence=0.0,
            rationale="identity key is not present in any other source system",
        )

    def _candidate_unresolved(self, record: IdentityRecord) -> IdentityCandidate:
        return IdentityCandidate(
            candidate_id=_stable_hash(self.policy.policy_id, "unres",
                                       record.is_resolved_label),
            outcome=ResolutionOutcome.UNRESOLVED,
            members=(record,),
            canonical_entity_ref=None,
            evidence=(),
            confidence=None,
            rationale="identity signal is missing or blank; insufficient evidence",
        )

    def _evidence(self, members: Sequence[IdentityRecord]) -> tuple[IdentityEvidence, ...]:
        result: list[IdentityEvidence] = []
        for member in members:
            for signal in self.policy.signals:
                value = member.canonical_attributes.get(signal.canonical_attribute)
                result.append(
                    IdentityEvidence(
                        source_system=member.source_system,
                        source_identity=member.is_resolved_label,
                        signal=signal.canonical_attribute,
                        value=None if value is None else str(value),
                        provenance=member.provenance,
                    )
                )
        return tuple(result)

    def _decide(
        self, candidates: Sequence[IdentityCandidate], decision_at: str
    ) -> list[IdentityDecision]:
        prior: dict[str, None] = {}
        decisions: list[IdentityDecision] = []
        for index, candidate in enumerate(candidates):
            outcome = self._decision_outcome(candidate)
            decisions.append(
                IdentityDecision(
                    decision_id=_stable_hash(self.policy.policy_id, "d",
                                              candidate.candidate_id, str(index)),
                    outcome=outcome,
                    policy_id=self.policy.policy_id,
                    policy_version=self.policy.policy_version,
                    candidate_id=candidate.candidate_id,
                    decision_at=decision_at,
                    rationale=candidate.rationale,
                    prev_decision_id=list(decisions)[-1].decision_id if decisions else None,
                )
            )
        return decisions

    def _decision_outcome(self, candidate: IdentityCandidate) -> DecisionOutcome:
        if candidate.outcome == ResolutionOutcome.MATCHED:
            return DecisionOutcome.ACCEPTED
        if candidate.outcome == ResolutionOutcome.CONFLICT:
            return DecisionOutcome.CONFLICTING
        return DecisionOutcome.UNRESOLVED


def _deduplicate_candidates(candidates) -> list[IdentityCandidate]:
    seen: set[str] = set()
    unique: list[IdentityCandidate] = []
    for candidate in candidates:
        if candidate.candidate_id in seen:
            continue
        seen.add(candidate.candidate_id)
        unique.append(candidate)
    return unique


# ---------------------------------------------------------------------------
# Deterministic reference path
# ---------------------------------------------------------------------------
REFERENCE_POLICY = IdentityResolutionPolicy(
    policy_id="p7c-reference-policy",
    policy_version="P7C.1",
    signals=(IdentitySignal("gtin"),),
)


def reference_identity_records() -> tuple[IdentityRecord, tuple[IdentityRecord, ...]]:
    # Two source systems both reference the same canonical Product via a shared,
    # explicitly declared GTIN identity signal (one matched, one not matched).
    erp = IdentityRecord(
        source_system="erp",
        source_identity="product/MAT-1000",
        canonical_entity_ref="Material:MAT-1000",
        canonical_attributes={"materialId": "MAT-1000", "gtin": "08500000001015"},
        provenance="reference:row=1",
    )
    wms = IdentityRecord(
        source_system="wms",
        source_identity="sku/SKU-1000",
        canonical_entity_ref="Material:MAT-1000",
        canonical_attributes={"stockId": "SKU-1000", "gtin": "08500000001015"},
        provenance="reference:row=2",
    )
    orphan = IdentityRecord(
        source_system="tms",
        source_identity="ship/SHIP-9",
        canonical_entity_ref="Shipment:SHIP-9",
        canonical_attributes={"shipmentId": "SHIP-9", "gtin": "08500000009999"},
        provenance="reference:row=3",
    )
    return erp, (erp, wms, orphan)


def run_reference_identity_path() -> IdentityResolutionRun:
    """Deterministic reference path: explicit-key identity resolution."""
    _, records = reference_identity_records()
    resolver = IdentityResolver(REFERENCE_POLICY)
    return resolver.identify(records, decision_at="2026-08-19T10:00:00Z")


