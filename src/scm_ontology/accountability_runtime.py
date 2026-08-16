"""Public runtime boundary for the canonical accountability contract."""
from __future__ import annotations
from .accountability_contract import accountability_to_mapping, accountability_to_json
from .end_to_end_accountability import EndToEndAccountability

class AccountabilityRuntime:
    """Expose accountability results without leaking internal dataclass details."""
    def mapping(self, result: EndToEndAccountability) -> dict[str, object]:
        return accountability_to_mapping(result)

    def json(self, result: EndToEndAccountability) -> str:
        return accountability_to_json(result)
