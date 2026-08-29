"""Benchmark Runner Script for E10-01 Q1 Expansion Capital Protection.

Executes:
1. Standard 30-episode paired benchmark (E05, E06, E07, E08, E09-01, E10-01) -> results/e10_q1_capital_protection.json
2. Overnight 300-episode paired benchmark (E09-01 vs E10-01) -> results/e10_q1_capital_protection_overnight.json
"""

import sys
import json
import time
from pathlib import Path
import numpy as np
import kaggle_environments

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agricola.core.state import GameState
from agricola.strategy.water_first_hire_nw_cluster_roi import WaterFirstHIRENWClusterROIAgent
from agricola.strategy.hire_nw_cluster_roi import HIRENWClusterROIAgent
from agricola.strategy.hybrid_livestock_cluster_roi import HybridLivestockClusterROIAgent
from agricola.strategy.livestock_ablation_roi import LivestockAblationROIAgent
from agricola.strategy.q1_capital_protected_roi import Q1CapitalProtectedROIAgent


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
    else:
        raise ValueError(f"Unknown agent name: {name}")


def run_episode(agent_name: str, seed: int, opponent: str, position: str = "P0") -> dict:
    factory = get_agent_factory(agent_name)
    instance = factory()

    def agent_fn(obs, config):
        try:
            state = GameState(obs)
            return instance.act(state) if hasattr(instance, 'act') else instance.decide(state)
        except Exception:
            return {"farmer": ["PASS"], "hands": [], "market": []}

    env = kaggle_environments.make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed})

    if position == "P0":
        agents = [agent_fn, opponent]
        our_idx = 0
    else:
        agents = [opponent, agent_fn]
        our_idx = 1

    env.reset()
    env.run(agents)

    step_res = env.steps[-1]
    our_res = step_res[our_idx]
    reward = float(our_res["reward"]) if our_res["reward"] is not None else 0.0
    status = our_res["status"]

    weed_count = 0
    final_obs = step_res[0]["observation"]
    farms = final_obs.get("farms", [])
    if farms and len(farms) > our_idx:
        our_farm = farms[our_idx]
        tiles = our_farm.get("tiles", [])
        for row in tiles:
            for tile in row:
                if isinstance(tile, dict) and tile.get("kind") == "WEED":
                    weed_count += 1

    tel_dict = instance.telemetry.to_dict() if hasattr(instance, "telemetry") else {}

    return {
        "agent": agent_name,
        "seed": seed,
        "opponent": opponent,
        "position": position,
        "reward": reward,
        "status": status,
        "weed_count": weed_count,
        "telemetry": tel_dict
    }


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
        "coefficient_of_variation": float(np.std(arr, ddof=1) / np.mean(arr)) if np.mean(arr) > 0 else 0.0,
        "win_rate": float(wins_count / total * 100.0)
    }


def run_standard_30_benchmark():
    print("=" * 80)
    print("      RUNNING E10 STANDARD 30-EPISODE PAIRED BENCHMARK")
    print("=" * 80)

    episodes_spec = []
    # 10 vs pass
    for i in range(10):
        episodes_spec.append((100 * i, "pass", "P0" if i % 2 == 0 else "P1"))
    # 10 vs random
    for i in range(10):
        episodes_spec.append((100 * i, "random", "P0" if i % 2 == 0 else "P1"))
    # 10 vs starter
    for i in range(10):
        episodes_spec.append((100 * i, "starter", "P0" if i % 2 == 0 else "P1"))

    agents = ["E05", "E06", "E07", "E08", "E09_01", "E10_01"]
    raw_results = {a: [] for a in agents}

    t0 = time.time()
    for ep_idx, (seed, opp, pos) in enumerate(episodes_spec):
        print(f"[{ep_idx+1:02d}/30] Seed {seed:4d} | Opponent: {opp:<7} | Pos: {pos}")
        for agent_name in agents:
            res = run_episode(agent_name, seed, opp, pos)
            raw_results[agent_name].append(res)
            print(f"   -> {agent_name:<7}: Money = ${res['reward']:9.2f} | Status = {res['status']}")

    elapsed = time.time() - t0
    print(f"\nStandard 30-Episode Benchmark completed in {elapsed:.2f}s.")

    # Calculate summaries
    summaries = {}
    for a in agents:
        rewards = [r["reward"] for r in raw_results[a]]
        wins = sum(1 for r in raw_results[a] if r["status"] == "DONE" and r["reward"] > 0)
        summaries[a] = compute_metrics(rewards, wins, len(rewards))

    # Paired Deltas E10 vs E09-01
    e09_rewards = [r["reward"] for r in raw_results["E09_01"]]
    e10_rewards = [r["reward"] for r in raw_results["E10_01"]]
    paired_deltas = [e10_rewards[i] - e09_rewards[i] for i in range(30)]

    paired_summary = {
        "mean_paired_delta": float(np.mean(paired_deltas)),
        "median_paired_delta": float(np.median(paired_deltas)),
        "paired_wins": int(sum(1 for d in paired_deltas if d > 0)),
        "paired_ties": int(sum(1 for d in paired_deltas if d == 0)),
        "paired_losses": int(sum(1 for d in paired_deltas if d < 0)),
        "win_rate_vs_e09": float(sum(1 for d in paired_deltas if d > 0) / 30.0 * 100.0)
    }

    dataset = {
        "experiment": "E10 Standard 30-Episode Benchmark",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "elapsed_seconds": round(elapsed, 2),
        "summaries": summaries,
        "paired_e10_vs_e09": paired_summary,
        "raw_results": raw_results
    }

    out_file = Path("results/e10_q1_capital_protection.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)

    print(f"Saved standard benchmark dataset to: {out_file}")
    return dataset


def run_overnight_300_benchmark():
    print("=" * 80)
    print("      RUNNING E10 OVERNIGHT 300-EPISODE PAIRED BENCHMARK (E09-01 vs E10-01)")
    print("=" * 80)

    episodes_spec = []
    # 100 vs pass (seeds 1000..1099)
    for i in range(100):
        episodes_spec.append((1000 + i, "pass", "P0" if i % 2 == 0 else "P1"))
    # 100 vs random (seeds 2000..2099)
    for i in range(100):
        episodes_spec.append((2000 + i, "random", "P0" if i % 2 == 0 else "P1"))
    # 100 vs starter (seeds 3000..3099)
    for i in range(100):
        episodes_spec.append((3000 + i, "starter", "P0" if i % 2 == 0 else "P1"))

    agents = ["E09_01", "E10_01"]
    raw_results = {a: [] for a in agents}

    t0 = time.time()
    for ep_idx, (seed, opp, pos) in enumerate(episodes_spec):
        if (ep_idx + 1) % 10 == 0 or ep_idx == 0:
            print(f"[{ep_idx+1:03d}/300] Seed {seed:4d} | Opponent: {opp:<7} | Pos: {pos}")
        for agent_name in agents:
            res = run_episode(agent_name, seed, opp, pos)
            raw_results[agent_name].append(res)

    elapsed = time.time() - t0
    print(f"\nOvernight 300-Episode Benchmark completed in {elapsed:.2f}s.")

    summaries = {}
    for a in agents:
        rewards = [r["reward"] for r in raw_results[a]]
        wins = sum(1 for r in raw_results[a] if r["status"] == "DONE" and r["reward"] > 0)
        summaries[a] = compute_metrics(rewards, wins, len(rewards))

    e09_rewards = [r["reward"] for r in raw_results["E09_01"]]
    e10_rewards = [r["reward"] for r in raw_results["E10_01"]]
    paired_deltas = [e10_rewards[i] - e09_rewards[i] for i in range(300)]

    paired_summary = {
        "mean_paired_delta": float(np.mean(paired_deltas)),
        "median_paired_delta": float(np.median(paired_deltas)),
        "paired_wins": int(sum(1 for d in paired_deltas if d > 0)),
        "paired_ties": int(sum(1 for d in paired_deltas if d == 0)),
        "paired_losses": int(sum(1 for d in paired_deltas if d < 0)),
        "win_rate_vs_e09": float(sum(1 for d in paired_deltas if d > 0) / 300.0 * 100.0)
    }

    # Audit Worst Episodes for E10-01
    worst_e10_indices = np.argsort(e10_rewards)[:10]
    worst_episodes_audit = []
    for idx in worst_e10_indices:
        r09 = raw_results["E09_01"][idx]
        r10 = raw_results["E10_01"][idx]
        worst_episodes_audit.append({
            "idx": int(idx),
            "seed": r10["seed"],
            "opponent": r10["opponent"],
            "position": r10["position"],
            "e09_money": r09["reward"],
            "e10_money": r10["reward"],
            "delta": r10["reward"] - r09["reward"],
            "e10_buy_land_step": r10["telemetry"]["land_breakdown"]["buy_land_step"],
            "e10_seed_spending": r10["telemetry"]["spending"]["seeds"],
            "e10_melon_revenue": r10["telemetry"]["realized_revenue"].get("MELON", 0.0)
        })

    dataset = {
        "experiment": "E10 Overnight 300-Episode Paired Benchmark",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "elapsed_seconds": round(elapsed, 2),
        "summaries": summaries,
        "paired_e10_vs_e09": paired_summary,
        "worst_10_episodes_audit": worst_episodes_audit,
        "raw_results": raw_results
    }

    out_file = Path("results/e10_q1_capital_protection_overnight.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)

    print(f"Saved overnight benchmark dataset to: {out_file}")
    return dataset


if __name__ == "__main__":
    run_standard_30_benchmark()

