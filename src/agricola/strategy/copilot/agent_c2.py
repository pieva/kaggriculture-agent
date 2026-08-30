from typing import Any, Dict, Optional

from agricola.strategy.copilot.c2_config import CopilotC2Config
from agricola.strategy.copilot.c2_policy import CopilotC2Policy


class CopilotC2Agent:
    """C2 candidate entrypoint for the Copilot model."""

    def __init__(self, config: Optional[CopilotC2Config] = None):
        self.config = config or CopilotC2Config()
        self.policy = CopilotC2Policy(config=self.config)

    def __call__(
        self, obs: Dict[str, Any], configuration: Optional[Any] = None
    ) -> Dict[str, Any]:
        player_index = int(obs.get("player", 0))
        return self.policy.decide(obs, player_index=player_index)

    def act(self, state: Any) -> Dict[str, Any]:
        obs = state.raw_obs if hasattr(state, "raw_obs") else state
        return self.__call__(obs)

    def decide(self, state: Any) -> Dict[str, Any]:
        return self.act(state)
