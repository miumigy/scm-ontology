from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ExtensionLifecycleError(ValueError):
    pass


class ExtensionLifecycleState(str, Enum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    APPLIED = "applied"
    REJECTED = "rejected"
    ROLLED_BACK = "rolled_back"
    DEPRECATED = "deprecated"


_ALLOWED_TRANSITIONS: dict[ExtensionLifecycleState, frozenset[ExtensionLifecycleState]] = {
    ExtensionLifecycleState.PROPOSED: frozenset({ExtensionLifecycleState.ACCEPTED, ExtensionLifecycleState.REJECTED}),
    ExtensionLifecycleState.ACCEPTED: frozenset({ExtensionLifecycleState.APPLIED, ExtensionLifecycleState.REJECTED}),
    ExtensionLifecycleState.APPLIED: frozenset({ExtensionLifecycleState.ROLLED_BACK, ExtensionLifecycleState.DEPRECATED}),
    ExtensionLifecycleState.ROLLED_BACK: frozenset({ExtensionLifecycleState.DEPRECATED}),
    ExtensionLifecycleState.REJECTED: frozenset(),
    ExtensionLifecycleState.DEPRECATED: frozenset(),
}


@dataclass(frozen=True)
class ExtensionLifecycle:
    state: ExtensionLifecycleState

    def transition(self, target: ExtensionLifecycleState) -> ExtensionLifecycle:
        if target not in _ALLOWED_TRANSITIONS[self.state]:
            raise ExtensionLifecycleError(
                f"invalid extension lifecycle transition: {self.state.value} -> {target.value}"
            )
        return ExtensionLifecycle(target)
