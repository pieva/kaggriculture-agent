"""Antigravity C2 100K 3Q Central Cluster Agent Entrypoint."""

from __future__ import annotations

from typing import Any

from agricola.strategy.antigravity.antigravity_3q_central_cluster import (
    Antigravity3QCentralClusterPolicy,
    CENTRAL_3Q_SPEC_VERSION,
)


class AntigravityC2_100K_Central_Agent:
    """Antigravity C2 100K 3Q Central Cluster Candidate Agent."""

    def __init__(
        self,
        config: Any = None,
        *,
        run_context: dict[str, Any] | None = None,
    ) -> None:
        self.policy = Antigravity3QCentralClusterPolicy(config=config, run_context=run_context)
        self.antigravity_100k_instance = self.policy
        self.last_exception: str | None = None
        self.error_count: int = 0
        self.fallback_count: int = 0

    def act(
        self,
        observation: dict[str, Any],
        configuration: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self.policy.act(observation, configuration=configuration)

    def __call__(
        self,
        observation: dict[str, Any],
        configuration: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        try:
            return self.act(observation, configuration=configuration)
        except Exception as exc:
            self.last_exception = f"{type(exc).__name__}: {exc}"
            self.error_count += 1
            self.fallback_count += 1
            return {"farmer": ["PASS"], "hands": [], "market": []}

    def telemetry_snapshot(self) -> dict[str, Any]:
        return self.policy.telemetry_snapshot()


def create_agent(config: Any = None, run_context: dict[str, Any] | None = None) -> AntigravityC2_100K_Central_Agent:
    return AntigravityC2_100K_Central_Agent(config=config, run_context=run_context)
