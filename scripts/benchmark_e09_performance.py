"""Benchmark execution script for E09-04 — VERIFY Livestock Subsystem Ablation.

Runs 30 paired episodes for E05, E06, E07, E08 (Livestock ON), and E09-01 (Livestock OFF) against standard opponents (10 x pass, 10 x random, 10 x starter).
Calculates paired deltas (E09-01 vs E08 primary, E09-01 vs E07 secondary), aggregate statistics, and detailed telemetry.
Saves output to results/e09_livestock_ablation.json.
"""

import sys
import os
import time
import json
import numpy as np

sys.path.insert(0, os.path.abspath("src"))

from agricola.evaluation.runner import run_episode
from agricola.strategy.hire_nw_cluster_roi import HIRENWClusterROIAgent
from agricola.strategy.water_first_hire_nw_cluster_roi import WaterFirstHIRENWClusterROIAgent
from agricola.strategy.hybrid_livestock_cluster_roi import HybridLivestockClusterROIAgent, CompetitiveConfig
from agricola.strategy.livestock_ablation_roi import LivestockAblationROIAgent
from agricola.core.state import GameState


def agent_decide(agent, gs: GameState):
    if hasattr(agent, "decide"):
        return agent.decide(gs)
    elif hasattr(agent, "act"):
        return agent.act(gs)
    raise AttributeError("Agent has neither decide nor act method")


def run_benchmark():
    opponents = ["pass", "random", "starter"]
    episodes_per_opp = 10
    total_episodes_per_agent = len(opponents) * episodes_per_opp  # 30 episodes
    
    e07_config = CompetitiveConfig(
        target_productive_tiles=24,
        wheat_tiles=6,
        melon_tiles=12,
        carrot_tiles=6
    )
    e08_config = CompetitiveConfig()  # Default E08 (40 tiles, Livestock ON)
    e09_config = CompetitiveConfig()  # Default E09 (40 tiles, Livestock OFF)
    
    agent_configs = {
        "E05": {"name": "HIRENWClusterROIAgent", "factory": lambda: HIRENWClusterROIAgent()},
        "E06": {"name": "WaterFirstHIRENWClusterROIAgent", "factory": lambda: WaterFirstHIRENWClusterROIAgent()},
        "E07": {"name": "HybridLivestockClusterROIAgent (24 tiles)", "factory": lambda: HybridLivestockClusterROIAgent(config=e07_config)},
        "E08": {"name": "HybridLivestockClusterROIAgent (40 tiles)", "factory": lambda: HybridLivestockClusterROIAgent(config=e08_config)},
        "E09_01": {"name": "LivestockAblationROIAgent (40 tiles)", "factory": lambda: LivestockAblationROIAgent(config=e09_config)}
    }
    
    raw_results = {key: [] for key in agent_configs}
    e09_telemetries = []
    
    print("=" * 85, flush=True)
    print("      E09-04 — VERIFY LIVESTOCK ABLATION BENCHMARK (30 EPISODES PER AGENT)", flush=True)
    print("=" * 85, flush=True)
    print(f"Agents: {list(agent_configs.keys())}", flush=True)
    print(f"Opponents: {opponents} ({episodes_per_opp} eps each, 5 P0 / 5 P1)", flush=True)
    print(f"Total episodes per agent: {total_episodes_per_agent}", flush=True)
    print("-" * 85, flush=True)
    
    start_bench_time = time.time()
    
    for opp in opponents:
        print(f"\n--- Benchmark vs Opponent: '{opp}' (10 episodes) ---", flush=True)
        p0_count = episodes_per_opp // 2
        
        for ep_idx in range(episodes_per_opp):
            playing_as_p0 = ep_idx < p0_count
            seed = ep_idx * 100
            
            for agent_key, cfg_info in agent_configs.items():
                agent_inst = cfg_info["factory"]()
                
                def tracked_fn(obs, config):
                    gs = GameState(obs)
                    return agent_decide(agent_inst, gs)
                
                if playing_as_p0:
                    ep_res = run_episode(tracked_fn, opp, steps=720, seed=seed, track_p0=True, track_p1=False)
                    my_reward = ep_res["p0_reward"]
                    opp_reward = ep_res["p1_reward"]
                    my_dq = ep_res["disqualified_p0"]
                    my_latency = ep_res["p0_agent_mean_latency_ms"]
                    starvation = ep_res.get("p0_starvation", {})
                    position = "P0"
                else:
                    ep_res = run_episode(opp, tracked_fn, steps=720, seed=seed, track_p0=False, track_p1=True)
                    my_reward = ep_res["p1_reward"]
                    opp_reward = ep_res["p0_reward"]
                    my_dq = ep_res["disqualified_p1"]
                    my_latency = ep_res["p1_agent_mean_latency_ms"]
                    starvation = ep_res.get("p1_starvation", {})
                    position = "P1"
                    
                record = {
                    "agent": agent_key,
                    "opponent": opp,
                    "seed": seed,
                    "position": position,
                    "episode_idx": ep_idx,
                    "global_idx": len(raw_results[agent_key]),
                    "completed": ep_res["completed"],
                    "disqualified": my_dq,
                    "reward": my_reward,
                    "opp_reward": opp_reward,
                    "win": my_reward > opp_reward,
                    "draw": my_reward == opp_reward,
                    "loss": my_reward < opp_reward,
                    "latency_ms": my_latency,
                    "weed_count": starvation.get("weed_count", 0),
                    "unwatered_end_of_day_ratio_pct": starvation.get("unwatered_end_of_day_ratio_pct", 0.0)
                }
                
                if agent_key == "E09_01" and hasattr(agent_inst, "telemetry"):
                    tel_dict = agent_inst.telemetry.to_dict()
                    record["telemetry"] = tel_dict
                    e09_telemetries.append(tel_dict)
                    
                raw_results[agent_key].append(record)
                
            e09_r = raw_results["E09_01"][-1]["reward"]
            e08_r = raw_results["E08"][-1]["reward"]
            e07_r = raw_results["E07"][-1]["reward"]
            e06_r = raw_results["E06"][-1]["reward"]
            print(f"Ep {ep_idx+1:2d} ({position} vs {opp:<7} seed={seed:3d}): E09_01=${e09_r:7.2f} | E08=${e08_r:7.2f} | E07=${e07_r:7.2f} | Delta(E09-E08)=${e09_r-e08_r:+7.2f}", flush=True)

    total_bench_duration = time.time() - start_bench_time
    print(f"\nBenchmark completed in {total_bench_duration:.2f} seconds.")
    
    # Process Summary Statistics
    summary = {}
    for agent_key in agent_configs:
        recs = raw_results[agent_key]
        rewards = [r["reward"] for r in recs]
        wins = sum(1 for r in recs if r["win"])
        draws = sum(1 for r in recs if r["draw"])
        losses = sum(1 for r in recs if r["loss"])
        completed = sum(1 for r in recs if r["completed"])
        dqs = sum(1 for r in recs if r["disqualified"])
        weeds = [r["weed_count"] for r in recs]
        latencies = [r["latency_ms"] for r in recs if r["latency_ms"] > 0]
        
        summary[agent_key] = {
            "agent_name": agent_configs[agent_key]["name"],
            "total_episodes": len(recs),
            "completed": completed,
            "completion_rate_pct": (completed / len(recs)) * 100.0,
            "disqualified": dqs,
            "disqualification_rate_pct": (dqs / len(recs)) * 100.0,
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "win_rate_pct": (wins / len(recs)) * 100.0,
            "mean_final_money": float(np.mean(rewards)),
            "std_dev_money": float(np.std(rewards, ddof=1)),
            "median_final_money": float(np.median(rewards)),
            "min_final_money": float(np.min(rewards)),
            "max_final_money": float(np.max(rewards)),
            "total_weed_count": int(sum(weeds)),
            "mean_weed_count": float(np.mean(weeds)),
            "mean_latency_ms": float(np.mean(latencies)) if latencies else 0.0,
            "opponent_breakdown": {}
        }
        
        for opp in opponents:
            opp_recs = [r for r in recs if r["opponent"] == opp]
            opp_rewards = [r["reward"] for r in opp_recs]
            opp_wins = sum(1 for r in opp_recs if r["win"])
            opp_draws = sum(1 for r in opp_recs if r["draw"])
            opp_losses = sum(1 for r in opp_recs if r["loss"])
            
            summary[agent_key]["opponent_breakdown"][opp] = {
                "n": len(opp_recs),
                "wins": opp_wins,
                "draws": opp_draws,
                "losses": opp_losses,
                "win_rate_pct": (opp_wins / len(opp_recs)) * 100.0,
                "mean_final_money": float(np.mean(opp_rewards)),
                "std_dev_money": float(np.std(opp_rewards, ddof=1)),
                "median_final_money": float(np.median(opp_rewards)),
            }

    # Deltas (E09_01 vs E08 primary, E09_01 vs E07 secondary, E09_01 vs E06)
    e09_mean = summary["E09_01"]["mean_final_money"]
    e08_mean = summary["E08"]["mean_final_money"]
    e07_mean = summary["E07"]["mean_final_money"]
    e06_mean = summary["E06"]["mean_final_money"]
    
    deltas = {
        "E09_01_vs_E08_PRIMARY": {
            "mean_money_delta": e09_mean - e08_mean,
            "mean_money_pct_delta": ((e09_mean - e08_mean) / e08_mean) * 100.0,
            "median_money_delta": summary["E09_01"]["median_final_money"] - summary["E08"]["median_final_money"],
        },
        "E09_01_vs_E07_SECONDARY": {
            "mean_money_delta": e09_mean - e07_mean,
            "mean_money_pct_delta": ((e09_mean - e07_mean) / e07_mean) * 100.0,
            "median_money_delta": summary["E09_01"]["median_final_money"] - summary["E07"]["median_final_money"],
        },
        "E09_01_vs_E06_SHIPPED": {
            "mean_money_delta": e09_mean - e06_mean,
            "mean_money_pct_delta": ((e09_mean - e06_mean) / e06_mean) * 100.0,
            "gap_to_E06": e06_mean - e09_mean,
        }
    }

    # Paired Comparisons
    paired = {}
    for compare_key, opp_agent in [("E09_01_vs_E08", "E08"), ("E09_01_vs_E07", "E07"), ("E09_01_vs_E06", "E06")]:
        e09_rewards = np.array([r["reward"] for r in raw_results["E09_01"]])
        opp_rewards = np.array([r["reward"] for r in raw_results[opp_agent]])
        paired_diffs = e09_rewards - opp_rewards
        
        better = int(np.sum(paired_diffs > 0))
        equal = int(np.sum(paired_diffs == 0))
        worse = int(np.sum(paired_diffs < 0))
        
        paired[compare_key] = {
            "better": better,
            "equal": equal,
            "worse": worse,
            "better_pct": (better / len(paired_diffs)) * 100.0,
            "mean_paired_delta": float(np.mean(paired_diffs)),
            "median_paired_delta": float(np.median(paired_diffs)),
            "std_dev_paired_delta": float(np.std(paired_diffs, ddof=1)),
        }

    # Aggregate E09_01 Telemetry Diagnostics
    e09_diagnostics = {
        "land": {
            "configured_crop_tiles": 40,
            "mean_peak_productive_tiles": float(np.mean([t["land_breakdown"]["peak_productive_tiles"] for t in e09_telemetries])),
            "mean_daily_productive_tiles": float(np.mean([t["land_breakdown"]["mean_daily_productive_tiles"] for t in e09_telemetries])),
            "mean_q0_harvested": float(np.mean([t["land_breakdown"]["q0"]["harvested"] for t in e09_telemetries])),
            "mean_q1_harvested": float(np.mean([t["land_breakdown"]["q1"]["harvested"] for t in e09_telemetries])),
            "mean_q0_worked": float(np.mean([t["land_breakdown"]["q0"]["worked"] for t in e09_telemetries])),
            "mean_q1_worked": float(np.mean([t["land_breakdown"]["q1"]["worked"] for t in e09_telemetries])),
        },
        "workforce_shares": {
            "mean_action_steps": float(np.mean([t["workforce"]["action_steps"] for t in e09_telemetries])),
            "mean_movement_steps": float(np.mean([t["workforce"]["movement_steps"] for t in e09_telemetries])),
            "mean_idle_steps": float(np.mean([t["workforce"]["idle_steps"] for t in e09_telemetries])),
            "mean_productive_share_pct": float(np.mean([t["workforce"]["action_steps"]/max(1, t["workforce"]["action_steps"]+t["workforce"]["movement_steps"]+t["workforce"]["idle_steps"])*100 for t in e09_telemetries])),
            "mean_movement_share_pct": float(np.mean([t["workforce"]["movement_steps"]/max(1, t["workforce"]["action_steps"]+t["workforce"]["movement_steps"]+t["workforce"]["idle_steps"])*100 for t in e09_telemetries])),
            "mean_idle_share_pct": float(np.mean([t["workforce"]["idle_steps"]/max(1, t["workforce"]["action_steps"]+t["workforce"]["movement_steps"]+t["workforce"]["idle_steps"])*100 for t in e09_telemetries])),
        },
        "backlog": {
            "mean_needs_water": float(np.mean([t["backlog"]["mean_needs_water"] for t in e09_telemetries])),
            "mean_harvest_ready": float(np.mean([t["backlog"]["mean_harvest_ready"] for t in e09_telemetries])),
            "mean_plant_pending": float(np.mean([t["backlog"]["mean_plant_pending"] for t in e09_telemetries])),
        },
        "capital_liquidity": {
            "mean_minimum_cash": float(np.mean([t["minimum_cash"] for t in e09_telemetries])),
            "mean_seed_spending": float(np.mean([t["spending"]["seeds"] for t in e09_telemetries])),
            "mean_melon_revenue": float(np.mean([t["realized_revenue"].get("MELON", 0.0) for t in e09_telemetries])),
        }
    }

    # Save full JSON artifact
    benchmark_payload = {
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "benchmark_duration_sec": total_bench_duration,
            "episodes_per_agent": total_episodes_per_agent,
            "opponents": opponents,
        },
        "e09_config": CompetitiveConfig().__dict__,
        "summary": summary,
        "deltas": deltas,
        "paired": paired,
        "e09_diagnostics": e09_diagnostics,
        "raw_results": raw_results
    }
    
    os.makedirs("results", exist_ok=True)
    with open("results/e09_livestock_ablation.json", "w") as f:
        json.dump(benchmark_payload, f, indent=2)
        
    print("\n" + "=" * 85)
    print("      SUMMARY OF E09-01 LOCAL PERFORMANCE BENCHMARK RESULTS")
    print("=" * 85)
    print(f"{'Agent':<8} | {'Completion':<10} | {'DQ':<5} | {'W/D/L':<10} | {'Win Rate':<9} | {'Mean Final Money':<20} | {'Median':<10}")
    print("-" * 85)
    for k in ["E05", "E06", "E07", "E08", "E09_01"]:
        s = summary[k]
        wdl = f"{s['wins']}/{s['draws']}/{s['losses']}"
        print(f"{k:<8} | {s['completion_rate_pct']:9.1f}% | {s['disqualified']:5d} | {wdl:<10} | {s['win_rate_pct']:8.1f}% | ${s['mean_final_money']:10.2f} ± ${s['std_dev_money']:6.2f} | ${s['median_final_money']:8.2f}")
    print("-" * 85)
    print(f"E09-01 vs E08 (PRIMARY) Mean Delta:   ${deltas['E09_01_vs_E08_PRIMARY']['mean_money_delta']:+9.2f} ({deltas['E09_01_vs_E08_PRIMARY']['mean_money_pct_delta']:+6.2f}%)")
    print(f"E09-01 vs E08 (PRIMARY) Paired Win:   {paired['E09_01_vs_E08']['better']}/{len(raw_results['E09_01'])} episodes ({paired['E09_01_vs_E08']['better_pct']:.1f}%)")
    print("-" * 85)
    print(f"E09-01 vs E07 (SECONDARY) Mean Delta: ${deltas['E09_01_vs_E07_SECONDARY']['mean_money_delta']:+9.2f} ({deltas['E09_01_vs_E07_SECONDARY']['mean_money_pct_delta']:+6.2f}%)")
    print(f"E09-01 vs E06 (SHIPPED) Mean Delta:   ${deltas['E09_01_vs_E06_SHIPPED']['mean_money_delta']:+9.2f} ({deltas['E09_01_vs_E06_SHIPPED']['mean_money_pct_delta']:+6.2f}%)")
    print("=" * 85)


if __name__ == "__main__":
    run_benchmark()
