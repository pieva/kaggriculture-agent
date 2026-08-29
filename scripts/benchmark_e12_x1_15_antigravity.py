"""
Benchmark runner for E12-X1.15-ANTIGRAVITY Independent Candidate.
Evaluates X1.12 baseline vs X1.15 Antigravity candidate across development and holdout seeds.
"""

from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from kaggle_environments import make

from agricola.core.state import CROPS, GameState
from agricola.strategy.productive_mass_roi import ProductiveMassConfig, ProductiveMassROIAgent

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT_ROOT / "results" / "e12" / "x115_antigravity"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DEV_SEEDS = [0, 421521921, 1056561958, 1273000467]
HOLDOUT_SEEDS = [2026082801, 2026082802, 2026082803, 2026082804]

def build_agent(mode_name: str, **kwargs) -> ProductiveMassROIAgent:
    config = ProductiveMassConfig(
        productive_core_mode=mode_name,
        enable_land_expansion=True,
        **kwargs
    )
    return ProductiveMassROIAgent(config=config)

def action_kind(action: List[Any]) -> str:
    return str(action[0]) if action else "PASS"

def is_movement(action: List[Any]) -> bool:
    return action_kind(action) in {"NORTH", "SOUTH", "EAST", "WEST", "N", "S", "E", "W"}

def is_productive(action: List[Any]) -> bool:
    return action_kind(action) in {
        "PLANT", "WATER", "DIG", "HARVEST", "FEED", "CARE",
        "COLLECT_FERTILIZER", "BUILD_PASTURE", "PICKUP", "PLACE", "DROP",
    }

def scan_livestock(state: GameState) -> Dict[str, int]:
    counts = {"COW": 0, "SHEEP": 0}
    for y in range(10):
        for x in range(10):
            tile = state.get_tile(x, y)
            if isinstance(tile, dict) and tile.get("kind") == "PASTURE":
                animal = tile.get("animal")
                if animal in counts:
                    counts[animal] += 1
    for animal in counts:
        counts[animal] += state.get_shed_count(animal)
        for worker_id in range(1 + len(state.hands_positions)):
            counts[animal] += state.get_worker_inventory_count(worker_id, animal)
    return counts

def run_episode(mode_name: str, seed: int, **kwargs) -> Dict[str, Any]:
    agent = build_agent(mode_name, **kwargs)
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed})
    steps = env.reset()
    daily: Dict[int, Dict[str, Any]] = {}
    action_counts = {"productive": 0, "movement": 0, "idle": 0}
    q1_day: Optional[int] = None
    q2_day: Optional[int] = None

    for step_num in range(720):
        obs = steps[0].observation
        state = GameState(obs)
        crop_tiles = agent._x112_crop_positions(state)
        metrics = agent._x113_backlog_metrics(state, crop_tiles)
        day = state.day + 1
        owned = agent._x18_owned_quadrants(state)
        if owned >= 2 and q1_day is None:
            q1_day = day
        if owned >= 3 and q2_day is None:
            q2_day = day

        daily[day] = {
            "day": day,
            "cash": state.money,
            "hands": len(state.hands_positions),
            "workers": 1 + len(state.hands_positions),
            "owned_quadrants": owned,
            **metrics,
        }

        action = agent.act(state)
        for unit_action in [action.get("farmer", ["PASS"])] + action.get("hands", []):
            if is_movement(unit_action):
                action_counts["movement"] += 1
            elif is_productive(unit_action):
                action_counts["productive"] += 1
            else:
                action_counts["idle"] += 1

        steps = env.step([action, {}])
        if steps[0].status in ("DONE", "INVALID", "ERROR"):
            break

    final_obs = steps[0].observation
    final_state = GameState(final_obs)
    final_money = final_state.money
    peak_hands = max((d["hands"] for d in daily.values()), default=0)
    mean_hands = sum(d["hands"] for d in daily.values()) / max(1, len(daily))
    peak_crop_tiles = max((d["active_crops"] for d in daily.values()), default=0)
    mean_crop_tiles = sum(d["active_crops"] for d in daily.values()) / max(1, len(daily))
    weed_tile_days = sum(d["weeds"] for d in daily.values())
    unwatered_tile_days = sum(d["unwatered"] for d in daily.values())
    harvested_empty_tile_days = sum(d["harvested_empty"] for d in daily.values())
    final_owned = agent._x18_owned_quadrants(final_state)
    livestock = scan_livestock(final_state)

    total_actions = sum(action_counts.values())
    prod_ratio = action_counts["productive"] / max(1, total_actions)

    return {
        "mode": mode_name,
        "seed": seed,
        "status": steps[0].status,
        "final_money": final_money,
        "peak_hands": peak_hands,
        "mean_hands": round(mean_hands, 2),
        "peak_crop_tiles": peak_crop_tiles,
        "mean_crop_tiles": round(mean_crop_tiles, 2),
        "weed_tile_days": weed_tile_days,
        "unwatered_tile_days": unwatered_tile_days,
        "harvested_empty_tile_days": harvested_empty_tile_days,
        "productive_actions": action_counts["productive"],
        "movement_actions": action_counts["movement"],
        "idle_actions": action_counts["idle"],
        "productive_ratio": round(prod_ratio, 3),
        "livestock_final": livestock,
        "q1_day": q1_day,
        "q2_day": q2_day,
        "owned_quadrants_final": final_owned,
    }

def main():
    seeds_to_run = DEV_SEEDS
    if "--holdout" in sys.argv:
        seeds_to_run = HOLDOUT_SEEDS

    print(f"\n{'='*75}")
    print(f"RUNNING BENCHMARK (seeds: {seeds_to_run})")
    print(f"{'='*75}")

    modes = [
        ("X1.12_Baseline", "E12_TRUEBELIEF_ENGINE_X112", {}),
        ("X1.15_Antigravity", "E12_X115_ANTIGRAVITY_INDEPENDENT", {}),
    ]

    results = []
    for label, mode_name, kwargs in modes:
        for seed in seeds_to_run:
            print(f"Running {label:<20} on seed {seed}...", end="", flush=True)
            res = run_episode(mode_name, seed, **kwargs)
            res["label"] = label
            results.append(res)
            print(f" -> ${res['final_money']:<8.0f} (PeakHands: {res['peak_hands']}, Quads: {res['owned_quadrants_final']}, Q1: D{res['q1_day']}, Q2: D{res['q2_day']}, LS: {res['livestock_final']})")

    # Output table
    print(f"\n{'='*75}")
    print(f"{'Label':<20} {'Seed':<12} {'Final Money':<12} {'Quads':<6} {'Hands':<10} {'WeedTD':<8} {'Livestock':<18}")
    print("-" * 75)
    for r in results:
        ls_str = f"C:{r['livestock_final']['COW']} S:{r['livestock_final']['SHEEP']}"
        print(f"{r['label']:<20} {r['seed']:<12} ${r['final_money']:<11.0f} {r['owned_quadrants_final']:<6} {r['peak_hands']} ({r['mean_hands']}) {r['weed_tile_days']:<8} {ls_str:<18}")

    return results

if __name__ == "__main__":
    main()
