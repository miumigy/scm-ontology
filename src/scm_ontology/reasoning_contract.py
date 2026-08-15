from __future__ import annotations

from dataclasses import dataclass

from .reasoning_result import ReasoningResult


class ReasoningContractError(ValueError):
    pass


_ALLOWED_STATUSES = frozenset({"matched", "no_match", "failed"})


@dataclass(frozen=True)
class ReasoningContract:
    result: ReasoningResult


def validate_reasoning_contract(contract: ReasoningContract) -> None:
    """Validate lifecycle/status invariants for a reasoning result."""
    result = contract.result
    if result.status not in _ALLOWED_STATUSES:
        raise ReasoningContractError(f"unsupported reasoning status: {result.status}")

    if result.status == "matched" and not result.matches:
        raise ReasoningContractError("matched result must contain at least one match")

    if result.status == "no_match" and result.matches:
        raise ReasoningContractError("no_match result must not contain matches")

    if result.status == "failed" and result.matches:
        raise ReasoningContractError("failed result must not contain matches")
