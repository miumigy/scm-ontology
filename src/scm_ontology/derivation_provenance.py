from dataclasses import dataclass


@dataclass(frozen=True)
class DerivationProvenance:
    """Canonical link from a derivation step to its provenance sources."""

    rule_id: str
    input_fact_ids: tuple[str, ...]
    source_relationship_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.rule_id:
            raise ValueError("rule_id must not be empty")
        if any(not value for value in self.input_fact_ids):
            raise ValueError("input_fact_ids must not contain empty values")
        if any(not value for value in self.source_relationship_ids):
            raise ValueError("source_relationship_ids must not contain empty values")
