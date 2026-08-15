import pytest

from scm_ontology.extension_lifecycle import (
    ExtensionLifecycle,
    ExtensionLifecycleError,
    ExtensionLifecycleState,
)


def test_extension_lifecycle_supports_governed_happy_path() -> None:
    lifecycle = ExtensionLifecycle(ExtensionLifecycleState.PROPOSED)
    lifecycle = lifecycle.transition(ExtensionLifecycleState.ACCEPTED)
    lifecycle = lifecycle.transition(ExtensionLifecycleState.APPLIED)
    lifecycle = lifecycle.transition(ExtensionLifecycleState.DEPRECATED)
    assert lifecycle.state is ExtensionLifecycleState.DEPRECATED


def test_extension_lifecycle_rejects_skipping_governance() -> None:
    lifecycle = ExtensionLifecycle(ExtensionLifecycleState.PROPOSED)
    with pytest.raises(ExtensionLifecycleError):
        lifecycle.transition(ExtensionLifecycleState.APPLIED)


def test_rejected_extension_is_terminal() -> None:
    lifecycle = ExtensionLifecycle(ExtensionLifecycleState.REJECTED)
    with pytest.raises(ExtensionLifecycleError):
        lifecycle.transition(ExtensionLifecycleState.ACCEPTED)
