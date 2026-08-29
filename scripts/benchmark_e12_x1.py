"""Benchmark runner for E12-X1.0 — Centered Hybrid Farm Scaling (Cow-First + Progressive 2x2 Core)."""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import Dict, Any, List

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agricola.strategy.productive_mass_roi import ProductiveMassROIAgent, ProductiveMassConfig
from agricola.core.state import GameState
from kaggle_environments import make

# Reference Datasets
B3_REF_RESULTS = {0: 30234.00, 100: 30072.00, 200: 31460.00, 300: 20014.00, 400: 20448.00}
B3_REF_MEAN = 26445.60

X1_4_REF_RESULTS = {0: 22555.00, 100: 28235.00, 200: 28274.00, 300: 28474.00, 400: 28508.00}
X1_4_REF_MEAN = 27209.20

X1_6_REF_RESULTS = {0: 29297.00, 100: 29095.00, 200: 34634.00, 300: 22318.00, 400: 22197.00}
X1_6_REF_MEAN = 27508.20

X1_7_REF_RESULTS = {0: 30220.00, 100: 30081.00, 200: 33371.00, 300: 23391.00, 400: 23356.00}
X1_7_REF_MEAN = 28083.80

E12_X1_3_CONFIG = ProductiveMassConfig(
    productive_core_mode="E12_HYBRID_FULL_SCALING",
    epu_level=3,
    enable_land_expansion=True,
    workforce_scaling_mode="LEGACY",
    multi_hire_mode="CORRECTED_MULTI",
    land_buy_mode="IMMEDIATE",
    protect_expansion_capital=False,
    stop_hire_day=26,
    max_hires_per_day=4,
    max_workers=6,
    target_tiles_per_worker=5.0,
    operating_reserve=50.0
)

def run_episode(agent_instance: ProductiveMassROIAgent, seed: int, opponent_name: str, steps: int = 720) -> Dict[str, Any]:
    """Run a single episode and return complete telemetry."""
    env = make("kaggriculture", configuration={"episodeSteps": steps, "seed": seed})
    state = env.reset()

    for step in range(steps):
        obs0 = state[0].observation
        gs = GameState(obs0)
        act = agent_instance.act(gs)
        try:
            state = env.step([act, {}])
        except Exception:
            break
        if state[0].status in ("DONE", "INVALID", "ERROR"):
            break

    tel = agent_instance.telemetry
    
    # Calculate Milk Revenue & Harvested
    milk_rev = tel.realized_revenue.get("MILK", 0.0)
    milk_harv = getattr(tel, "milk_harvested", 0)

    ep_data = {
        "seed": seed,
        "opponent": opponent_name,
        "final_money": tel.final_money,
        "peak_active_tiles": tel.peak_productive_tiles,
        "peak_productive_tiles": tel.peak_productive_tiles,
        "peak_workforce": tel.peak_simultaneous_workers,
        "peak_simultaneous_workers": tel.peak_simultaneous_workers,
        "owned_quadrants": getattr(agent_instance, "owned_quadrants", 1),
        "milk_harvested": milk_harv,
        "milk_revenue": milk_rev,
        "active_cows": getattr(tel, "active_cow_count", 0),
        "cows_owned": getattr(tel, "cows_acquired", 0),
        "active_pastures": getattr(tel, "active_pasture_count", 0),
        "turn_first_cow": getattr(tel, "turn_first_cow", None),
        "day_first_cow": getattr(tel, "day_first_cow", None),
        "spending_seeds": tel.spending_seeds,
        "spending_land": tel.spending_land,
        "spending_workforce": tel.spending_workforce,
        "spending_livestock": tel.spending_livestock,
        "realized_revenue": tel.realized_revenue
    }
    return ep_data


def benchmark_e12(stage: str = "B") -> Dict[str, Any]:
    """Run Stage A0 (1 seed) or Stage B (5 paired seeds) benchmark for E12-X1.0."""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    run_id = f"E12-X1.3-{timestamp}"
    results_dir = Path(__file__).parent.parent / "results" / "e12" / run_id
    results_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== LAUNCHING E12-X1.3 STAGE {stage} ({run_id}) ===")

    if stage == "A0":
        seeds_opponents = [(0, "pass")]
    else:
        seeds_opponents = [
            (0, "pass"),
            (100, "pass"),
            (200, "random"),
            (300, "random"),
            (400, "starter"),
        ]

    treatment_episodes = []

    for idx, (seed, opp) in enumerate(seeds_opponents, 1):
        agent_treat = ProductiveMassROIAgent(config=E12_X1_3_CONFIG)
        treat_data = run_episode(agent_treat, seed, opp)
        treat_data["run_id"] = run_id
        treat_data["max_owned_quadrants"] = treat_data.get("owned_quadrants", 1)
        treat_data["peak_workforce"] = treat_data.get("peak_simultaneous_workers", 1)
        treat_data["q2_unlocked"] = treat_data.get("owned_quadrants", 1) >= 2
        treat_data["q2_unlock_day"] = getattr(agent_treat.telemetry, "buy_land_day", None)
        treat_data["q3_unlocked"] = treat_data.get("owned_quadrants", 1) >= 3
        treat_data["q3_unlock_day"] = getattr(agent_treat.telemetry, "q2_buy_land_day", None)
        treatment_episodes.append(treat_data)

        b3_money = B3_REF_RESULTS.get(seed, None)
        x16_money = X1_6_REF_RESULTS.get(seed, None)
        x17_money = X1_7_REF_RESULTS.get(seed, None)

        delta_vs_b3 = (treat_data["final_money"] - b3_money) if b3_money is not None else None
        delta_vs_x16 = (treat_data["final_money"] - x16_money) if x16_money is not None else None
        delta_vs_x17 = (treat_data["final_money"] - x17_money) if x17_money is not None else None

        treat_data["delta_vs_b3"] = delta_vs_b3
        treat_data["delta_vs_x16"] = delta_vs_x16
        treat_data["delta_vs_x17"] = delta_vs_x17

        q_count = treat_data.get("owned_quadrants", 1)
        peak_wk = treat_data.get("peak_simultaneous_workers", 1)
        peak_act = treat_data.get("peak_active_tiles", 0)
        cows_owned = treat_data.get("cows_acquired", 0)
        active_cows = treat_data.get("active_cow_count", 0)
        active_pastures = treat_data.get("active_pasture_count", 0)
        turn_cow1 = treat_data.get("turn_first_cow")
        milk_harv = treat_data.get("milk_harvested", 0)
        milk_rev = treat_data.get("milk_revenue", 0.0)

        print(f"Episode {idx:2d}/{len(seeds_opponents)} | Seed {seed:3d} vs {opp:7s} | Money: ${treat_data['final_money']:8.2f} (X1.7: ${x17_money}, B3: ${b3_money})")
        print(f"  Turn Cow #1: {turn_cow1} | Cows Owned: {cows_owned} | Active Cows: {active_cows} | Pastures: {active_pastures}")
        print(f"  Milk Harvested: {milk_harv} units | Milk Revenue: ${milk_rev:.2f}")
        print(f"  Owned Quads: {q_count} | Peak Workers: {peak_wk} | Peak Active Tiles: {peak_act}")
        print()

    # Summary calculations
    import dataclasses
    import numpy as np

    treat_moneys = [e["final_money"] for e in treatment_episodes]
    mean_treat = float(np.mean(treat_moneys))
    median_treat = float(np.median(treat_moneys))
    std_treat = float(np.std(treat_moneys, ddof=1)) if len(treat_moneys) > 1 else 0.0
    min_treat = float(np.min(treat_moneys))
    max_treat = float(np.max(treat_moneys))

    x12_vs_b3_mean_delta = mean_treat - B3_REF_MEAN
    x12_vs_x16_mean_delta = mean_treat - X1_6_REF_MEAN
    x12_vs_x17_mean_delta = mean_treat - X1_7_REF_MEAN

    b3_deltas = [e["delta_vs_b3"] for e in treatment_episodes if e.get("delta_vs_b3") is not None]
    x16_deltas = [e["delta_vs_x16"] for e in treatment_episodes if e.get("delta_vs_x16") is not None]
    x17_deltas = [e["delta_vs_x17"] for e in treatment_episodes if e.get("delta_vs_x17") is not None]

    paired_wins_b3 = sum(1 for d in b3_deltas if d > 0)
    paired_wins_x16 = sum(1 for d in x16_deltas if d > 0)
    paired_wins_x17 = sum(1 for d in x17_deltas if d > 0)

    import dataclasses
    config_dict = dataclasses.asdict(E12_X1_3_CONFIG)
    config_dict["run_id"] = run_id
    config_dict["expected_episodes"] = len(seeds_opponents)
    config_dict["subphase"] = "E12-X1.3"
    config_dict["stage"] = stage

    config_file = results_dir / "config.json"
    episodes_file = results_dir / "episodes.json"
    summary_file = results_dir / "summary.json"

    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config_dict, f, indent=2)

    episodes_file_data = {
        "run_id": run_id,
        "episodes": treatment_episodes
    }

    with open(episodes_file, "w", encoding="utf-8") as f:
        json.dump(episodes_file_data, f, indent=2)

    import hashlib
    def get_hash(fp):
        h = hashlib.sha256()
        with open(fp, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()

    summary_dict = {
        "run_id": run_id,
        "config_sha256": get_hash(config_file),
        "episodes_sha256": get_hash(episodes_file),
        "episodes_count": len(treatment_episodes),
        "economy": {
            "mean_money": mean_treat,
            "median_money": median_treat,
            "std_money": std_treat,
            "min_money": min_treat,
            "max_money": max_treat,
            "x12_vs_b3_mean_delta": x12_vs_b3_mean_delta,
            "x12_vs_x16_mean_delta": x12_vs_x16_mean_delta,
            "x12_vs_x17_mean_delta": x12_vs_x17_mean_delta,
            "paired_wins_vs_b3": paired_wins_b3,
            "paired_wins_vs_x16": paired_wins_x16,
            "paired_wins_vs_x17": paired_wins_x17,
            "mean_paired_delta_vs_b3": float(np.mean(b3_deltas)) if b3_deltas else 0.0,
            "mean_paired_delta_vs_x16": float(np.mean(x16_deltas)) if x16_deltas else 0.0,
            "mean_paired_delta_vs_x17": float(np.mean(x17_deltas)) if x17_deltas else 0.0,
        },
        "land": {
            "q2_unlock_rate": float(sum(1 for e in treatment_episodes if e.get("max_owned_quadrants", 1) >= 3) / len(treatment_episodes) * 100.0),
            "q3_unlock_rate": float(sum(1 for e in treatment_episodes if e.get("max_owned_quadrants", 1) >= 4) / len(treatment_episodes) * 100.0)
        },
        "production": {
            "mean_peak_active_tiles": float(np.mean([e.get("peak_active_tiles", 0) for e in treatment_episodes]))
        },
        "workforce": {
            "mean_peak_workforce": float(np.mean([e.get("peak_simultaneous_workers", 1) for e in treatment_episodes]))
        },
        "livestock_telemetry": {
            "mean_cows_acquired": float(np.mean([e.get("cows_acquired", 0) for e in treatment_episodes])),
            "mean_active_cows": float(np.mean([e.get("active_cow_count", 0) for e in treatment_episodes])),
            "mean_active_pastures": float(np.mean([e.get("active_pasture_count", 0) for e in treatment_episodes])),
            "mean_turn_first_cow": float(np.mean([e["turn_first_cow"] for e in treatment_episodes if e.get("turn_first_cow") is not None])) if any(e.get("turn_first_cow") is not None for e in treatment_episodes) else None,
            "mean_milk_harvested": float(np.mean([e.get("milk_harvested", 0) for e in treatment_episodes])),
            "mean_milk_revenue": float(np.mean([e.get("milk_revenue", 0.0) for e in treatment_episodes])),
        }
    }

    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary_dict, f, indent=2)

    print("\n=== BENCHMARK COMPLETED — RUNNING PROVENANCE VERIFIER ===")
    from verify_e11_run_provenance import verify_run
    ok = verify_run(results_dir)
    if not ok:
        print(f"PROVENANCE VERIFICATION FAILED FOR {results_dir}")
        sys.exit(1)

    print(f"SUCCESS: E12-X1.0 STAGE {stage} ESTABLISHED AND VERIFIED IN {results_dir}")
    print(f"Mean Money: ${mean_treat:.2f} | Delta vs X1.7: ${x12_vs_x17_mean_delta:+.2f} | Delta vs B3: ${x12_vs_b3_mean_delta:+.2f}\n")

    return summary_dict

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run E12 benchmark")
    parser.add_argument("--stage", type=str, default="B", choices=["A0", "B"], help="Stage A0 (1 seed) or B (5 paired seeds)")
    args = parser.parse_args()
    benchmark_e12(stage=args.stage)
