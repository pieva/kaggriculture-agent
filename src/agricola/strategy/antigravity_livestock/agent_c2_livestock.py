"""Antigravity C2 Livestock Strategy Agent Callable (LS1)."""

from __future__ import annotations

from typing import Any, Dict, Optional

from agricola.strategy.antigravity_livestock.c2_livestock_config import AntigravityC2LivestockConfig
from agricola.strategy.antigravity_livestock.c2_livestock_policy import AntigravityC2LivestockPolicy


class AntigravityC2LivestockAgent:
    """Agent implementation wrapping Antigravity C2 Livestock Diagnostic Policy."""

    def __init__(self, config: Optional[AntigravityC2LivestockConfig] = None) -> None:
        self.config = config or AntigravityC2LivestockConfig()
        self.policy = AntigravityC2LivestockPolicy(config=self.config)

    def __call__(
        self,
        observation: Dict[str, Any],
        configuration: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Process observation and produce standardized action schema for Kaggle engine."""
        unit_actions = self.policy.decide_actions(observation)
        farmer_action = unit_actions[0] if unit_actions else ["PASS"]
        hands_actions = unit_actions[1:] if len(unit_actions) > 1 else []
        market_orders = self.policy.decide_market_orders(observation)

        return {
            "farmer": farmer_action,
            "hands": hands_actions,
            "market": market_orders,
        }
