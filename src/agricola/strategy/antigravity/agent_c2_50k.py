"""Antigravity C2 50K Strategy Agent.

Callable candidate for the MODEL_SPEC C2 tournament (50K Codex Transfer Build).
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from agricola.strategy.antigravity.c2_50k_config import AntigravityC2_50K_Config
from agricola.strategy.antigravity.antigravity_compact_q0 import (
    AntigravityC2_50K_Policy,
    MODEL_SPEC_VERSION,
    FOUNDATION_CHECKPOINT,
)


class AntigravityC2_50K_Agent:
    """Antigravity C2 50K Tournament Candidate Agent."""

    def __init__(
        self,
        config: Optional[AntigravityC2_50K_Config] = None,
        *,
        run_context: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.config = config or AntigravityC2_50K_Config.load()
        self.policy = AntigravityC2_50K_Policy(config=self.config, run_context=run_context)
        self.antigravity_50k_instance = self.policy
        self.last_exception: Optional[str] = None
        self.error_count: int = 0
        self.fallback_count: int = 0

    def act(
        self,
        observation: Dict[str, Any],
        configuration: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate action dict for environment."""
        return self.policy.act(observation, configuration=configuration)

    def __call__(
        self,
        observation: Dict[str, Any],
        configuration: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Standard Kaggle-compatible callable entrypoint."""
        try:
            return self.act(observation, configuration=configuration)
        except Exception as exc:
            self.last_exception = f"{type(exc).__name__}: {exc}"
            self.error_count += 1
            self.fallback_count += 1
            return {"farmer": ["PASS"], "hands": [], "market": []}


def create_agent(run_context: Optional[Dict[str, Any]] = None) -> AntigravityC2_50K_Agent:
    """Factory helper creating an Antigravity 50K agent."""
    return AntigravityC2_50K_Agent(run_context=run_context)


__all__ = [
    "AntigravityC2_50K_Agent",
    "create_agent",
    "MODEL_SPEC_VERSION",
    "FOUNDATION_CHECKPOINT",
]
