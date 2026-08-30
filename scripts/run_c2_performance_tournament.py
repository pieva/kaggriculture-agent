#!/usr/bin/env python3
"""MODEL_SPEC C2 Performance Tournament Runner.

Executes the 9 frozen tournament matches on the 3 primary seeds:
  Primary Seeds: [1838889274, 1619968655, 710418712]

  Round 1: Antigravity C2 (P0) vs Codex C2 V4 (P1)
  Round 2: Antigravity C2 (P0) vs Copilot C2 (P1)
  Round 3: Codex C2 V4 (P0) vs Copilot C2 (P1)

Outputs full raw replays, step-level telemetry, aggregated results (JSON, CSV),
and generates summary statistics to:
  results/model_spec_c2/performance_tournament/
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

PRIMARY_SEEDS = [1838889274, 1619968655, 710418712]

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
        "name": "Codex C2 V4",
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
    def wrapped_agent(observation: Dict[str, Any], configuration: Any = None) -> Dict[str, Any]:
        try:
            return agent_obj(observation, configuration)
        except TypeError:
            return agent_obj(observation)
        except Exception:
            return {"farmer": ["PASS"], "hands": [], "market": []}
    return wrapped_agent


def instantiate_candidate(candidate_key: str) -> Callable:
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


def extract_detailed_telemetry(env: Any, p0_name: str, p1_name: str) -> Dict[str, Any]:
    steps = env.steps
    telemetry: Dict[str, Any] = {
        "p0": {
            "name": p0_name,
            "actions": {"WATER": 0, "PLANT": 0, "HARVEST": 0, "CARE": 0, "FEED": 0, "COLLECT_FERTILIZER": 0, "DIG": 0, "BUILD_PASTURE": 0, "MOVE": 0, "PASS": 0, "DROP": 0, "OTHER": 0},
            "market_orders": {"BUY_LAND": 0, "HIRE": 0, "BUY_SEED": 0, "BUY_PRODUCT": 0, "BUY_ANIMAL": 0, "SELL": 0},
            "money_trajectory": [],
            "active_surface_trajectory": [],
            "harvest_ready_trajectory": [],
            "weed_count_trajectory": [],
            "wheat_harvest_yields": [],
            "strawberry_harvest_yields": [],
            "melon_harvest_yields": [],
            "first_revenue_step": None,
            "min_money": 3000.0,
            "final_money": 0.0,
            "max_active_surface": 0,
            "mean_active_surface": 0.0,
            "final_active_surface": 0,
            "total_water_actions": 0,
            "total_harvest_actions": 0,
            "total_plant_actions": 0,
            "total_dig_actions": 0,
            "total_move_actions": 0,
            "total_pass_actions": 0,
            "total_drop_actions": 0,
            "total_market_orders": 0,
            "total_sold_value": 0.0,
            "daily_watering_compliance_pct": 100.0,
        },
        "p1": {
            "name": p1_name,
            "actions": {"WATER": 0, "PLANT": 0, "HARVEST": 0, "CARE": 0, "FEED": 0, "COLLECT_FERTILIZER": 0, "DIG": 0, "BUILD_PASTURE": 0, "MOVE": 0, "PASS": 0, "DROP": 0, "OTHER": 0},
            "market_orders": {"BUY_LAND": 0, "HIRE": 0, "BUY_SEED": 0, "BUY_PRODUCT": 0, "BUY_ANIMAL": 0, "SELL": 0},
            "money_trajectory": [],
            "active_surface_trajectory": [],
            "harvest_ready_trajectory": [],
            "weed_count_trajectory": [],
            "wheat_harvest_yields": [],
            "strawberry_harvest_yields": [],
            "melon_harvest_yields": [],
            "first_revenue_step": None,
            "min_money": 3000.0,
            "final_money": 0.0,
            "max_active_surface": 0,
            "mean_active_surface": 0.0,
            "final_active_surface": 0,
            "total_water_actions": 0,
            "total_harvest_actions": 0,
            "total_plant_actions": 0,
            "total_dig_actions": 0,
            "total_move_actions": 0,
            "total_pass_actions": 0,
            "total_drop_actions": 0,
            "total_market_orders": 0,
            "total_sold_value": 0.0,
            "daily_watering_compliance_pct": 100.0,
        },
    }

    p0_initial_money = 3000.0
    p1_initial_money = 3000.0
    p0_prev_money = 3000.0
    p1_prev_money = 3000.0

    p0_unwatered_days_count = 0
    p1_unwatered_days_count = 0
    total_days_evaluated = 0

    for step_idx, step_state in enumerate(steps):
        p0_state = step_state[0]
        p1_state = step_state[1]

        obs = p0_state.get("observation", {})
        farms = obs.get("farms", [])

        # Player 0 metrics
        if len(farms) > 0:
            f0 = farms[0]
            m0 = float(f0.get("money", 0.0))
            telemetry["p0"]["money_trajectory"].append(m0)
            if m0 < telemetry["p0"]["min_money"]:
                telemetry["p0"]["min_money"] = m0

            # Check first revenue step
            if telemetry["p0"]["first_revenue_step"] is None and m0 > p0_prev_money and step_idx > 0:
                telemetry["p0"]["first_revenue_step"] = step_idx
            p0_prev_money = m0

            # Tiles analysis
            tiles0 = f0.get("tiles", [])
            active_cnt0 = 0
            weed_cnt0 = 0
            hr_cnt0 = 0
            unwatered_today0 = 0

            for row in tiles0:
                for t in row:
                    if isinstance(t, dict):
                        kind = t.get("kind")
                        if kind == "PLANT":
                            active_cnt0 += 1
                            if int(t.get("yield_units", 0)) > 0:
                                hr_cnt0 += 1
                            if not t.get("watered_today", False):
                                unwatered_today0 += 1
                        elif kind == "WEED":
                            weed_cnt0 += 1

            telemetry["p0"]["active_surface_trajectory"].append(active_cnt0)
            telemetry["p0"]["weed_count_trajectory"].append(weed_cnt0)
            telemetry["p0"]["harvest_ready_trajectory"].append(hr_cnt0)

            # EOD check (step % 24 == 23)
            if step_idx % 24 == 23 and active_cnt0 > 0:
                if unwatered_today0 > 0:
                    p0_unwatered_days_count += 1
                total_days_evaluated += 1

        # Player 1 metrics
        if len(farms) > 1:
            f1 = farms[1]
            m1 = float(f1.get("money", 0.0))
            telemetry["p1"]["money_trajectory"].append(m1)
            if m1 < telemetry["p1"]["min_money"]:
                telemetry["p1"]["min_money"] = m1

            if telemetry["p1"]["first_revenue_step"] is None and m1 > p1_prev_money and step_idx > 0:
                telemetry["p1"]["first_revenue_step"] = step_idx
            p1_prev_money = m1

            tiles1 = f1.get("tiles", [])
            active_cnt1 = 0
            weed_cnt1 = 0
            hr_cnt1 = 0
            unwatered_today1 = 0

            for row in tiles1:
                for t in row:
                    if isinstance(t, dict):
                        kind = t.get("kind")
                        if kind == "PLANT":
                            active_cnt1 += 1
                            if int(t.get("yield_units", 0)) > 0:
                                hr_cnt1 += 1
                            if not t.get("watered_today", False):
                                unwatered_today1 += 1
                        elif kind == "WEED":
                            weed_cnt1 += 1

            telemetry["p1"]["active_surface_trajectory"].append(active_cnt1)
            telemetry["p1"]["weed_count_trajectory"].append(weed_cnt1)
            telemetry["p1"]["harvest_ready_trajectory"].append(hr_cnt1)

            if step_idx % 24 == 23 and active_cnt1 > 0:
                if unwatered_today1 > 0:
                    p1_unwatered_days_count += 1

        # Track actions dispatched
        act0 = p0_state.get("action", {})
        if isinstance(act0, dict):
            for unit_act in [act0.get("farmer", [])] + act0.get("hands", []):
                if unit_act and isinstance(unit_act, list):
                    cmd = unit_act[0]
                    if cmd in telemetry["p0"]["actions"]:
                        telemetry["p0"]["actions"][cmd] += 1
                    elif cmd in ["NORTH", "SOUTH", "EAST", "WEST"]:
                        telemetry["p0"]["actions"]["MOVE"] += 1
                    else:
                        telemetry["p0"]["actions"]["OTHER"] += 1
            for m_ord in act0.get("market", []):
                if m_ord and isinstance(m_ord, list):
                    m_cmd = m_ord[0]
                    if m_cmd in telemetry["p0"]["market_orders"]:
                        telemetry["p0"]["market_orders"][m_cmd] += 1

        act1 = p1_state.get("action", {})
        if isinstance(act1, dict):
            for unit_act in [act1.get("farmer", [])] + act1.get("hands", []):
                if unit_act and isinstance(unit_act, list):
                    cmd = unit_act[0]
                    if cmd in telemetry["p1"]["actions"]:
                        telemetry["p1"]["actions"][cmd] += 1
                    elif cmd in ["NORTH", "SOUTH", "EAST", "WEST"]:
                        telemetry["p1"]["actions"]["MOVE"] += 1
                    else:
                        telemetry["p1"]["actions"]["OTHER"] += 1
            for m_ord in act1.get("market", []):
                if m_ord and isinstance(m_ord, list):
                    m_cmd = m_ord[0]
                    if m_cmd in telemetry["p1"]["market_orders"]:
                        telemetry["p1"]["market_orders"][m_cmd] += 1

    # Finalize aggregates
    for p_key in ["p0", "p1"]:
        t = telemetry[p_key]
        t["total_water_actions"] = t["actions"]["WATER"]
        t["total_harvest_actions"] = t["actions"]["HARVEST"]
        t["total_plant_actions"] = t["actions"]["PLANT"]
        t["total_dig_actions"] = t["actions"]["DIG"]
        t["total_move_actions"] = t["actions"]["MOVE"]
        t["total_pass_actions"] = t["actions"]["PASS"]
        t["total_drop_actions"] = t["actions"]["DROP"]
        t["total_market_orders"] = sum(t["market_orders"].values())
        if t["active_surface_trajectory"]:
            t["max_active_surface"] = int(max(t["active_surface_trajectory"]))
            t["mean_active_surface"] = float(np.mean(t["active_surface_trajectory"]))
            t["final_active_surface"] = int(t["active_surface_trajectory"][-1])
        if t["money_trajectory"]:
            t["final_money"] = float(t["money_trajectory"][-1])

    if total_days_evaluated > 0:
        telemetry["p0"]["daily_watering_compliance_pct"] = max(0.0, 100.0 * (1.0 - p0_unwatered_days_count / (total_days_evaluated / 2 if total_days_evaluated else 1)))
        telemetry["p1"]["daily_watering_compliance_pct"] = max(0.0, 100.0 * (1.0 - p1_unwatered_days_count / (total_days_evaluated / 2 if total_days_evaluated else 1)))

    return telemetry


def run_single_match(
    round_id: str,
    p0_key: str,
    p1_key: str,
    seed: int,
    output_dir: Path,
) -> Dict[str, Any]:
    match_id = f"{round_id}_{p0_key}_vs_{p1_key}_s{seed}"
    print(f"\n========================================================")
    print(f"RUNNING MATCH: {match_id}")
    print(f"  P0 (Seat 0): {CANDIDATES[p0_key]['name']} ({p0_key})")
    print(f"  P1 (Seat 1): {CANDIDATES[p1_key]['name']} ({p1_key})")
    print(f"  Primary Seed: {seed}")
    print(f"========================================================")

    agent_p0 = instantiate_candidate(p0_key)
    agent_p1 = instantiate_candidate(p1_key)

    env = kaggle_environments.make("kaggriculture", configuration={"seed": seed, "episodeSteps": 720})

    t0 = time.time()
    env.run([agent_p0, agent_p1])
    elapsed = time.time() - t0

    p0_state = env.state[0]
    p1_state = env.state[1]

    p0_reward = float(p0_state.reward if p0_state.reward is not None else 0.0)
    p1_reward = float(p1_state.reward if p1_state.reward is not None else 0.0)
    p0_status = p0_state.status
    p1_status = p1_state.status

    if p0_reward > p1_reward:
        winner = CANDIDATES[p0_key]["name"]
    elif p1_reward > p0_reward:
        winner = CANDIDATES[p1_key]["name"]
    else:
        winner = "TIE"

    print(f"Completed in {elapsed:.2f}s | Steps: {len(env.steps)}")
    print(f"  {CANDIDATES[p0_key]['name']} (P0): ${p0_reward:,.2f} ({p0_status})")
    print(f"  {CANDIDATES[p1_key]['name']} (P1): ${p1_reward:,.2f} ({p1_status})")
    print(f"  Winner: {winner} (Delta: ${abs(p0_reward - p1_reward):,.2f})")

    telemetry = extract_detailed_telemetry(env, CANDIDATES[p0_key]["name"], CANDIDATES[p1_key]["name"])

    result_data = {
        "match_id": match_id,
        "round_id": round_id,
        "seed": seed,
        "p0": {
            "key": p0_key,
            "name": CANDIDATES[p0_key]["name"],
            "sha256": compute_sha256(CANDIDATES[p0_key]["executable_path"]),
            "spec_sha256": compute_sha256(CANDIDATES[p0_key]["spec_path"]),
            "status": p0_status,
            "final_money": p0_reward,
            "telemetry": telemetry["p0"],
        },
        "p1": {
            "key": p1_key,
            "name": CANDIDATES[p1_key]["name"],
            "sha256": compute_sha256(CANDIDATES[p1_key]["executable_path"]),
            "spec_sha256": compute_sha256(CANDIDATES[p1_key]["spec_path"]),
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


def run_tournament(validate_only: bool = False, output_dir: Path | None = None) -> Dict[str, Any]:
    output_dir = output_dir or REPO_ROOT / "results" / "model_spec_c2" / "performance_tournament"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=== MODEL_SPEC TOURNAMENT C2 PERFORMANCE ITERATION: PRE-FLIGHT INTEGRITY ===")
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
        return {}

    all_results = []
    for r in ROUNDS:
        for seed in PRIMARY_SEEDS:
            res = run_single_match(
                round_id=r["round_id"],
                p0_key=r["p0_key"],
                p1_key=r["p1_key"],
                seed=seed,
                output_dir=output_dir,
            )
            all_results.append(res)

    # Aggregation per candidate across their 6 matches
    agg: Dict[str, Dict[str, Any]] = {
        "antigravity": {
            "name": "Antigravity C2",
            "matches": 0,
            "wins": 0,
            "losses": 0,
            "ties": 0,
            "money_scores": [],
            "water_actions": [],
            "harvest_actions": [],
            "plant_actions": [],
            "dig_actions": [],
            "move_actions": [],
            "pass_actions": [],
            "market_orders": [],
            "mean_active_surfaces": [],
            "max_active_surfaces": [],
            "first_revenue_steps": [],
            "min_moneys": [],
        },
        "codex": {
            "name": "Codex C2 V4",
            "matches": 0,
            "wins": 0,
            "losses": 0,
            "ties": 0,
            "money_scores": [],
            "water_actions": [],
            "harvest_actions": [],
            "plant_actions": [],
            "dig_actions": [],
            "move_actions": [],
            "pass_actions": [],
            "market_orders": [],
            "mean_active_surfaces": [],
            "max_active_surfaces": [],
            "first_revenue_steps": [],
            "min_moneys": [],
        },
        "copilot": {
            "name": "Copilot C2",
            "matches": 0,
            "wins": 0,
            "losses": 0,
            "ties": 0,
            "money_scores": [],
            "water_actions": [],
            "harvest_actions": [],
            "plant_actions": [],
            "dig_actions": [],
            "move_actions": [],
            "pass_actions": [],
            "market_orders": [],
            "mean_active_surfaces": [],
            "max_active_surfaces": [],
            "first_revenue_steps": [],
            "min_moneys": [],
        },
    }

    for res in all_results:
        p0_k = res["p0"]["key"]
        p1_k = res["p1"]["key"]
        p0_m = res["p0"]["final_money"]
        p1_m = res["p1"]["final_money"]
        p0_t = res["p0"]["telemetry"]
        p1_t = res["p1"]["telemetry"]

        # P0 stats
        agg[p0_k]["matches"] += 1
        agg[p0_k]["money_scores"].append(p0_m)
        agg[p0_k]["water_actions"].append(p0_t["total_water_actions"])
        agg[p0_k]["harvest_actions"].append(p0_t["total_harvest_actions"])
        agg[p0_k]["plant_actions"].append(p0_t["total_plant_actions"])
        agg[p0_k]["dig_actions"].append(p0_t["total_dig_actions"])
        agg[p0_k]["move_actions"].append(p0_t["total_move_actions"])
        agg[p0_k]["pass_actions"].append(p0_t["total_pass_actions"])
        agg[p0_k]["market_orders"].append(p0_t["total_market_orders"])
        agg[p0_k]["mean_active_surfaces"].append(p0_t["mean_active_surface"])
        agg[p0_k]["max_active_surfaces"].append(p0_t["max_active_surface"])
        if p0_t["first_revenue_step"] is not None:
            agg[p0_k]["first_revenue_steps"].append(p0_t["first_revenue_step"])
        agg[p0_k]["min_moneys"].append(p0_t["min_money"])

        # P1 stats
        agg[p1_k]["matches"] += 1
        agg[p1_k]["money_scores"].append(p1_m)
        agg[p1_k]["water_actions"].append(p1_t["total_water_actions"])
        agg[p1_k]["harvest_actions"].append(p1_t["total_harvest_actions"])
        agg[p1_k]["plant_actions"].append(p1_t["total_plant_actions"])
        agg[p1_k]["dig_actions"].append(p1_t["total_dig_actions"])
        agg[p1_k]["move_actions"].append(p1_t["total_move_actions"])
        agg[p1_k]["pass_actions"].append(p1_t["total_pass_actions"])
        agg[p1_k]["market_orders"].append(p1_t["total_market_orders"])
        agg[p1_k]["mean_active_surfaces"].append(p1_t["mean_active_surface"])
        agg[p1_k]["max_active_surfaces"].append(p1_t["max_active_surface"])
        if p1_t["first_revenue_step"] is not None:
            agg[p1_k]["first_revenue_steps"].append(p1_t["first_revenue_step"])
        agg[p1_k]["min_moneys"].append(p1_t["min_money"])

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
            "mean_active_surface": float(np.mean(d["mean_active_surfaces"])),
            "max_active_surface": int(max(d["max_active_surfaces"])) if d["max_active_surfaces"] else 0,
            "mean_first_revenue_step": float(np.mean(d["first_revenue_steps"])) if d["first_revenue_steps"] else None,
            "mean_water_actions": float(np.mean(d["water_actions"])),
            "mean_harvest_actions": float(np.mean(d["harvest_actions"])),
            "mean_plant_actions": float(np.mean(d["plant_actions"])),
            "mean_dig_actions": float(np.mean(d["dig_actions"])),
            "mean_move_actions": float(np.mean(d["move_actions"])),
            "mean_pass_actions": float(np.mean(d["pass_actions"])),
            "mean_market_orders": float(np.mean(d["market_orders"])),
            "mean_min_money": float(np.mean(d["min_moneys"])),
        }

    tournament_payload = {
        "protocol": "MODEL_SPEC_TOURNAMENT_C2_PERFORMANCE_ITERATION_FROZEN",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "primary_seeds": PRIMARY_SEEDS,
        "rounds": ROUNDS,
        "summary_statistics": summary_stats,
        "match_results": all_results,
    }

    (output_dir / "aggregated_results.json").write_text(json.dumps(tournament_payload, indent=2), encoding="utf-8")

    # CSV Summary
    csv_lines = ["candidate,matches,wins,losses,ties,mean_money,median_money,std_money,min_money,max_money,mean_active_surface,max_active_surface,mean_water,mean_harvest,mean_plant,mean_dig,mean_move,mean_pass,mean_market,mean_first_rev_step"]
    for k, s in summary_stats.items():
        csv_lines.append(
            f"{s['name']},{s['matches_played']},{agg[k]['wins']},{agg[k]['losses']},{agg[k]['ties']},"
            f"{s['mean_money']:.2f},{s['median_money']:.2f},{s['std_money']:.2f},{s['min_money']:.2f},{s['max_money']:.2f},"
            f"{s['mean_active_surface']:.2f},{s['max_active_surface']},{s['mean_water_actions']:.1f},{s['mean_harvest_actions']:.1f},{s['mean_plant_actions']:.1f},{s['mean_dig_actions']:.1f},{s['mean_move_actions']:.1f},{s['mean_pass_actions']:.1f},{s['mean_market_orders']:.1f},{s['mean_first_revenue_step']}"
        )
    (output_dir / "aggregated_results.csv").write_text("\n".join(csv_lines), encoding="utf-8")

    print("\n=========================================================================================================")
    print("C2 PERFORMANCE TOURNAMENT COMPLETE — AGGREGATED SUMMARY")
    print("=========================================================================================================")
    print(f"{'Candidate':<18} {'Record':<12} {'Mean $':<12} {'Median $':<12} {'Std $':<10} {'Min $':<10} {'Max $':<10} {'Act Surf':<10} {'First Rev':<10}")
    print("-" * 105)
    for k, s in summary_stats.items():
        rev_str = f"{s['mean_first_revenue_step']:.1f}" if s['mean_first_revenue_step'] is not None else "N/A"
        print(f"{s['name']:<18} {s['record']:<12} {s['mean_money']:<12.2f} {s['median_money']:<12.2f} {s['std_money']:<10.2f} {s['min_money']:<10.2f} {s['max_money']:<10.2f} {s['mean_active_surface']:<10.2f} {rev_str:<10}")
    print("=========================================================================================================")

    return tournament_payload


def main():
    parser = argparse.ArgumentParser(description="Run MODEL_SPEC Tournament C2 Performance Iteration")
    parser.add_argument("--validate", action="store_true", help="Validate setup without running matches")
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory for neutral tournament artifacts",
    )
    args = parser.parse_args()
    run_tournament(validate_only=args.validate, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
