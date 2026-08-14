"""Canonical semantic rule composition primitives for S54."""

from dataclasses import dataclass


@dataclass(frozen=True)
class InferenceStep:
    """One ordered application of an inference rule."""

    rule_id: str
    input_fact_ids: tuple[str, ...]
    output_fact_id: str


@dataclass(frozen=True)
class Derivation:
    """An ordered, acyclic sequence of inference steps."""

    steps: tuple[InferenceStep, ...]

    def __post_init__(self) -> None:
        produced: set[str] = set()
        for step in self.steps:
            if not step.rule_id:
                raise ValueError("rule_id must not be empty")
            if not step.output_fact_id:
                raise ValueError("output_fact_id must not be empty")
            if step.output_fact_id in produced:
                raise ValueError("output_fact_id must be unique within a derivation")
            if step.output_fact_id in step.input_fact_ids:
                raise ValueError("an inference step cannot consume its own output")
            produced.add(step.output_fact_id)

    def validate_forward_references(self, explicit_fact_ids: set[str] | frozenset[str]) -> None:
        """Reject references to facts produced only by later steps."""
        available = set(explicit_fact_ids)
        for step in self.steps:
            missing = set(step.input_fact_ids) - available
            if missing:
                raise ValueError(
                    "inference step references unavailable facts: " + ", ".join(sorted(missing))
                )
            available.add(step.output_fact_id)
