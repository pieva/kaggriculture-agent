"""
Forensic parser and analysis script for Episode 101971376.
Produces:
- DAILY_TIMELINE.csv
- ACTION_LEDGER.csv
- MARKET_LEDGER.csv
- EVIDENCE_MATRIX.csv
- Detailed analysis JSON for FORENSIC_REPLAY_ANALYSIS.md
"""

import json
import csv
from pathlib import Path
from typing import Dict, Any, List, Tuple
from collections import defaultdict

REPLAY_PATH = Path("data/replays/reference/101971376.json")
OUT_DIR = Path("results/e13/episode_101971376/antigravity")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def analyze():
    print(f"Loading {REPLAY_PATH}...")
    with open(REPLAY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    agents = data.get("info", {}).get("Agents", [])
    rewards = data.get("rewards", [])
    seed = data.get("info", {}).get("seed")
    episode_id = data.get("info", {}).get("EpisodeId")

    print(f"Episode: {episode_id}, Seed: {seed}")
    print(f"Player 0: {agents[0]['Name']} -> Final: ${rewards[0]}")
    print(f"Player 1: {agents[1]['Name']} -> Final: ${rewards[1]}")

    steps = data.get("steps", [])
    num_steps = len(steps)
    print(f"Total steps: {num_steps}")

    # Track daily timelines
    # Day -> Player -> metrics
    daily_timeline = []
    
    # Action Ledger
    action_counts = {
        0: defaultdict(int),
        1: defaultdict(int)
    }
    action_counts_by_phase = {
        0: {"early (D1-10)": defaultdict(int), "mid (D11-20)": defaultdict(int), "late (D21-30)": defaultdict(int)},
        1: {"early (D1-10)": defaultdict(int), "mid (D11-20)": defaultdict(int), "late (D21-30)": defaultdict(int)}
    }
    
    # Market Ledger
    market_ledger = []
    
    # Financial summaries
    financial_summary = {
        0: {
            "revenue": defaultdict(float),
            "revenue_qty": defaultdict(int),
            "spending": defaultdict(float),
            "spending_qty": defaultdict(int),
            "hire_costs": 0.0,
            "land_costs": 0.0,
        },
        1: {
            "revenue": defaultdict(float),
            "revenue_qty": defaultdict(int),
            "spending": defaultdict(float),
            "spending_qty": defaultdict(int),
            "hire_costs": 0.0,
            "land_costs": 0.0,
        }
    }

    # Step-by-step state tracking
    prev_unlocked = {0: ["NW"], 1: ["NW"]}
    prev_money = {0: 3000.0, 1: 3000.0}

    # Daily aggregations
    # Store at end of each day (hour 23)
    daily_records = []

    for step_idx, step_pair in enumerate(steps):
        # step_pair has 2 agent states
        p0_step = step_pair[0]
        p1_step = step_pair[1]
        
        obs0 = p0_step.get("observation", {})
        obs1 = p1_step.get("observation", {})
        
        day = obs0.get("day", 0) + 1
        hour = obs0.get("hour", 0)
        market_obs = obs0.get("market", {})
        prices = market_obs.get("prices", {})

        phase = "early (D1-10)" if day <= 10 else ("mid (D11-20)" if day <= 20 else "late (D21-30)")

        # Analyze each player
        for p_idx, p_step, obs in [(0, p0_step, obs0), (1, p1_step, obs1)]:
            action = p_step.get("action", {})
            farm = obs.get("farms", [{}, {}])[p_idx]
            priv = obs.get("private", {})
            
            # Action processing
            farmer_act = action.get("farmer", ["PASS"])
            hands_acts = action.get("hands", [])
            market_acts = action.get("market", [])

            # Categorize physical actions
            all_unit_acts = [farmer_act] + hands_acts
            for act in all_unit_acts:
                act_name = act[0] if act else "PASS"
                action_counts[p_idx][act_name] += 1
                action_counts_by_phase[p_idx][phase][act_name] += 1

            # Process Market Actions
            for m in market_acts:
                if not m:
                    continue
                m_type = m[0]
                if m_type == "HIRE":
                    action_counts[p_idx]["HIRE"] += 1
                    action_counts_by_phase[p_idx][phase]["HIRE"] += 1
                    # Hire cost in kaggriculture: nth hire of day costs fib(n)
                    # We can track from money difference
                    market_ledger.append({
                        "player": p_idx,
                        "player_name": agents[p_idx]["Name"],
                        "day": day,
                        "hour": hour,
                        "step": step_idx,
                        "type": "HIRE",
                        "item": "HAND",
                        "quantity": 1,
                        "price": None,
                        "total_value": None
                    })
                elif m_type == "BUY_LAND":
                    action_counts[p_idx]["BUY_LAND"] += 1
                    action_counts_by_phase[p_idx][phase]["BUY_LAND"] += 1
                    market_ledger.append({
                        "player": p_idx,
                        "player_name": agents[p_idx]["Name"],
                        "day": day,
                        "hour": hour,
                        "step": step_idx,
                        "type": "BUY_LAND",
                        "item": "LAND_QUADRANT",
                        "quantity": 1,
                        "price": None,
                        "total_value": None
                    })
                elif m_type == "BUY_SEED":
                    crop = m[1]
                    qty = int(m[2]) if len(m) > 2 else 1
                    # Seed prices in agricola: WHEAT: 10, MELON: 80, STRAWBERRY: 40, CARROT: 20, TOMATO: 30
                    seed_prices = {"WHEAT": 10, "MELON": 80, "STRAWBERRY": 40, "CARROT": 20, "TOMATO": 30}
                    unit_p = seed_prices.get(crop, 0)
                    cost = unit_p * qty
                    financial_summary[p_idx]["spending"][f"SEED_{crop}"] += cost
                    financial_summary[p_idx]["spending_qty"][f"SEED_{crop}"] += qty
                    action_counts[p_idx]["BUY_SEED"] += 1
                    action_counts_by_phase[p_idx][phase]["BUY_SEED"] += 1
                    market_ledger.append({
                        "player": p_idx,
                        "player_name": agents[p_idx]["Name"],
                        "day": day,
                        "hour": hour,
                        "step": step_idx,
                        "type": "BUY_SEED",
                        "item": crop,
                        "quantity": qty,
                        "price": unit_p,
                        "total_value": cost
                    })
                elif m_type == "BUY_ANIMAL":
                    animal = m[1]
                    qty = int(m[2]) if len(m) > 2 else 1
                    animal_prices = {"COW": 400, "SHEEP": 500, "GOOSE": 300}
                    unit_p = animal_prices.get(animal, 0)
                    cost = unit_p * qty
                    financial_summary[p_idx]["spending"][f"ANIMAL_{animal}"] += cost
                    financial_summary[p_idx]["spending_qty"][f"ANIMAL_{animal}"] += qty
                    action_counts[p_idx]["BUY_ANIMAL"] += 1
                    action_counts_by_phase[p_idx][phase]["BUY_ANIMAL"] += 1
                    market_ledger.append({
                        "player": p_idx,
                        "player_name": agents[p_idx]["Name"],
                        "day": day,
                        "hour": hour,
                        "step": step_idx,
                        "type": "BUY_ANIMAL",
                        "item": animal,
                        "quantity": qty,
                        "price": unit_p,
                        "total_value": cost
                    })
                elif m_type == "BUY_PRODUCT":
                    prod = m[1]
                    qty = int(m[2]) if len(m) > 2 else 1
                    unit_p = prices.get(prod, 0)
                    cost = unit_p * qty
                    financial_summary[p_idx]["spending"][f"PRODUCT_{prod}"] += cost
                    financial_summary[p_idx]["spending_qty"][f"PRODUCT_{prod}"] += qty
                    action_counts[p_idx]["BUY_PRODUCT"] += 1
                    action_counts_by_phase[p_idx][phase]["BUY_PRODUCT"] += 1
                    market_ledger.append({
                        "player": p_idx,
                        "player_name": agents[p_idx]["Name"],
                        "day": day,
                        "hour": hour,
                        "step": step_idx,
                        "type": "BUY_PRODUCT",
                        "item": prod,
                        "quantity": qty,
                        "price": unit_p,
                        "total_value": cost
                    })
                elif m_type == "SELL":
                    prod = m[1]
                    qty = int(m[2]) if len(m) > 2 else 1
                    unit_p = prices.get(prod, 0)
                    rev = unit_p * qty
                    financial_summary[p_idx]["revenue"][prod] += rev
                    financial_summary[p_idx]["revenue_qty"][prod] += qty
                    action_counts[p_idx]["SELL"] += 1
                    action_counts_by_phase[p_idx][phase]["SELL"] += 1
                    market_ledger.append({
                        "player": p_idx,
                        "player_name": agents[p_idx]["Name"],
                        "day": day,
                        "hour": hour,
                        "step": step_idx,
                        "type": "SELL",
                        "item": prod,
                        "quantity": qty,
                        "price": unit_p,
                        "total_value": rev
                    })

        # At end of day (hour 23), record daily snapshot
        if hour == 23:
            for p_idx, p_step, obs in [(0, p0_step, obs0), (1, p1_step, obs1)]:
                farm = obs.get("farms", [{}, {}])[p_idx]
                priv = obs.get("private", {})
                tiles = farm.get("tiles", [])
                
                crops_count = defaultdict(int)
                animals_count = defaultdict(int)
                weeds_count = 0
                pastures_count = 0
                empty_count = 0
                unwatered_count = 0
                yield_ready_count = 0

                for r in range(10):
                    for c in range(10):
                        t = tiles[r][c]
                        if t is None:
                            empty_count += 1
                        elif isinstance(t, dict):
                            kind = t.get("kind")
                            if kind == "WEED":
                                weeds_count += 1
                            elif kind == "PASTURE":
                                pastures_count += 1
                                animal = t.get("animal")
                                if animal:
                                    animals_count[animal] += 1
                            elif kind == "PLANT":
                                crop = t.get("crop", "WHEAT")
                                crops_count[crop] += 1
                                if not t.get("watered_today", False):
                                    unwatered_count += 1
                                if t.get("yield_units", 0) > 0:
                                    yield_ready_count += 1

                shed = priv.get("shed", {})
                seeds = priv.get("seeds", {})
                unlocked = farm.get("unlocked_quadrants", [])
                money = farm.get("money", 0.0)
                hands = len(farm.get("hands", []))
                hires_today = farm.get("hires_today", 0)

                daily_records.append({
                    "day": day,
                    "player": p_idx,
                    "player_name": agents[p_idx]["Name"],
                    "money": money,
                    "hands": hands,
                    "hires_today": hires_today,
                    "unlocked_quadrants": len(unlocked),
                    "quadrant_names": "+".join(unlocked),
                    "total_crops": sum(crops_count.values()),
                    "wheat_crops": crops_count["WHEAT"],
                    "melon_crops": crops_count["MELON"],
                    "strawberry_crops": crops_count["STRAWBERRY"],
                    "carrot_crops": crops_count["CARROT"],
                    "tomato_crops": crops_count["TOMATO"],
                    "pastures": pastures_count,
                    "cows_on_field": animals_count["COW"],
                    "sheep_on_field": animals_count["SHEEP"],
                    "cows_in_shed": shed.get("COW", 0),
                    "sheep_in_shed": shed.get("SHEEP", 0),
                    "weeds": weeds_count,
                    "empty_owned": empty_count,
                    "unwatered_crops": unwatered_count,
                    "yield_ready_crops": yield_ready_count,
                    "shed_wheat": shed.get("WHEAT", 0),
                    "shed_milk": shed.get("MILK", 0),
                    "shed_wool": shed.get("WOOL", 0),
                    "shed_fertilizer": shed.get("FERTILIZER", 0),
                    "shed_melon": shed.get("MELON", 0),
                    "shed_strawberry": shed.get("STRAWBERRY", 0),
                    "seeds_wheat": seeds.get("WHEAT", 0),
                    "seeds_melon": seeds.get("MELON", 0),
                    "seeds_strawberry": seeds.get("STRAWBERRY", 0),
                })

    # Write DAILY_TIMELINE.csv
    timeline_csv = OUT_DIR / "DAILY_TIMELINE.csv"
    with open(timeline_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=daily_records[0].keys())
        writer.writeheader()
        writer.writerows(daily_records)

    # Write MARKET_LEDGER.csv
    market_csv = OUT_DIR / "MARKET_LEDGER.csv"
    if market_ledger:
        with open(market_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=market_ledger[0].keys())
            writer.writeheader()
            writer.writerows(market_ledger)

    # Write ACTION_LEDGER.csv
    action_csv = OUT_DIR / "ACTION_LEDGER.csv"
    with open(action_csv, "w", newline="", encoding="utf-8") as f:
        all_actions = sorted(list(set(list(action_counts[0].keys()) + list(action_counts[1].keys()))))
        writer = csv.writer(f)
        writer.writerow(["player", "player_name", "phase", "action", "count"])
        for p_idx in (0, 1):
            for act in all_actions:
                writer.writerow([p_idx, agents[p_idx]["Name"], "ALL", act, action_counts[p_idx][act]])
            for phase in ("early (D1-10)", "mid (D11-20)", "late (D21-30)"):
                for act in all_actions:
                    writer.writerow([p_idx, agents[p_idx]["Name"], phase, act, action_counts_by_phase[p_idx][phase][act]])

    # Print summary statistics
    print("\n--- REVENUE BREAKDOWN ---")
    for p_idx in (0, 1):
        name = agents[p_idx]["Name"]
        revs = financial_summary[p_idx]["revenue"]
        total_rev = sum(revs.values())
        print(f"\n{name} (Player {p_idx}) Total Realized Revenue: ${total_rev:.2f}")
        for k, v in sorted(revs.items(), key=lambda x: -x[1]):
            qty = financial_summary[p_idx]["revenue_qty"][k]
            pct = (v / total_rev * 100) if total_rev > 0 else 0
            print(f"  {k:<15}: ${v:<10.2f} ({qty:>4} units, {pct:>5.1f}%)")

    print("\n--- SPENDING BREAKDOWN ---")
    for p_idx in (0, 1):
        name = agents[p_idx]["Name"]
        spends = financial_summary[p_idx]["spending"]
        total_spend = sum(spends.values())
        print(f"\n{name} (Player {p_idx}) Total Tracked Spending: ${total_spend:.2f}")
        for k, v in sorted(spends.items(), key=lambda x: -x[1]):
            qty = financial_summary[p_idx]["spending_qty"][k]
            print(f"  {k:<18}: ${v:<10.2f} ({qty:>4} units)")

    print("\n--- ACTION SUMMARY ---")
    for p_idx in (0, 1):
        name = agents[p_idx]["Name"]
        total_acts = sum(action_counts[p_idx].values())
        print(f"\n{name} (Player {p_idx}) Total Actions: {total_acts}")
        for k, v in sorted(action_counts[p_idx].items(), key=lambda x: -x[1]):
            pct = (v / total_acts * 100) if total_acts > 0 else 0
            print(f"  {k:<18}: {v:<6} ({pct:>5.1f}%)")

    return {
        "agents": agents,
        "rewards": rewards,
        "seed": seed,
        "episode_id": episode_id,
        "financial_summary": financial_summary,
        "action_counts": action_counts,
        "action_counts_by_phase": action_counts_by_phase
    }

if __name__ == "__main__":
    analyze()
