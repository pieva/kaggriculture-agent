"""Benchmark runner for E12-X1.11 — Q0+Q1 80k Economic Engine.

Seeds: 0 and 421521921
Target: final_money >= 80,000 on BOTH seeds
Domain Constraint: owned_quadrants == 2 (Q0 + Q1 ONLY)
"""

import os
import sys
import json
import time
import hashlib
import argparse
from pathlib import Path
from typing import Dict, Any, List

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agricola.strategy.productive_mass_roi import ProductiveMassROIAgent, ProductiveMassConfig
from agricola.core.state import GameState
from kaggle_environments import make

# X1.11 Configuration
X111_CONFIG = ProductiveMassConfig(
    productive_core_mode="E12_Q0Q1_80K_ENGINE_X111",
    enable_land_expansion=True,
    target_cows=8,
    max_workers=6,
    stop_hire_day=1,
)

# Required seeds from DEFINE spec
REQUIRED_SEEDS = [0, 421521921]
TARGET_MONEY = 80000.0


def run_episode(seed: int, config: ProductiveMassConfig = None) -> Dict[str, Any]:
    """Run a single episode with full telemetry extraction."""
    cfg = config or X111_CONFIG
    agent = ProductiveMassROIAgent(config=cfg)

    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed})
    state = env.reset()

    for step in range(720):
        obs0 = state[0].observation
        gs = GameState(obs0)
        act = agent.act(gs)
        try:
            state = env.step([act, {}])
        except Exception as e:
            print(f"  [WARN] Step {step} exception: {e}")
            break
        if state[0].status in ("DONE", "INVALID", "ERROR"):
            break

    tel = agent.telemetry

    # Extract X1.11 contribution telemetry
    milk_rev = getattr(agent, '_x111_milk_revenue_total', 0.0)
    crop_rev = getattr(agent, '_x111_crop_revenue_total', 0.0)
    retail_wheat = getattr(agent, '_x111_retail_wheat_spend', 0.0)
    harvests = getattr(agent, '_x111_harvests_count', 0)
    milk_harvested = getattr(agent, '_x111_milk_harvested_count', 0)
    wheat_fed = getattr(agent, '_x111_wheat_fed_count', 0)
    move_steps = getattr(agent, '_x111_movement_steps', 0)
    action_steps = getattr(agent, '_x111_action_steps', 0)
    pastures_built = getattr(agent, '_x111_pastures_built', 0)
    cows_bought = getattr(agent, '_x111_cows_bought', 0)
    seeds_spent = getattr(agent, '_x111_seeds_spent', 0.0)
    milk_sold = getattr(agent, '_x111_milk_sold_total', 0)

    ep_data = {
        "seed": seed,
        "final_money": tel.final_money,
        "starting_money": tel.starting_money,
        "minimum_cash": tel.minimum_cash,
        "owned_quadrants": agent.owned_quadrants,
        "peak_productive_tiles": tel.peak_productive_tiles,
        "peak_simultaneous_workers": tel.peak_simultaneous_workers,
        # Contribution ladder telemetry
        "milk_revenue": milk_rev,
        "crop_revenue": crop_rev,
        "retail_wheat_spend": retail_wheat,
        "crop_harvests": harvests,
        "milk_harvested": milk_harvested,
        "milk_sold": milk_sold,
        "wheat_fed": wheat_fed,
        "cows_bought": cows_bought,
        "pastures_built": pastures_built,
        "seeds_spent": seeds_spent,
        "movement_steps": move_steps,
        "action_steps": action_steps,
        "movement_pct": round(move_steps / max(1, move_steps + action_steps) * 100, 1),
        # Spending
        "spending_seeds": tel.spending_seeds,
        "spending_land": tel.spending_land,
        "spending_workforce": tel.spending_workforce,
        "spending_livestock": tel.spending_livestock,
        # Revenue breakdown
        "realized_revenue": dict(tel.realized_revenue),
        "quantities_sold": dict(tel.quantities_sold),
    }
    return ep_data


def print_contribution_ladder(ep: Dict[str, Any]):
    """Print contribution ladder analysis for one episode."""
    fm = ep["final_money"]
    milk = ep["milk_revenue"]
    crop = ep["crop_revenue"]
    retail = ep["retail_wheat_spend"]

    print(f"\n  --- Contribution Ladder ---")
    print(f"  | Final Money:          ${fm:>10,.2f}  {'PASS' if fm >= TARGET_MONEY else 'FAIL'}")
    print(f"  | Owned Quadrants:      {ep['owned_quadrants']:>10d}  {'Q0+Q1' if ep['owned_quadrants'] == 2 else 'CONSTRAINT VIOLATION'}")
    print(f"  |")
    print(f"  | Milk Revenue:         ${milk:>10,.2f}  ({ep['milk_sold']} sold, {ep['milk_harvested']} harvested)")
    print(f"  | Crop Revenue:         ${crop:>10,.2f}  ({ep['crop_harvests']} harvests)")
    print(f"  | Retail Wheat Spend:   ${retail:>10,.2f}  (emergency only)")
    print(f"  |")
    print(f"  | Peak Active Tiles:    {ep['peak_productive_tiles']:>10d}")
    print(f"  | Peak Workers:         {ep['peak_simultaneous_workers']:>10d}")
    print(f"  | Cows Bought:          {ep['cows_bought']:>10d}")
    print(f"  | Pastures Built:       {ep['pastures_built']:>10d}")
    print(f"  | Worker Movement %:    {ep['movement_pct']:>9.1f}%")
    print(f"  |")
    print(f"  | Spending: Seeds ${ep['spending_seeds']:,.0f} | Land ${ep['spending_land']:,.0f} | Workers ${ep['spending_workforce']:,.0f} | Livestock ${ep['spending_livestock']:,.0f}")
    print(f"  | Revenue: {', '.join(f'{k}=${v:,.0f}' for k, v in ep['realized_revenue'].items() if v > 0)}")
    print(f"  ----\n")


def benchmark_x111() -> Dict[str, Any]:
    """Run E12-X1.11 benchmark on required seeds with full verification."""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    run_id = f"E12-X1.11-{timestamp}"
    results_dir = Path(__file__).parent.parent / "results" / "e12" / "x111"
    results_dir.mkdir(parents=True, exist_ok=True)

    print(f"{'='*70}")
    print(f"  E12-X1.11 -- Q0+Q1 80k Economic Engine -- BENCHMARK")
    print(f"  Run ID: {run_id}")
    print(f"  Target: final_money >= ${TARGET_MONEY:,.0f} on seeds {REQUIRED_SEEDS}")
    print(f"  Domain: Q0 + Q1 ONLY (owned_quadrants == 2)")
    print(f"{'='*70}\n")

    episodes = []
    all_pass = True

    for idx, seed in enumerate(REQUIRED_SEEDS, 1):
        print(f"  Running Episode {idx}/{len(REQUIRED_SEEDS)} -- Seed {seed}...", flush=True)
        t0 = time.perf_counter()
        ep = run_episode(seed)
        elapsed = time.perf_counter() - t0
        ep["run_id"] = run_id
        ep["elapsed_seconds"] = round(elapsed, 1)
        # Derived fields for provenance verifier
        ep["max_owned_quadrants"] = ep["owned_quadrants"]
        ep["peak_active_tiles"] = ep["peak_productive_tiles"]
        ep["peak_workforce"] = ep["peak_simultaneous_workers"]
        ep["q1_unlocked"] = ep["owned_quadrants"] >= 2
        ep["q2_unlocked"] = ep["owned_quadrants"] >= 3
        ep["q2_unlock_day"] = None
        ep["q3_unlocked"] = ep["owned_quadrants"] >= 3
        ep["q3_unlock_day"] = None
        episodes.append(ep)

        money_pass = ep["final_money"] >= TARGET_MONEY
        domain_pass = ep["owned_quadrants"] == 2
        if not money_pass or not domain_pass:
            all_pass = False

        print(f"  Seed {seed} | ${ep['final_money']:,.2f} | {elapsed:.1f}s | {'PASS' if money_pass and domain_pass else 'FAIL'}")
        print_contribution_ladder(ep)

    # Summary
    import numpy as np
    moneys = [e["final_money"] for e in episodes]
    mean_money = float(np.mean(moneys))
    min_money = float(np.min(moneys))
    max_money = float(np.max(moneys))

    summary = {
        "run_id": run_id,
        "target_money": TARGET_MONEY,
        "all_seeds_pass": all_pass,
        "episodes_count": len(episodes),
        "economy": {
            "mean_money": mean_money,
            "median_money": float(np.median(moneys)),
            "std_money": float(np.std(moneys, ddof=1)) if len(moneys) > 1 else 0.0,
            "min_money": min_money,
            "max_money": max_money,
        },
        "domain": {
            "all_q0q1_only": all(e["owned_quadrants"] == 2 for e in episodes),
        },
        "contribution_ladder": {
            "mean_milk_revenue": float(np.mean([e["milk_revenue"] for e in episodes])),
            "mean_crop_revenue": float(np.mean([e["crop_revenue"] for e in episodes])),
            "mean_retail_wheat_spend": float(np.mean([e["retail_wheat_spend"] for e in episodes])),
            "mean_crop_harvests": float(np.mean([e["crop_harvests"] for e in episodes])),
            "mean_milk_harvested": float(np.mean([e["milk_harvested"] for e in episodes])),
            "mean_milk_sold": float(np.mean([e["milk_sold"] for e in episodes])),
            "mean_cows_bought": float(np.mean([e["cows_bought"] for e in episodes])),
            "mean_movement_pct": float(np.mean([e["movement_pct"] for e in episodes])),
            "mean_peak_tiles": float(np.mean([e["peak_productive_tiles"] for e in episodes])),
        },
        "land": {
            "q1_unlock_rate": float(sum(1 for e in episodes if e.get("max_owned_quadrants", 1) >= 2) / len(episodes) * 100.0),
            "q2_unlock_rate": float(sum(1 for e in episodes if e.get("max_owned_quadrants", 1) >= 3) / len(episodes) * 100.0),
            "q3_unlock_rate": float(sum(1 for e in episodes if e.get("max_owned_quadrants", 1) >= 4) / len(episodes) * 100.0),
        },
        "production": {
            "mean_peak_active_tiles": float(np.mean([e.get("peak_active_tiles", 0) for e in episodes])),
        },
        "workforce": {
            "mean_peak_workforce": float(np.mean([e.get("peak_simultaneous_workers", 1) for e in episodes])),
        },
    }

    # Save artifacts
    import dataclasses
    config_dict = dataclasses.asdict(X111_CONFIG)
    config_dict["run_id"] = run_id
    config_dict["expected_episodes"] = len(REQUIRED_SEEDS)
    config_dict["subphase"] = "E12-X1.11"
    config_dict["stage"] = "VERIFY"

    config_file = results_dir / "config.json"
    episodes_file = results_dir / "episodes.json"
    summary_file = results_dir / "summary.json"

    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config_dict, f, indent=2)

    with open(episodes_file, "w", encoding="utf-8") as f:
        json.dump({"run_id": run_id, "episodes": episodes}, f, indent=2)

    def get_hash(fp):
        h = hashlib.sha256()
        with open(fp, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()

    summary["config_sha256"] = get_hash(config_file)
    summary["episodes_sha256"] = get_hash(episodes_file)

    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Final verdict
    print(f"\n{'='*70}")
    print(f"  BENCHMARK RESULT: {'ALL SEEDS PASS' if all_pass else 'FAIL -- TARGET NOT MET'}")
    print(f"  Mean Money:  ${mean_money:,.2f}")
    print(f"  Min Money:   ${min_money:,.2f}")
    print(f"  Max Money:   ${max_money:,.2f}")
    print(f"  Results:     {results_dir}")
    print(f"{'='*70}\n")

    return summary


if __name__ == "__main__":
    benchmark_x111()
