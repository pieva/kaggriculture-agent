"""Local research harness for the non-promoted 6-6-2 V3 candidate.

This module imports repository code and is intentionally not a standalone
Kaggle submission. The E17 delta tournament found it behaviorally identical
to the V2 control in 28/28 comparable profiles.
"""

from __future__ import annotations

from agricola.strategy.copilot.e17_topology_662_candidates import (
    CodexE17TopologyCap662V3Agent,
    create_codex_e17_topology_cap_662_v3,
)

RELEASE_ID = "CODEX-E17.3-TOPOLOGY-FILL-662-V3"
MODEL_SPEC_VERSION = "CODEX-E17.3-TOPOLOGY-FILL-662-V3"


def create_agent() -> CodexE17TopologyCap662V3Agent:
    return create_codex_e17_topology_cap_662_v3()


agent = create_agent()

__all__ = ["MODEL_SPEC_VERSION", "RELEASE_ID", "agent", "create_agent"]
