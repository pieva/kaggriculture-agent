"""Top-level Kaggle submission agent function."""

from typing import Dict, Any, Optional
from agricola.core.state import GameState
from agricola.strategy.water_first_hire_nw_cluster_roi import WaterFirstHIRENWClusterROIAgent

# Global agent instance for E06 Water-First evaluation
_agent_instance = WaterFirstHIRENWClusterROIAgent()


def agent(observation: Dict[str, Any], configuration: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Kaggle submission entry point.

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
