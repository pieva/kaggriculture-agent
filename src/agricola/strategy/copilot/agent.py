"""Copilot independent strategy wrapper built on the shared Kaggriculture engine."""

from typing import Any, Dict, Optional

from agricola.core.state import GameState
from agricola.strategy.copilot.config import CopilotConfig
from agricola.strategy.productive_mass_roi import ProductiveMassConfig, ProductiveMassROIAgent


class CopilotROIAgent:
    """Independent Copilot wrapper that keeps its model namespace isolated."""

    def __init__(self, config: Optional[CopilotConfig] = None):
        self.config = config or CopilotConfig()
        self._delegate = ProductiveMassROIAgent(
            config=ProductiveMassConfig(
                productive_core_mode="E12_X115_COPILOT_INDEPENDENT",
                enable_land_expansion=self.config.enable_land_expansion,
                target_cows=self.config.target_cows,
                target_sheep=self.config.target_sheep,
                max_workers=self.config.max_hands,
                stop_hire_day=self.config.stop_hire_day,
            )
        )

    def act(self, state: GameState) -> Dict[str, Any]:
        return self._delegate.act(state)

    def decide(self, state: GameState) -> Dict[str, Any]:
        return self._delegate.decide(state)
