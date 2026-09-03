"""Smoke test for the tournament-derived Codex 6-6-2 V3 agent."""

from __future__ import annotations

from agricola.strategy.copilot.e17_topology_662_candidates import (
    CodexE17TopologyCap662V3Agent,
    create_codex_e17_topology_cap_662_v3,
)


def test_codex_topology_cap_662_v3_builds_and_initializes() -> None:
    policy = create_codex_e17_topology_cap_662_v3(run_context={"seed": 26090101})
    instance = policy.codex_e17_topology_662_v3_instance
    assert isinstance(instance, CodexE17TopologyCap662V3Agent)
    assert instance.candidate_id == "CODEX_E17_3_TOPOLOGY_FILL_662_V3"
    assert instance.model_spec_version == "CODEX-E17.3-TOPOLOGY-FILL-662-V3"
    assert instance.q2_pasture_cap == 2
    assert len(instance.pasture_targets) == 14
    assert len(instance.reclaimed_crop_targets) == 5
    assert instance.livestock_resource_cap == 15
