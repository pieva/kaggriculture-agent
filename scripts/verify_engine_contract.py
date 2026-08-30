"""Verify all claims of the Codex Engine Contract Audit directly against the local runtime engine."""

import hashlib
import json
from pathlib import Path

# 1. Check file fingerprints
ENV_DIR = Path(".venv/Lib/site-packages/kaggle_environments/envs/kaggriculture")
DIST_INFO = Path(".venv/Lib/site-packages/kaggle_environments-1.32.7.dist-info")

manifest_files = [
    DIST_INFO / "METADATA",
    ENV_DIR / "AGENTS.md",
    ENV_DIR / "README.md",
    ENV_DIR / "kaggriculture.json",
    ENV_DIR / "kaggriculture.py",
]

print("=== 1. FILE FINGERPRINTS ===")
manifest_entries = []
for p in sorted(manifest_files):
    if p.exists():
        content = p.read_bytes()
        sha = hashlib.sha256(content).hexdigest()
        rel_path = str(p).replace("\\", "/")
        print(f"{rel_path}\t{sha}")
        manifest_entries.append(f"{rel_path}\t{sha}")
    else:
        print(f"MISSING: {p}")

aggregate_string = "\n".join(manifest_entries)
aggregate_sha = hashlib.sha256(aggregate_string.encode("utf-8")).hexdigest()
print(f"\nAggregate SHA256: {aggregate_sha}")
expected_agg = "4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d"
print(f"Expected Agg SHA: {expected_agg}")
print(f"MATCH: {aggregate_sha == expected_agg}")

# 2. Inspect Engine Constants and Logic
print("\n=== 2. ENGINE CONSTANTS ===")
from kaggle_environments.envs.kaggriculture.kaggriculture import CROPS, ANIMALS, PRODUCTS

print(f"CROPS: {list(CROPS.keys())}")
for c, spec in CROPS.items():
    print(f"  {c}: cost={spec['cost']}, first_yield={spec['first_yield']}, max_yield_day={spec.get('max_yield_day')}, "
          f"interval={spec['interval']}, lifespan={spec.get('lifespan')}, max_yield={spec['max_yield']}")

print(f"\nANIMALS: {list(ANIMALS.keys())}")
for a, spec in ANIMALS.items():
    print(f"  {a}: cost={spec['cost']}, structure={spec['structure']}, first_output={spec['first_output']}, "
          f"interval={spec['interval']}, output_product={spec['output_product']}, max_output={spec['max_output']}")

print(f"\nPRODUCTS: {list(PRODUCTS.keys())}")
for pr, spec in PRODUCTS.items():
    print(f"  {pr}: price={spec.get('price', spec.get('base_price'))}")

# 3. Simulate Animal Refresh Matrix
print("\n=== 3. ANIMAL EOD REFRESH SIMULATION ===")
from kaggle_environments.envs.kaggriculture import kaggriculture as kag

# Test COW at day 4 (first output day for COW: first_output = 4)
# We test 4 combinations: (fed_today, cared_today) with consecutive_unfed = 0
def simulate_cow(fed_today: bool, cared_today: bool, consecutive_unfed: int, pending_care: int, age: int):
    plant_or_anim = {
        "kind": "PASTURE",
        "animal": "COW",
        "age": age, # in days
        "fed_today": fed_today,
        "cared_today": cared_today,
        "consecutive_unfed": consecutive_unfed,
        "pending_care_bonus": pending_care,
        "product_ready": False,
        "fertilizer_ready": False,
    }
    farm = {
        "tiles": [[plant_or_anim]],
        "money": 1000,
        "unlocked_quadrants": ["NW"],
    }
    state = {
        "farms": [farm],
    }

    # Run _daily_refresh_animals
    kag._daily_refresh_animals(state, 0)

    tile = farm["tiles"][0][0]
    return tile

# COW: first_output = 4. When placed at Day 0, at Day 4 it is age=4 (which matches first_output).
print("\nTesting COW on first production day (age=4, first_output=4, consecutive_unfed=0, pending_care=0):")
for fed in [True, False]:
    for cared in [True, False]:
        res = simulate_cow(fed_today=fed, cared_today=cared, consecutive_unfed=0, pending_care=0, age=4)
        print(f"  fed={fed:5s}, cared={cared:5s} => product_ready={res.get('product_ready')}, "
              f"output_amount={res.get('product_amount', res.get('amount'))}, "
              f"fertilizer_ready={res.get('fertilizer_ready')}, "
              f"consecutive_unfed={res.get('consecutive_unfed')}, "
              f"pending_care={res.get('pending_care_bonus')}")

# Test escape: when consecutive_unfed reaches threshold (3 for COW / SHEEP / GOOSE)
print("\nTesting COW Escape when consecutive_unfed reaches 3:")
res_escape = simulate_cow(fed_today=False, cared_today=False, consecutive_unfed=2, pending_care=0, age=4)
print(f"  Entering with consecutive_unfed=2 and fed=False => tile={res_escape}")

# 4. Simulate Fertilizer Effect on Plants
print("\n=== 4. FERTILIZER SIMULATION ON PLANTS ===")
def simulate_plant_eod(crop: str, age: int, watered: bool, fert_days: int, current_yield: int):
    tile = {
        "kind": "PLANT",
        "crop": crop,
        "age": age,
        "watered_today": watered,
        "fertilized_days": fert_days,
        "yield": current_yield,
        "consecutive_unwatered": 0,
        "ready": False,
    }
    farm = {
        "tiles": [[tile]],
    }
    state = {"farms": [farm]}

    kag._daily_refresh_plants(state, 0)
    return farm["tiles"][0][0]

print("Testing WHEAT at age=1 -> age=2 (first_yield=2):")
res_unfert = simulate_plant_eod("WHEAT", age=1, watered=True, fert_days=0, current_yield=0)
print(f"  Watered, Unfertilized (fert_days=0) => yield={res_unfert.get('yield')}, age={res_unfert.get('age')}")

res_fert = simulate_plant_eod("WHEAT", age=1, watered=True, fert_days=2, current_yield=0)
print(f"  Watered, Fertilized   (fert_days=2) => yield={res_fert.get('yield')}, age={res_fert.get('age')}, fert_days_left={res_fert.get('fertilized_days')}")

# 5. Simulate Inventory DROP vs PLACE
print("\n=== 5. INVENTORY DROP VS PLACE ===")
import kaggle_environments.envs.kaggriculture.kaggriculture as k_env

# Check drop and place logic directly in source
import inspect
print("Inspecting _apply_unit_action DROP and PLACE handling...")
lines = inspect.getsourcelines(kag._apply_unit_action)[0]
for idx, l in enumerate(lines):
    if "action_name == 'DROP'" in l or "action_name == 'PLACE'" in l:
        print("".join(lines[idx:idx+25]))
        print("-" * 60)
