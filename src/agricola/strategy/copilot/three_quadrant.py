"""Copilot's 3Q central-cluster tournament candidate."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agricola.strategy.antigravity.antigravity_3q_central_cluster import (
    Q0_CENTRAL_PASTURES,
    Q1_CENTRAL_PASTURES,
    Q2_CENTRAL_PASTURES,
    Q2_CONCENTRIC_CROPS,
    Antigravity3QCentralClusterPolicy,
)
from agricola.strategy.antigravity.c2_75k_config import AntigravityC2_75K_Config

COPILOT_3Q_SPEC_VERSION = "COPILOT-C2-3Q-CENTRAL-CLUSTER-13W-V1.0"
_CONFIG_PATH = (
    Path(__file__).resolve().parents[4]
    / "configs"
    / "model_spec_c2"
    / "COPILOT_C2_3Q_CENTRAL_CLUSTER_CONFIG.json"
)

COPILOT_3Q_ROLE_SEQUENCE = (
    "RELIEF_LOGISTICS",
    "CROP_ZONE_0",
    "CROP_ZONE_1",
    "CROP_ZONE_2",
    "LIVESTOCK_COW_Q0",
    "LIVESTOCK_SHEEP_Q0",
    "FERTILIZER_LOGISTICS_Q0",
    "CROP_ZONE_3",
    "CROP_ZONE_4",
    "CROP_ZONE_5",
    "LIVESTOCK_COW_Q1",
    "LIVESTOCK_SHEEP_Q1",
    "FERTILIZER_LOGISTICS_Q1",
)

__all__ = [
    "COPILOT_3Q_ROLE_SEQUENCE",
    "COPILOT_3Q_SPEC_VERSION",
    "Q0_CENTRAL_PASTURES",
    "Q1_CENTRAL_PASTURES",
    "Q2_CENTRAL_PASTURES",
    "Q2_CONCENTRIC_CROPS",
    "CopilotThreeQAgent",
    "CopilotThreeQPolicy",
]


class CopilotThreeQPolicy(Antigravity3QCentralClusterPolicy):
    """Thirteen-worker central cluster retained for baseline measurement only."""

    def __init__(
        self,
        config: AntigravityC2_75K_Config | None = None,
        *,
        run_context: dict[str, Any] | None = None,
    ) -> None:
        if config is None:
            config = AntigravityC2_75K_Config.load(_CONFIG_PATH)
        super().__init__(config=config, run_context=run_context)
        self.candidate_id = "COPILOT_C2_3Q_CENTRAL_CLUSTER"
        self.model_spec_version = COPILOT_3Q_SPEC_VERSION
        self.config.workforce_total = 13
        self.config.q0_workforce_total = 7
        self.config.q1_workforce_total = 13


class CopilotThreeQAgent:
    """Kaggle-compatible entrypoint for the Copilot 3Q candidate."""

    def __init__(self, config: AntigravityC2_75K_Config | None = None) -> None:
        self.policy = CopilotThreeQPolicy(config=config)

    def __call__(
        self, observation: dict[str, Any], configuration: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        return self.policy.act(observation, configuration)

    def act(
        self, observation: dict[str, Any], configuration: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        return self.__call__(observation, configuration)
