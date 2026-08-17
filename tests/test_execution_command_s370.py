import pytest

from scm_ontology.execution_command import ExecutionCommandError, build_execution_command


def test_s370_rejects_non_authorized_decision_input():
    with pytest.raises(ExecutionCommandError, match="AuthorizedDecision"):
        build_execution_command(object(), command_type="replenishment", command_id="cmd-1")
