"""Antigravity C2 150K+ Candidate Agent Entry Point.

Central Mega-Cluster, 20-Animal Livestock & Strawberry-Dominant Engine.
"""

from __future__ import annotations

from typing import Any

from agricola.strategy.antigravity.antigravity_150k_mega_cluster import (
    Antigravity150KMegaPolicy,
)


class AntigravityC2_150K_Agent:
    """Antigravity 150K candidate agent wrapper."""

    def __init__(self, config: Any = None, run_context: dict[str, Any] | None = None) -> None:
        self.policy = Antigravity150KMegaPolicy(config=config, run_context=run_context)

    def __call__(self, observation: dict[str, Any], configuration: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.policy.act(observation, configuration)

    def act(self, observation: dict[str, Any], configuration: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.policy.act(observation, configuration)

    def telemetry_snapshot(self) -> dict[str, Any]:
        return self.policy.telemetry_snapshot()


def create_agent(config: Any = None, run_context: dict[str, Any] | None = None) -> AntigravityC2_150K_Agent:
    return AntigravityC2_150K_Agent(config=config, run_context=run_context)
