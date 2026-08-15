import pytest

from scm_ontology.reasoning_contract import (
    ReasoningContract,
    ReasoningContractError,
    validate_reasoning_contract,
)
from scm_ontology.reasoning_result import ReasoningResult


def test_matched_result_requires_matches() -> None:
    with pytest.raises(ReasoningContractError):
        validate_reasoning_contract(ReasoningContract(ReasoningResult("result:1", "matched")))


def test_no_match_result_has_no_matches() -> None:
    validate_reasoning_contract(ReasoningContract(ReasoningResult("result:1", "no_match")))


def test_failed_result_has_no_matches() -> None:
    validate_reasoning_contract(ReasoningContract(ReasoningResult("result:1", "failed")))


def test_unsupported_status_is_rejected() -> None:
    with pytest.raises(ReasoningContractError):
        validate_reasoning_contract(ReasoningContract(ReasoningResult("result:1", "unknown")))
