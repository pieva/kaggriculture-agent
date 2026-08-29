"""
Inspect kaggriculture environment rules for BUY_LAND.
"""
from kaggle_environments import make

env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": 0})
steps = env.reset()

obs = steps[0].observation
print(f"Config: {env.configuration}")
print(f"Farm keys: {obs['farms'][0].keys()}")
print(f"Starting money: {obs['farms'][0]['money']}")
print(f"Unlocked quads: {obs['farms'][0]['unlocked_quadrants']}")

# Test BUY_LAND action directly
# Step 1: BUY_LAND with sufficient money
act0 = {"farmer": ["PASS"], "hands": [], "market": [["BUY_LAND"]]}
steps = env.step([act0, {}])
obs1 = steps[0].observation
print(f"After BUY_LAND step 1: money={obs1['farms'][0]['money']}, unlocked={obs1['farms'][0]['unlocked_quadrants']}")

# Give money if needed and test Q2
# Step 2: BUY_LAND again
act1 = {"farmer": ["PASS"], "hands": [], "market": [["BUY_LAND"]]}
steps = env.step([act1, {}])
obs2 = steps[0].observation
print(f"After BUY_LAND step 2: money={obs2['farms'][0]['money']}, unlocked={obs2['farms'][0]['unlocked_quadrants']}")
