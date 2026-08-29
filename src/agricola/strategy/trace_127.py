"""
Trace seed 1273000467 for X1.15.
"""
from kaggle_environments import make
from agricola.core.state import GameState
from agricola.strategy.productive_mass_roi import ProductiveMassConfig, ProductiveMassROIAgent

agent = ProductiveMassROIAgent(config=ProductiveMassConfig(
    productive_core_mode="E12_X115_ANTIGRAVITY_INDEPENDENT",
    enable_land_expansion=True
))

env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": 1273000467})
steps = env.reset()

print(f"{'Day':<5} {'Hour':<5} {'Cash':<8} {'Hands':<6} {'Quads':<6} {'Cows':<5} {'Sheep':<6} {'Wheat':<7} {'Weeds':<6} {'Market Orders'}")
print("-" * 85)

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
        weeds = sum(1 for y in range(10) for x in range(10) if isinstance(state.get_tile(x, y), dict) and state.get_tile(x, y).get("kind") == "WEED")
        wheat_shed = state.get_shed_count("WHEAT")
        m_str = str(m_acts) if m_acts else ""
        print(f"{day:<5} {hour:<5} ${state.money:<7.0f} {len(state.hands_positions):<6} {agent._x18_owned_quadrants(state):<6} {animals['COW']:<5} {animals['SHEEP']:<6} {wheat_shed:<7} {weeds:<6} {m_str}")
        
    steps = env.step([action, {}])
    if steps[0].status in ("DONE", "INVALID", "ERROR"):
        break

print(f"\nFinal Money: ${GameState(steps[0].observation).money:.2f}")
