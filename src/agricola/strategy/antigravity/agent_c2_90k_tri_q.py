"""Antigravity C2 90K Tri-Quadrant Strategy Agent.

Callable candidate for the MODEL_SPEC C2 tournament (90K Tri-Quadrant Q0+Q1+Q2 Build).
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from agricola.strategy.antigravity.c2_75k_config import AntigravityC2_75K_Config
from agricola.strategy.antigravity.antigravity_tri_q0_q1_q2 import (
    AntigravityTriQPolicy,
    TRI_MODEL_SPEC_VERSION,
)
from agricola.strategy.antigravity.antigravity_compact_q0 import FOUNDATION_CHECKPOINT


class AntigravityC2_90K_Agent:
    """Antigravity C2 90K Tri-Quadrant Candidate Agent."""

    def __init__(
        self,
        config: Optional[AntigravityC2_75K_Config] = None,
        *,
        run_context: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.config = config or AntigravityC2_75K_Config.load()
        self.policy = AntigravityTriQPolicy(config=self.config, run_context=run_context)
        self.antigravity_90k_instance = self.policy
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


def create_agent(run_context: Optional[Dict[str, Any]] = None) -> AntigravityC2_90K_Agent:
    """Factory helper creating an Antigravity 90K agent."""
    return AntigravityC2_90K_Agent(run_context=run_context)
