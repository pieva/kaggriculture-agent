"""Antigravity C2 Strategy Agent.

Callable candidate for the MODEL_SPEC C2 tournament.
"""

from typing import Any, Dict, Optional

from agricola.strategy.antigravity.c2_config import AntigravityC2Config
from agricola.strategy.antigravity.c2_policy import AntigravityC2Policy


class AntigravityC2Agent:
    """Antigravity C2 Tournament Candidate Agent."""

    def __init__(self, config: Optional[AntigravityC2Config] = None):
        self.config = config or AntigravityC2Config()
        self.policy = AntigravityC2Policy(config=self.config)

    def act(self, observation: Dict[str, Any], player_index: int = 0) -> Dict[str, Any]:
        """Generate action dict for environment."""
        unit_actions = self.policy.decide_actions(observation, player_index=player_index)
        farmer_action = unit_actions[0] if unit_actions else ["PASS"]
        hands_actions = unit_actions[1:] if len(unit_actions) > 1 else []
        market_orders = self.policy.decide_market_orders(observation, player_index=player_index)
        return {
            "farmer": farmer_action,
            "hands": hands_actions,
            "market": market_orders,
        }

    def __call__(
        self,
        observation: Dict[str, Any],
        configuration: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Standard Kaggle-compatible callable entrypoint."""
        try:
            return self.act(observation)
        except Exception:
            return {"farmer": ["PASS"], "hands": [], "market": []}
