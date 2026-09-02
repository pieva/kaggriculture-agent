"""Benchmark execution script for E07-08 — VERIFY Local Performance.

Runs 30 paired episodes for E05, E06, and E07 against standard opponents (10 x pass, 10 x random, 10 x starter).
Calculates aggregate statistics, paired deltas, opponent breakdowns, and detailed E07 economic diagnostics.
Saves output to experiments/archive/e07/artifacts/competitive_baseline.json.
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
    total_episodes_per_agent = len(opponents) * episodes_per_opp # 30 episodes
    
    agent_configs = {
        "E05": {"name": "HIRENWClusterROIAgent", "factory": lambda: HIRENWClusterROIAgent()},
        "E06": {"name": "WaterFirstHIRENWClusterROIAgent", "factory": lambda: WaterFirstHIRENWClusterROIAgent()},
        "E07": {"name": "HybridLivestockClusterROIAgent", "factory": lambda: HybridLivestockClusterROIAgent()}
    }
    
    # Structure to hold results per agent
    raw_results = {key: [] for key in agent_configs}
    e07_telemetries = []
    
    print("=" * 80, flush=True)
    print("      E07-08 — VERIFY LOCAL PERFORMANCE BENCHMARK (30 EPISODES PER AGENT)", flush=True)
    print("=" * 80, flush=True)
    print(f"Agents: {list(agent_configs.keys())}", flush=True)
    print(f"Opponents: {opponents} ({episodes_per_opp} eps each, 5 P0 / 5 P1)", flush=True)
    print(f"Total episodes per agent: {total_episodes_per_agent}", flush=True)
    print("-" * 80, flush=True)
    
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
                
                if agent_key == "E07" and hasattr(agent_inst, "telemetry"):
                    tel_dict = agent_inst.telemetry.to_dict()
                    record["telemetry"] = tel_dict
                    e07_telemetries.append(tel_dict)
                    
                raw_results[agent_key].append(record)
                
            e07_r = raw_results["E07"][-1]["reward"]
            e06_r = raw_results["E06"][-1]["reward"]
            e05_r = raw_results["E05"][-1]["reward"]
            print(f"Ep {ep_idx+1:2d} ({position} vs {opp:<7} seed={seed:3d}): E07=${e07_r:7.2f} | E06=${e06_r:7.2f} | E05=${e05_r:7.2f} | Delta(E07-E06)=${e07_r-e06_r:+7.2f}", flush=True)

    total_bench_duration = time.time() - start_bench_time
    print(f"\nBenchmark completed in {total_bench_duration:.2f} seconds.")
    
    # Process Summary Statistics for each agent
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
        
        # Opponent Breakdown
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

    # Deltas
    deltas = {
        "E07_vs_E06": {
            "mean_money_delta": summary["E07"]["mean_final_money"] - summary["E06"]["mean_final_money"],
            "mean_money_pct_delta": ((summary["E07"]["mean_final_money"] - summary["E06"]["mean_final_money"]) / summary["E06"]["mean_final_money"]) * 100.0,
            "median_money_delta": summary["E07"]["median_final_money"] - summary["E06"]["median_final_money"],
            "median_money_pct_delta": ((summary["E07"]["median_final_money"] - summary["E06"]["median_final_money"]) / summary["E06"]["median_final_money"]) * 100.0,
            "win_rate_delta_pct": summary["E07"]["win_rate_pct"] - summary["E06"]["win_rate_pct"],
        },
        "E07_vs_E05": {
            "mean_money_delta": summary["E07"]["mean_final_money"] - summary["E05"]["mean_final_money"],
            "mean_money_pct_delta": ((summary["E07"]["mean_final_money"] - summary["E05"]["mean_final_money"]) / summary["E05"]["mean_final_money"]) * 100.0,
            "median_money_delta": summary["E07"]["median_final_money"] - summary["E05"]["median_final_money"],
            "median_money_pct_delta": ((summary["E07"]["median_final_money"] - summary["E05"]["median_final_money"]) / summary["E05"]["median_final_money"]) * 100.0,
            "win_rate_delta_pct": summary["E07"]["win_rate_pct"] - summary["E05"]["win_rate_pct"],
        }
    }

    # Paired Comparisons (E07 vs E06, E07 vs E05)
    paired = {}
    for compare_key, opp_agent in [("E07_vs_E06", "E06"), ("E07_vs_E05", "E05")]:
        e07_rewards = np.array([r["reward"] for r in raw_results["E07"]])
        opp_rewards = np.array([r["reward"] for r in raw_results[opp_agent]])
        paired_diffs = e07_rewards - opp_rewards
        
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

    # Aggregate E07 Diagnostics from Telemetry
    e07_diagnostics = {
        "land": {
            "buy_land_executed_count": sum(1 for t in e07_telemetries if t["land_breakdown"]["buy_land_step"] is not None),
            "mean_buy_land_step": float(np.mean([t["land_breakdown"]["buy_land_step"] for t in e07_telemetries if t["land_breakdown"]["buy_land_step"] is not None])) if any(t["land_breakdown"]["buy_land_step"] is not None for t in e07_telemetries) else 0.0,
            "mean_q1_harvests": float(np.mean([t["land_breakdown"]["q1"]["harvested"] for t in e07_telemetries])),
            "mean_q1_worked": float(np.mean([t["land_breakdown"]["q1"]["worked"] for t in e07_telemetries])),
        },
        "workforce": {
            "mean_hire_attempted": float(np.mean([t["workforce"]["hire_attempted"] for t in e07_telemetries])),
            "mean_hire_accepted": float(np.mean([t["workforce"]["hire_accepted"] for t in e07_telemetries])),
            "mean_hire_spending": float(np.mean([t["spending"]["workforce"] for t in e07_telemetries])),
            "mean_peak_workers": float(np.mean([t["workforce"]["peak_simultaneous_workers"] for t in e07_telemetries])),
        },
        "crops": {
            "mean_wheat_harvested": float(np.mean([t["wheat_accounting"]["harvested"] for t in e07_telemetries])),
            "mean_wheat_bought": float(np.mean([t["wheat_accounting"]["bought"] for t in e07_telemetries])),
            "mean_wheat_fed": float(np.mean([t["wheat_accounting"]["fed"] for t in e07_telemetries])),
            "mean_wheat_sold": float(np.mean([t["wheat_accounting"]["sold"] for t in e07_telemetries])),
            "mean_melon_sold": float(np.mean([t["market"]["quantities_sold"].get("MELON", 0) for t in e07_telemetries])),
            "mean_carrot_sold": float(np.mean([t["market"]["quantities_sold"].get("CARROT", 0) for t in e07_telemetries])),
            "mean_melon_revenue": float(np.mean([t["realized_revenue"].get("MELON", 0.0) for t in e07_telemetries])),
            "mean_carrot_revenue": float(np.mean([t["realized_revenue"].get("CARROT", 0.0) for t in e07_telemetries])),
            "mean_wheat_revenue": float(np.mean([t["realized_revenue"].get("WHEAT", 0.0) for t in e07_telemetries])),
        },
        "livestock": {
            "mean_cows_purchased": float(np.mean([t["livestock"]["cows"] for t in e07_telemetries])),
            "mean_sheep_purchased": float(np.mean([t["livestock"]["sheep"] for t in e07_telemetries])),
            "mean_pastures_built": float(np.mean([t["livestock"]["pastures_built"] for t in e07_telemetries])),
            "mean_animals_placed": float(np.mean([t["livestock"]["animals_placed"] for t in e07_telemetries])),
            "mean_feed_attempted": float(np.mean([t["livestock"]["feed_attempted"] for t in e07_telemetries])),
            "mean_feed_successful": float(np.mean([t["livestock"]["feed_successful"] for t in e07_telemetries])),
            "mean_wheat_consumed": float(np.mean([t["livestock"]["feed_consumed"] for t in e07_telemetries])),
            "mean_milk_harvested": float(np.mean([t["livestock"]["milk_harvested"] for t in e07_telemetries])),
            "mean_milk_sold": float(np.mean([t["market"]["quantities_sold"].get("MILK", 0) for t in e07_telemetries])),
            "mean_milk_revenue": float(np.mean([t["realized_revenue"].get("MILK", 0.0) for t in e07_telemetries])),
            "mean_wool_sold": float(np.mean([t["market"]["quantities_sold"].get("WOOL", 0) for t in e07_telemetries])),
            "mean_wool_revenue": float(np.mean([t["realized_revenue"].get("WOOL", 0.0) for t in e07_telemetries])),
            "mean_livestock_spending": float(np.mean([t["spending"]["livestock"] for t in e07_telemetries])),
        },
        "capital_deployment": {
            "mean_seed_spending": float(np.mean([t["spending"]["seeds"] for t in e07_telemetries])),
            "mean_workforce_spending": float(np.mean([t["spending"]["workforce"] for t in e07_telemetries])),
            "mean_land_spending": float(np.mean([t["spending"]["land"] for t in e07_telemetries])),
            "mean_livestock_spending": float(np.mean([t["spending"]["livestock"] for t in e07_telemetries])),
            "mean_total_investment": float(np.mean([t["spending"]["seeds"] + t["spending"]["workforce"] + t["spending"]["land"] + t["spending"]["livestock"] for t in e07_telemetries])),
            "mean_minimum_cash": float(np.mean([t["minimum_cash"] for t in e07_telemetries])),
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
        "frozen_e07_config": CompetitiveConfig().__dict__,
        "summary": summary,
        "deltas": deltas,
        "paired": paired,
        "e07_diagnostics": e07_diagnostics,
        "raw_results": raw_results
    }
    
    os.makedirs("results", exist_ok=True)
    with open("experiments/archive/e07/artifacts/competitive_baseline.json", "w") as f:
        json.dump(benchmark_payload, f, indent=2)
        
    print("\n" + "=" * 80)
    print("      SUMMARY OF LOCAL PERFORMANCE BENCHMARK RESULTS")
    print("=" * 80)
    print(f"{'Agent':<6} | {'Completion':<10} | {'DQ':<5} | {'W/D/L':<10} | {'Win Rate':<9} | {'Mean Final Money':<20} | {'Median':<10}")
    print("-" * 80)
    for k in ["E05", "E06", "E07"]:
        s = summary[k]
        wdl = f"{s['wins']}/{s['draws']}/{s['losses']}"
        print(f"{k:<6} | {s['completion_rate_pct']:9.1f}% | {s['disqualified']:5d} | {wdl:<10} | {s['win_rate_pct']:8.1f}% | ${s['mean_final_money']:10.2f} ± ${s['std_dev_money']:6.2f} | ${s['median_final_money']:8.2f}")
    print("-" * 80)
    print(f"E07 vs E06 Mean Delta:   ${deltas['E07_vs_E06']['mean_money_delta']:+9.2f} ({deltas['E07_vs_E06']['mean_money_pct_delta']:+6.2f}%)")
    print(f"E07 vs E06 Median Delta: ${deltas['E07_vs_E06']['median_money_delta']:+9.2f} ({deltas['E07_vs_E06']['median_money_pct_delta']:+6.2f}%)")
    print(f"E07 vs E06 Paired Win:   {paired['E07_vs_E06']['better']}/{len(raw_results['E07'])} episodes ({paired['E07_vs_E06']['better_pct']:.1f}%)")
    print("-" * 80)
    print(f"E07 vs E05 Mean Delta:   ${deltas['E07_vs_E05']['mean_money_delta']:+9.2f} ({deltas['E07_vs_E05']['mean_money_pct_delta']:+6.2f}%)")
    print(f"E07 vs E05 Median Delta: ${deltas['E07_vs_E05']['median_money_delta']:+9.2f} ({deltas['E07_vs_E05']['median_money_pct_delta']:+6.2f}%)")
    print(f"E07 vs E05 Paired Win:   {paired['E07_vs_E05']['better']}/{len(raw_results['E07'])} episodes ({paired['E07_vs_E05']['better_pct']:.1f}%)")

if __name__ == "__main__":
    run_benchmark()
