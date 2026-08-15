import pytest

from scm_ontology.extension_application_idempotency import (
    ExtensionAlreadyApplied,
    ExtensionApplicationKey,
    ensure_not_already_applied,
)


def test_new_application_is_allowed() -> None:
    key = ExtensionApplicationKey("proposal:1", "v2")
    assert ensure_not_already_applied(key, frozenset()) is True


def test_duplicate_application_is_rejected() -> None:
    key = ExtensionApplicationKey("proposal:1", "v2")
    with pytest.raises(ExtensionAlreadyApplied):
        ensure_not_already_applied(key, frozenset({key}))
