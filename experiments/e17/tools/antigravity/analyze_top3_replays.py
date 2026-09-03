#!/usr/bin/env python3
"""Forensic quantitative analysis script for E17 Top 3 benchmark replays.

Agent owner: Antigravity (AGENT_ID = antigravity)
Environment: Kaggriculture (kaggle-environments 1.32.7, kaggriculture 0.1.0)
Target replays: 9 episodes from data/replays/json/
Outputs:
- experiments/e17/artifacts/discovery/antigravity/E17_TOP3_REPLAY_METRICS.json
- experiments/e17/reports/antigravity/E17_TOP3_REPLAY_ANALYSIS.md
"""

from __future__ import annotations

import collections
import copy
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

BENCHMARK_REPLAYS = [
    "data/replays/json/104527555.json",
    "data/replays/json/104541810.json",
    "data/replays/json/104543983.json",
    "data/replays/json/104547425.json",
    "data/replays/json/104564762.json",
    "data/replays/json/104577270.json",
    "data/replays/json/104578185.json",
    "data/replays/json/104586335.json",
    "data/replays/json/104586487.json",
]

MOVE_OPS = {"NORTH", "SOUTH", "EAST", "WEST"}
PRODUCTIVE_OPS = {
    "PLANT", "WATER", "HARVEST", "DIG", "BUILD_COOP", "BUILD_PASTURE",
    "FEED", "CARE", "COLLECT_FERTILIZER", "FERTILIZE"
}
HANDLING_OPS = {"PICKUP", "PLACE", "DROP"}

QUAD_NAME_TO_ID = {"NW": 0, "NE": 1, "SW": 2, "SE": 3}
QUAD_ID_TO_NAME = {0: "Q0_NW", 1: "Q1_NE", 2: "Q2_SW", 3: "Q3_SE"}

def get_quadrant_id(x: int, y: int) -> int:
    """Return quadrant index 0 (NW), 1 (NE), 2 (SW), 3 (SE)."""
    if x < 5 and y < 5:
        return 0
    elif x >= 5 and y < 5:
        return 1
    elif x < 5 and y >= 5:
        return 2
    else:
        return 3

def compute_sha256(filepath: str) -> str:
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def analyze_episode(filepath: str) -> Dict[str, Any]:
    file_sha = compute_sha256(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    info = data.get("info", {})
    ep_id = info.get("EpisodeId")
    team_names = info.get("TeamNames", ["Unknown_P0", "Unknown_P1"])
    seed = info.get("seed")
    steps = data.get("steps", [])
    num_steps = len(steps)
    module_ver = data.get("module_version", "unknown")
    statuses = [steps[-1][p].get("status", "unknown") for p in (0, 1)]
    final_rewards = [float(steps[-1][p].get("reward", 0.0)) for p in (0, 1)]

    # Analysis per player
    players_data = {}
    for p in (0, 1):
        agent_name = team_names[p]

        # Tracking variables
        daily_metrics = [] # day 0 to 29

        # Overall accumulators
        action_op_counts = collections.Counter()
        market_order_counts = collections.Counter()

        crop_planted_counts = collections.Counter()
        crop_harvested_counts = collections.Counter()
        animal_purchased_counts = collections.Counter()
        structure_built_counts = collections.Counter()

        fertilizer_applied = 0
        fertilizer_collected = 0
        feed_actions = 0
        care_actions = 0
        water_actions = 0
        harvest_actions = 0
        dig_actions = 0

        # Spatial & Routing
        total_moves = 0
        total_passes = 0
        total_productive = 0
        total_handling = 0

        # Quadrant unlocks
        q_unlock_step = {"Q0_NW": 0, "Q1_NE": None, "Q2_SW": None, "Q3_SE": None}
        q_unlock_day = {"Q0_NW": 0, "Q1_NE": None, "Q2_SW": None, "Q3_SE": None}

        # Animal escape tracking
        prev_animals_count = 0
        animal_escapes_detected = 0

        # Track daily snapshots
        for d in range(30):
            day_steps = range(d * 24, (d + 1) * 24)
            start_step = d * 24
            end_step = (d + 1) * 24 - 1

            # Start and End observation
            obs_start = steps[start_step][p]["observation"]
            obs_end = steps[end_step][p]["observation"]

            farm_start = obs_start["farms"][p]
            farm_end = obs_end["farms"][p]

            money_start = float(farm_start.get("money", 0.0))
            money_end = float(farm_end.get("money", 0.0))
            money_delta = money_end - money_start

            # Unlocked quadrants at end of day
            raw_unlocked = farm_end.get("unlocked_quadrants", ["NW"])
            unlocked_quad_ids = []
            for item in raw_unlocked:
                if isinstance(item, str) and item in QUAD_NAME_TO_ID:
                    qid = QUAD_NAME_TO_ID[item]
                    qname = QUAD_ID_TO_NAME[qid]
                elif isinstance(item, int):
                    qid = item
                    qname = QUAD_ID_TO_NAME[qid]
                else:
                    continue
                unlocked_quad_ids.append(qid)
                if q_unlock_step[qname] is None:
                    # Search exact step in this day
                    for st in day_steps:
                        uq_st = steps[st][p]["observation"]["farms"][p].get("unlocked_quadrants", [])
                        uq_set = {QUAD_NAME_TO_ID.get(x, x) for x in uq_st}
                        if qid in uq_set:
                            q_unlock_step[qname] = st
                            q_unlock_day[qname] = d
                            break

            # Farm hands hired today
            hands_counts_in_day = [len(steps[st][p]["observation"]["farms"][p].get("hands", [])) for st in day_steps]
            max_hands_today = max(hands_counts_in_day) if hands_counts_in_day else 0
            hires_today = farm_end.get("hires_today", 0)

            # Tile state at end of day
            tiles = farm_end.get("tiles", [])

            active_crops = collections.Counter()
            active_animals = collections.Counter()
            active_structures = collections.Counter()
            quad_tile_usage = {"Q0_NW": 0, "Q1_NE": 0, "Q2_SW": 0, "Q3_SE": 0}
            quad_crops = {"Q0_NW": 0, "Q1_NE": 0, "Q2_SW": 0, "Q3_SE": 0}
            quad_animals = {"Q0_NW": 0, "Q1_NE": 0, "Q2_SW": 0, "Q3_SE": 0}
            quad_weeds = {"Q0_NW": 0, "Q1_NE": 0, "Q2_SW": 0, "Q3_SE": 0}
            weed_count = 0
            empty_unlocked_tiles = 0
            unwatered_crops_at_eod = 0
            unfed_animals_at_eod = 0

            for y in range(len(tiles)):
                for x in range(len(tiles[y])):
                    tile = tiles[y][x]
                    qid = get_quadrant_id(x, y)
                    qname = QUAD_ID_TO_NAME[qid]
                    if tile is None:
                        if qid in unlocked_quad_ids:
                            empty_unlocked_tiles += 1
                    elif isinstance(tile, dict):
                        kind = tile.get("kind")
                        if kind == "PLANT":
                            crop_type = tile.get("crop")
                            active_crops[crop_type] += 1
                            quad_crops[qname] += 1
                            quad_tile_usage[qname] += 1
                            if not tile.get("watered_today", False):
                                unwatered_crops_at_eod += 1
                        elif kind in ("COOP", "PASTURE"):
                            active_structures[kind] += 1
                            animal = tile.get("animal")
                            if animal:
                                active_animals[animal] += 1
                                quad_animals[qname] += 1
                                quad_tile_usage[qname] += 1
                                if not tile.get("fed_today", False):
                                    unfed_animals_at_eod += 1
                        elif kind == "WEED":
                            weed_count += 1
                            quad_weeds[qname] += 1

            cur_animals_total = sum(active_animals.values())
            if d > 0 and cur_animals_total < prev_animals_count:
                animal_escapes_detected += (prev_animals_count - cur_animals_total)
            prev_animals_count = cur_animals_total

            # Inventory at end of day
            private_end = obs_end.get("private", {})
            shed_inv = private_end.get("shed", {})
            seeds_inv = private_end.get("seeds", {})
            worker_invs = private_end.get("inventories", [])
            total_shed_items = sum(shed_inv.values())
            total_worker_items = sum(sum(w.values()) for w in worker_invs)

            # Actions in this day
            day_action_ops = collections.Counter()
            day_market_ops = collections.Counter()
            day_moves = 0
            day_passes = 0
            day_prod = 0
            day_handling = 0

            for st in day_steps:
                st_data = steps[st][p]
                act = st_data.get("action", {})
                if not act:
                    continue

                # Farmer action
                farmer_act = act.get("farmer", [])
                if farmer_act:
                    op = farmer_act[0]
                    day_action_ops[op] += 1
                    action_op_counts[op] += 1
                    if op in MOVE_OPS:
                        day_moves += 1
                        total_moves += 1
                    elif op == "PASS":
                        day_passes += 1
                        total_passes += 1
                    elif op in PRODUCTIVE_OPS:
                        day_prod += 1
                        total_productive += 1
                    elif op in HANDLING_OPS:
                        day_handling += 1
                        total_handling += 1

                    if op == "PLANT" and len(farmer_act) > 1:
                        crop_planted_counts[farmer_act[1]] += 1
                    elif op == "BUILD_COOP":
                        structure_built_counts["COOP"] += 1
                    elif op == "BUILD_PASTURE":
                        structure_built_counts["PASTURE"] += 1
                    elif op == "FERTILIZE":
                        fertilizer_applied += 1
                    elif op == "COLLECT_FERTILIZER":
                        fertilizer_collected += 1
                    elif op == "FEED":
                        feed_actions += 1
                    elif op == "CARE":
                        care_actions += 1
                    elif op == "WATER":
                        water_actions += 1
                    elif op == "HARVEST":
                        harvest_actions += 1
                    elif op == "DIG":
                        dig_actions += 1

                # Hands actions
                for hand_act in act.get("hands", []):
                    if not hand_act:
                        continue
                    op = hand_act[0]
                    day_action_ops[op] += 1
                    action_op_counts[op] += 1
                    if op in MOVE_OPS:
                        day_moves += 1
                        total_moves += 1
                    elif op == "PASS":
                        day_passes += 1
                        total_passes += 1
                    elif op in PRODUCTIVE_OPS:
                        day_prod += 1
                        total_productive += 1
                    elif op in HANDLING_OPS:
                        day_handling += 1
                        total_handling += 1

                    if op == "PLANT" and len(hand_act) > 1:
                        crop_planted_counts[hand_act[1]] += 1
                    elif op == "BUILD_COOP":
                        structure_built_counts["COOP"] += 1
                    elif op == "BUILD_PASTURE":
                        structure_built_counts["PASTURE"] += 1
                    elif op == "FERTILIZE":
                        fertilizer_applied += 1
                    elif op == "COLLECT_FERTILIZER":
                        fertilizer_collected += 1
                    elif op == "FEED":
                        feed_actions += 1
                    elif op == "CARE":
                        care_actions += 1
                    elif op == "WATER":
                        water_actions += 1
                    elif op == "HARVEST":
                        harvest_actions += 1
                    elif op == "DIG":
                        dig_actions += 1

                # Market actions
                for m_ord in act.get("market", []):
                    if not m_ord:
                        continue
                    m_op = m_ord[0]
                    day_market_ops[m_op] += 1
                    market_order_counts[m_op] += 1

                    if m_op == "BUY_ANIMAL" and len(m_ord) > 1:
                        animal_purchased_counts[m_ord[1]] += (m_ord[2] if len(m_ord) > 2 else 1)

            daily_metrics.append({
                "day": d,
                "money_start": money_start,
                "money_end": money_end,
                "money_delta": money_delta,
                "unlocked_quadrants": copy.deepcopy(raw_unlocked),
                "num_unlocked_quadrants": len(unlocked_quad_ids),
                "max_hands": max_hands_today,
                "hires_today": hires_today,
                "active_crops": dict(active_crops),
                "total_crops": sum(active_crops.values()),
                "active_animals": dict(active_animals),
                "total_animals": sum(active_animals.values()),
                "active_structures": dict(active_structures),
                "total_structures": sum(active_structures.values()),
                "quad_tile_usage": quad_tile_usage,
                "quad_crops": quad_crops,
                "quad_animals": quad_animals,
                "quad_weeds": quad_weeds,
                "weed_count": weed_count,
                "empty_unlocked_tiles": empty_unlocked_tiles,
                "unwatered_crops_at_eod": unwatered_crops_at_eod,
                "unfed_animals_at_eod": unfed_animals_at_eod,
                "shed_items_total": total_shed_items,
                "shed_inventory": dict(shed_inv),
                "seeds_inventory": dict(seeds_inv),
                "worker_items_total": total_worker_items,
                "day_moves": day_moves,
                "day_passes": day_passes,
                "day_productive": day_prod,
                "day_handling": day_handling,
                "day_action_ops": dict(day_action_ops),
                "day_market_ops": dict(day_market_ops),
            })

        # Endgame & liquidation analysis (Days 27..29, steps 648..719)
        endgame_sells = collections.Counter()
        endgame_sells_by_day = {27: collections.Counter(), 28: collections.Counter(), 29: collections.Counter()}
        for st in range(648, 720):
            d = st // 24
            act = steps[st][p].get("action", {})
            for m_ord in act.get("market", []):
                if m_ord and m_ord[0] == "SELL":
                    item = m_ord[1] if len(m_ord) > 1 else "UNKNOWN"
                    qty = m_ord[2] if len(m_ord) > 2 else 1
                    endgame_sells[item] += qty
                    if d in endgame_sells_by_day:
                        endgame_sells_by_day[d][item] += qty

        terminal_obs = steps[-1][p]["observation"]
        terminal_farm = terminal_obs["farms"][p]
        terminal_tiles = terminal_farm["tiles"]
        terminal_private = terminal_obs.get("private", {})
        terminal_shed = terminal_private.get("shed", {})
        terminal_seeds = terminal_private.get("seeds", {})
        terminal_worker_invs = terminal_private.get("inventories", [])

        # Granular terminal quadrant tile breakdown
        terminal_quadrants = {}
        for q_target in ["Q0_NW", "Q1_NE", "Q2_SW"]:
            terminal_quadrants[q_target] = {
                "empty_uncultivated": 0,
                "weeds": 0,
                "total_uncultivated": 0,
                "crops": {},
                "total_crops": 0,
                "animals": {},
                "total_animals": 0,
                "empty_structures": {},
                "total_empty_structures": 0,
                "total_tiles": 25
            }

        for y in range(10):
            for x in range(10):
                qid = get_quadrant_id(x, y)
                qname = QUAD_ID_TO_NAME[qid]
                if qname == "Q3_SE":
                    continue
                t = terminal_tiles[y][x]
                qd = terminal_quadrants[qname]
                if t is None:
                    qd["empty_uncultivated"] += 1
                elif isinstance(t, dict):
                    k = t.get("kind")
                    if k == "PLANT":
                        c = t.get("crop", "UNKNOWN")
                        qd["crops"][c] = qd["crops"].get(c, 0) + 1
                        qd["total_crops"] += 1
                    elif k in ("COOP", "PASTURE"):
                        a = t.get("animal")
                        if a:
                            qd["animals"][a] = qd["animals"].get(a, 0) + 1
                            qd["total_animals"] += 1
                        else:
                            qd["empty_structures"][k] = qd["empty_structures"].get(k, 0) + 1
                            qd["total_empty_structures"] += 1
                    elif k == "WEED":
                        qd["weeds"] += 1

            for q_target in ["Q0_NW", "Q1_NE", "Q2_SW"]:
                qd = terminal_quadrants[q_target]
                qd["total_uncultivated"] = qd["empty_uncultivated"] + qd["weeds"]

        market_prices = terminal_obs.get("market", {}).get("prices", {})
        unsold_inventory_val = 0.0
        for item, qty in terminal_shed.items():
            price = market_prices.get(item, 0.0)
            unsold_inventory_val += qty * price
        for winv in terminal_worker_invs:
            for item, qty in winv.items():
                price = market_prices.get(item, 0.0)
                unsold_inventory_val += qty * price

        total_hires_count = sum(m["hires_today"] for m in daily_metrics)
        peak_money = max(m["money_end"] for m in daily_metrics)
        peak_crops = max(m["total_crops"] for m in daily_metrics)
        peak_animals = max(m["total_animals"] for m in daily_metrics)
        peak_hands = max(m["max_hands"] for m in daily_metrics)

        move_to_prod_ratio = (total_moves / total_productive) if total_productive > 0 else 0.0

        players_data[f"player_{p}"] = {
            "player_index": p,
            "agent_name": agent_name,
            "final_reward": final_rewards[p],
            "terminal_status": statuses[p],
            "quadrant_unlock_steps": q_unlock_step,
            "quadrant_unlock_days": q_unlock_day,
            "total_hires_count": total_hires_count,
            "peak_hands": peak_hands,
            "peak_money": peak_money,
            "peak_crops": peak_crops,
            "peak_animals": peak_animals,
            "animal_escapes_detected": animal_escapes_detected,
            "total_actions": {
                "moves": total_moves,
                "passes": total_passes,
                "productive": total_productive,
                "handling": total_handling,
                "move_to_productive_ratio": round(move_to_prod_ratio, 4),
            },
            "action_op_breakdown": dict(action_op_counts),
            "market_order_breakdown": dict(market_order_counts),
            "crops_planted": dict(crop_planted_counts),
            "animals_purchased": dict(animal_purchased_counts),
            "structures_built": dict(structure_built_counts),
            "care_stats": {
                "water_actions": water_actions,
                "fertilizer_applied": fertilizer_applied,
                "fertilizer_collected": fertilizer_collected,
                "feed_actions": feed_actions,
                "care_actions": care_actions,
                "harvest_actions": harvest_actions,
                "dig_actions": dig_actions,
            },
            "terminal_quadrant_breakdown": terminal_quadrants,
            "endgame_liquidation": {
                "sells_days_27_29": dict(endgame_sells),
                "sells_by_day": {k: dict(v) for k, v in endgame_sells_by_day.items()},
                "terminal_shed_inventory": dict(terminal_shed),
                "terminal_seeds_inventory": dict(terminal_seeds),
                "terminal_worker_inventories": terminal_worker_invs,
                "estimated_unsold_inventory_value": round(unsold_inventory_val, 2),
            },
            "daily_metrics": daily_metrics,
        }

    return {
        "episode_id": ep_id,
        "file_sha256": file_sha,
        "module_version": module_ver,
        "seed": seed,
        "num_steps": num_steps,
        "team_names": team_names,
        "final_rewards": {
            team_names[0]: final_rewards[0],
            team_names[1]: final_rewards[1],
        },
        "winner": team_names[0] if final_rewards[0] > final_rewards[1] else (team_names[1] if final_rewards[1] > final_rewards[0] else "TIE"),
        "margin": abs(final_rewards[0] - final_rewards[1]),
        "players": players_data,
    }


def aggregate_top3_metrics(episodes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Aggregate metrics across episodes by top 3 agents."""
    agents = ["tetsuya", "OceanMix", "Crop Dusta", "Driz Lo", "QQ Farming", "yukino"]

    agent_stats = {}
    for ag in agents:
        agent_stats[ag] = {
            "episodes_played": 0,
            "wins": 0,
            "losses": 0,
            "scores": [],
            "margins": [],
            "q1_unlock_days": [],
            "q1_unlock_steps": [],
            "q2_unlock_days": [],
            "q2_unlock_steps": [],
            "q3_unlock_days": [],
            "peak_hands_list": [],
            "total_hires_list": [],
            "peak_crops_list": [],
            "peak_animals_list": [],
            "total_productive_list": [],
            "total_moves_list": [],
            "total_passes_list": [],
            "move_prod_ratios": [],
            "crops_planted_total": collections.Counter(),
            "animals_purchased_total": collections.Counter(),
            "water_actions_total": 0,
            "fertilizer_applied_total": 0,
            "fertilizer_collected_total": 0,
            "feed_actions_total": 0,
            "care_actions_total": 0,
            "harvest_actions_total": 0,
            "dig_actions_total": 0,
            "animal_escapes_total": 0,
            "unsold_inventory_values": [],
            "terminal_shed_items_total": 0,
            "endgame_sells_total": collections.Counter(),
            "terminal_quad_uncultivated": {"Q0_NW": 0, "Q1_NE": 0, "Q2_SW": 0},
            "terminal_quad_crops": {"Q0_NW": 0, "Q1_NE": 0, "Q2_SW": 0},
            "terminal_quad_animals": {"Q0_NW": 0, "Q1_NE": 0, "Q2_SW": 0},
        }

    for ep in episodes:
        winner = ep["winner"]
        for p_key, p_data in ep["players"].items():
            ag_name = p_data["agent_name"]
            if ag_name not in agent_stats:
                continue

            st = agent_stats[ag_name]
            st["episodes_played"] += 1
            if winner == ag_name:
                st["wins"] += 1
            else:
                st["losses"] += 1

            st["scores"].append(p_data["final_reward"])

            opp_name = [name for name in ep["team_names"] if name != ag_name][0]
            opp_score = ep["final_rewards"][opp_name]
            st["margins"].append(p_data["final_reward"] - opp_score)

            q_days = p_data["quadrant_unlock_days"]
            q_steps = p_data["quadrant_unlock_steps"]
            if q_days.get("Q1_NE") is not None:
                st["q1_unlock_days"].append(q_days["Q1_NE"])
                st["q1_unlock_steps"].append(q_steps["Q1_NE"])
            if q_days.get("Q2_SW") is not None:
                st["q2_unlock_days"].append(q_days["Q2_SW"])
                st["q2_unlock_steps"].append(q_steps["Q2_SW"])
            if q_days.get("Q3_SE") is not None:
                st["q3_unlock_days"].append(q_days["Q3_SE"])

            st["peak_hands_list"].append(p_data["peak_hands"])
            st["total_hires_list"].append(p_data["total_hires_count"])
            st["peak_crops_list"].append(p_data["peak_crops"])
            st["peak_animals_list"].append(p_data["peak_animals"])
            st["animal_escapes_total"] += p_data.get("animal_escapes_detected", 0)

            st["total_productive_list"].append(p_data["total_actions"]["productive"])
            st["total_moves_list"].append(p_data["total_actions"]["moves"])
            st["total_passes_list"].append(p_data["total_actions"]["passes"])
            st["move_prod_ratios"].append(p_data["total_actions"]["move_to_productive_ratio"])

            st["crops_planted_total"].update(p_data["crops_planted"])
            st["animals_purchased_total"].update(p_data["animals_purchased"])

            c_stats = p_data["care_stats"]
            st["water_actions_total"] += c_stats.get("water_actions", 0)
            st["fertilizer_applied_total"] += c_stats["fertilizer_applied"]
            st["fertilizer_collected_total"] += c_stats["fertilizer_collected"]
            st["feed_actions_total"] += c_stats["feed_actions"]
            st["care_actions_total"] += c_stats["care_actions"]
            st["harvest_actions_total"] += c_stats.get("harvest_actions", 0)
            st["dig_actions_total"] += c_stats.get("dig_actions", 0)

            tq = p_data.get("terminal_quadrant_breakdown", {})
            for q_name in ["Q0_NW", "Q1_NE", "Q2_SW"]:
                if q_name in tq:
                    st["terminal_quad_uncultivated"][q_name] += tq[q_name]["total_uncultivated"]
                    st["terminal_quad_crops"][q_name] += tq[q_name]["total_crops"]
                    st["terminal_quad_animals"][q_name] += tq[q_name]["total_animals"]

            eg = p_data["endgame_liquidation"]
            st["unsold_inventory_values"].append(eg["estimated_unsold_inventory_value"])
            st["terminal_shed_items_total"] += sum(eg["terminal_shed_inventory"].values())
            st["endgame_sells_total"].update(eg["sells_days_27_29"])

    summary = {}
    for ag, st in agent_stats.items():
        if st["episodes_played"] == 0:
            continue
        n = st["episodes_played"]
        scores = st["scores"]
        scores_sorted = sorted(scores)
        median_score = scores_sorted[len(scores_sorted)//2]
        mean_score = sum(scores) / n
        mean_margin = sum(st["margins"]) / n

        summary[ag] = {
            "episodes_count": n,
            "record": f"{st['wins']}W - {st['losses']}L",
            "win_rate": round(st["wins"] / n, 4),
            "score_mean": round(mean_score, 2),
            "score_median": round(median_score, 2),
            "score_min": min(scores),
            "score_max": max(scores),
            "margin_mean": round(mean_margin, 2),
            "q1_unlock_day_mean": round(sum(st["q1_unlock_days"])/len(st["q1_unlock_days"]), 2) if st["q1_unlock_days"] else None,
            "q1_unlock_step_mean": round(sum(st["q1_unlock_steps"])/len(st["q1_unlock_steps"]), 1) if st["q1_unlock_steps"] else None,
            "q2_unlock_day_mean": round(sum(st["q2_unlock_days"])/len(st["q2_unlock_days"]), 2) if st["q2_unlock_days"] else None,
            "q2_unlock_step_mean": round(sum(st["q2_unlock_steps"])/len(st["q2_unlock_steps"]), 1) if st["q2_unlock_steps"] else None,
            "q3_unlock_day_mean": round(sum(st["q3_unlock_days"])/len(st["q3_unlock_days"]), 2) if st["q3_unlock_days"] else None,
            "peak_hands_mean": round(sum(st["peak_hands_list"])/n, 2),
            "total_hires_mean": round(sum(st["total_hires_list"])/n, 2),
            "peak_crops_mean": round(sum(st["peak_crops_list"])/n, 2),
            "peak_animals_mean": round(sum(st["peak_animals_list"])/n, 2),
            "animal_escapes_total": st["animal_escapes_total"],
            "productive_actions_mean": round(sum(st["total_productive_list"])/n, 2),
            "move_actions_mean": round(sum(st["total_moves_list"])/n, 2),
            "pass_actions_mean": round(sum(st["total_passes_list"])/n, 2),
            "move_to_productive_ratio_mean": round(sum(st["move_prod_ratios"])/n, 4),
            "terminal_quadrant_averages": {
                "Q0_NW": {
                    "uncultivated_mean": round(st["terminal_quad_uncultivated"]["Q0_NW"]/n, 1),
                    "crops_mean": round(st["terminal_quad_crops"]["Q0_NW"]/n, 1),
                    "animals_mean": round(st["terminal_quad_animals"]["Q0_NW"]/n, 1),
                },
                "Q1_NE": {
                    "uncultivated_mean": round(st["terminal_quad_uncultivated"]["Q1_NE"]/n, 1),
                    "crops_mean": round(st["terminal_quad_crops"]["Q1_NE"]/n, 1),
                    "animals_mean": round(st["terminal_quad_animals"]["Q1_NE"]/n, 1),
                },
                "Q2_SW": {
                    "uncultivated_mean": round(st["terminal_quad_uncultivated"]["Q2_SW"]/n, 1),
                    "crops_mean": round(st["terminal_quad_crops"]["Q2_SW"]/n, 1),
                    "animals_mean": round(st["terminal_quad_animals"]["Q2_SW"]/n, 1),
                },
            },
            "crops_planted_per_episode": {k: round(v/n, 2) for k, v in st["crops_planted_total"].items()},
            "animals_purchased_per_episode": {k: round(v/n, 2) for k, v in st["animals_purchased_total"].items()},
            "care_actions_per_episode": {
                "water_actions": round(st["water_actions_total"]/n, 2),
                "fertilizer_applied": round(st["fertilizer_applied_total"]/n, 2),
                "fertilizer_collected": round(st["fertilizer_collected_total"]/n, 2),
                "feed_actions": round(st["feed_actions_total"]/n, 2),
                "care_actions": round(st["care_actions_total"]/n, 2),
                "harvest_actions": round(st["harvest_actions_total"]/n, 2),
                "dig_actions": round(st["dig_actions_total"]/n, 2),
            },
            "unsold_inventory_value_mean": round(sum(st["unsold_inventory_values"])/n, 2),
            "terminal_shed_items_mean": round(st["terminal_shed_items_total"]/n, 2),
            "endgame_sells_per_episode": {k: round(v/n, 2) for k, v in st["endgame_sells_total"].items()},
        }

    return summary


def main():
    print("[E17 Independent Analysis] Starting extraction of 9 benchmark replays...")

    analyzed_episodes = []
    for fp in BENCHMARK_REPLAYS:
        print(f"Processing {fp}...")
        ep_res = analyze_episode(fp)
        analyzed_episodes.append(ep_res)

    top3_summary = aggregate_top3_metrics(analyzed_episodes)

    uncomputable_fields = [
        "opponent_intent_prior_to_transition",
        "counterfactual_market_price_without_opponent",
        "exact_path_planner_internal_state",
        "dynamic_working_set_intent_overlay",
        "future_rng_draws_at_decision_time"
    ]

    output_data = {
        "provenance": {
            "agent_id": "antigravity",
            "analysis_pass": "E17_TOP3_INDEPENDENT_DISCOVERY",
            "foundation_manifest_ref": "docs/foundation/FOUNDATION_C2_1_MANIFEST.md",
            "ontology_ref": "docs/foundation/ontology/ONTOLOGY_C2_1.md",
            "state_machine_ref": "docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md",
            "feature_model_ref": "docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md",
            "model_spec_ref": "docs/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2_3Q_POST_FOUNDATION_REVIEW.md",
            "engine_fingerprint": "4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d",
            "schema_version": "1.0.0",
            "corpus_replays_count": len(BENCHMARK_REPLAYS),
        },
        "replay_file_hashes": {
            Path(fp).name: compute_sha256(fp) for fp in BENCHMARK_REPLAYS
        },
        "uncomputable_fields_declaration": uncomputable_fields,
        "top3_comparative_summary": top3_summary,
        "episodes": analyzed_episodes,
    }

    out_json_path = "experiments/e17/artifacts/discovery/antigravity/E17_TOP3_REPLAY_METRICS.json"
    os.makedirs(os.path.dirname(out_json_path), exist_ok=True)
    with open(out_json_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    print(f"[E17 Independent Analysis] Successfully generated {out_json_path}")


if __name__ == "__main__":
    main()
