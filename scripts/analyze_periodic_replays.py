"""Analyze the 4 Kaggle benchmark replays to extract biological, operational, and market periodicity."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple
from collections import defaultdict, Counter

BENCHMARK_DIR = Path(__file__).resolve().parents[1] / "docs" / "benchmark"
REPLAYS = {
    "LuCcc_103484828": BENCHMARK_DIR / "103484828.json",
    "Gordeev_103473619": BENCHMARK_DIR / "103473619.json",
    "Dipin_103462357": BENCHMARK_DIR / "103462357.json",
    "Petar_103464592": BENCHMARK_DIR / "103464592.json",
}


def analyze_replay(name: str, path: Path) -> Dict[str, Any]:
    print(f"Loading {name} from {path}...")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Kaggle episode structure: steps is a list of steps, each step has list of agent states [p0, p1]
    steps = data.get("steps", [])
    if not steps:
        return {"error": "no steps"}

    # Identify opponent player index (Antigravity vs Opponent)
    # Check rewards at last step
    last_step = steps[-1]
    r0 = last_step[0].get("reward", 0.0)
    r1 = last_step[1].get("reward", 0.0)

    # Opponent is the high-scoring player
    opp_idx = 1 if (r1 or 0) > (r0 or 0) else 0
    ant_idx = 1 - opp_idx

    print(f"  {name}: P0 reward={r0}, P1 reward={r1} => Opponent index = {opp_idx}")

    # Track opponent metrics across all steps
    timeline = []
    action_counts = Counter()
    crop_events = []
    animal_events = []
    market_events = []
    land_events = []
    hire_events = []

    # State tracking
    tile_history = {} # (x, y) -> list of states

    for step_idx, step_data in enumerate(steps):
        agent_state = step_data[opp_idx]
        obs = agent_state.get("observation", {})
        action = agent_state.get("action", {})
        reward = agent_state.get("reward", 0.0)

        farms = obs.get("farms", [])
        opp_farm = farms[opp_idx] if opp_idx < len(farms) else {}
        money = opp_farm.get("money", 0.0)
        unlocked_quadrants = opp_farm.get("unlocked_quadrants", ["NW"])
        farmer_pos = opp_farm.get("farmer", [4, 4])
        hands_pos = opp_farm.get("hands", [])
        tiles = opp_farm.get("tiles", [])

        # Actions taken by opponent
        farmer_act = action.get("farmer", ["PASS"]) if isinstance(action, dict) else ["PASS"]
        hands_act = action.get("hands", []) if isinstance(action, dict) else []
        market_act = action.get("market", []) if isinstance(action, dict) else []

        all_unit_actions = [farmer_act] + hands_act
        for act in all_unit_actions:
            if isinstance(act, list) and act:
                action_counts[act[0]] += 1
                if act[0] == "PLANT":
                    crop_events.append({"step": step_idx, "action": "PLANT", "crop": act[1] if len(act) > 1 else "UNKNOWN"})
                elif act[0] == "HARVEST":
                    crop_events.append({"step": step_idx, "action": "HARVEST"})
                elif act[0] == "WATER":
                    crop_events.append({"step": step_idx, "action": "WATER"})
                elif act[0] in ("FEED", "CARE", "COLLECT_FERTILIZER"):
                    animal_events.append({"step": step_idx, "action": act[0]})

        for m_act in market_act:
            if isinstance(m_act, list) and m_act:
                market_events.append({"step": step_idx, "order": m_act})
                if m_act[0] == "BUY_LAND":
                    land_events.append({"step": step_idx, "money_before": money})
                elif m_act[0] == "HIRE":
                    hire_events.append({"step": step_idx, "hands_after": len(hands_pos) + 1})

        # Count active tiles
        crop_count = 0
        pasture_count = 0
        animal_count = Counter()
        crop_species_count = Counter()
        for r_idx, row in enumerate(tiles):
            for c_idx, cell in enumerate(row):
                if isinstance(cell, dict):
                    k = cell.get("kind")
                    if k == "PLANT":
                        crop_count += 1
                        crop_species_count[cell.get("crop", "UNK")] += 1
                    elif k == "PASTURE":
                        pasture_count += 1
                        an = cell.get("animal")
                        if an:
                            animal_count[an] += 1

        timeline.append({
            "step": step_idx,
            "day": step_idx // 24,
            "hour": step_idx % 24,
            "money": money,
            "reward": reward,
            "quadrants": len(unlocked_quadrants) if isinstance(unlocked_quadrants, list) else int(unlocked_quadrants),
            "hands": len(hands_pos),
            "crop_tiles": crop_count,
            "crops": dict(crop_species_count),
            "pastures": pasture_count,
            "animals": dict(animal_count),
            "actions": [a[0] if isinstance(a, list) and a else "PASS" for a in all_unit_actions],
            "market_orders": market_act,
        })

    # Summary statistics
    total_steps = len(steps)
    quadrants_final = timeline[-1]["quadrants"]
    final_score = timeline[-1]["money"] or timeline[-1]["reward"]
    final_hands = timeline[-1]["hands"]

    return {
        "name": name,
        "opp_idx": opp_idx,
        "final_score": final_score,
        "antigravity_score": r0 if opp_idx == 1 else r1,
        "quadrants_final": quadrants_final,
        "total_steps": total_steps,
        "final_hands": final_hands,
        "action_counts": dict(action_counts),
        "land_events": land_events,
        "hire_events": hire_events,
        "crop_species_used": list(set(e.get("crop") for e in crop_events if "crop" in e)),
        "market_orders_total": len(market_events),
        "market_order_types": Counter(e["order"][0] for e in market_events),
        "timeline": timeline,
    }


def main():
    results = {}
    for name, path in REPLAYS.items():
        if path.exists():
            res = analyze_replay(name, path)
            results[name] = res
        else:
            print(f"File not found: {path}")

    # Output detailed report
    report_path = BENCHMARK_DIR / "REPLAY_ANALYSIS_SUMMARY.json"
    with open(report_path, "w", encoding="utf-8") as f:
        # Save compact version without entire full step dump
        compact = {}
        for k, v in results.items():
            compact[k] = {
                "name": v["name"],
                "final_score": v["final_score"],
                "antigravity_score": v["antigravity_score"],
                "quadrants_final": v["quadrants_final"],
                "final_hands": v["final_hands"],
                "action_counts": v["action_counts"],
                "land_events": v["land_events"],
                "hire_events": v["hire_events"],
                "crop_species_used": v["crop_species_used"],
                "market_order_types": v["market_order_types"],
                # Sample trajectory points every 24 steps (daily)
                "daily_trajectory": [t for t in v["timeline"] if t["hour"] == 0 or t["step"] == len(v["timeline"]) - 1],
            }
        json.dump(compact, f, indent=2)
    print(f"Summary written to {report_path}")


if __name__ == "__main__":
    main()
