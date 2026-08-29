"""Fast counterfactual benchmark for E12-X1.14 Workforce Capacity First."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List, Optional

from kaggle_environments import make

from agricola.core.state import CROPS, GameState
from agricola.strategy.productive_mass_roi import ProductiveMassConfig, ProductiveMassROIAgent


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT_ROOT / "results" / "e12" / "x114"
PRIMARY_SEEDS = [0, 421521921]
VALIDATION_SEEDS = [1056561958, 1273000467]


VARIANTS = {
    "A": {
        "label": "X1.12 baseline unchanged",
        "mode": "E12_TRUEBELIEF_ENGINE_X112",
        "x114_variant": "A",
    },
    "B": {
        "label": "workforce aggressive, Q2 disabled",
        "mode": "E12_WORKFORCE_CAPACITY_X114",
        "x114_variant": "B",
    },
    "C": {
        "label": "workforce aggressive + crop maintenance priority",
        "mode": "E12_WORKFORCE_CAPACITY_X114",
        "x114_variant": "C",
    },
    "D": {
        "label": "C + livestock expansion brake",
        "mode": "E12_WORKFORCE_CAPACITY_X114",
        "x114_variant": "D",
    },
    "E": {
        "label": "Q1-protected workforce capacity",
        "mode": "E12_WORKFORCE_CAPACITY_X114",
        "x114_variant": "E",
    },
    "F": {
        "label": "E + crop priority + livestock brake",
        "mode": "E12_WORKFORCE_CAPACITY_X114",
        "x114_variant": "F",
    },
}


def build_agent(variant: str) -> ProductiveMassROIAgent:
    spec = VARIANTS[variant]
    config = ProductiveMassConfig(
        productive_core_mode=spec["mode"],
        enable_land_expansion=True,
        target_cows=7,
        target_sheep=4,
        max_workers=6,
        stop_hire_day=1,
        x114_variant=spec["x114_variant"],
        x114_max_hands=12,
        x113_q2_enabled=False,
    )
    return ProductiveMassROIAgent(config=config)


def action_kind(action: List[Any]) -> str:
    return str(action[0]) if action else "PASS"


def is_movement(action: List[Any]) -> bool:
    return action_kind(action) in {"NORTH", "SOUTH", "EAST", "WEST", "N", "S", "E", "W"}


def is_productive(action: List[Any]) -> bool:
    return action_kind(action) in {
        "PLANT",
        "WATER",
        "DIG",
        "HARVEST",
        "FEED",
        "CARE",
        "COLLECT_FERTILIZER",
        "BUILD_PASTURE",
        "PICKUP",
        "PLACE",
        "DROP",
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


def run_episode(variant: str, seed: int) -> Dict[str, Any]:
    agent = build_agent(variant)
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed})
    steps = env.reset()
    daily: Dict[int, Dict[str, Any]] = {}
    action_counts = {"productive": 0, "movement": 0, "idle": 0}
    q1_day: Optional[int] = None

    for _ in range(720):
        obs = steps[0].observation
        state = GameState(obs)
        crop_tiles = agent._x112_crop_positions(state)
        metrics = agent._x113_backlog_metrics(state, crop_tiles)
        day = state.day + 1
        owned = agent._x18_owned_quadrants(state)
        if owned >= 2 and q1_day is None:
            q1_day = day
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

    final_state = GameState(steps[0].observation)
    days = list(daily.values())
    hands = [d["hands"] for d in days]
    crop_surface = [d["active_crops"] for d in days]
    cash = [d["cash"] for d in days]
    final_money = float(steps[0].reward or 0.0)
    return {
        "variant": variant,
        "label": VARIANTS[variant]["label"],
        "seed": seed,
        "status": steps[0].status,
        "final_money": final_money,
        "peak_hands": max(hands) if hands else 0,
        "mean_hands": round(mean(hands), 2) if hands else 0,
        "peak_crop_tiles": max(crop_surface) if crop_surface else 0,
        "mean_crop_tiles": round(mean(crop_surface), 2) if crop_surface else 0,
        "weed_tile_days": sum(d["weeds"] for d in days),
        "harvested_empty_tile_days": sum(d["harvested_empty"] for d in days),
        "unwatered_tile_days": sum(d["unwatered"] for d in days),
        "productive_actions": action_counts["productive"],
        "movement_actions": action_counts["movement"],
        "idle_actions": action_counts["idle"],
        "productive_to_movement_ratio": round(action_counts["productive"] / max(1, action_counts["movement"]), 3),
        "livestock_final": scan_livestock(final_state),
        "q1": q1_day is not None,
        "q1_day": q1_day,
        "owned_quadrants_final": agent._x18_owned_quadrants(final_state),
        "min_cash": round(min(cash), 2) if cash else 0,
        "mean_cash": round(mean(cash), 2) if cash else 0,
    }


def write_outputs(results: List[Dict[str, Any]]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "counterfactual_results.json").write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    fields = list(results[0].keys()) if results else []
    with (OUT_DIR / "counterfactual_results.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in results:
            writer.writerow({k: json.dumps(v, sort_keys=True) if isinstance(v, dict) else v for k, v in row.items()})

    lines = [
        "# E12-X1.14 Counterfactual Log",
        "",
        "| Variant | Seed | Final | Peak/Mean Hands | Peak/Mean Crop | Weed tile-days | Empty tile-days | Livestock | Q1 | Prod/Move |",
        "|---|---:|---:|---|---|---:|---:|---|---|---:|",
    ]
    for row in results:
        livestock = ", ".join(f"{k}:{v}" for k, v in row["livestock_final"].items()) or "none"
        lines.append(
            f"| {row['variant']} | {row['seed']} | ${row['final_money']:.0f} | "
            f"{row['peak_hands']}/{row['mean_hands']} | {row['peak_crop_tiles']}/{row['mean_crop_tiles']} | "
            f"{row['weed_tile_days']} | {row['harvested_empty_tile_days']} | {livestock} | "
            f"{'D' + str(row['q1_day']) if row['q1'] else 'no'} | {row['productive_to_movement_ratio']} |"
        )
    (OUT_DIR / "COUNTERFACTUAL_LOG.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    results: List[Dict[str, Any]] = []
    for variant in VARIANTS:
        for seed in PRIMARY_SEEDS + VALIDATION_SEEDS:
            results.append(run_episode(variant, seed))
    write_outputs(results)
    for row in results:
        print(
            f"{row['variant']} seed {row['seed']}: ${row['final_money']:.0f}, "
            f"hands {row['peak_hands']}/{row['mean_hands']}, crop {row['peak_crop_tiles']}/{row['mean_crop_tiles']}, "
            f"weeds {row['weed_tile_days']}, livestock {row['livestock_final']}"
        )


if __name__ == "__main__":
    main()
