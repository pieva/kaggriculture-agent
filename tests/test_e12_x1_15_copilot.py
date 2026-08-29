from agricola.core.state import GameState
from agricola.strategy.productive_mass_roi import ProductiveMassConfig, ProductiveMassROIAgent


def test_copilot_mode_dispatches_without_mutating_config():
    config = ProductiveMassConfig(
        productive_core_mode="E12_X115_COPILOT_INDEPENDENT",
        target_cows=7,
        target_sheep=4,
    )
    agent = ProductiveMassROIAgent(config=config)
    state = GameState({
        "step": 0,
        "day": 0,
        "hour": 0,
        "player": 0,
        "farms": [{
            "money": 3000.0,
            "farmer": [4, 4],
            "hands": [],
            "tiles": [[None] * 10 for _ in range(10)],
            "unlocked_quadrants": ["NW"],
        }],
        "private": {
            "shed": {"WHEAT": 0, "COW": 0, "SHEEP": 0},
            "seeds": {"WHEAT": 0, "MELON": 0, "STRAWBERRY": 0},
            "inventories": [{}],
        },
    })

    action = agent.act(state)

    assert set(action) == {"farmer", "hands", "market"}
    assert config.target_cows == 7
    assert config.target_sheep == 4


def test_copilot_mode_has_state_based_low_capacity_envelope():
    config = ProductiveMassConfig(productive_core_mode="E12_X115_COPILOT_INDEPENDENT")
    agent = ProductiveMassROIAgent(config=config)
    assert agent.config.productive_core_mode == "E12_X115_COPILOT_INDEPENDENT"
