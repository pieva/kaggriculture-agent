"""
Inspect cow status and worker actions on seed 1273000467.
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

for step_num in range(720):
    obs = steps[0].observation
    state = GameState(obs)
    day = state.day + 1
    hour = state.hour
    
    if day in (20, 21) and hour in (0, 6, 12, 18, 23):
        # Inspect cows
        cows = []
        for y in range(10):
            for x in range(10):
                tile = state.get_tile(x, y)
                if isinstance(tile, dict) and tile.get("kind") == "PASTURE" and tile.get("animal") == "COW":
                    cows.append({
                        "pos": (x, y),
                        "fed": tile.get("fed_today"),
                        "cared": tile.get("cared_today"),
                        "yield": tile.get("yield_units")
                    })
        fed_cnt = sum(1 for c in cows if c["fed"])
        cared_cnt = sum(1 for c in cows if c["cared"])
        yield_cnt = sum(c["yield"] for c in cows)
        print(f"Day {day:02d} H{hour:02d}: Total Cows={len(cows)}, Fed={fed_cnt}, Cared={cared_cnt}, Yield={yield_cnt}, ShedWheat={state.get_shed_count('WHEAT')}")
        
    action = agent.act(state)
    steps = env.step([action, {}])
    if steps[0].status in ("DONE", "INVALID", "ERROR"):
        break
