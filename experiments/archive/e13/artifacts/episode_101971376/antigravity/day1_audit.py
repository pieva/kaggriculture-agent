"""
Inspect Day 1 Turn 0 to 23 step-by-step between Player 0 and Player 1.
"""

import json
from pathlib import Path

REPLAY_PATH = Path("data/replays/reference/101971376.json")

with open(REPLAY_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

steps = data.get("steps", [])

print("=== DAY 1 STEP-BY-STEP AUDIT ===")
for step_idx in range(24):
    obs0 = steps[step_idx][0]["observation"]
    obs1 = steps[step_idx][1]["observation"]
    act0 = steps[step_idx][0]["action"]
    act1 = steps[step_idx][1]["action"]
    
    hour = obs0["hour"]
    f0 = obs0["farms"][0]
    f1 = obs1["farms"][1]
    
    print(f"\n--- STEP {step_idx:02d} (Day 1 Hour {hour:02d}) ---")
    print(f"Pietro: Money=${f0['money']:.0f}, Farmer={f0['farmer']}, Hands={len(f0['hands'])}")
    print(f"  Farmer Action: {act0.get('farmer')}")
    print(f"  Hands Actions: {act0.get('hands')}")
    print(f"  Market Action: {act0.get('market')}")
    print(f"Harith: Money=${f1['money']:.0f}, Farmer={f1['farmer']}, Hands={len(f1['hands'])}")
    print(f"  Farmer Action: {act1.get('farmer')}")
    print(f"  Hands Actions: {act1.get('hands')}")
    print(f"  Market Action: {act1.get('market')}")
