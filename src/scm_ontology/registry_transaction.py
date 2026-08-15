from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


class RegistryTransactionError(ValueError):
    pass


@dataclass(frozen=True)
class RegistryTransaction(Generic[T]):
    before: T
    after: T

    def commit(self) -> T:
        """Return the prepared immutable snapshot as the transaction result."""
        return self.after


def prepare_registry_transaction(before: T, after: T) -> RegistryTransaction[T]:
    """Prepare an atomic snapshot transition; no external state is mutated."""
    if before == after:
        raise RegistryTransactionError("transaction must contain a registry change")
    return RegistryTransaction(before=before, after=after)
