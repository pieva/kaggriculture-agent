"""Deep forensic inspection of each replay: crops, livestock, workforce, land expansion, and market operations."""

from __future__ import annotations

import json
from pathlib import Path
from collections import defaultdict, Counter

BENCHMARK_DIR = Path(__file__).resolve().parents[1] / "docs" / "benchmark"
REPLAYS = {
    "LuCcc": (BENCHMARK_DIR / "103484828.json", 1),
    "Gordeev": (BENCHMARK_DIR / "103473619.json", 0),
    "Dipin": (BENCHMARK_DIR / "103462357.json", 1),
    "Petar": (BENCHMARK_DIR / "103464592.json", 1),
}


def deep_inspect_player(name: str, path: Path, opp_idx: int):
    print("=" * 80)
    print(f"DEEP INSPECTION: {name} (Opponent Index: {opp_idx})")
    print("=" * 80)

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    steps = data["steps"]

    # Tracking metrics
    hiring_timeline = []
    land_timeline = []
    animal_purchases = []
    seed_purchases = []
    product_purchases = []
    sales = []

    crop_plantings = [] # step, day, hour, crop, pos
    crop_harvests = [] # step, day, hour, crop, pos, yield
    daily_actions = defaultdict(Counter) # day -> Counter of action types
    daily_crops = defaultdict(Counter) # day -> Counter of crop counts
    daily_animals = defaultdict(Counter) # day -> Counter of animal counts
    daily_money = {}

    # Animal tile tracking
    animal_positions = set()
    pasture_positions = set()

    for step_idx, step_data in enumerate(steps):
        day = step_idx // 24
        hour = step_idx % 24
        agent_state = step_data[opp_idx]
        obs = agent_state["observation"]
        action = agent_state.get("action", {})

        farm = obs["farms"][opp_idx]
        money = farm["money"]
        if hour == 0:
            daily_money[day] = money

        quads = farm.get("unlocked_quadrants", ["NW"])
        quad_count = len(quads) if isinstance(quads, list) else int(quads)

        tiles = farm.get("tiles", [])
        hands = farm.get("hands", [])

        # Actions
        farmer_act = action.get("farmer", ["PASS"]) if isinstance(action, dict) else ["PASS"]
        hands_act = action.get("hands", []) if isinstance(action, dict) else []
        market_act = action.get("market", []) if isinstance(action, dict) else []

        all_acts = [farmer_act] + hands_act
        for act in all_acts:
            if isinstance(act, list) and act:
                daily_actions[day][act[0]] += 1
                if act[0] == "PLANT" and len(act) > 1:
                    crop_plantings.append((step_idx, day, hour, act[1]))
                elif act[0] == "HARVEST":
                    crop_harvests.append((step_idx, day, hour))

        for m_act in market_act:
            if isinstance(m_act, list) and m_act:
                m_type = m_act[0]
                if m_type == "BUY_LAND":
                    land_timeline.append((step_idx, day, hour, quad_count))
                elif m_type == "HIRE":
                    hiring_timeline.append((step_idx, day, hour, len(hands)))
                elif m_type == "BUY_ANIMAL":
                    animal_purchases.append((step_idx, day, hour, m_act[1], m_act[2] if len(m_act) > 2 else 1))
                elif m_type == "BUY_SEED":
                    seed_purchases.append((step_idx, day, hour, m_act[1], m_act[2] if len(m_act) > 2 else 1))
                elif m_type == "BUY_PRODUCT":
                    product_purchases.append((step_idx, day, hour, m_act[1], m_act[2] if len(m_act) > 2 else 1))
                elif m_type == "SELL":
                    sales.append((step_idx, day, hour, m_act[1], m_act[2] if len(m_act) > 2 else 1))

        # Check tiles
        for r_idx, row in enumerate(tiles):
            for c_idx, cell in enumerate(row):
                if isinstance(cell, dict):
                    k = cell.get("kind")
                    if k == "PLANT":
                        daily_crops[day][cell.get("crop")] += 1
                    elif k == "PASTURE":
                        pasture_positions.add((c_idx, r_idx))
                        an = cell.get("animal")
                        if an:
                            animal_positions.add((c_idx, r_idx))
                            daily_animals[day][an] += 1

    print(f"\n--- 1. LAND & WORKFORCE ---")
    print(f"Final Money: ${steps[-1][opp_idx]['reward']:,.2f}")
    print(f"Final Quadrants: {len(farm.get('unlocked_quadrants', ['NW']))}")
    print(f"Land Expansion Events: {land_timeline[:10]}")
    print(f"Total Hires: {len(hiring_timeline)}")
    print(f"Hires per Day:")
    hires_by_day = Counter(t[1] for t in hiring_timeline)
    for d in sorted(hires_by_day.keys()):
        print(f"  Day {d}: {hires_by_day[d]} hires")

    print(f"\n--- 2. LIVESTOCK ARCHITECTURE ---")
    print(f"Pasture Tiles Count: {len(pasture_positions)}")
    print(f"Pasture Positions: {sorted(pasture_positions)}")
    print(f"Animal Purchases: {animal_purchases}")
    print(f"Product (Feed) Purchases: {product_purchases[:10]}")
    print(f"Daily Animal Population Profile:")
    for d in range(0, 30, 3):
        print(f"  Day {d:2d}: {dict(daily_animals[d])}")

    print(f"\n--- 3. CROPS & PLANTING PROFILE ---")
    print(f"Total PLANT actions: {len(crop_plantings)}")
    plants_by_crop = Counter(p[3] for p in crop_plantings)
    print(f"Plants by crop: {plants_by_crop}")
    print(f"Plants by Day & Crop (Sample):")
    plants_by_day_crop = defaultdict(Counter)
    for p in crop_plantings:
        plants_by_day_crop[p[1]][p[3]] += 1
    for d in range(0, 30):
        if plants_by_day_crop[d]:
            print(f"  Day {d:2d}: {dict(plants_by_day_crop[d])}")

    print(f"\n--- 4. DAILY ACTION PROFILE (Sample Days) ---")
    for d in range(0, 30, 3):
        print(f"  Day {d:2d}: {dict(daily_actions[d])}")

    print(f"\n--- 5. SALES & MONETIZATION ---")
    print(f"Total SELL orders: {len(sales)}")
    sales_by_product = Counter(s[3] for s in sales)
    total_units_sold = defaultdict(int)
    for s in sales:
        total_units_sold[s[3]] += s[4]
    print(f"Sales orders by product: {sales_by_product}")
    print(f"Total units sold by product: {dict(total_units_sold)}")
    print(f"Sales timing by day:")
    sales_by_day = defaultdict(list)
    for s in sales:
        sales_by_day[s[1]].append((s[3], s[4]))
    for d in sorted(sales_by_day.keys()):
        print(f"  Day {d:2d}: {sales_by_day[d]}")


def main():
    for name, (path, opp_idx) in REPLAYS.items():
        deep_inspect_player(name, path, opp_idx)


if __name__ == "__main__":
    main()
