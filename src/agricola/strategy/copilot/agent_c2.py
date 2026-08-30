from typing import Any, Dict, Optional

from agricola.strategy.copilot.c2_config import CopilotC2Config
from agricola.strategy.copilot.c2_policy import CopilotC2Policy


class CopilotC2Agent:
    """C2 candidate entrypoint for the Copilot model."""

    def __init__(self, config: Optional[CopilotC2Config] = None):
        self.config = config or CopilotC2Config()
        self.policy = CopilotC2Policy(config=self.config)

    def __call__(self, obs: Dict[str, Any]) -> Dict[str, Any]:
        actions = self.policy.decide_actions(obs, player_index=0)
        if not actions:
            return {"farmer": ["PASS"], "hands": [], "market": []}
        farmer = actions[0]
        hands = actions[1:]
        return {"farmer": farmer, "hands": hands, "market": []}

    def act(self, state: Any) -> Dict[str, Any]:
        obs = state.raw_obs if hasattr(state, "raw_obs") else state
        return self.__call__(obs)

    def decide(self, state: Any) -> Dict[str, Any]:
        return self.act(state)
