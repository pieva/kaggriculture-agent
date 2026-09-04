"""Smoke test for the early-herd Codex 6-6-2 V4 agent."""

from __future__ import annotations

from agricola.strategy.copilot.e17_topology_662_candidates import (
    CodexE17TopologyCap662V4Agent,
    create_codex_e17_topology_cap_662_v4,
)


def test_codex_topology_cap_662_v4_builds_and_initializes() -> None:
    policy = create_codex_e17_topology_cap_662_v4(
        run_context={"seed": 26090101},
        config_path="docs/model_specs/codex/e17/configs/CODEX_E17_3_TOPOLOGY_CAP_662_V4.json",
    )
    instance = policy.codex_e17_topology_662_v4_instance
    assert isinstance(instance, CodexE17TopologyCap662V4Agent)
    assert instance.candidate_id == "CODEX_E17_3_TOPOLOGY_FILL_662_V4"
    assert instance.model_spec_version == "CODEX-E17.3-TOPOLOGY-FILL-662-V4"
    assert instance.q2_pasture_cap == 2
    assert len(instance.pasture_targets) == 14
    assert len(instance.reclaimed_crop_targets) == 5
    assert instance.early_livestock_cap == 3
    assert instance.early_livestock_activation_day == 6
