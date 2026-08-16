"""Connect negotiated semantic contracts to the canonical runtime pipeline."""
from __future__ import annotations
from dataclasses import dataclass
from .semantic_contract_e2e import SemanticContractSession
from .semantic_runtime import DecisionTrace, RuntimePipeline, build_runtime_pipeline
from .profile_enforcement import enforce_capabilities

@dataclass(frozen=True)
class ContractRuntime:
    session: SemanticContractSession

    def build_pipeline(self, trace: DecisionTrace, *, rationale: str, request_id: str, capability: str = "planning") -> RuntimePipeline:
        enforce_capabilities(self.session.profile, {capability})
        elements = {"decision_trace": trace, "reasoning_provenance": rationale, "execution_request": request_id}
        self.session.build_bundle(elements)
        return build_runtime_pipeline(trace, rationale=rationale, request_id=request_id)
