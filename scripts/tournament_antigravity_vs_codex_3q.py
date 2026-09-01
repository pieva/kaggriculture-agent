#!/usr/bin/env python3
"""Internal Tournament: Antigravity 3Q Central Cluster vs Codex 3Q Elastic."""

from __future__ import annotations

import csv
import json
import statistics
import sys
from pathlib import Path
from typing import Any

from kaggle_environments import make

from agricola.strategy.antigravity.agent_c2_100k_central import (
    create_agent as create_ag_agent,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# Load Codex agent from submission_codex.py
import importlib.util
codex_spec = importlib.util.spec_from_file_location("submission_codex", str(PROJECT_ROOT / "submission" / "submission_codex.py"))
codex_module = importlib.util.module_from_spec(codex_spec)
sys.modules["submission_codex"] = codex_module
codex_spec.loader.exec_module(codex_module)
codex_agent_fn = codex_module.agent

SEEDS = [26090101, 26090102, 26090103, 1838889274, 1619968655, 710418712, 562040596]


def run_match(seed: int, ag_seat: int) -> dict[str, Any]:
    ag_agent = create_ag_agent(run_context={"seed": seed, "seat": ag_seat})
    
    if ag_seat == 0:
        agents = [ag_agent.act, codex_agent_fn]
    else:
        agents = [codex_agent_fn, ag_agent.act]

    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24})
    env.run(agents)

    p0_farm = env.steps[-1][0]["observation"]["farms"][0]
    p1_farm = env.steps[-1][1]["observation"]["farms"][1]

    ag_farm = p0_farm if ag_seat == 0 else p1_farm
    cd_farm = p1_farm if ag_seat == 0 else p0_farm

    ag_money = float(ag_farm.get("money", 0.0))
    cd_money = float(cd_farm.get("money", 0.0))

    t_ag = ag_agent.telemetry_snapshot()
    winner = "ANTIGRAVITY" if ag_money > cd_money else ("CODEX" if cd_money > ag_money else "TIE")

    return {
        "seed": seed,
        "ag_seat": ag_seat,
        "antigravity_money": ag_money,
        "codex_money": cd_money,
        "margin": ag_money - cd_money,
        "winner": winner,
        "ag_quadrants": len(ag_farm.get("unlocked_quadrants", [])),
        "cd_quadrants": len(cd_farm.get("unlocked_quadrants", [])),
        "ag_melons": int(t_ag.get("MELON_units", 0)),
        "ag_milk": int(t_ag.get("MILK_units", 0)),
        "ag_wool": int(t_ag.get("WOOL_units", 0)),
        "ag_escapes": int(t_ag.get("ANIMAL_ESCAPE", 0)),
    }


def main():
    print("=" * 80)
    print("INTERNAL HEAD-TO-HEAD TOURNAMENT: ANTIGRAVITY 3Q CENTRAL vs CODEX 3Q ELASTIC")
    print("=" * 80)

    matches = []
    for s in SEEDS:
        # Match with Antigravity as Player 0
        m1 = run_match(s, ag_seat=0)
        matches.append(m1)
        print(f"Seed {s:10d} (Seat 0): AG ${m1['antigravity_money']:8.2f} vs CODEX ${m1['codex_money']:8.2f} -> {m1['winner']} (+${m1['margin']:8.2f})")

        # Match with Antigravity as Player 1 (Seat Swap)
        m2 = run_match(s, ag_seat=1)
        matches.append(m2)
        print(f"Seed {s:10d} (Seat 1): AG ${m2['antigravity_money']:8.2f} vs CODEX ${m2['codex_money']:8.2f} -> {m2['winner']} (+${m2['margin']:8.2f})")

    ag_wins = sum(1 for m in matches if m["winner"] == "ANTIGRAVITY")
    cd_wins = sum(1 for m in matches if m["winner"] == "CODEX")
    ties = sum(1 for m in matches if m["winner"] == "TIE")

    ag_mean_money = statistics.mean(m["antigravity_money"] for m in matches)
    cd_mean_money = statistics.mean(m["codex_money"] for m in matches)

    print("=" * 80)
    print(f"TOURNAMENT SUMMARY:")
    print(f"Total Matches: {len(matches)}")
    print(f"Antigravity Wins: {ag_wins} ({ag_wins/len(matches)*100:.1f}%)")
    print(f"Codex Wins:       {cd_wins} ({cd_wins/len(matches)*100:.1f}%)")
    print(f"Ties:             {ties}")
    print(f"Antigravity Mean Money: ${ag_mean_money:.2f}")
    print(f"Codex Mean Money:       ${cd_mean_money:.2f}")
    print(f"Antigravity Lead:       +${ag_mean_money - cd_mean_money:.2f}")
    print("=" * 80)

    out_csv = PROJECT_ROOT / "results" / "model_spec_c2" / "antigravity" / "ANTIGRAVITY_VS_CODEX_3Q_TOURNAMENT_RESULTS.csv"
    out_json = PROJECT_ROOT / "results" / "model_spec_c2" / "antigravity" / "ANTIGRAVITY_VS_CODEX_3Q_TOURNAMENT_RESULTS.json"

    with open(out_json, "w") as f:
        json.dump({
            "summary": {
                "total_matches": len(matches),
                "ag_wins": ag_wins,
                "cd_wins": cd_wins,
                "ties": ties,
                "ag_mean_money": ag_mean_money,
                "cd_mean_money": cd_mean_money,
                "ag_lead": ag_mean_money - cd_mean_money,
            },
            "matches": matches,
        }, f, indent=2)

    with open(out_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(matches[0].keys()))
        writer.writeheader()
        writer.writerows(matches)

    print(f"Saved tournament results to {out_csv} and {out_json}")


if __name__ == "__main__":
    main()
