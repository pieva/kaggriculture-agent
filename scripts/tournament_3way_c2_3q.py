#!/usr/bin/env python3
"""Triangular 3-Way Tournament: Antigravity 3Q vs Codex 3Q vs Copilot 3Q."""

from __future__ import annotations

import csv
import importlib.util
import json
import statistics
import sys
from pathlib import Path
from typing import Any, Callable

from kaggle_environments import make

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from agricola.strategy.antigravity.agent_c2_100k_central import (
    create_agent as create_ag_agent,
)
from agricola.strategy.copilot.three_quadrant import CopilotThreeQPolicy

# Load Codex from submission_codex.py
codex_spec = importlib.util.spec_from_file_location(
    "submission_codex", str(PROJECT_ROOT / "submission" / "submission_codex.py")
)
codex_module = importlib.util.module_from_spec(codex_spec)
sys.modules["submission_codex"] = codex_module
codex_spec.loader.exec_module(codex_module)

SEEDS = [26090101, 26090102, 26090103, 1838889274, 1619968655, 710418712, 562040596]


def get_agent(name: str, seed: int, seat: int) -> tuple[Callable, Any]:
    if name == "ANTIGRAVITY":
        ag = create_ag_agent(run_context={"seed": seed, "seat": seat})
        return ag.act, ag
    elif name == "CODEX":
        cd_fn = codex_module.create_agent(run_context={"seed": seed, "seat": seat})
        return cd_fn, None
    elif name == "COPILOT":
        cp = CopilotThreeQPolicy(run_context={"seed": seed, "seat": seat})
        return cp.act, cp
    else:
        raise ValueError(f"Unknown agent: {name}")


def run_single_match(agent0_name: str, agent1_name: str, seed: int) -> dict[str, Any]:
    fn0, obj0 = get_agent(agent0_name, seed, seat=0)
    fn1, obj1 = get_agent(agent1_name, seed, seat=1)

    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24})
    env.run([fn0, fn1])

    p0_farm = env.steps[-1][0]["observation"]["farms"][0]
    p1_farm = env.steps[-1][1]["observation"]["farms"][1]

    m0 = float(p0_farm.get("money", 0.0))
    m1 = float(p1_farm.get("money", 0.0))

    winner = agent0_name if m0 > m1 else (agent1_name if m1 > m0 else "TIE")

    return {
        "seed": seed,
        "player0": agent0_name,
        "player1": agent1_name,
        "money_p0": m0,
        "money_p1": m1,
        "winner": winner,
        "margin_p0": m0 - m1,
        "p0_quadrants": len(p0_farm.get("unlocked_quadrants", [])),
        "p1_quadrants": len(p1_farm.get("unlocked_quadrants", [])),
    }


def main():
    print("=" * 85)
    print("TRIANGULAR 3-WAY 3Q TOURNAMENT: ANTIGRAVITY vs CODEX vs COPILOT")
    print("=" * 85)

    pairs = [
        ("ANTIGRAVITY", "CODEX"),
        ("ANTIGRAVITY", "COPILOT"),
        ("CODEX", "COPILOT"),
    ]

    all_matches = []
    standings = {
        "ANTIGRAVITY": {"wins": 0, "losses": 0, "ties": 0, "money_scores": [], "matches": 0},
        "CODEX": {"wins": 0, "losses": 0, "ties": 0, "money_scores": [], "matches": 0},
        "COPILOT": {"wins": 0, "losses": 0, "ties": 0, "money_scores": [], "matches": 0},
    }

    h2h_matrix = {
        "ANTIGRAVITY": {"CODEX": [0, 0], "COPILOT": [0, 0]},
        "CODEX": {"ANTIGRAVITY": [0, 0], "COPILOT": [0, 0]},
        "COPILOT": {"ANTIGRAVITY": [0, 0], "CODEX": [0, 0]},
    }

    for p0_name, p1_name in pairs:
        print(f"\n--- PAIR: {p0_name} vs {p1_name} ---")
        for s in SEEDS:
            # Match 1: P0 as Seat 0, P1 as Seat 1
            res1 = run_single_match(p0_name, p1_name, s)
            all_matches.append(res1)
            
            standings[p0_name]["matches"] += 1
            standings[p1_name]["matches"] += 1
            standings[p0_name]["money_scores"].append(res1["money_p0"])
            standings[p1_name]["money_scores"].append(res1["money_p1"])

            if res1["winner"] == p0_name:
                standings[p0_name]["wins"] += 1
                standings[p1_name]["losses"] += 1
                h2h_matrix[p0_name][p1_name][0] += 1
                h2h_matrix[p1_name][p0_name][1] += 1
            elif res1["winner"] == p1_name:
                standings[p1_name]["wins"] += 1
                standings[p0_name]["losses"] += 1
                h2h_matrix[p1_name][p0_name][0] += 1
                h2h_matrix[p0_name][p1_name][1] += 1
            else:
                standings[p0_name]["ties"] += 1
                standings[p1_name]["ties"] += 1

            print(f"Seed {s:10d} | {p0_name:11s} ${res1['money_p0']:8.2f} vs {p1_name:7s} ${res1['money_p1']:8.2f} -> {res1['winner']}")

            # Match 2: Seat Swap (P1 as Seat 0, P0 as Seat 1)
            res2 = run_single_match(p1_name, p0_name, s)
            all_matches.append(res2)

            standings[p0_name]["matches"] += 1
            standings[p1_name]["matches"] += 1
            standings[p0_name]["money_scores"].append(res2["money_p1"])
            standings[p1_name]["money_scores"].append(res2["money_p0"])

            if res2["winner"] == p0_name:
                standings[p0_name]["wins"] += 1
                standings[p1_name]["losses"] += 1
                h2h_matrix[p0_name][p1_name][0] += 1
                h2h_matrix[p1_name][p0_name][1] += 1
            elif res2["winner"] == p1_name:
                standings[p1_name]["wins"] += 1
                standings[p0_name]["losses"] += 1
                h2h_matrix[p1_name][p0_name][0] += 1
                h2h_matrix[p0_name][p1_name][1] += 1
            else:
                standings[p0_name]["ties"] += 1
                standings[p1_name]["ties"] += 1

            print(f"Seed {s:10d} | {p1_name:11s} ${res2['money_p0']:8.2f} vs {p0_name:7s} ${res2['money_p1']:8.2f} -> {res2['winner']}")

    print("\n" + "=" * 85)
    print("FINAL 3-WAY TOURNAMENT STANDINGS")
    print("=" * 85)
    print(f"{'Agent':<15} | {'Wins':<5} | {'Losses':<6} | {'Ties':<4} | {'Win Rate':<10} | {'Mean Final Money':<16}")
    print("-" * 85)
    for agent_name in ("ANTIGRAVITY", "COPILOT", "CODEX"):
        st = standings[agent_name]
        wr = st["wins"] / st["matches"] * 100
        mean_m = statistics.mean(st["money_scores"])
        print(f"{agent_name:<15} | {st['wins']:<5} | {st['losses']:<6} | {st['ties']:<4} | {wr:6.1f}%    | ${mean_m:14.2f}")
    print("=" * 85)

    # Save outputs
    out_dir = PROJECT_ROOT / "results" / "model_spec_c2"
    out_json = out_dir / "THREE_WAY_3Q_TOURNAMENT_RESULTS.json"
    out_csv = out_dir / "THREE_WAY_3Q_TOURNAMENT_RESULTS.csv"

    serializable_standings = {}
    for k, v in standings.items():
        serializable_standings[k] = {
            "wins": v["wins"],
            "losses": v["losses"],
            "ties": v["ties"],
            "matches": v["matches"],
            "win_rate": v["wins"] / v["matches"],
            "mean_money": statistics.mean(v["money_scores"]),
        }

    with open(out_json, "w") as f:
        json.dump({
            "standings": serializable_standings,
            "h2h_matrix": h2h_matrix,
            "matches": all_matches,
        }, f, indent=2)

    with open(out_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_matches[0].keys()))
        writer.writeheader()
        writer.writerows(all_matches)

    print(f"\nSaved tournament results to {out_json} and {out_csv}")


if __name__ == "__main__":
    main()
