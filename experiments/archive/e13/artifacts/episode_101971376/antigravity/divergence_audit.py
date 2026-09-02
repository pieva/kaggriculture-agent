"""
Deep trajectory and divergence inspection for Episode 101971376.
"""

import json
from pathlib import Path

REPLAY_PATH = Path("data/replays/reference/101971376.json")

with open(REPLAY_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

steps = data.get("steps", [])

print("=== TIMELINE DIVERGENCE AUDIT ===")
print(f"{'Day':<4} {'H':<3} {'P0 Money':<10} {'P1 Money':<10} {'P0 Quads':<9} {'P1 Quads':<9} {'P0 Crops':<9} {'P1 Crops':<9} {'P0 Water':<9} {'P1 Water':<9} {'P0 LS':<10} {'P1 LS':<10}")
print("-" * 115)

p0_cum_water = 0
p1_cum_water = 0

for step_idx, step_pair in enumerate(steps):
    obs0 = step_pair[0]["observation"]
    obs1 = step_pair[1]["observation"]
    day = obs0.get("day", 0) + 1
    hour = obs0.get("hour", 0)
    
    act0 = step_pair[0]["action"]
    act1 = step_pair[1]["action"]

    # Count water actions this turn
    for act in [act0.get("farmer", ["PASS"])] + act0.get("hands", []):
        if act and act[0] == "WATER":
            p0_cum_water += 1
    for act in [act1.get("farmer", ["PASS"])] + act1.get("hands", []):
        if act and act[0] == "WATER":
            p1_cum_water += 1

    if hour == 23:
        f0 = obs0["farms"][0]
        f1 = obs1["farms"][1]
        
        # Count crops
        c0 = sum(1 for r in range(10) for c in range(10) if isinstance(f0["tiles"][r][c], dict) and f0["tiles"][r][c].get("kind") == "PLANT")
        c1 = sum(1 for r in range(10) for c in range(10) if isinstance(f1["tiles"][r][c], dict) and f1["tiles"][r][c].get("kind") == "PLANT")
        
        # Count animals
        a0 = sum(1 for r in range(10) for c in range(10) if isinstance(f0["tiles"][r][c], dict) and f0["tiles"][r][c].get("kind") == "PASTURE" and f0["tiles"][r][c].get("animal"))
        a1 = sum(1 for r in range(10) for c in range(10) if isinstance(f1["tiles"][r][c], dict) and f1["tiles"][r][c].get("kind") == "PASTURE" and f1["tiles"][r][c].get("animal"))
        
        ls0_str = f"A:{a0}"
        ls1_str = f"A:{a1}"
        
        print(f"{day:<4} {hour:<3} ${f0['money']:<9.0f} ${f1['money']:<9.0f} {len(f0['unlocked_quadrants']):<9} {len(f1['unlocked_quadrants']):<9} {c0:<9} {c1:<9} {p0_cum_water:<9} {p1_cum_water:<9} {ls0_str:<10} {ls1_str:<10}")

