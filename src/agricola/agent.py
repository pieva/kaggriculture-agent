"""Top-level Kaggle submission agent function."""

from typing import Dict, Any, Optional
from agricola.core.state import GameState
from agricola.baseline.carrot_loop import CarrotLoopAgent

# Global agent instance for state persistence across turns if needed
_agent_instance = CarrotLoopAgent()


def agent(observation: Dict[str, Any], configuration: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Kaggle submission entry point.

    Args:
        observation: State dictionary provided by Kaggle Environments.
        configuration: Episode configuration parameters.

    Returns:
        Action dictionary with keys 'farmer', 'hands', 'market'.
    """
    try:
        state = GameState(observation)
        return _agent_instance.act(state)
    except Exception:
        # Fallback safe action on any unhandled exception to prevent disqualification
        return {"farmer": ["PASS"], "hands": [], "market": []}
