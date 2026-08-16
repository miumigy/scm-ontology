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
        # Only elements actually negotiated by the profile participate in the
        # contract boundary. Provenance remains part of the runtime lineage,
        # but is not implicitly exposed as a wire-level semantic element.
        self.session.build_bundle({"decision_trace": trace, "execution_request": request_id})
        return build_runtime_pipeline(trace, rationale=rationale, request_id=request_id)
