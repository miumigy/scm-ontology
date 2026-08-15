import pytest

from scm_ontology.registry_transaction import RegistryTransactionError, prepare_registry_transaction


def test_transaction_commits_prepared_snapshot() -> None:
    tx = prepare_registry_transaction(("old",), ("old", "new"))
    assert tx.commit() == ("old", "new")
    assert tx.before == ("old",)


def test_transaction_rejects_noop() -> None:
    with pytest.raises(RegistryTransactionError):
        prepare_registry_transaction(("same",), ("same",))
