"""Copilot V2 3Q strategy package."""

from agricola.strategy.copilot.e18_opponent_reactive_v1 import (
    CopilotE18OpponentReactiveConfig,
    CopilotE18OpponentReactiveV1Policy,
    create_agent,
    create_copilot_e18_opponent_reactive_v1,
    load_copilot_e18_opponent_reactive_v1_config,
)
from agricola.strategy.copilot.three_quadrant import (
    COPILOT_3Q_ROLE_SEQUENCE,
    COPILOT_3Q_SPEC_VERSION,
    CopilotThreeQAgent,
    CopilotThreeQPolicy,
)

__all__ = [
    "COPILOT_3Q_ROLE_SEQUENCE",
    "COPILOT_3Q_SPEC_VERSION",
    "CopilotE18OpponentReactiveConfig",
    "CopilotE18OpponentReactiveV1Policy",
    "CopilotThreeQAgent",
    "CopilotThreeQPolicy",
    "create_agent",
    "create_copilot_e18_opponent_reactive_v1",
    "load_copilot_e18_opponent_reactive_v1_config",
]
