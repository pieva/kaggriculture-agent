"""Benchmark runner for E11-VB1 Verified Baseline Re-establishment.

Executes a 30-episode paired benchmark of E11-VB1 (and E10 Control)
with versioned, append-only JSON artifacts, full config serialization,
and SHA-256 dataset provenance verification.
"""

import sys
import json
import hashlib
import time
import subprocess
from pathlib import Path
from dataclasses import asdict
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agricola.evaluation.runner import run_episode
from agricola.strategy.productive_mass_roi import ProductiveMassROIAgent, ProductiveMassConfig
from agricola.strategy.q1_capital_protected_roi import Q1CapitalProtectedROIAgent
from agricola.core.state import GameState
try:
    from verify_e11_run_provenance import verify_run, compute_sha256
except ImportError:
    from scripts.verify_e11_run_provenance import verify_run, compute_sha256


# 1. Fully Explicit Immutable E11-VB1 Configuration
E11_VB1_CONFIG = ProductiveMassConfig(
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
    accumulation_3q_mode="LEGACY_LOCK",
    accumulation_3q_optional_reserve=1300.0,
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


def get_git_info() -> dict:
    try:
        sha = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        status = subprocess.check_output(["git", "status", "--porcelain"], text=True).strip()
        is_dirty = len(status) > 0
    except Exception:
        sha = "UNCOMMITTED"
        is_dirty = True
    return {"git_sha": sha, "is_dirty": is_dirty}


def run_benchmark():
    timestamp_str = time.strftime("%Y%m%d-%H%M%S")
    run_id = f"E11-VB1-{timestamp_str}"
    
    output_dir = Path("results/e11") / run_id
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== LAUNCHING E11-VB1 VERIFIED BASELINE BENCHMARK ({run_id}) ===")
    
    opponents = ["pass", "random", "starter"]
    seeds = [ep * 100 for ep in range(10)]
    protocol = []
    for opp in opponents:
        for seed in seeds:
            protocol.append((opp, seed))

    # Save Config Snapshot
    git_info = get_git_info()
    config_snapshot = {
        "run_id": run_id,
        "variant_id": "E11-VB1",
        "strategy_class": "ProductiveMassROIAgent",
        "config_parameters": asdict(E11_VB1_CONFIG),
        "environment_specs": {
            "steps": 720,
            "episodes": 30,
            "opponents": opponents,
            "seeds": seeds
        },
        "git_info": git_info
    }
    
    config_path = output_dir / "config.json"
    with open(config_path, "w") as f:
        json.dump(config_snapshot, f, indent=2)

    # 1. Run E10 Control (30 Paired Episodes)
    print("\n--- Running E10 Control (30 Episodes) ---")
    e10_rewards = []
    for idx, (opp, seed) in enumerate(protocol):
        agent = Q1CapitalProtectedROIAgent()
        playing_as_p0 = (idx % 2 == 0)
        def fn(obs, c):
            return agent.act(GameState(obs))
        if playing_as_p0:
            res = run_episode(fn, opp, steps=720, seed=seed, track_p0=True, track_p1=False)
            rew = res["p0_reward"]
        else:
            res = run_episode(opp, fn, steps=720, seed=seed, track_p0=False, track_p1=True)
            rew = res["p1_reward"]
        e10_rewards.append(rew)

    e10_mean = float(np.mean(e10_rewards))
    print(f"E10 Control Mean Final Money: ${e10_mean:.2f} ± ${np.std(e10_rewards, ddof=1):.2f}")

    # 2. Run E11-VB1 (30 Paired Episodes)
    print("\n--- Running E11-VB1 Verified Baseline (30 Episodes) ---")
    episodes_records = []
    e11_rewards = []

    for idx, (opp, seed) in enumerate(protocol):
        agent = ProductiveMassROIAgent(config=E11_VB1_CONFIG)
        playing_as_p0 = (idx % 2 == 0)
        
        # Checkpoint trajectory tracking
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
                    "workforce": 1 + len(gs.hands_positions)
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

        e11_rewards.append(rew)
        
        # Extract land unlock events
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
            "variant_id": "E11-VB1",
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
            "q2_unlock_step": q3_step,
            "q3_unlocked": bool(agent.owned_quadrants >= 4),
            "q3_unlock_day": q3_day,
            "q3_unlock_step": q3_step,
            "peak_active_tiles": int(agent.telemetry.peak_productive_tiles),
            "peak_workforce": int(agent.telemetry.peak_simultaneous_workers),
            "checkpoints": checkpoints
        }
        episodes_records.append(ep_record)
        print(f"Episode {idx+1:2d}/30 | Seed {seed:3d} vs {opp:7s} | Money: ${rew:7.2f} | Q: {agent.owned_quadrants} | PeakWk: {agent.telemetry.peak_simultaneous_workers} | PeakAct: {agent.telemetry.peak_productive_tiles}")

    # Save Raw Episodes JSON
    episodes_payload = {
        "run_id": run_id,
        "variant_id": "E11-VB1",
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
        "variant_id": "E11-VB1",
        "timestamp": timestamp_str,
        "config_sha256": config_sha,
        "episodes_sha256": episodes_sha,
        "economy": {
            "mean_money": float(np.mean(e11_rewards)),
            "median_money": float(np.median(e11_rewards)),
            "std_money": float(np.std(e11_rewards, ddof=1)),
            "min_money": float(np.min(e11_rewards)),
            "max_money": float(np.max(e11_rewards)),
            "e10_control_mean_money": e10_mean,
            "delta_vs_e10": float(np.mean(e11_rewards) - e10_mean)
        },
        "land": {
            "q2_unlock_rate": float(sum(1 for q in quads if q >= 3) / 30.0 * 100.0),
            "q2_mean_day": float(np.mean(q2_days)) if q2_days else None,
            "q3_unlock_rate": float(sum(1 for q in quads if q >= 4) / 30.0 * 100.0),
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
        print(f"\nSUCCESS: E11-VB1 VERIFIED BASELINE ESTABLISHED IN {output_dir}")
    else:
        print(f"\nFAIL: PROVENANCE VERIFICATION FAILED FOR {output_dir}")
        sys.exit(1)


if __name__ == "__main__":
    run_benchmark()
