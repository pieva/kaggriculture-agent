"""Benchmark runner for E11-X1 Verified 3Q Capital Accumulation Treatment.

Protocol Stages:
- Stage A (Smoke): 1 episode
- Stage B (Mini Verification): 5 paired episodes vs E11-VB1
- Stage C (Standard Iteration): 10 paired episodes vs E11-VB1

Outputs append-only versioned artifacts under results/e11/E11-X1-<timestamp>/
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


# 1. E11-X1 Controlled Single-Variable Treatment Config
E11_X1_CONFIG = ProductiveMassConfig(
    target_quadrants=4,
    stop_expansion_day=18,
    expansion_gate_mode="MIN_OPERATIONAL",
    q1_expansion_min_q0_active=6,
    q2_expansion_min_active=8,
    q3_expansion_min_active=12,
    capital_release_mode="BINARY",
    protect_expansion_capital=True,
    expansion_operating_buffer=100.0,
    imminent_land_cash_threshold=900.0,
    accumulation_3q_mode="DISCIPLINED_ACCUMULATION", # CONTROLLED CHANGE
    accumulation_3q_optional_reserve=500.0,          # CONTROLLED CHANGE ($500 float floor)
    productive_window_budget_cap=600.0,
    productive_window_max_day=11,
    prefer_land_before_optional_hire=False,
    prefer_land_before_livestock=True,
    workforce_scaling_mode="LEGACY",
    pre_land_hiring_enabled=True,
    max_pre_land_hiring_cost=25.0,
    max_workers=10,
    target_tiles_per_worker=7.0,
    operating_reserve=300.0,
    minimum_cash_after_hire=200.0,
    max_hires_per_day=2,
    stop_hire_day=20,
    locality_enabled=True,
    cross_quadrant_spillover=True,
    target_productive_tiles=80,
    liquidity_crop="CARROT",
    growth_crop_1="TOMATO",
    growth_crop_2="STRAWBERRY",
    growth_crop_3="MELON",
    feed_crop="WHEAT",
    wheat_feed_tiles_target=12,
    melon_plant_cutoff_day=18,
    strawberry_plant_cutoff_day=20,
    tomato_plant_cutoff_day=22,
    all_plant_cutoff_day=26,
    livestock_enabled=True,
    target_cows=6,
    target_sheep=4,
    feed_safety_buffer=4,
    stop_sheep_buy_day=18,
    stop_cow_buy_day=20,
    cow_cost=400.0,
    sheep_cost=500.0,
    reinvestment_threshold=1500.0,
    inventory_flush_start_day=27
)


def run_x1_benchmark(stage: str = "B"):
    timestamp_str = time.strftime("%Y%m%d-%H%M%S")
    run_id = f"E11-X1-{timestamp_str}"
    
    output_dir = Path("results/e11") / run_id
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== LAUNCHING E11-X1 BENCHMARK STAGE {stage} ({run_id}) ===")

    # Define standard seed protocol for iteration benchmark
    if stage == "A":
        protocol = [("pass", 0)]
    elif stage == "B":
        protocol = [
            ("pass", 0), ("pass", 100),
            ("random", 200), ("random", 300),
            ("starter", 400)
        ]
    else:  # Stage C (10 Paired Episodes)
        protocol = [
            ("pass", 0), ("pass", 100), ("pass", 200), ("pass", 300),
            ("random", 400), ("random", 500), ("random", 600),
            ("starter", 700), ("starter", 800), ("starter", 900)
        ]

    # Save Config Snapshot
    git_info = get_git_info()
    config_snapshot = {
        "run_id": run_id,
        "variant_id": "E11-X1",
        "strategy_class": "ProductiveMassROIAgent",
        "config_delta_vs_vb1": {
            "accumulation_3q_mode": ("LEGACY_LOCK", "DISCIPLINED_ACCUMULATION"),
            "accumulation_3q_optional_reserve": (1300.0, 500.0)
        },
        "config_parameters": asdict(E11_X1_CONFIG),
        "environment_specs": {
            "steps": 720,
            "episodes": len(protocol),
            "protocol": protocol
        },
        "git_info": git_info
    }
    
    config_path = output_dir / "config.json"
    with open(config_path, "w") as f:
        json.dump(config_snapshot, f, indent=2)

    # 1. Run E11-VB1 Baseline Controls
    print("\n--- Running E11-VB1 Controls ---")
    vb1_rewards = []
    vb1_quads = []
    for idx, (opp, seed) in enumerate(protocol):
        agent = ProductiveMassROIAgent(config=E11_VB1_CONFIG)
        playing_as_p0 = (idx % 2 == 0)
        def fn(obs, c):
            return agent.act(GameState(obs))
        if playing_as_p0:
            res = run_episode(fn, opp, steps=720, seed=seed, track_p0=True, track_p1=False)
            rew = res["p0_reward"]
        else:
            res = run_episode(opp, fn, steps=720, seed=seed, track_p0=False, track_p1=True)
            rew = res["p1_reward"]
        vb1_rewards.append(rew)
        vb1_quads.append(agent.owned_quadrants)

    vb1_3q_rate = sum(1 for q in vb1_quads if q >= 3) / len(vb1_quads) * 100.0
    print(f"E11-VB1 Baseline Mean Money: ${np.mean(vb1_rewards):.2f} | 3Q Unlock Rate: {vb1_3q_rate:.1f}%")

    # 2. Run E11-X1 Treatment
    print(f"\n--- Running E11-X1 Treatment (N={len(protocol)}) ---")
    episodes_records = []
    x1_rewards = []

    for idx, (opp, seed) in enumerate(protocol):
        agent = ProductiveMassROIAgent(config=E11_X1_CONFIG)
        playing_as_p0 = (idx % 2 == 0)
        
        checkpoints = {}
        
        def tracked_fn(obs, c):
            gs = GameState(obs)
            res = agent.act(gs)
            
            if gs.step in [180, 360, 540, 720]:
                checkpoints[f"step_{gs.step}"] = {
                    "day": gs.day,
                    "money": gs.money,
                    "owned_quadrants": agent.owned_quadrants,
                    "active_tiles": agent.telemetry.daily_productive_tiles_history[-1] if agent.telemetry.daily_productive_tiles_history else 0,
                    "workforce": 1 + len(gs.hands_positions),
                    "capital_gap_to_3q": max(0.0, 1100.0 - gs.money)
                }
            return res

        if playing_as_p0:
            res = run_episode(tracked_fn, opp, steps=720, seed=seed, track_p0=True, track_p1=False)
            rew = res["p0_reward"]
            pos = "p0"
        else:
            res = run_episode(opp, tracked_fn, steps=720, seed=seed, track_p0=False, track_p1=True)
            rew = res["p1_reward"]
            pos = "p1"

        x1_rewards.append(rew)
        
        events = agent.telemetry.events
        q2_day = None
        q2_step = None
        q3_day = None
        q3_step = None
        
        for ev in events:
            if ev.get("event") == "BUY_LAND":
                desc = ev.get("description", "")
                if "Q2" in desc or "75 tiles" in desc:
                    q2_day = ev.get("day")
                    q2_step = ev.get("step")
                elif "Q3" in desc or "100 tiles" in desc:
                    q3_day = ev.get("day")
                    q3_step = ev.get("step")

        ep_record = {
            "run_id": run_id,
            "variant_id": "E11-X1",
            "episode_index": idx,
            "seed": seed,
            "opponent": opp,
            "position": pos,
            "final_money": float(rew),
            "status": res.get("status", "COMPLETE"),
            "max_owned_quadrants": int(agent.owned_quadrants),
            "max_owned_tiles": int(agent.owned_quadrants * 25),
            "q2_unlocked": bool(agent.owned_quadrants >= 3),
            "q2_unlock_day": q2_day,
            "q2_unlock_step": q2_step,
            "q3_unlocked": bool(agent.owned_quadrants >= 4),
            "q3_unlock_day": q3_day,
            "q3_unlock_step": q3_step,
            "peak_active_tiles": int(agent.telemetry.peak_productive_tiles),
            "peak_workforce": int(agent.telemetry.peak_simultaneous_workers),
            "checkpoints": checkpoints
        }
        episodes_records.append(ep_record)
        print(f"Episode {idx+1:2d}/{len(protocol)} | Seed {seed:3d} vs {opp:7s} | Money: ${rew:7.2f} | Q: {agent.owned_quadrants} | PeakWk: {agent.telemetry.peak_simultaneous_workers} | PeakAct: {agent.telemetry.peak_productive_tiles}")

    # Save Raw Episodes JSON
    episodes_payload = {
        "run_id": run_id,
        "variant_id": "E11-X1",
        "episode_count": len(episodes_records),
        "episodes": episodes_records
    }
    episodes_path = output_dir / "episodes.json"
    with open(episodes_path, "w") as f:
        json.dump(episodes_payload, f, indent=2)

    # Compute Hashes
    config_sha = compute_sha256(config_path)
    episodes_sha = compute_sha256(episodes_path)

    # Compute Summary
    quads = [r["max_owned_quadrants"] for r in episodes_records]
    peak_act = [r["peak_active_tiles"] for r in episodes_records]
    peak_wk = [r["peak_workforce"] for r in episodes_records]
    
    q2_days = [r["q2_unlock_day"] for r in episodes_records if r["q2_unlocked"]]
    q3_days = [r["q3_unlock_day"] for r in episodes_records if r["q3_unlocked"]]

    summary_payload = {
        "run_id": run_id,
        "variant_id": "E11-X1",
        "stage": stage,
        "timestamp": timestamp_str,
        "config_sha256": config_sha,
        "episodes_sha256": episodes_sha,
        "economy": {
            "mean_money": float(np.mean(x1_rewards)),
            "median_money": float(np.median(x1_rewards)),
            "std_money": float(np.std(x1_rewards, ddof=1)) if len(x1_rewards) > 1 else 0.0,
            "min_money": float(np.min(x1_rewards)),
            "max_money": float(np.max(x1_rewards)),
            "vb1_baseline_mean_money": float(np.mean(vb1_rewards)),
            "delta_vs_vb1": float(np.mean(x1_rewards) - np.mean(vb1_rewards))
        },
        "land": {
            "q2_unlock_rate": float(sum(1 for q in quads if q >= 3) / len(quads) * 100.0),
            "q2_mean_day": float(np.mean(q2_days)) if q2_days else None,
            "q3_unlock_rate": float(sum(1 for q in quads if q >= 4) / len(quads) * 100.0),
            "q3_mean_day": float(np.mean(q3_days)) if q3_days else None,
            "mean_owned_quadrants": float(np.mean(quads)),
            "peak_owned_land_tiles": int(max(quads) * 25)
        },
        "production": {
            "mean_peak_active_tiles": float(np.mean(peak_act)),
            "max_peak_active_tiles": int(max(peak_act))
        },
        "workforce": {
            "mean_peak_workforce": float(np.mean(peak_wk)),
            "max_peak_workforce": int(max(peak_wk))
        }
    }

    summary_path = output_dir / "summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary_payload, f, indent=2)

    print("\n=== BENCHMARK COMPLETED — RUNNING PROVENANCE VERIFIER ===")
    verified = verify_run(output_dir)
    if verified:
        print(f"\nSUCCESS: E11-X1 STAGE {stage} ESTABLISHED AND VERIFIED IN {output_dir}")
    else:
        print(f"\nFAIL: PROVENANCE VERIFICATION FAILED FOR {output_dir}")
        sys.exit(1)

    return summary_payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["A", "B", "C"], default="B")
    args = parser.parse_args()
    run_x1_benchmark(stage=args.stage)
