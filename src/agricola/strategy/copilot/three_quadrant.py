"""Copilot V2 3Q high-density candidate.

This candidate intentionally does not inherit the Antigravity central-cluster
policy.  It uses the validated high-density three-quadrant execution routine,
including its feed correction, behind a Copilot-owned public interface.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from agricola.strategy.codex.codex_v9_routine_data import ROUTINE_ACTIONS, ROUTINE_SHA256

COPILOT_3Q_SPEC_VERSION = "COPILOT-C2-V2.0-3Q-HIGH-DENSITY"
_CONFIG_PATH = (
    Path(__file__).resolve().parents[4]
    / "docs"
    / "model_specs"
    / "copilot"
    / "configs"
    / "COPILOT_C2_V2_0_3Q_HIGH_DENSITY_CONFIG.json"
)
_SAFE_PASS = {"farmer": ["PASS"], "hands": [], "market": []}

# Retained as a capacity contract for callers that previously consumed the
# worker-sequence constant. The routine activates the farmer and twelve hands.
COPILOT_3Q_ROLE_SEQUENCE = tuple(f"ROUTINE_SLOT_{index}" for index in range(13))

__all__ = [
    "COPILOT_3Q_ROLE_SEQUENCE",
    "COPILOT_3Q_SPEC_VERSION",
    "CopilotThreeQAgent",
    "CopilotThreeQPolicy",
    "load_copilot_3q_config",
]


def load_copilot_3q_config(path: Path | str | None = None) -> dict[str, Any]:
    """Load and validate the immutable execution envelope for Copilot V2."""
    config_path = Path(path) if path is not None else _CONFIG_PATH
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if config.get("candidate_id") != "COPILOT_C2_V2_0_3Q_HIGH_DENSITY":
        raise ValueError("unexpected Copilot V2 candidate_id")
    if config.get("model_spec_version") != COPILOT_3Q_SPEC_VERSION:
        raise ValueError("unexpected Copilot V2 model_spec_version")
    if int(config.get("quadrants_owned", 0)) != 3:
        raise ValueError("Copilot V2 requires three quadrants")
    if int(config.get("workforce_total", 0)) != len(COPILOT_3Q_ROLE_SEQUENCE):
        raise ValueError("Copilot V2 requires the farmer plus twelve hands")
    if config.get("routine_sha256") != ROUTINE_SHA256:
        raise ValueError("Copilot V2 routine provenance does not match")
    if int(config.get("feed_correction_step", -1)) != 195:
        raise ValueError("Copilot V2 requires the D8 feed correction")
    return deepcopy(config)


class CopilotThreeQPolicy:
    """Deterministic high-density 3Q executor with Copilot-owned telemetry."""

    def __init__(
        self,
        candidate_config: dict[str, Any] | None = None,
        *,
        run_context: dict[str, Any] | None = None,
    ) -> None:
        self.config = deepcopy(candidate_config or load_copilot_3q_config())
        self.candidate_id = str(self.config["candidate_id"])
        self.model_spec_version = COPILOT_3Q_SPEC_VERSION
        self.run_context = deepcopy(run_context or {})
        self.error_count = 0
        self.fallback_count = 0
        self.last_exception: str | None = None

    def __call__(
        self, observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        del configuration
        step = int(observation.get("step", 0))
        if not 0 <= step < len(ROUTINE_ACTIONS):
            return deepcopy(_SAFE_PASS)

        action = deepcopy(ROUTINE_ACTIONS[step])
        if step == int(self.config["feed_correction_step"]):
            for order in action.get("market", []) or []:
                if order[:2] == ["BUY_PRODUCT", "WHEAT"]:
                    order[2] = max(
                        int(self.config["minimum_d8_wheat_purchase"]), int(order[2])
                    )
                    break
            action["market"] = [
                order
                for order in action.get("market", []) or []
                if order[:2] != ["BUY_ANIMAL", "COW"]
            ]
        return action

    def act(
        self, observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        return self(observation, configuration)

    def telemetry_snapshot(self) -> dict[str, Any]:
        return {
            "agent_version": self.model_spec_version,
            "candidate_id": self.candidate_id,
            "routine_sha256": ROUTINE_SHA256,
            "errors": self.error_count,
            "fallbacks": self.fallback_count,
            "last_exception": self.last_exception,
        }


class CopilotThreeQAgent:
    """Kaggle-compatible entrypoint for Copilot V2."""

    def __init__(self, candidate_config: dict[str, Any] | None = None) -> None:
        self.policy = CopilotThreeQPolicy(candidate_config=candidate_config)

    def __call__(
        self, observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        return self.policy(observation, configuration)

    def act(
        self, observation: dict[str, Any], configuration: Any = None
    ) -> dict[str, Any]:
        return self.__call__(observation, configuration)
