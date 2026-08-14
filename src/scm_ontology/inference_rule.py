from dataclasses import dataclass


@dataclass(frozen=True)
class InferenceRule:
    """Canonical rule mapping premise semantics to a conclusion semantics.

    A rule defines an inference pattern; it does not execute inference and does
    not identify concrete fact instances produced by a derivation step.
    """

    rule_id: str
    premise_types: tuple[str, ...]
    conclusion_type: str

    def __post_init__(self) -> None:
        if not self.rule_id:
            raise ValueError("rule_id must not be empty")
        if not self.premise_types:
            raise ValueError("premise_types must not be empty")
        if any(not item for item in self.premise_types):
            raise ValueError("premise_types must not contain empty values")
        if not self.conclusion_type:
            raise ValueError("conclusion_type must not be empty")
