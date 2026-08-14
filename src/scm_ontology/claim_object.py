from dataclasses import dataclass
from typing import Any, Literal


@dataclass(frozen=True)
class ClaimObject:
    """Canonical object of a Claim.

    An object is either a reference to a canonical/external entity or a literal
    value. The contract does not prescribe identifier, datatype, URI, or
    persistence semantics.
    """

    kind: Literal["reference", "value"]
    reference: str | None = None
    value: Any = None

    def __post_init__(self) -> None:
        if self.kind not in {"reference", "value"}:
            raise ValueError("kind must be 'reference' or 'value'")
        if self.kind == "reference":
            if not self.reference:
                raise ValueError("reference must not be empty for reference objects")
            if self.value is not None:
                raise ValueError("value must be None for reference objects")
        elif self.reference is not None:
            raise ValueError("reference must be None for value objects")

    @classmethod
    def reference_object(cls, reference: str) -> "ClaimObject":
        return cls(kind="reference", reference=reference)

    @classmethod
    def value_object(cls, value: Any) -> "ClaimObject":
        return cls(kind="value", value=value)
