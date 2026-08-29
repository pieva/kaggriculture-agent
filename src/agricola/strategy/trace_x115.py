"""
Trace daily progression of X1.15 on seed 421521921.
"""
import json
from kaggle_environments import make
from agricola.core.state import GameState
from agricola.strategy.productive_mass_roi import ProductiveMassConfig, ProductiveMassROIAgent

agent = ProductiveMassROIAgent(config=ProductiveMassConfig(
    productive_core_mode="E12_X115_ANTIGRAVITY_INDEPENDENT",
    enable_land_expansion=True
))

env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": 421521921})
steps = env.reset()

print(f"{'Day':<5} {'Hour':<5} {'Cash':<8} {'Hands':<6} {'Quads':<6} {'Cows':<5} {'Sheep':<6} {'Pastures':<9} {'Weeds':<6} {'Actions'}")
print("-" * 80)

for step_num in range(720):
    obs = steps[0].observation
    state = GameState(obs)
    day = state.day + 1
    hour = state.hour
    
    action = agent.act(state)
    m_acts = action.get("market", [])
    
    if hour == 0 or any(m[0] in ("BUY_LAND", "BUY_ANIMAL") for m in m_acts if isinstance(m, list)):
        animals = {"COW": 0, "SHEEP": 0}
        for y in range(10):
            for x in range(10):
                tile = state.get_tile(x, y)
                if isinstance(tile, dict) and tile.get("kind") == "PASTURE":
                    a = tile.get("animal")
                    if a in animals:
                        animals[a] += 1
        pastures = len(agent._x19_pasture_tiles(state))
        weeds = sum(1 for y in range(10) for x in range(10) if isinstance(state.get_tile(x, y), dict) and state.get_tile(x, y).get("kind") == "WEED")
        m_str = str(m_acts) if m_acts else ""
        print(f"{day:<5} {hour:<5} ${state.money:<7.0f} {len(state.hands_positions):<6} {agent._x18_owned_quadrants(state):<6} {animals['COW']:<5} {animals['SHEEP']:<6} {pastures:<9} {weeds:<6} {m_str}")
        
    steps = env.step([action, {}])
    if steps[0].status in ("DONE", "INVALID", "ERROR"):
        break

print(f"\nFinal Money: ${GameState(steps[0].observation).money:.2f}")
