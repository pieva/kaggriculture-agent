#!/usr/bin/env python3
"""MODEL_SPEC C2 Tournament Runner.

Executes the frozen 3-round pairwise tournament across the 3 pre-declared seeds:
  Round 1: Antigravity C2 (P0) vs Codex C2 (P1)
  Round 2: Antigravity C2 (P0) vs Copilot C2 (P1)
  Round 3: Codex C2 (P0) vs Copilot C2 (P1)

Seeds:
  Seed 1: 1113294977
  Seed 2: 3033283457
  Seed 3: 1678077158

Outputs full raw replays, step-level telemetry, and aggregated statistics to:
  results/model_spec_c2/tournament/
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

import kaggle_environments
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]

SEEDS = [1113294977, 3033283457, 1678077158]

CANDIDATES = {
    "antigravity": {
        "candidate_id": "ANTIGRAVITY_C2",
        "name": "Antigravity C2",
        "spec_path": "docs/model/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2.md",
        "executable_path": "src/agricola/strategy/antigravity/agent_c2.py",
        "config_path": "src/agricola/strategy/antigravity/c2_config.py",
    },
    "codex": {
        "candidate_id": "CODEX_C2",
        "name": "Codex C2",
        "spec_path": "docs/model/model_specs/codex/MODEL_SPEC_CODEX_C2.md",
        "executable_path": "src/agricola/strategy/codex_c2.py",
        "config_path": "configs/model_spec_c2/CODEX_C2_CONFIG.json",
    },
    "copilot": {
        "candidate_id": "COPILOT_C2",
        "name": "Copilot C2",
        "spec_path": "docs/model/model_specs/copilot/MODEL_SPEC_COPILOT_C2.md",
        "executable_path": "src/agricola/strategy/copilot/agent_c2.py",
        "config_path": "src/agricola/strategy/copilot/c2_config.py",
    },
}

ROUNDS = [
    {
        "round_id": "R1",
        "p0_key": "antigravity",
        "p1_key": "codex",
    },
    {
        "round_id": "R2",
        "p0_key": "antigravity",
        "p1_key": "copilot",
    },
    {
        "round_id": "R3",
        "p0_key": "codex",
        "p1_key": "copilot",
    },
]


def compute_sha256(filepath: Path | str) -> str:
    p = Path(filepath)
    if not p.is_absolute():
        p = REPO_ROOT / p
    if not p.exists():
        return "FILE_NOT_FOUND"
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def make_tournament_agent_wrapper(agent_obj: Any) -> Callable:
    """Neutral wrapper ensuring callable compatibility with Kaggle environment signatures."""
    def wrapped_agent(observation: Dict[str, Any], configuration: Any = None) -> Dict[str, Any]:
        try:
            return agent_obj(observation, configuration)
        except TypeError:
            return agent_obj(observation)
        except Exception:
            return {"farmer": ["PASS"], "hands": [], "market": []}
    return wrapped_agent


def instantiate_candidate(candidate_key: str) -> Callable:
    """Instantiate a fresh callable agent for a given candidate."""
    if candidate_key == "antigravity":
        from agricola.strategy.antigravity.agent_c2 import AntigravityC2Agent
        return make_tournament_agent_wrapper(AntigravityC2Agent())
    elif candidate_key == "codex":
        from agricola.strategy.codex_c2 import create_agent
        return make_tournament_agent_wrapper(create_agent())
    elif candidate_key == "copilot":
        from agricola.strategy.copilot.agent_c2 import CopilotC2Agent
        return make_tournament_agent_wrapper(CopilotC2Agent())
    else:
        raise ValueError(f"Unknown candidate key: {candidate_key}")


def extract_telemetry(env: Any, p0_name: str, p1_name: str) -> Dict[str, Any]:
    """Extract step-by-step and aggregate telemetry from completed episode."""
    steps = env.steps
    telemetry: Dict[str, Any] = {
        "p0": {
            "name": p0_name,
            "actions": {"WATER": 0, "PLANT": 0, "HARVEST": 0, "CARE": 0, "FEED": 0, "COLLECT_FERTILIZER": 0, "DIG": 0, "BUILD_PASTURE": 0, "MOVE": 0, "PASS": 0, "OTHER": 0},
            "market_orders": {"BUY_LAND": 0, "HIRE": 0, "BUY_SEED": 0, "BUY_PRODUCT": 0, "BUY_ANIMAL": 0, "SELL": 0},
            "money_trajectory": [],
            "active_surface_trajectory": [],
            "harvest_ready_trajectory": [],
            "weed_count_trajectory": [],
            "final_money": 0.0,
            "crop_target_attainment": 0.0,
            "mean_active_surface": 0.0,
            "max_active_surface": 0,
            "total_water_actions": 0,
            "total_harvest_actions": 0,
            "total_plant_actions": 0,
            "total_dig_actions": 0,
            "total_move_actions": 0,
            "total_pass_actions": 0,
            "total_market_orders": 0,
        },
        "p1": {
            "name": p1_name,
            "actions": {"WATER": 0, "PLANT": 0, "HARVEST": 0, "CARE": 0, "FEED": 0, "COLLECT_FERTILIZER": 0, "DIG": 0, "BUILD_PASTURE": 0, "MOVE": 0, "PASS": 0, "OTHER": 0},
            "market_orders": {"BUY_LAND": 0, "HIRE": 0, "BUY_SEED": 0, "BUY_PRODUCT": 0, "BUY_ANIMAL": 0, "SELL": 0},
            "money_trajectory": [],
            "active_surface_trajectory": [],
            "harvest_ready_trajectory": [],
            "weed_count_trajectory": [],
            "final_money": 0.0,
            "crop_target_attainment": 0.0,
            "mean_active_surface": 0.0,
            "max_active_surface": 0,
            "total_water_actions": 0,
            "total_harvest_actions": 0,
            "total_plant_actions": 0,
            "total_dig_actions": 0,
            "total_move_actions": 0,
            "total_pass_actions": 0,
            "total_market_orders": 0,
        },
    }

    moves = {"NORTH", "SOUTH", "EAST", "WEST"}

    for step_idx, step_data in enumerate(steps):
        for p_idx, p_key in [(0, "p0"), (1, "p1")]:
            agent_step = step_data[p_idx]
            action = agent_step.get("action", {}) or {}
            farmer_act = action.get("farmer", ["PASS"]) if isinstance(action, dict) else ["PASS"]
            hands_acts = action.get("hands", []) if isinstance(action, dict) else []
            market_acts = action.get("market", []) if isinstance(action, dict) else []

            all_unit_acts = [farmer_act] + (hands_acts if isinstance(hands_acts, list) else [])
            for u_act in all_unit_acts:
                if isinstance(u_act, list) and u_act:
                    op = str(u_act[0]).upper()
                    if op in moves:
                        telemetry[p_key]["actions"]["MOVE"] += 1
                    elif op in telemetry[p_key]["actions"]:
                        telemetry[p_key]["actions"][op] += 1
                    else:
                        telemetry[p_key]["actions"]["OTHER"] += 1

            if isinstance(market_acts, list):
                for m_act in market_acts:
                    if isinstance(m_act, list) and m_act:
                        m_op = str(m_act[0]).upper()
                        if m_op in telemetry[p_key]["market_orders"]:
                            telemetry[p_key]["market_orders"][m_op] += 1

            obs = agent_step.get("observation", {}) or {}
            farms = obs.get("farms", [])
            if farms and len(farms) > p_idx:
                farm = farms[p_idx]
                money = float(farm.get("money", 0.0))
                telemetry[p_key]["money_trajectory"].append(money)

                # Tile statistics
                tiles = farm.get("tiles", [])
                active_plants = 0
                harvest_ready = 0
                weeds = 0
                day = int(obs.get("day", 0))
                for row in tiles:
                    for tile in row:
                        if isinstance(tile, dict):
                            k = tile.get("kind")
                            if k == "PLANT":
                                active_plants += 1
                                if int(tile.get("yield_units", 0) or 0) > 0:
                                    planted_day = int(tile.get("planted_day", 0) or 0)
                                    crop_name = str(tile.get("crop", "WHEAT")).upper()
                                    # Wheat: 2/3, Strawberry: 5/10, Melon: 8/10
                                    first_yield = 3 if crop_name == "WHEAT" else (5 if crop_name == "STRAWBERRY" else 8)
                                    if (day - planted_day) >= first_yield:
                                        harvest_ready += 1
                            elif k == "WEED":
                                weeds += 1

                telemetry[p_key]["active_surface_trajectory"].append(active_plants)
                telemetry[p_key]["harvest_ready_trajectory"].append(harvest_ready)
                telemetry[p_key]["weed_count_trajectory"].append(weeds)

    # Compute aggregate metrics
    for p_key in ["p0", "p1"]:
        t = telemetry[p_key]
        t["final_money"] = t["money_trajectory"][-1] if t["money_trajectory"] else 0.0
        t["mean_active_surface"] = float(np.mean(t["active_surface_trajectory"])) if t["active_surface_trajectory"] else 0.0
        t["max_active_surface"] = int(np.max(t["active_surface_trajectory"])) if t["active_surface_trajectory"] else 0
        t["crop_target_attainment"] = min(1.0, t["mean_active_surface"] / 17.0)
        t["total_water_actions"] = t["actions"]["WATER"]
        t["total_harvest_actions"] = t["actions"]["HARVEST"]
        t["total_plant_actions"] = t["actions"]["PLANT"]
        t["total_dig_actions"] = t["actions"]["DIG"]
        t["total_move_actions"] = t["actions"]["MOVE"]
        t["total_pass_actions"] = t["actions"]["PASS"]
        t["total_market_orders"] = sum(t["market_orders"].values())

    return telemetry


def run_single_match(
    round_id: str,
    p0_key: str,
    p1_key: str,
    seed: int,
    output_dir: Path,
) -> Dict[str, Any]:
    """Execute a single tournament match."""
    p0_info = CANDIDATES[p0_key]
    p1_info = CANDIDATES[p1_key]

    match_id = f"{round_id}_{p0_key}_vs_{p1_key}_S{seed}"
    print(f"\n========================================================")
    print(f"Executing: {match_id}")
    print(f"  P0: {p0_info['name']} ({p0_info['executable_path']})")
    print(f"  P1: {p1_info['name']} ({p1_info['executable_path']})")
    print(f"  Seed: {seed}")
    print(f"========================================================")

    agent_p0 = instantiate_candidate(p0_key)
    agent_p1 = instantiate_candidate(p1_key)

    t0 = time.time()
    env = kaggle_environments.make("kaggriculture", configuration={"seed": seed, "episodeSteps": 720}, debug=True)
    env.run([agent_p0, agent_p1])
    elapsed = time.time() - t0

    final_step = env.steps[-1]
    p0_reward = float(final_step[0].get("reward", 0.0) or 0.0)
    p1_reward = float(final_step[1].get("reward", 0.0) or 0.0)
    p0_status = final_step[0].get("status", "DONE")
    p1_status = final_step[1].get("status", "DONE")

    if p0_reward > p1_reward:
        winner = p0_info["name"]
    elif p1_reward > p0_reward:
        winner = p1_info["name"]
    else:
        winner = "TIE"

    print(f"Completed in {elapsed:.2f}s | Steps: {len(env.steps)}")
    print(f"  {p0_info['name']} (P0): ${p0_reward:,.2f} ({p0_status})")
    print(f"  {p1_info['name']} (P1): ${p1_reward:,.2f} ({p1_status})")
    print(f"  Winner: {winner} (Delta: ${abs(p0_reward - p1_reward):,.2f})")

    telemetry = extract_telemetry(env, p0_info["name"], p1_info["name"])

    result_data = {
        "match_id": match_id,
        "round_id": round_id,
        "seed": seed,
        "p0": {
            "key": p0_key,
            "name": p0_info["name"],
            "sha256": compute_sha256(p0_info["executable_path"]),
            "spec_sha256": compute_sha256(p0_info["spec_path"]),
            "status": p0_status,
            "final_money": p0_reward,
            "telemetry": telemetry["p0"],
        },
        "p1": {
            "key": p1_key,
            "name": p1_info["name"],
            "sha256": compute_sha256(p1_info["executable_path"]),
            "spec_sha256": compute_sha256(p1_info["spec_path"]),
            "status": p1_status,
            "final_money": p1_reward,
            "telemetry": telemetry["p1"],
        },
        "winner": winner,
        "money_delta": p0_reward - p1_reward,
        "elapsed_seconds": elapsed,
        "total_steps": len(env.steps),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }

    # Save individual match artifacts
    match_dir = output_dir / "raw" / match_id
    match_dir.mkdir(parents=True, exist_ok=True)
    (match_dir / "summary.json").write_text(json.dumps(result_data, indent=2), encoding="utf-8")
    (match_dir / "replay.json").write_text(json.dumps(env.toJSON(), indent=2), encoding="utf-8")

    return result_data


def run_tournament(validate_only: bool = False, output_dir: Path | None = None) -> None:
    output_dir = output_dir or REPO_ROOT / "results" / "model_spec_c2" / "tournament"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=== MODEL_SPEC TOURNAMENT C2 PRE-FLIGHT INTEGRITY ===")
    for key, c in CANDIDATES.items():
        exec_sha = compute_sha256(c["executable_path"])
        spec_sha = compute_sha256(c["spec_path"])
        cfg_sha = compute_sha256(c["config_path"])
        print(f"[{key.upper()}] {c['name']}")
        print(f"  Executable: {c['executable_path']} (SHA: {exec_sha[:16]}...)")
        print(f"  Spec:       {c['spec_path']} (SHA: {spec_sha[:16]}...)")
        print(f"  Config:     {c['config_path']} (SHA: {cfg_sha[:16]}...)")

    if validate_only:
        print("\nPre-flight validation complete. No matches run.")
        return

    all_results = []
    for r in ROUNDS:
        for seed in SEEDS:
            res = run_single_match(
                round_id=r["round_id"],
                p0_key=r["p0_key"],
                p1_key=r["p1_key"],
                seed=seed,
                output_dir=output_dir,
            )
            all_results.append(res)

    # Aggregation per candidate
    agg: Dict[str, Dict[str, Any]] = {
        "antigravity": {"name": "Antigravity C2", "matches": 0, "wins": 0, "losses": 0, "ties": 0, "money_scores": [], "water_actions": [], "harvest_actions": [], "plant_actions": [], "dig_actions": [], "market_orders": [], "mean_active_surfaces": []},
        "codex": {"name": "Codex C2", "matches": 0, "wins": 0, "losses": 0, "ties": 0, "money_scores": [], "water_actions": [], "harvest_actions": [], "plant_actions": [], "dig_actions": [], "market_orders": [], "mean_active_surfaces": []},
        "copilot": {"name": "Copilot C2", "matches": 0, "wins": 0, "losses": 0, "ties": 0, "money_scores": [], "water_actions": [], "harvest_actions": [], "plant_actions": [], "dig_actions": [], "market_orders": [], "mean_active_surfaces": []},
    }

    for res in all_results:
        p0_k = res["p0"]["key"]
        p1_k = res["p1"]["key"]
        p0_m = res["p0"]["final_money"]
        p1_m = res["p1"]["final_money"]
        p0_t = res["p0"]["telemetry"]
        p1_t = res["p1"]["telemetry"]

        agg[p0_k]["matches"] += 1
        agg[p0_k]["money_scores"].append(p0_m)
        agg[p0_k]["water_actions"].append(p0_t["total_water_actions"])
        agg[p0_k]["harvest_actions"].append(p0_t["total_harvest_actions"])
        agg[p0_k]["plant_actions"].append(p0_t["total_plant_actions"])
        agg[p0_k]["dig_actions"].append(p0_t["total_dig_actions"])
        agg[p0_k]["market_orders"].append(p0_t["total_market_orders"])
        agg[p0_k]["mean_active_surfaces"].append(p0_t["mean_active_surface"])

        agg[p1_k]["matches"] += 1
        agg[p1_k]["money_scores"].append(p1_m)
        agg[p1_k]["water_actions"].append(p1_t["total_water_actions"])
        agg[p1_k]["harvest_actions"].append(p1_t["total_harvest_actions"])
        agg[p1_k]["plant_actions"].append(p1_t["total_plant_actions"])
        agg[p1_k]["dig_actions"].append(p1_t["total_dig_actions"])
        agg[p1_k]["market_orders"].append(p1_t["total_market_orders"])
        agg[p1_k]["mean_active_surfaces"].append(p1_t["mean_active_surface"])

        if p0_m > p1_m:
            agg[p0_k]["wins"] += 1
            agg[p1_k]["losses"] += 1
        elif p1_m > p0_m:
            agg[p1_k]["wins"] += 1
            agg[p0_k]["losses"] += 1
        else:
            agg[p0_k]["ties"] += 1
            agg[p1_k]["ties"] += 1

    summary_stats = {}
    for k, d in agg.items():
        scores = np.array(d["money_scores"])
        summary_stats[k] = {
            "name": d["name"],
            "matches_played": d["matches"],
            "record": f"{d['wins']}W - {d['losses']}L - {d['ties']}T",
            "mean_money": float(np.mean(scores)),
            "median_money": float(np.median(scores)),
            "std_money": float(np.std(scores, ddof=1)) if len(scores) > 1 else 0.0,
            "min_money": float(np.min(scores)),
            "max_money": float(np.max(scores)),
            "mean_water_actions": float(np.mean(d["water_actions"])),
            "mean_harvest_actions": float(np.mean(d["harvest_actions"])),
            "mean_plant_actions": float(np.mean(d["plant_actions"])),
            "mean_dig_actions": float(np.mean(d["dig_actions"])),
            "mean_market_orders": float(np.mean(d["market_orders"])),
            "mean_active_surface": float(np.mean(d["mean_active_surfaces"])),
        }

    tournament_payload = {
        "protocol": "MODEL_SPEC_TOURNAMENT_C2_FROZEN_V1",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "seeds": SEEDS,
        "rounds": ROUNDS,
        "summary_statistics": summary_stats,
        "match_results": all_results,
    }

    (output_dir / "aggregated_results.json").write_text(json.dumps(tournament_payload, indent=2), encoding="utf-8")

    # CSV Summary
    csv_lines = ["candidate,matches,wins,losses,ties,mean_money,median_money,std_money,min_money,max_money,mean_active_surface,mean_water,mean_harvest,mean_plant,mean_dig,mean_market"]
    for k, s in summary_stats.items():
        csv_lines.append(
            f"{s['name']},{s['matches_played']},{agg[k]['wins']},{agg[k]['losses']},{agg[k]['ties']},"
            f"{s['mean_money']:.2f},{s['median_money']:.2f},{s['std_money']:.2f},{s['min_money']:.2f},{s['max_money']:.2f},"
            f"{s['mean_active_surface']:.2f},{s['mean_water_actions']:.1f},{s['mean_harvest_actions']:.1f},{s['mean_plant_actions']:.1f},{s['mean_dig_actions']:.1f},{s['mean_market_orders']:.1f}"
        )
    (output_dir / "aggregated_results.csv").write_text("\n".join(csv_lines), encoding="utf-8")

    print("\n========================================================")
    print("TOURNAMENT COMPLETE — AGGREGATED SUMMARY")
    print("========================================================")
    print(f"{'Candidate':<16} {'Record':<12} {'Mean $':<12} {'Median $':<12} {'Std $':<10} {'Min $':<10} {'Max $':<10} {'Active Surf':<12}")
    print("-" * 96)
    for k, s in summary_stats.items():
        print(f"{s['name']:<16} {s['record']:<12} {s['mean_money']:<12.2f} {s['median_money']:<12.2f} {s['std_money']:<10.2f} {s['min_money']:<10.2f} {s['max_money']:<10.2f} {s['mean_active_surface']:<12.2f}")
    print("========================================================")


def main():
    parser = argparse.ArgumentParser(description="Run MODEL_SPEC Tournament C2")
    parser.add_argument("--validate", action="store_true", help="Validate setup without running matches")
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory for neutral tournament artifacts (defaults to the original tournament path)",
    )
    args = parser.parse_args()
    run_tournament(validate_only=args.validate, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
