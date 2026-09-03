"""Local harness for the late, non-admitted 6-6-2 V4 prototype.

This module imports repository code and is intentionally not a standalone
Kaggle submission. E17 closed before an economic benchmark of this prototype.
"""

from __future__ import annotations

from agricola.strategy.copilot.e17_topology_662_candidates import (
    CodexE17TopologyCap662V4Agent,
    create_codex_e17_topology_cap_662_v4,
)

RELEASE_ID = "CODEX-E17.3-TOPOLOGY-FILL-662-V4"
MODEL_SPEC_VERSION = "CODEX-E17.3-TOPOLOGY-FILL-662-V4"


def create_agent() -> CodexE17TopologyCap662V4Agent:
    return create_codex_e17_topology_cap_662_v4(
        config_path="experiments/e17/configs/codex/CODEX_E17_3_TOPOLOGY_CAP_662_V4.json"
    )


agent = create_agent()

__all__ = ["MODEL_SPEC_VERSION", "RELEASE_ID", "agent", "create_agent"]
