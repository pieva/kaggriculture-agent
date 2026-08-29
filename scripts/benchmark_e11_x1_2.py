"""Benchmark runner for E11-X1.2 E06 Productive Core Restoration & Corrected Multi-HIRE Treatment.

Protocol Stages:
- Stage A (Smoke): 1 episode
- Stage B (Mini Verification): 5 paired episodes vs E11-VB1
- Stage C (Standard Iteration): 10 paired episodes vs E11-VB1 (if Stage B mean money > $5k or 3Q unlock > 0)

Outputs append-only versioned artifacts under results/e11/E11-X1.2-<timestamp>/
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
from agricola.core.state import GameState
try:
    from benchmark_e11_vb1 import E11_VB1_CONFIG, get_git_info
except ImportError:
    from scripts.benchmark_e11_vb1 import E11_VB1_CONFIG, get_git_info
try:
    from verify_e11_run_provenance import verify_run, compute_sha256
except ImportError:
    from scripts.verify_e11_run_provenance import verify_run, compute_sha256


# Define explicit E11-X1.2 Treatment Config
E11_X1_2_CONFIG = ProductiveMassConfig(
    protect_expansion_capital=True,
    expansion_gate_mode="MIN_OPERATIONAL",
    q1_expansion_min_q0_active=10,
    q2_expansion_min_active=15,
    q3_expansion_min_active=25,
    workforce_scaling_mode="LEGACY",
    target_tiles_per_worker=7.0,
    accumulation_3q_mode="LEGACY_LOCK",
    accumulation_3q_optional_reserve=500.0,
    productive_core_mode="E06_RESTORED",
    multi_hire_mode="CORRECTED_MULTI",
    land_buy_mode="PRODUCTIVE_SURPLUS",
    surplus_land_threshold=1300.0,
    compact_footprint_size=9,
)


def run_benchmark(stage: str = "B"):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    run_id = f"E11-X1.2-{timestamp}"
    results_dir = Path(__file__).parent.parent / "results" / "e11" / run_id
    results_dir.mkdir(parents=True, exist_ok=True)
    
    seeds = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
    opponents = ["pass", "pass", "random", "random", "starter", "pass", "random", "starter", "pass", "random"]
    
    if stage == "A":
        num_episodes = 1
    elif stage == "B":
        num_episodes = 5
    elif stage == "C":
        num_episodes = 10
    else:
        raise ValueError(f"Unknown stage: {stage}")

    print(f"=== LAUNCHING E11-X1.2 BENCHMARK STAGE {stage} ({run_id}) ===")
    
    # Save config.json once
    config_dict = asdict(E11_X1_2_CONFIG)
    config_dict["run_id"] = run_id
    config_dict["expected_episodes"] = num_episodes
    config_dict["stage"] = stage
    config_path = results_dir / "config.json"
    with open(config_path, "w") as f:
        json.dump(config_dict, f, indent=2)

    # 1. Run E11-VB1 Control Baseline
    print("\n--- Running E11-VB1 Controls ---")
    vb1_rewards = []
    vb1_3q_unlocks = []
    for i in range(num_episodes):
        seed = seeds[i]
        opp = opponents[i]
        agent_vb1 = ProductiveMassROIAgent(config=E11_VB1_CONFIG)
        res_vb1 = run_episode(lambda obs, c: agent_vb1.act(GameState(obs)), opp, steps=720, seed=seed)
        vb1_rewards.append(res_vb1["p0_reward"])
        vb1_3q_unlocks.append(1 if agent_vb1.owned_quadrants >= 3 else 0)

    print(f"E11-VB1 Baseline Mean Money: ${np.mean(vb1_rewards):.2f} | 3Q Unlock Rate: {np.mean(vb1_3q_unlocks)*100:.1f}%")

    # 2. Run E11-X1.2 Treatment
    print(f"\n--- Running E11-X1.2 Treatment (N={num_episodes}) ---")
    episodes_data = []
    treatment_rewards = []
    treatment_3q_unlocks = []
    
    for i in range(num_episodes):
        seed = seeds[i]
        opp = opponents[i]
        agent_x1_2 = ProductiveMassROIAgent(config=E11_X1_2_CONFIG)
        res_x1_2 = run_episode(lambda obs, c: agent_x1_2.act(GameState(obs)), opp, steps=720, seed=seed)
        
        rew = res_x1_2["p0_reward"]
        treatment_rewards.append(rew)
        q_count = agent_x1_2.owned_quadrants
        treatment_3q_unlocks.append(1 if q_count >= 3 else 0)
        
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
            "peak_workforce": int(agent_x1_2.telemetry.peak_simultaneous_workers),
            "peak_active_tiles": int(max(agent_x1_2.telemetry.daily_productive_tiles_history, default=0)),
            "spending_land": float(agent_x1_2.telemetry.spending_land),
            "spending_workforce": float(agent_x1_2.telemetry.spending_workforce),
            "spending_seeds": float(agent_x1_2.telemetry.spending_seeds),
            "events_log": agent_x1_2.telemetry.events
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

    summary_data = {
        "run_id": run_id,
        "stage": stage,
        "episodes_count": num_episodes,
        "git_info": get_git_info(),
        "config_sha256": config_sha256,
        "episodes_sha256": episodes_sha256,
        "economy": {
            "mean_money": float(np.mean(rewards)),
            "median_money": float(np.median(rewards)),
            "std_money": float(np.std(rewards, ddof=1)) if len(rewards) > 1 else 0.0,
            "min_money": float(np.min(rewards)),
            "max_money": float(np.max(rewards)),
            "vb1_baseline_mean_money": float(np.mean(vb1_rewards))
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
        print(f"\nSUCCESS: E11-X1.2 STAGE {stage} ESTABLISHED AND VERIFIED IN {results_dir}\n")
    else:
        print(f"\nFAILURE: PROVENANCE VERIFIER REJECTED {results_dir}\n")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run E11-X1.2 Benchmark")
    parser.add_argument("--stage", type=str, default="B", choices=["A", "B", "C"], help="Protocol stage: A (1 ep), B (5 ep), C (10 ep)")
    args = parser.parse_args()
    run_benchmark(stage=args.stage)
