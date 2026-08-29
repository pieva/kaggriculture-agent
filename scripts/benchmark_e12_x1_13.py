"""Counterfactual benchmark for E12-X1.13 dynamic allocation."""

import argparse
import csv
import json
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List, Optional, Tuple

from kaggle_environments import make

from agricola.core.state import CROPS, GameState
from agricola.strategy.productive_mass_roi import ProductiveMassConfig, ProductiveMassROIAgent


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT_ROOT / "results" / "e12" / "x113"
PRIMARY_SEEDS = [0, 421521921]
VALIDATION_SEEDS = [200, 777, 20260828]


VARIANTS = {
    "A": {
        "label": "X1.12 baseline unchanged",
        "mode": "E12_TRUEBELIEF_ENGINE_X112",
        "x113_variant": "A",
        "q2": False,
        "cows": 7,
        "sheep": 4,
    },
    "B": {
        "label": "livestock dynamic gate, Q2 disabled",
        "mode": "E12_DYNAMIC_ALLOCATION_X113",
        "x113_variant": "B",
        "q2": False,
        "cows": 6,
        "sheep": 3,
    },
    "C": {
        "label": "livestock gate + workload HIRE, Q2 disabled",
        "mode": "E12_DYNAMIC_ALLOCATION_X113",
        "x113_variant": "C",
        "q2": False,
        "cows": 6,
        "sheep": 3,
    },
    "D": {
        "label": "livestock gate + workload HIRE + dynamic Q2",
        "mode": "E12_DYNAMIC_ALLOCATION_X113",
        "x113_variant": "D",
        "q2": True,
        "cows": 6,
        "sheep": 3,
    },
    "E": {
        "label": "D + crop-SLA-first assignment",
        "mode": "E12_DYNAMIC_ALLOCATION_X113",
        "x113_variant": "E",
        "q2": True,
        "cows": 6,
        "sheep": 3,
    },
}


def build_agent(variant: str) -> ProductiveMassROIAgent:
    spec = VARIANTS[variant]
    config = ProductiveMassConfig(
        productive_core_mode=spec["mode"],
        enable_land_expansion=True,
        target_cows=spec["cows"],
        target_sheep=spec["sheep"],
        max_workers=6,
        stop_hire_day=1,
        x113_variant=spec["x113_variant"],
        x113_q2_enabled=spec["q2"],
        x113_livestock_safety_cow_cap=spec["cows"],
        x113_livestock_safety_sheep_cap=spec["sheep"],
    )
    return ProductiveMassROIAgent(config=config)


def action_kind(action: List[Any]) -> str:
    if not action:
        return "PASS"
    return str(action[0])


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


def summarize_inventory(state: GameState) -> Dict[str, int]:
    items = set(state.shed.keys())
    for inventory in state.inventories:
        items.update(inventory.keys())
    out = {}
    for item in sorted(items):
        total = state.get_shed_count(item)
        for worker_id in range(1 + len(state.hands_positions)):
            total += state.get_worker_inventory_count(worker_id, item)
        if total:
            out[item] = total
    return out


def run_episode(variant: str, seed: int) -> Dict[str, Any]:
    agent = build_agent(variant)
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed})
    steps = env.reset()
    daily: Dict[int, Dict[str, Any]] = {}
    action_counts = {"productive": 0, "movement": 0, "idle": 0}
    spending = {"seeds": 0.0, "livestock": 0.0, "product": 0.0, "hands": 0.0, "land": 0.0}
    revenue = {"crop": 0.0, "MILK": 0.0, "WOOL": 0.0, "FERTILIZER": 0.0, "WHEAT": 0.0}
    q2_purchase_day: Optional[int] = None
    q2_cash_after_purchase: Optional[float] = None
    q2_first_productive_day: Optional[int] = None

    for _ in range(720):
        obs = steps[0].observation
        state = GameState(obs)
        crop_tiles = agent._x113_crop_positions(state) if variant != "A" else agent._x112_crop_positions(state)
        metrics = agent._x113_backlog_metrics(state, crop_tiles)
        day = state.day + 1
        daily[day] = {
            "day": day,
            "cash": state.money,
            "workers": 1 + len(state.hands_positions),
            **metrics,
        }

        if q2_purchase_day is not None and q2_first_productive_day is None:
            if metrics["productive_by_quadrant"].get("Q2", 0) > 0:
                q2_first_productive_day = day

        action = agent.act(state)
        all_actions = [action.get("farmer", ["PASS"])] + action.get("hands", [])
        for unit_action in all_actions:
            if is_movement(unit_action):
                action_counts["movement"] += 1
            elif is_productive(unit_action):
                action_counts["productive"] += 1
            else:
                action_counts["idle"] += 1

        before_owned = agent._x18_owned_quadrants(state)
        for order in action.get("market", []):
            kind = action_kind(order)
            if kind == "HIRE":
                spending["hands"] += 20.0
            elif kind == "BUY_LAND":
                cost = agent._next_land_cost(state) or 0.0
                spending["land"] += cost
                if before_owned == 2 and q2_purchase_day is None:
                    q2_purchase_day = day
                    q2_cash_after_purchase = state.money - cost
            elif kind == "BUY_SEED":
                crop = order[1]
                qty = int(order[2])
                spending["seeds"] += qty * CROPS.get(crop, {}).get("seed", 0.0)
            elif kind == "BUY_PRODUCT":
                item = order[1]
                qty = int(order[2])
                spending["product"] += qty * state.get_price(item)
            elif kind == "BUY_ANIMAL":
                animal = order[1]
                qty = int(order[2])
                spending["livestock"] += qty * (400.0 if animal == "COW" else 500.0)
            elif kind == "SELL":
                item = order[1]
                qty = int(order[2])
                value = qty * state.get_price(item)
                if item in ("MILK", "WOOL", "FERTILIZER", "WHEAT"):
                    revenue[item] += value
                else:
                    revenue["crop"] += value

        steps = env.step([action, {}])
        if steps[0].status in ("DONE", "INVALID", "ERROR"):
            break

    final_state = GameState(steps[0].observation)
    final_money = float(steps[0].reward or 0.0)
    days = list(daily.values())
    crop_surface = [d["active_crops"] for d in days]
    productive_surface = [d["active_crops"] + d["pastures"] for d in days]
    q2_payback_proxy = None
    if q2_cash_after_purchase is not None:
        q2_payback_proxy = final_money - q2_cash_after_purchase

    return {
        "variant": variant,
        "label": VARIANTS[variant]["label"],
        "seed": seed,
        "final_money": final_money,
        "status": steps[0].status,
        "mean_crop_tiles": round(mean(crop_surface), 2) if crop_surface else 0,
        "peak_crop_tiles": max(crop_surface) if crop_surface else 0,
        "mean_productive_tiles": round(mean(productive_surface), 2) if productive_surface else 0,
        "peak_productive_tiles": max(productive_surface) if productive_surface else 0,
        "weed_tile_days": sum(d["weeds"] for d in days),
        "harvested_empty_tile_days": sum(d["harvested_empty"] for d in days),
        "unwatered_tile_days": sum(d["unwatered"] for d in days),
        "final_backlog_per_worker": days[-1]["backlog_per_worker"] if days else 0,
        "productive_actions": action_counts["productive"],
        "movement_actions": action_counts["movement"],
        "idle_actions": action_counts["idle"],
        "productive_to_movement_ratio": round(action_counts["productive"] / max(1, action_counts["movement"]), 3),
        "spending": spending,
        "revenue": revenue,
        "livestock_final": scan_livestock(final_state),
        "owned_quadrants_final": agent._x18_owned_quadrants(final_state),
        "q2_purchased": q2_purchase_day is not None,
        "q2_purchase_day": q2_purchase_day,
        "q2_first_productive_day": q2_first_productive_day,
        "q2_time_to_activation": (
            q2_first_productive_day - q2_purchase_day
            if q2_purchase_day is not None and q2_first_productive_day is not None
            else None
        ),
        "q2_payback_proxy": q2_payback_proxy,
        "inventory_final": summarize_inventory(final_state),
    }


def write_outputs(results: List[Dict[str, Any]]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUT_DIR / "counterfactual_results.json"
    csv_path = OUT_DIR / "counterfactual_results.csv"
    md_path = OUT_DIR / "COUNTERFACTUAL_LOG.md"

    json_path.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    fieldnames = [
        "variant", "label", "seed", "final_money", "mean_crop_tiles", "peak_crop_tiles",
        "mean_productive_tiles", "peak_productive_tiles", "weed_tile_days",
        "harvested_empty_tile_days", "unwatered_tile_days", "productive_actions",
        "movement_actions", "productive_to_movement_ratio", "owned_quadrants_final",
        "q2_purchased", "q2_purchase_day", "q2_time_to_activation", "q2_payback_proxy",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow({k: row.get(k) for k in fieldnames})

    lines = [
        "# X1.13 Dynamic Allocation Counterfactual Log",
        "",
        "| Variant | Seed | Final | Mean Crop | Peak Crop | Weeds TD | Empty TD | Unwatered TD | Prod/Move | Livestock | Q2 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in results:
        livestock = f"{row['livestock_final'].get('COW', 0)}C/{row['livestock_final'].get('SHEEP', 0)}S"
        q2 = "no"
        if row["q2_purchased"]:
            q2 = f"day {row['q2_purchase_day']} / act {row['q2_time_to_activation']}"
        lines.append(
            f"| {row['variant']} | {row['seed']} | ${row['final_money']:,.0f} | "
            f"{row['mean_crop_tiles']} | {row['peak_crop_tiles']} | {row['weed_tile_days']} | "
            f"{row['harvested_empty_tile_days']} | {row['unwatered_tile_days']} | "
            f"{row['productive_to_movement_ratio']} | {livestock} | {q2} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validation", action="store_true", help="Include three extra validation seeds.")
    parser.add_argument("--variants", default="ABCDE", help="Variant letters to run.")
    args = parser.parse_args()

    seeds = PRIMARY_SEEDS + (VALIDATION_SEEDS if args.validation else [])
    results = []
    for variant in args.variants:
        for seed in seeds:
            result = run_episode(variant, seed)
            results.append(result)
            print(
                f"{variant} seed {seed}: ${result['final_money']:,.0f}, "
                f"crop mean/peak {result['mean_crop_tiles']}/{result['peak_crop_tiles']}, "
                f"Q2={result['q2_purchased']}"
            )
    write_outputs(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
