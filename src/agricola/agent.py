"""Top-level Kaggle submission agent function for E12-X1.10 Continuous Productive Surface."""

from typing import Dict, Any, Optional
from agricola.core.state import GameState
from agricola.strategy.productive_mass_roi import ProductiveMassROIAgent, ProductiveMassConfig

# E12-X1.10 Configuration (continuous productive surface architecture)
E12_X1_10_CONFIG = ProductiveMassConfig(
    productive_core_mode="E12_CONTINUOUS_SURFACE_X110",
    epu_level=3,
    enable_land_expansion=True,
    workforce_scaling_mode="LAND_CO_SCALING",
    multi_hire_mode="CORRECTED_MULTI",
    land_buy_mode="IMMEDIATE",
    stop_hire_day=26,
    max_hires_per_day=8,
    target_tiles_per_worker=7.0,
    max_workers=9,
    target_cows=8
)

_agent_instance = ProductiveMassROIAgent(config=E12_X1_10_CONFIG)


def agent(observation: Dict[str, Any], configuration: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Kaggle submission entry point for E12-X1.10 Continuous Productive Surface.

    Args:
        observation: State dictionary provided by Kaggle Environments.

    Returns:
        Action dictionary with keys 'farmer', 'hands', 'market'.
    """
    try:
        state = GameState(observation)
        return _agent_instance.act(state)
    except Exception:
        # Fallback safe action on any unhandled exception to prevent disqualification
        return {"farmer": ["PASS"], "hands": [], "market": []}
