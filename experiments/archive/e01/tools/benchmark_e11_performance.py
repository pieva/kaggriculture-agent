"""Benchmark Runner Script for E11 Productive Mass Expansion Series (E11-01 to E11-06).

Runs 30 paired episodes for E05, E06, E08, E09-01, E10-01, E11-01, E11-02, E11-03, E11-04, E11-05, and E11-06.
Calculates paired deltas, aggregate statistics, architectural deployment metrics (Q2/Q3 unlocks, peak land, workforce, active tiles, utilization), crop telemetry, state machine telemetry, and trajectory telemetry.
Saves output to experiments/archive/e11/artifacts/productive_mass.json.
"""

import sys
import os
import time
import json
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agricola.evaluation.runner import run_episode
from agricola.strategy.hire_nw_cluster_roi import HIRENWClusterROIAgent
from agricola.strategy.water_first_hire_nw_cluster_roi import WaterFirstHIRENWClusterROIAgent
from agricola.strategy.hybrid_livestock_cluster_roi import HybridLivestockClusterROIAgent
from agricola.strategy.livestock_ablation_roi import LivestockAblationROIAgent
from agricola.strategy.q1_capital_protected_roi import Q1CapitalProtectedROIAgent
from agricola.strategy.productive_mass_roi import ProductiveMassROIAgent, ProductiveMassConfig
from agricola.core.state import GameState


def get_agent_factory(name: str):
    if name == "E05":
        return lambda: HIRENWClusterROIAgent()
    elif name == "E06":
        return lambda: WaterFirstHIRENWClusterROIAgent()
    elif name in ("E07", "E08"):
        return lambda: HybridLivestockClusterROIAgent()
    elif name == "E09_01":
        return lambda: LivestockAblationROIAgent()
    elif name == "E10_01":
        return lambda: Q1CapitalProtectedROIAgent()
    elif name == "E11_01":
        return lambda: ProductiveMassROIAgent(config=ProductiveMassConfig(
            protect_expansion_capital=False,
            expansion_gate_mode="LEGACY_SATURATION",
            capital_release_mode="BINARY",
            workforce_scaling_mode="LEGACY",
            prefer_land_before_optional_hire=False,
            target_tiles_per_worker=7.0
        ))
    elif name == "E11_02":
        return lambda: ProductiveMassROIAgent(config=ProductiveMassConfig(
            protect_expansion_capital=True,
            expansion_gate_mode="LEGACY_SATURATION",
            capital_release_mode="BINARY",
            workforce_scaling_mode="LEGACY",
            prefer_land_before_optional_hire=True,
            target_tiles_per_worker=7.0
        ))
    elif name == "E11_03":
        return lambda: ProductiveMassROIAgent(config=ProductiveMassConfig(
            protect_expansion_capital=True,
            expansion_gate_mode="MIN_OPERATIONAL",
            capital_release_mode="BINARY",
            workforce_scaling_mode="LEGACY",
            prefer_land_before_optional_hire=False,
            target_tiles_per_worker=7.0
        ))
    elif name == "E11_04":
        return lambda: ProductiveMassROIAgent(config=ProductiveMassConfig(
            protect_expansion_capital=True,
            expansion_gate_mode="MIN_OPERATIONAL",
            capital_release_mode="SYNCHRONIZED",
            workforce_scaling_mode="LEGACY",
            prefer_land_before_optional_hire=False,
            target_tiles_per_worker=7.0
        ))
    elif name == "E11_05":
        return lambda: ProductiveMassROIAgent(config=ProductiveMassConfig(
            protect_expansion_capital=True,
            expansion_gate_mode="MIN_OPERATIONAL",
            capital_release_mode="STAGED",
            workforce_scaling_mode="LEGACY",
            prefer_land_before_optional_hire=False,
            target_tiles_per_worker=7.0
        ))
    elif name == "E11_06":
        return lambda: ProductiveMassROIAgent(config=ProductiveMassConfig(
            protect_expansion_capital=True,
            expansion_gate_mode="MIN_OPERATIONAL",
            capital_release_mode="BINARY",
            workforce_scaling_mode="LAND_CO_SCALING",
            prefer_land_before_optional_hire=False,
            target_tiles_per_worker=5.0
        ))
    else:
        raise ValueError(f"Unknown agent name: {name}")


def compute_metrics(rewards, wins_count, total):
    arr = np.array(rewards, dtype=float)
    return {
        "episodes": int(total),
        "mean_final_money": float(np.mean(arr)),
        "std_dev": float(np.std(arr, ddof=1)) if total > 1 else 0.0,
        "median_final_money": float(np.median(arr)),
        "min_final_money": float(np.min(arr)),
        "max_final_money": float(np.max(arr)),
        "percentiles": {
            "P5": float(np.percentile(arr, 5)),
            "P10": float(np.percentile(arr, 10)),
            "P25": float(np.percentile(arr, 25)),
            "P50": float(np.percentile(arr, 50)),
            "P75": float(np.percentile(arr, 75)),
            "P90": float(np.percentile(arr, 90)),
            "P95": float(np.percentile(arr, 95)),
        },
        "episodes_under_10k": int(np.sum(arr < 10000.0)),
        "episodes_under_20k": int(np.sum(arr < 20000.0)),
        "episodes_under_50k": int(np.sum(arr < 50000.0)),
        "coefficient_of_variation": float(np.std(arr, ddof=1) / np.mean(arr)) if np.mean(arr) > 0 else 0.0,
        "win_rate": float(wins_count / total * 100.0)
    }


def run_standard_30_benchmark():
    print("=" * 95, flush=True)
    print("   RUNNING E11 REPRODUCIBILITY AUDIT BENCHMARK (30 PAIRED EPISODES)", flush=True)
    print("=" * 95, flush=True)

    opponents = ["pass", "random", "starter"]
    episodes_per_opp = 10

    agent_keys = ["E05", "E06", "E08", "E09_01", "E10_01", "E11_01", "E11_02", "E11_03", "E11_04", "E11_05", "E11_06"]
    raw_results = {a: [] for a in agent_keys}
    raw_telemetry = {a: [] for a in agent_keys}

    t0 = time.time()
    for opp_idx, opp in enumerate(opponents):
        print(f"\n--- Benchmark vs Opponent: '{opp}' (10 episodes) ---", flush=True)
        for ep_idx in range(episodes_per_opp):
            playing_as_p0 = (ep_idx % 2 == 0)
            seed = ep_idx * 100
            pos = "P0" if playing_as_p0 else "P1"

            for agent_name in agent_keys:
                agent_inst = get_agent_factory(agent_name)()

                def agent_wrapper(obs, config):
                    gs = GameState(obs)
                    return agent_inst.act(gs)

                if playing_as_p0:
                    res = run_episode(agent_wrapper, opp, steps=720, seed=seed, track_p0=True, track_p1=False)
                    rew = res["p0_reward"]
                    status = res["p0_status"]
                else:
                    res = run_episode(opp, agent_wrapper, steps=720, seed=seed, track_p0=False, track_p1=True)
                    rew = res["p1_reward"]
                    status = res["p1_status"]

                tel_dict = getattr(agent_inst, "telemetry", None)
                tel_summary = tel_dict.to_dict() if tel_dict else {}
                owned_q = getattr(agent_inst, "owned_quadrants", 1)

                raw_results[agent_name].append({
                    "seed": seed,
                    "opponent": opp,
                    "position": pos,
                    "reward": rew,
                    "status": status,
                    "owned_quadrants": owned_q,
                    "telemetry": tel_summary
                })

            # Print progress for E10-01, E11-01, E11-03, E11-06
            r_e10 = raw_results["E10_01"][-1]["reward"]
            r_e11_01 = raw_results["E11_01"][-1]["reward"]
            r_e11_03 = raw_results["E11_03"][-1]["reward"]
            r_e11_06 = raw_results["E11_06"][-1]["reward"]
            print(f"Ep {ep_idx+1:2d}/10 ({opp:7s}) | Seed {seed:4d} ({pos}) | E10-01: ${r_e10:7.1f} | E11-01: ${r_e11_01:7.1f} | E11-03: ${r_e11_03:7.1f} | E11-06: ${r_e11_06:7.1f}", flush=True)

    elapsed = time.time() - t0
    print(f"\nCompleted 30 Paired Episodes in {elapsed:.2f}s", flush=True)

    # Compute Summary Statistics
    summary = {}
    ref_rewards = [r["reward"] for r in raw_results["E10_01"]]

    for agent_name in agent_keys:
        rewards = [r["reward"] for r in raw_results[agent_name]]
        wins = sum(1 for i in range(len(rewards)) if rewards[i] > ref_rewards[i])
        metrics = compute_metrics(rewards, wins, len(rewards))

        # Architectural metrics
        quads = [r["owned_quadrants"] for r in raw_results[agent_name]]
        q2_unlocks = sum(1 for q in quads if q >= 3)
        q3_unlocks = sum(1 for q in quads if q >= 4)
        
        metrics["architectural_deployment"] = {
            "mean_quadrants": float(np.mean(quads)),
            "q2_unlock_rate_pct": float(q2_unlocks / len(quads) * 100.0),
            "q3_unlock_rate_pct": float(q3_unlocks / len(quads) * 100.0),
        }

        # Compute paired deltas vs E10-01
        paired_deltas = [rewards[i] - ref_rewards[i] for i in range(len(rewards))]
        metrics["paired_vs_e10_01"] = {
            "mean_delta": float(np.mean(paired_deltas)),
            "median_delta": float(np.median(paired_deltas)),
            "paired_wins": wins,
            "paired_win_rate_pct": float(wins / len(rewards) * 100.0),
        }

        summary[agent_name] = metrics

    # Save to JSON
    output_path = Path("experiments/archive/e11/artifacts/productive_mass.json")
    output_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "benchmark_summary": summary,
        "raw_results": raw_results
    }
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"\nSaved benchmark results to {output_path}", flush=True)

    print("\n" + "=" * 95, flush=True)
    print("   E11 REPRODUCIBILITY BENCHMARK SUMMARY TABLE", flush=True)
    print("=" * 95, flush=True)
    print(f"{'Variant':12s} | {'Mean Money':12s} | {'Median':12s} | {'Std Dev':10s} | {'Mean Q':8s} | {'Q2 Unlock%':11s} | {'Wins vs E10':12s}")
    print("-" * 95, flush=True)

    for a in agent_keys:
        m = summary[a]
        arch = m["architectural_deployment"]
        p = m["paired_vs_e10_01"]
        print(f"{a:12s} | ${m['mean_final_money']:10.2f} | ${m['median_final_money']:10.2f} | ±${m['std_dev']:8.2f} | {arch['mean_quadrants']:8.2f} | {arch['q2_unlock_rate_pct']:10.1f}% | {p['paired_wins']:2d}/30 ({p['paired_win_rate_pct']:4.1f}%)")
    print("=" * 95, flush=True)


if __name__ == "__main__":
    run_standard_30_benchmark()
