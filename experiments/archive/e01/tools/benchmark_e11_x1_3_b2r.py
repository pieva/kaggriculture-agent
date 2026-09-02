"""Benchmark runner for E11-X1.3-B2R — Spatially Equivalent 3x EPU Scaling (27 tiles, 1 Land Purchase)."""

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

# Historical References
A_REF_MEAN = 26888.40  # X1.3-A 1x EPU
B_REF_MEAN = 28727.40  # X1.3-B 2x EPU
OLD_B2_REF_MEAN = 9808.40  # Old B2 3x EPU Day-0 Buy

E11_X1_3_B2R_CONFIG = ProductiveMassConfig(
    productive_core_mode="E06_REPLICATED",
    epu_level=3,
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
        except Exception as e:
            print(f"Error on step {step}: {e}")
            break

    final_obs = state[0].observation
    final_money = final_obs.farms[0]["money"]
    ep_data = agent_instance.telemetry.to_dict()
    ep_data["seed"] = seed
    ep_data["opponent"] = opponent_name
    ep_data["final_money"] = final_money
    
    # B2R Specific Telemetry extract
    ep_data["buy_land_day"] = getattr(agent_instance.telemetry, "buy_land_day", None)
    ep_data["buy_land_step"] = getattr(agent_instance.telemetry, "buy_land_executed_step", None)
    ep_data["actual_trigger_value"] = getattr(agent_instance.telemetry, "actual_trigger_value", None)
    ep_data["epu2_activation_day"] = getattr(agent_instance.telemetry, "epu2_activation_day", None)
    ep_data["epu3_activation_day"] = getattr(agent_instance.telemetry, "epu3_activation_day", None)
    
    e2_act = ep_data["epu2_activation_day"]
    e3_act = ep_data["epu3_activation_day"]
    if e2_act is not None and e3_act is not None:
        ep_data["activation_delta"] = e3_act - e2_act
    else:
        ep_data["activation_delta"] = None
        
    ep_data["full_27_tiles_day"] = getattr(agent_instance.telemetry, "full_27_tiles_day", None)
    ep_data["full_27_tiles_step"] = getattr(agent_instance.telemetry, "full_27_tiles_step", None)
    ep_data["time_to_full_27_tiles_days"] = getattr(agent_instance.telemetry, "time_to_full_27_tiles_days", None)

    return ep_data


def benchmark_b2r(stage: str = "B") -> Dict[str, Any]:
    """Run Stage A0 (1 seed) or Stage B (5 paired seeds) benchmark for B2R."""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    run_id = f"E11-X1.3-B2R-{timestamp}"
    results_dir = Path(__file__).parent.parent / "results" / "e11" / run_id
    results_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== LAUNCHING E11-X1.3-B2R STAGE {stage} ({run_id}) ===")

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
        agent_treat = ProductiveMassROIAgent(config=E11_X1_3_B2R_CONFIG)
        treat_data = run_episode(agent_treat, seed, opp)
        treat_data["run_id"] = run_id
        treat_data["max_owned_quadrants"] = treat_data.get("owned_quadrants", 1)
        treat_data["peak_active_tiles"] = treat_data.get("peak_productive_tiles", 0)
        treat_data["peak_workforce"] = treat_data.get("peak_simultaneous_workers", 1)
        treat_data["q2_unlocked"] = treat_data.get("owned_quadrants", 1) >= 2
        treat_data["q3_unlocked"] = treat_data.get("owned_quadrants", 1) >= 3
        treat_data["q2_unlock_day"] = treat_data.get("buy_land_day") if treat_data["q2_unlocked"] else None
        treat_data["q3_unlock_day"] = None
        treatment_episodes.append(treat_data)

        q_count = treat_data.get("owned_quadrants", 1)
        peak_wk = treat_data.get("peak_simultaneous_workers", 1)
        peak_act = treat_data.get("peak_active_tiles", 0)
        buy_day = treat_data.get("buy_land_day")
        trig = treat_data.get("actual_trigger_value")
        e2_day = treat_data.get("epu2_activation_day")
        e3_day = treat_data.get("epu3_activation_day")
        full_day = treat_data.get("full_27_tiles_day")
        time_to_full = treat_data.get("time_to_full_27_tiles_days")

        print(f"Episode {idx:2d}/{len(seeds_opponents)} | Seed {seed:3d} vs {opp:7s} | Money: ${treat_data['final_money']:8.2f}")
        print(f"  Land Buy Day: {buy_day} (Trigger: ${trig}) | EPU2 Act Day: {e2_day} | EPU3 Act Day: {e3_day} | Full 27 Tiles Day: {full_day} (Time post-buy: {time_to_full}d)")
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

    b2r_vs_a_delta = mean_treat - A_REF_MEAN
    b2r_vs_b_delta = mean_treat - B_REF_MEAN
    b2r_vs_a_ratio = (mean_treat / A_REF_MEAN) * 100.0

    b_vs_a_delta = B_REF_MEAN - A_REF_MEAN
    land_amortization_gain = (b2r_vs_a_delta / b_vs_a_delta) if abs(b_vs_a_delta) > 1e-5 else 0.0

    config_dict = dataclasses.asdict(E11_X1_3_B2R_CONFIG)
    config_dict["run_id"] = run_id
    config_dict["expected_episodes"] = len(seeds_opponents)
    config_dict["subphase"] = "B2R"
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

    quads = [e.get("max_owned_quadrants", 1) for e in treatment_episodes]
    peak_act = [e.get("peak_active_tiles", 0) for e in treatment_episodes]
    peak_wk = [e.get("peak_workforce", 1) for e in treatment_episodes]

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
            "b2r_vs_a_delta": b2r_vs_a_delta,
            "b2r_vs_b_delta": b2r_vs_b_delta,
            "b2r_vs_a_ratio_pct": b2r_vs_a_ratio,
            "land_amortization_gain": land_amortization_gain,
        },
        "land": {
            "q2_unlock_rate": float(sum(1 for q in quads if q >= 3) / len(quads) * 100.0),
            "q3_unlock_rate": float(sum(1 for q in quads if q >= 4) / len(quads) * 100.0)
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
            "mean_epu3_activation_day": float(np.mean([e["epu3_activation_day"] for e in treatment_episodes if e["epu3_activation_day"] is not None])) if any(e["epu3_activation_day"] is not None for e in treatment_episodes) else None,
            "mean_activation_delta_days": float(np.mean([e["activation_delta"] for e in treatment_episodes if e["activation_delta"] is not None])) if any(e["activation_delta"] is not None for e in treatment_episodes) else None,
            "mean_full_27_tiles_day": float(np.mean([e["full_27_tiles_day"] for e in treatment_episodes if e["full_27_tiles_day"] is not None])) if any(e["full_27_tiles_day"] is not None for e in treatment_episodes) else None,
            "mean_time_to_full_27_tiles_days": float(np.mean([e["time_to_full_27_tiles_days"] for e in treatment_episodes if e["time_to_full_27_tiles_days"] is not None])) if any(e["time_to_full_27_tiles_days"] is not None for e in treatment_episodes) else None,
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

    print(f"SUCCESS: E11-X1.3-B2R STAGE {stage} ESTABLISHED AND VERIFIED IN {results_dir}")
    print(f"Mean Money: ${mean_treat:.2f} | Delta vs B: ${b2r_vs_b_delta:+.2f} | Land Amortization Gain: {land_amortization_gain:.2f}x\n")

    return summary_dict

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run E11-X1.3-B2R benchmark")
    parser.add_argument("--stage", type=str, default="B", choices=["A0", "B"], help="Stage A0 (1 seed) or B (5 paired seeds)")
    args = parser.parse_args()
    benchmark_b2r(stage=args.stage)
