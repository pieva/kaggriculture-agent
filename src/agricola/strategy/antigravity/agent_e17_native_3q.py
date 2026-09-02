"""Kaggle entrypoint for the Antigravity E17.0 native three-quadrant baseline."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agricola.strategy.antigravity.antigravity_e17_native_3q import (
    E17_NATIVE_MODEL_SPEC_VERSION,
    create_e17_native_agent,
)


REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CONFIG_PATH = (
    REPO_ROOT
    / "experiments"
    / "e17"
    / "configs"
    / "antigravity"
    / "ANTIGRAVITY_E17_0_NATIVE_3Q_BASELINE_CONFIG.json"
)


class AntigravityE17Native3QAgent:
    """Thin adapter around the native E17.0 policy factory."""

    def __init__(self, config_path: Path | str | None = None) -> None:
        self.policy = create_e17_native_agent(config_path=config_path or DEFAULT_CONFIG_PATH)

    def act(self, observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
        return self.policy(observation, configuration)


_AGENT = create_e17_native_agent(config_path=DEFAULT_CONFIG_PATH)


def agent(observation: dict[str, Any], configuration: Any = None) -> dict[str, Any]:
    return _AGENT(observation, configuration)


create_agent = create_e17_native_agent
MODEL_SPEC_VERSION = E17_NATIVE_MODEL_SPEC_VERSION


__all__ = [
    "AntigravityE17Native3QAgent",
    "MODEL_SPEC_VERSION",
    "agent",
    "create_agent",
]
