"""Benchmark runner for E11-X1.5 — Centered 2x4x4 Productive Core (32 tiles, 1 Land Purchase)."""

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
B3_REF_RESULTS = {
    0: 30234.00,
    100: 30072.00,
    200: 31460.00,
    300: 20014.00,
    400: 20448.00,
}
B3_REF_MEAN = 26445.60

X1_4_REF_RESULTS = {
    0: 22555.00,
    100: 28235.00,
    200: 28274.00,
    300: 28474.00,
    400: 28508.00,
}
X1_4_REF_MEAN = 27209.20

E11_X1_5_CONFIG = ProductiveMassConfig(
    productive_core_mode="E06_CENTERED",
    epu_level=2,
    enable_land_expansion=True,
    workforce_scaling_mode="LEGACY",
    multi_hire_mode="CORRECTED_MULTI",
    land_buy_mode="IMMEDIATE"
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

    final_obs = state[0].observation
    final_money = final_obs.farms[0]["money"]
    ep_data = agent_instance.telemetry.to_dict()
    ep_data["seed"] = seed
    ep_data["opponent"] = opponent_name
    ep_data["final_money"] = final_money
    
    # Telemetry extraction
    ep_data["peak_simultaneous_workers"] = ep_data.get("workforce", {}).get("peak_simultaneous_workers", 1)
    ep_data["peak_productive_tiles"] = ep_data.get("land_breakdown", {}).get("peak_productive_tiles", 0)
    ep_data["peak_active_tiles"] = ep_data["peak_productive_tiles"]
    ep_data["peak_workforce"] = ep_data["peak_simultaneous_workers"]
    ep_data["buy_land_day"] = getattr(agent_instance.telemetry, "buy_land_day", None)
    ep_data["buy_land_step"] = getattr(agent_instance.telemetry, "buy_land_executed_step", None)
    ep_data["actual_trigger_value"] = getattr(agent_instance.telemetry, "actual_trigger_value", None)
    ep_data["epu2_activation_day"] = getattr(agent_instance.telemetry, "epu2_activation_day", None)
    ep_data["day_reaching_16_active_tiles"] = getattr(agent_instance.telemetry, "day_reaching_16_active_tiles", None)
    ep_data["day_reaching_24_active_tiles"] = getattr(agent_instance.telemetry, "day_reaching_24_active_tiles", None)
    ep_data["day_reaching_30_active_tiles"] = getattr(agent_instance.telemetry, "day_reaching_30_active_tiles", None)
    ep_data["day_reaching_32_active_tiles"] = getattr(agent_instance.telemetry, "day_reaching_32_active_tiles", None)

    return ep_data


def benchmark_x1_5(stage: str = "B") -> Dict[str, Any]:
    """Run Stage A0 (1 seed) or Stage B (5 paired seeds) benchmark for X1.5."""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    run_id = f"E11-X1.5-{timestamp}"
    results_dir = Path(__file__).parent.parent / "results" / "e11" / run_id
    results_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== LAUNCHING E11-X1.5 STAGE {stage} ({run_id}) ===")

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
        agent_treat = ProductiveMassROIAgent(config=E11_X1_5_CONFIG)
        treat_data = run_episode(agent_treat, seed, opp)
        treat_data["run_id"] = run_id
        treat_data["max_owned_quadrants"] = treat_data.get("owned_quadrants", 1)
        treat_data["q2_unlocked"] = treat_data.get("owned_quadrants", 1) >= 2
        treat_data["q3_unlocked"] = treat_data.get("owned_quadrants", 1) >= 3
        treat_data["q2_unlock_day"] = treat_data.get("buy_land_day") if treat_data["q2_unlocked"] else None
        treat_data["q3_unlock_day"] = None
        treatment_episodes.append(treat_data)

        b3_money = B3_REF_RESULTS.get(seed, None)
        x14_money = X1_4_REF_RESULTS.get(seed, None)
        delta_vs_b3 = (treat_data["final_money"] - b3_money) if b3_money is not None else None
        delta_vs_x14 = (treat_data["final_money"] - x14_money) if x14_money is not None else None
        treat_data["delta_vs_b3"] = delta_vs_b3
        treat_data["delta_vs_x14"] = delta_vs_x14

        q_count = treat_data.get("owned_quadrants", 1)
        peak_wk = treat_data.get("peak_simultaneous_workers", 1)
        peak_act = treat_data.get("peak_active_tiles", 0)
        buy_day = treat_data.get("buy_land_day")
        trig = treat_data.get("actual_trigger_value")
        epu2_day = treat_data.get("epu2_activation_day")
        day16 = treat_data.get("day_reaching_16_active_tiles")
        day24 = treat_data.get("day_reaching_24_active_tiles")
        day32 = treat_data.get("day_reaching_32_active_tiles")

        print(f"Episode {idx:2d}/{len(seeds_opponents)} | Seed {seed:3d} vs {opp:7s} | Money: ${treat_data['final_money']:8.2f} (B3: ${b3_money}, X1.4: ${x14_money})")
        print(f"  Land Buy Day: {buy_day} (Trig: ${trig}) | EPU2 Act Day: {epu2_day}")
        print(f"  Day 16t: {day16} | Day 24t: {day24} | Day 32t: {day32}")
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

    x1_5_vs_b3_mean_delta = mean_treat - B3_REF_MEAN
    x1_5_vs_x14_mean_delta = mean_treat - X1_4_REF_MEAN

    b3_deltas = [e["delta_vs_b3"] for e in treatment_episodes if e.get("delta_vs_b3") is not None]
    x14_deltas = [e["delta_vs_x14"] for e in treatment_episodes if e.get("delta_vs_x14") is not None]

    paired_wins_b3 = sum(1 for d in b3_deltas if d > 0)
    paired_wins_x14 = sum(1 for d in x14_deltas if d > 0)

    config_dict = dataclasses.asdict(E11_X1_5_CONFIG)
    config_dict["run_id"] = run_id
    config_dict["expected_episodes"] = len(seeds_opponents)
    config_dict["subphase"] = "X1.5"
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

    peak_act = [e.get("peak_active_tiles", e.get("land_breakdown", {}).get("peak_productive_tiles", 0)) for e in treatment_episodes]
    peak_wk = [e.get("peak_workforce", e.get("workforce", {}).get("peak_simultaneous_workers", 1)) for e in treatment_episodes]

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
            "x1_5_vs_b3_mean_delta": x1_5_vs_b3_mean_delta,
            "x1_5_vs_x14_mean_delta": x1_5_vs_x14_mean_delta,
            "paired_wins_vs_b3": paired_wins_b3,
            "paired_wins_vs_x14": paired_wins_x14,
            "mean_paired_delta_vs_b3": float(np.mean(b3_deltas)) if b3_deltas else 0.0,
            "mean_paired_delta_vs_x14": float(np.mean(x14_deltas)) if x14_deltas else 0.0,
        },
        "land": {
            "q2_unlock_rate": float(sum(1 for q in [e.get("max_owned_quadrants", 1) for e in treatment_episodes] if q >= 2) / len(treatment_episodes) * 100.0),
            "q3_unlock_rate": float(sum(1 for q in [e.get("max_owned_quadrants", 1) for e in treatment_episodes] if q >= 3) / len(treatment_episodes) * 100.0)
        },
        "production": {
            "mean_peak_active_tiles": float(np.mean(peak_act))
        },
        "workforce": {
            "mean_peak_workforce": float(np.mean(peak_wk))
        },
        "telemetry_metrics": {
            "mean_buy_land_day": float(np.mean([e["buy_land_day"] for e in treatment_episodes if e["buy_land_day"] is not None])) if any(e["buy_land_day"] is not None for e in treatment_episodes) else None,
            "mean_trigger_value": float(np.mean([e["actual_trigger_value"] for e in treatment_episodes if e["actual_trigger_value"] is not None])) if any(e["actual_trigger_value"] is not None for e in treatment_episodes) else None,
            "mean_epu2_activation_day": float(np.mean([e["epu2_activation_day"] for e in treatment_episodes if e["epu2_activation_day"] is not None])) if any(e["epu2_activation_day"] is not None for e in treatment_episodes) else None,
            "mean_day_reaching_16_tiles": float(np.mean([e["day_reaching_16_active_tiles"] for e in treatment_episodes if e["day_reaching_16_active_tiles"] is not None])) if any(e["day_reaching_16_active_tiles"] is not None for e in treatment_episodes) else None,
            "mean_day_reaching_24_tiles": float(np.mean([e["day_reaching_24_active_tiles"] for e in treatment_episodes if e["day_reaching_24_active_tiles"] is not None])) if any(e["day_reaching_24_active_tiles"] is not None for e in treatment_episodes) else None,
            "mean_day_reaching_30_tiles": float(np.mean([e["day_reaching_30_active_tiles"] for e in treatment_episodes if e["day_reaching_30_active_tiles"] is not None])) if any(e["day_reaching_30_active_tiles"] is not None for e in treatment_episodes) else None,
            "mean_day_reaching_32_tiles": float(np.mean([e["day_reaching_32_active_tiles"] for e in treatment_episodes if e["day_reaching_32_active_tiles"] is not None])) if any(e["day_reaching_32_active_tiles"] is not None for e in treatment_episodes) else None,
            "mean_peak_active_tiles": float(np.mean(peak_act)),
            "mean_peak_workforce": float(np.mean(peak_wk))
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

    print(f"SUCCESS: E11-X1.5 STAGE {stage} ESTABLISHED AND VERIFIED IN {results_dir}")
    print(f"Mean Money: ${mean_treat:.2f} | Delta vs B3: ${x1_5_vs_b3_mean_delta:+.2f} | Delta vs X1.4: ${x1_5_vs_x14_mean_delta:+.2f}\n")

    return summary_dict

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run E11-X1.5 benchmark")
    parser.add_argument("--stage", type=str, default="B", choices=["A0", "B"], help="Stage A0 (1 seed) or B (5 paired seeds)")
    args = parser.parse_args()
    benchmark_x1_5(stage=args.stage)
