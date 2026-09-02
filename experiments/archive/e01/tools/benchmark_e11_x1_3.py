"""Benchmark runner for E11-X1.3 E06 Productive Unit Replication & Scaling.

Subphases:
- Subphase A (1x EPU Replication - 9 tiles): E06 mechanism replication
- Subphase B (2x EPU Scaling - 18 tiles): 2x scaling efficiency
- Subphase C (3x EPU Scaling - 27 tiles): 3x scaling efficiency

Stages:
- Stage A0: Seed 0 vs pass diagnostic (720 steps) vs E06 reference ($25,847.00)
- Stage B: 5 paired episodes vs E11-VB1 control
- Stage C: 10 paired episodes vs E11-VB1 control

Outputs append-only versioned artifacts under results/e11/E11-X1.3-<subphase>-<timestamp>/
and runs verify_e11_run_provenance verifier.
"""

import sys
import json
import time
import argparse
from pathlib import Path
from dataclasses import asdict
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agricola.evaluation.runner import run_episode
from agricola.strategy.productive_mass_roi import ProductiveMassROIAgent, ProductiveMassConfig
from agricola.strategy.water_first_hire_nw_cluster_roi import WaterFirstHIRENWClusterROIAgent
from agricola.core.state import GameState
try:
    from benchmark_e11_vb1 import E11_VB1_CONFIG, get_git_info
except ImportError:
    from scripts.benchmark_e11_vb1 import E11_VB1_CONFIG, get_git_info
try:
    from verify_e11_run_provenance import verify_run, compute_sha256
except ImportError:
    from scripts.verify_e11_run_provenance import verify_run, compute_sha256


# E11-X1.3-A Configuration (1x EPU 9-tile Replication)
E11_X1_3_A_CONFIG = ProductiveMassConfig(
    productive_core_mode="E06_REPLICATED",
    epu_level=1,
    enable_land_expansion=False,
    workforce_scaling_mode="LEGACY",
    multi_hire_mode="SINGLE_PER_DAY",
    land_buy_mode="IMMEDIATE"
)

# E11-X1.3-B Configuration (2x EPU 18-tile Scaling)
E11_X1_3_B_CONFIG = ProductiveMassConfig(
    productive_core_mode="E06_REPLICATED",
    epu_level=2,
    enable_land_expansion=True,
    workforce_scaling_mode="LEGACY",
    multi_hire_mode="SINGLE_PER_DAY",
    land_buy_mode="IMMEDIATE"
)

# E11-X1.3-C Configuration (3x EPU 27-tile Scaling)
E11_X1_3_C_CONFIG = ProductiveMassConfig(
    productive_core_mode="E06_REPLICATED",
    epu_level=3,
    enable_land_expansion=True,
    workforce_scaling_mode="LEGACY",
    multi_hire_mode="SINGLE_PER_DAY",
    land_buy_mode="IMMEDIATE"
)


def run_benchmark(subphase: str = "A", stage: str = "A0"):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    run_id = f"E11-X1.3-{subphase}-{timestamp}"
    results_dir = Path(__file__).parent.parent / "results" / "e11" / run_id
    results_dir.mkdir(parents=True, exist_ok=True)
    
    seeds = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
    opponents = ["pass", "pass", "random", "random", "starter", "pass", "random", "starter", "pass", "random"]
    
    if stage == "A0":
        num_episodes = 1
    elif stage == "B":
        num_episodes = 5
    elif stage == "C":
        num_episodes = 10
    else:
        raise ValueError(f"Unknown stage: {stage}")

    print(f"=== LAUNCHING E11-X1.3 SUBPHASE {subphase} STAGE {stage} ({run_id}) ===")
    
    if subphase == "A":
        treatment_config = E11_X1_3_A_CONFIG
    elif subphase == "B":
        treatment_config = E11_X1_3_B_CONFIG
    elif subphase == "C":
        treatment_config = E11_X1_3_C_CONFIG
    else:
        raise ValueError(f"Unknown subphase: {subphase}")

    # Save initial config.json
    config_dict = asdict(treatment_config)
    config_dict["run_id"] = run_id
    config_dict["expected_episodes"] = num_episodes
    config_dict["subphase"] = subphase
    config_dict["stage"] = stage
    config_path = results_dir / "config.json"
    with open(config_path, "w") as f:
        json.dump(config_dict, f, indent=2)

    # 1. Run Control Baseline (E06 for A0 diagnostic; E11-VB1 for multi-episode B/C)
    print("\n--- Running Control Baseline ---")
    control_rewards = []
    control_name = "E06" if stage == "A0" else "E11-VB1"
    
    for i in range(num_episodes):
        seed = seeds[i]
        opp = opponents[i]
        if stage == "A0":
            ctrl_agent = WaterFirstHIRENWClusterROIAgent()
            res_ctrl = run_episode(lambda obs, c: ctrl_agent.act(GameState(obs)), opp, steps=720, seed=seed)
        else:
            ctrl_agent = ProductiveMassROIAgent(config=E11_VB1_CONFIG)
            res_ctrl = run_episode(lambda obs, c: ctrl_agent.act(GameState(obs)), opp, steps=720, seed=seed)
        control_rewards.append(res_ctrl["p0_reward"])

    print(f"{control_name} Baseline Mean Money: ${np.mean(control_rewards):.2f}")

    # 2. Run E11-X1.3 Treatment
    print(f"\n--- Running E11-X1.3-{subphase} Treatment (N={num_episodes}) ---")
    episodes_data = []
    treatment_rewards = []
    
    for i in range(num_episodes):
        seed = seeds[i]
        opp = opponents[i]
        agent_treat = ProductiveMassROIAgent(config=treatment_config)
        res_treat = run_episode(lambda obs, c: agent_treat.act(GameState(obs)), opp, steps=720, seed=seed)
        
        rew = res_treat["p0_reward"]
        treatment_rewards.append(rew)
        q_count = agent_treat.owned_quadrants
        
        ep_record = {
            "run_id": run_id,
            "episode_id": i + 1,
            "seed": seed,
            "opponent": opp,
            "final_money": float(rew),
            "owned_quadrants": q_count,
            "max_owned_quadrants": q_count,
            "owned_tiles": q_count * 25,
            "q2_unlocked": bool(q_count >= 3),
            "q2_unlock_day": None,
            "q3_unlocked": bool(q_count >= 4),
            "q3_unlock_day": None,
            "peak_workforce": int(agent_treat.telemetry.peak_simultaneous_workers),
            "peak_active_tiles": int(max(agent_treat.telemetry.daily_productive_tiles_history, default=0)),
            "spending_land": float(agent_treat.telemetry.spending_land),
            "spending_workforce": float(agent_treat.telemetry.spending_workforce),
            "spending_seeds": float(agent_treat.telemetry.spending_seeds),
            "events_log": agent_treat.telemetry.events
        }
        episodes_data.append(ep_record)
        print(f"Episode {i+1:2d}/{num_episodes} | Seed {seed:3d} vs {opp:7s} | Money: ${rew:7.2f} | Q: {q_count} | PeakWk: {ep_record['peak_workforce']} | PeakAct: {ep_record['peak_active_tiles']}")

    # Save episodes.json
    episodes_payload = {
        "episode_count": len(episodes_data),
        "episodes": episodes_data
    }
    episodes_path = results_dir / "episodes.json"
    with open(episodes_path, "w") as f:
        json.dump(episodes_payload, f, indent=2)

    episodes_sha256 = compute_sha256(episodes_path)
    config_sha256 = compute_sha256(config_path)

    # Compute Summary Statistics matching verifier layout
    rewards = [ep["final_money"] for ep in episodes_data]
    quads = [ep["max_owned_quadrants"] for ep in episodes_data]
    peak_act = [ep["peak_active_tiles"] for ep in episodes_data]
    peak_wk = [ep["peak_workforce"] for ep in episodes_data]

    e06_ref_money = control_rewards[0] if stage == "A0" else 25847.00
    equivalence_ratio = float(np.mean(rewards) / e06_ref_money)

    summary_data = {
        "run_id": run_id,
        "subphase": subphase,
        "stage": stage,
        "episodes_count": num_episodes,
        "git_info": get_git_info(),
        "config_sha256": config_sha256,
        "episodes_sha256": episodes_sha256,
        "equivalence_metrics": {
            "control_name": control_name,
            "control_mean_money": float(np.mean(control_rewards)),
            "e06_seed0_ref_money": e06_ref_money,
            "equivalence_ratio_vs_e06_seed0": equivalence_ratio
        },
        "economy": {
            "mean_money": float(np.mean(rewards)),
            "median_money": float(np.median(rewards)),
            "std_money": float(np.std(rewards, ddof=1)) if len(rewards) > 1 else 0.0,
            "min_money": float(np.min(rewards)),
            "max_money": float(np.max(rewards))
        },
        "land": {
            "q2_unlock_rate": float(sum(1 for q in quads if q >= 3) / len(quads) * 100.0),
            "q3_unlock_rate": float(sum(1 for q in quads if q >= 4) / len(quads) * 100.0),
            "mean_owned_quadrants": float(np.mean(quads))
        },
        "production": {
            "mean_peak_active_tiles": float(np.mean(peak_act))
        },
        "workforce": {
            "mean_peak_workforce": float(np.mean(peak_wk))
        }
    }

    summary_path = results_dir / "summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary_data, f, indent=2)

    print("\n=== BENCHMARK COMPLETED — RUNNING PROVENANCE VERIFIER ===")
    verified = verify_run(results_dir)
    
    if verified:
        print(f"\nSUCCESS: E11-X1.3-{subphase} STAGE {stage} ESTABLISHED AND VERIFIED IN {results_dir}")
        print(f"Treatment Mean Money: ${np.mean(rewards):.2f} | Equivalence Ratio vs E06 Seed 0 (${e06_ref_money:.2f}): {equivalence_ratio*100:.1f}%\n")
    else:
        print(f"\nFAILURE: PROVENANCE VERIFIER REJECTED {results_dir}\n")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run E11-X1.3 Benchmark")
    parser.add_argument("--subphase", type=str, default="A", choices=["A", "B", "C"], help="Subphase: A (1x EPU 9t), B (2x EPU 18t), C (3x EPU 27t)")
    parser.add_argument("--stage", type=str, default="A0", choices=["A0", "B", "C"], help="Protocol stage: A0 (seed 0 diagnostic), B (5 ep), C (10 ep)")
    args = parser.parse_args()
    run_benchmark(subphase=args.subphase, stage=args.stage)
