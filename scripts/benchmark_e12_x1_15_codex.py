"""Counterfactual benchmark for E12-X1.15 Codex independent candidate."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean, median
from typing import Any, Dict, List, Optional

from kaggle_environments import make

from agricola.core.state import CROPS, GameState
from agricola.strategy.productive_mass_roi import ProductiveMassConfig, ProductiveMassROIAgent


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT_ROOT / "results" / "e12" / "x115_codex"
DEVELOPMENT_SEEDS = [0, 421521921, 1056561958, 1273000467]
HOLDOUT_SEEDS = [2026082801, 2026082802, 2026082803, 2026082804]


VARIANTS = {
    "X112": {
        "label": "X1.12 baseline",
        "mode": "E12_TRUEBELIEF_ENGINE_X112",
        "x115_variant": "A",
        "target_cows": 7,
        "target_sheep": 4,
    },
    "X115B": {
        "label": "Codex Q2 high-ceiling branch",
        "mode": "E12_X115_CODEX_INDEPENDENT",
        "x115_variant": "B",
        "target_cows": 10,
        "target_sheep": 5,
    },
    "X115C": {
        "label": "Codex conservative Q2 branch",
        "mode": "E12_X115_CODEX_INDEPENDENT",
        "x115_variant": "C",
        "target_cows": 9,
        "target_sheep": 4,
    },
    "X115D": {
        "label": "Codex early land-first Q2 branch",
        "mode": "E12_X115_CODEX_INDEPENDENT",
        "x115_variant": "D",
        "target_cows": 12,
        "target_sheep": 3,
    },
}


def build_agent(variant: str) -> ProductiveMassROIAgent:
    spec = VARIANTS[variant]
    config = ProductiveMassConfig(
        productive_core_mode=spec["mode"],
        enable_land_expansion=True,
        target_cows=spec["target_cows"],
        target_sheep=spec["target_sheep"],
        max_workers=6,
        stop_hire_day=1,
        x115_variant=spec["x115_variant"],
        x115_max_hands=12,
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


def summarize_market(action: Dict[str, Any], totals: Dict[str, Dict[str, int]]) -> None:
    for order in action.get("market", []):
        if not isinstance(order, list) or not order:
            continue
        verb = str(order[0])
        item = str(order[1]) if len(order) > 1 else ""
        qty = int(order[2]) if len(order) > 2 and isinstance(order[2], int) else 1
        if verb == "SELL":
            totals["sells"][item] = totals["sells"].get(item, 0) + qty
        elif verb in {"BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL"}:
            totals["buys"][item] = totals["buys"].get(item, 0) + qty


def run_episode(variant: str, seed: int) -> Dict[str, Any]:
    agent = build_agent(variant)
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed})
    steps = env.reset()
    daily: Dict[int, Dict[str, Any]] = {}
    action_counts = {"productive": 0, "movement": 0, "idle": 0}
    market_totals = {"sells": {}, "buys": {}}
    q1_day: Optional[int] = None
    q2_day: Optional[int] = None

    for _ in range(720):
        obs = steps[0].observation
        state = GameState(obs)
        crop_tiles = agent._x115_crop_positions(state) if variant.startswith("X115") else agent._x112_crop_positions(state)
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
        summarize_market(action, market_totals)
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
    productive_surface = [d["active_crops"] + d["pastures"] for d in days]
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
        "peak_productive_tiles": max(productive_surface) if productive_surface else 0,
        "mean_productive_tiles": round(mean(productive_surface), 2) if productive_surface else 0,
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
        "q2": q2_day is not None,
        "q2_day": q2_day,
        "owned_quadrants_final": agent._x18_owned_quadrants(final_state),
        "min_cash": round(min(cash), 2) if cash else 0,
        "mean_cash": round(mean(cash), 2) if cash else 0,
        "sells": market_totals["sells"],
        "buys": market_totals["buys"],
    }


def summarize_results(results: List[Dict[str, Any]], filename: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / f"{filename}.json").write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    fields = list(results[0].keys()) if results else []
    with (OUT_DIR / f"{filename}.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in results:
            writer.writerow({k: json.dumps(v, sort_keys=True) if isinstance(v, dict) else v for k, v in row.items()})

    by_variant: Dict[str, List[float]] = {}
    for row in results:
        by_variant.setdefault(row["variant"], []).append(row["final_money"])

    lines = [
        "# E12-X1.15 Codex Counterfactual Log",
        "",
        "| Variant | Seed | Final | Q1 | Q2 | Peak/Mean Hands | Peak/Mean Productive | Weeds | Livestock | Main sells | Prod/Move |",
        "|---|---:|---:|---|---|---|---|---:|---|---|---:|",
    ]
    for row in results:
        livestock = ", ".join(f"{k}:{v}" for k, v in row["livestock_final"].items()) or "none"
        sells = ", ".join(f"{k}:{v}" for k, v in sorted(row["sells"].items(), key=lambda item: item[1], reverse=True)[:5]) or "none"
        lines.append(
            f"| {row['variant']} | {row['seed']} | ${row['final_money']:.0f} | "
            f"{'D' + str(row['q1_day']) if row['q1'] else 'no'} | {'D' + str(row['q2_day']) if row['q2'] else 'no'} | "
            f"{row['peak_hands']}/{row['mean_hands']} | {row['peak_productive_tiles']}/{row['mean_productive_tiles']} | "
            f"{row['weed_tile_days']} | {livestock} | {sells} | {row['productive_to_movement_ratio']} |"
        )
    lines.extend(["", "## Aggregate", ""])
    lines.append("| Variant | Mean | Median | Min | Max |")
    lines.append("|---|---:|---:|---:|---:|")
    for variant, values in sorted(by_variant.items()):
        lines.append(f"| {variant} | ${mean(values):.0f} | ${median(values):.0f} | ${min(values):.0f} | ${max(values):.0f} |")
    (OUT_DIR / f"{filename}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    phase = "development"
    seeds = DEVELOPMENT_SEEDS
    variants = list(VARIANTS)
    results: List[Dict[str, Any]] = []
    for variant in variants:
        for seed in seeds:
            row = run_episode(variant, seed)
            results.append(row)
            print(
                f"{variant} seed {seed}: ${row['final_money']:.0f}, "
                f"Q1={row['q1_day']}, Q2={row['q2_day']}, "
                f"hands {row['peak_hands']}/{row['mean_hands']}, "
                f"productive {row['peak_productive_tiles']}/{row['mean_productive_tiles']}, "
                f"weeds {row['weed_tile_days']}, livestock {row['livestock_final']}"
            )
    summarize_results(results, f"{phase}_results")


if __name__ == "__main__":
    main()
