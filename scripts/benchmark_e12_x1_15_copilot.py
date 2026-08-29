from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean, median
from typing import Any

from kaggle_environments import make

from agricola.core.state import GameState
from agricola.strategy.productive_mass_roi import ProductiveMassConfig, ProductiveMassROIAgent

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "e12" / "x115_copilot"
SEEDS = [0, 421521921, 1056561958, 1273000467]


def action_kind(action: list[Any]) -> str:
    return str(action[0]) if action else "PASS"


def is_movement(action: list[Any]) -> bool:
    return action_kind(action) in {"NORTH", "SOUTH", "EAST", "WEST"}


def is_productive(action: list[Any]) -> bool:
    return action_kind(action) in {"PLANT", "WATER", "DIG", "HARVEST", "FEED", "CARE", "COLLECT_FERTILIZER", "BUILD_PASTURE", "BUILD_COOP", "PICKUP", "PLACE", "DROP", "FERTILIZE"}


def build_agent(mode: str) -> ProductiveMassROIAgent:
    return ProductiveMassROIAgent(config=ProductiveMassConfig(
        productive_core_mode=mode,
        enable_land_expansion=True,
        target_cows=7,
        target_sheep=4,
        max_workers=6,
        stop_hire_day=1,
    ))


def livestock(state: GameState) -> dict[str, int]:
    counts = {"COW": 0, "SHEEP": 0}
    for y in range(10):
        for x in range(10):
            tile = state.get_tile(x, y)
            if isinstance(tile, dict) and tile.get("kind") == "PASTURE" and tile.get("animal") in counts:
                counts[tile["animal"]] += 1
    for animal in counts:
        counts[animal] += state.get_shed_count(animal)
        for worker_id in range(1 + len(state.hands_positions)):
            counts[animal] += state.get_worker_inventory_count(worker_id, animal)
    return counts


def run_episode(mode: str, seed: int) -> dict[str, Any]:
    agent = build_agent(mode)
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed})
    steps = env.reset()
    daily: dict[int, dict[str, Any]] = {}
    counts = {"productive": 0, "movement": 0, "idle": 0}
    q1_day = None
    q2_day = None
    for _ in range(720):
        state = GameState(steps[0].observation)
        day = state.day + 1
        owned = agent._x18_owned_quadrants(state)
        daily[day] = {"hands": len(state.hands_positions), "crop": agent._x19_crop_count(state), "cash": state.money, "owned": owned}
        action = agent.act(state)
        for unit_action in [action.get("farmer", ["PASS"])] + action.get("hands", []):
            if is_movement(unit_action):
                counts["movement"] += 1
            elif is_productive(unit_action):
                counts["productive"] += 1
            else:
                counts["idle"] += 1
        for order in action.get("market", []):
            if order and order[0] == "BUY_LAND":
                if owned == 1 and q1_day is None:
                    q1_day = day
                elif owned == 2 and q2_day is None:
                    q2_day = day
        steps = env.step([action, {}])
        if steps[0].status in {"DONE", "INVALID", "ERROR"}:
            break
    final_state = GameState(steps[0].observation)
    rows = list(daily.values())
    hands = [row["hands"] for row in rows]
    crops = [row["crop"] for row in rows]
    return {
        "mode": mode,
        "seed": seed,
        "status": steps[0].status,
        "final_money": float(steps[0].reward or 0.0),
        "q1_day": q1_day,
        "q2_day": q2_day,
        "owned_quadrants": agent._x18_owned_quadrants(final_state),
        "peak_hands": max(hands, default=0),
        "mean_hands": round(mean(hands), 2) if hands else 0.0,
        "peak_crop_tiles": max(crops, default=0),
        "mean_crop_tiles": round(mean(crops), 2) if crops else 0.0,
        "productive_actions": counts["productive"],
        "movement_actions": counts["movement"],
        "idle_actions": counts["idle"],
        "productive_to_movement": round(counts["productive"] / max(1, counts["movement"]), 3),
        "livestock_final": livestock(final_state),
        "min_cash": min((row["cash"] for row in rows), default=0.0),
    }


def main() -> None:
    results = []
    for seed in SEEDS:
        results.append(run_episode("E12_TRUEBELIEF_ENGINE_X112", seed))
        results.append(run_episode("E12_X115_COPILOT_INDEPENDENT", seed))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "development_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    with (OUT_DIR / "RESULTS_TABLE.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    for mode in {row["mode"] for row in results}:
        values = [row["final_money"] for row in results if row["mode"] == mode]
        print(mode, "mean", round(mean(values), 2), "median", round(median(values), 2), "values", values)


if __name__ == "__main__":
    main()
